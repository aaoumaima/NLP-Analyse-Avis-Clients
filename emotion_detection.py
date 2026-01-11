# -*- coding: utf-8 -*-
"""
Module de détection d'émotions spécifiques
Émotions ciblées: joie/excitation, tristesse/déception, colère/frustration, surprise/étonnement
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re
from typing import Dict, Tuple

class EmotionDetector:
    """
    Détecteur d'émotions utilisant un modèle pré-entraîné
    """
    
    def __init__(self, model_name: str = "j-hartmann/emotion-english-distilroberta-base"):
        """
        Initialise le détecteur d'émotions
        
        Args:
            model_name: Nom du modèle HuggingFace à utiliser
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        
        # Mapping des émotions du modèle vers nos catégories
        self.emotion_mapping = {
            'joy': 'joie',
            'happiness': 'joie',
            'excitement': 'joie',
            'sadness': 'tristesse',
            'disappointment': 'tristesse',
            'anger': 'colère',
            'frustration': 'colère',
            'annoyance': 'colère',
            'surprise': 'surprise',
            'amazement': 'surprise',
            'neutral': 'neutre'
        }
        
        # Catégories finales
        self.categories = ['joie', 'tristesse', 'colère', 'surprise', 'neutre']
    
    def predict_emotion(self, text: str) -> Dict[str, float]:
        """
        Prédit l'émotion principale dans un texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire avec les probabilités pour chaque émotion
        """
        # Tokenisation
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Prédiction
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)[0]
            
        # Récupérer les labels du modèle
        emotion_labels = self.model.config.id2label
        
        # Mapper vers nos catégories
        emotion_scores = {cat: 0.0 for cat in self.categories}
        
        for idx, prob in enumerate(probs):
            label = emotion_labels[idx].lower()
            prob_value = float(prob.item())
            
            # Mapper l'émotion du modèle vers nos catégories
            for key, value in self.emotion_mapping.items():
                if key in label:
                    emotion_scores[value] += prob_value
                    break
        
        # Normaliser (au cas où)
        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {k: v/total for k, v in emotion_scores.items()}
        
        return emotion_scores
    
    def get_main_emotion(self, text: str) -> Tuple[str, float]:
        """
        Retourne l'émotion principale et sa confiance
        
        Args:
            text: Texte à analyser
            
        Returns:
            Tuple (émotion, confiance)
        """
        emotions = self.predict_emotion(text)
        main_emotion = max(emotions.items(), key=lambda x: x[1])
        return main_emotion[0], main_emotion[1]


class SimpleEmotionDetector:
    """
    Détecteur d'émotions basé sur des dictionnaires de mots-clés
    Alternative simple si le modèle n'est pas disponible
    """
    
    def __init__(self):
        # Dictionnaires d'émotions (en anglais et français)
        self.emotion_keywords = {
            'joie': [
                'excellent', 'amazing', 'wonderful', 'great', 'fantastic', 'love', 'perfect',
                'excellent', 'merveilleux', 'génial', 'fantastique', 'adorable', 'parfait',
                'superbe', 'délicieux', 'satisfait', 'content', 'heureux', 'ravie'
            ],
            'tristesse': [
                'disappointed', 'sad', 'bad', 'terrible', 'awful', 'worst', 'poor',
                'déçu', 'triste', 'mauvais', 'terrible', 'affreux', 'pire', 'médiocre',
                'décevant', 'tristesse', 'regret'
            ],
            'colère': [
                'angry', 'frustrated', 'annoyed', 'horrible', 'disgusting', 'hate', 'slow',
                'en colère', 'frustré', 'énervé', 'horrible', 'dégoûtant', 'déteste', 'lent',
                'frustration', 'colère', 'mécontent'
            ],
            'surprise': [
                'surprised', 'unexpected', 'wow', 'incredible', 'unbelievable', 'shocked',
                'surpris', 'inattendu', 'incroyable', 'impressionnant', 'étonnant', 'choqué'
            ]
        }
        
        # Compter les occurrences
        for emotion in self.emotion_keywords:
            self.emotion_keywords[emotion] = [word.lower() for word in self.emotion_keywords[emotion]]
    
    def predict_emotion(self, text: str) -> Dict[str, float]:
        """
        Prédit l'émotion basée sur les mots-clés
        
        Args:
            text: Texte à analyser
            
        Returns:
            Dictionnaire avec les scores pour chaque émotion
        """
        text_lower = text.lower()
        
        # Compter les occurrences
        scores = {emotion: 0 for emotion in self.emotion_keywords.keys()}
        scores['neutre'] = 0
        
        total_matches = 0
        
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[emotion] = count
            total_matches += count
        
        # Si aucun mot-clé trouvé, retourner neutre
        if total_matches == 0:
            scores['neutre'] = 1.0
            return scores
        
        # Normaliser en probabilités
        total = sum(scores.values())
        if total > 0:
            scores = {k: v/total for k, v in scores.items()}
        
        return scores
    
    def get_main_emotion(self, text: str) -> Tuple[str, float]:
        """
        Retourne l'émotion principale et sa confiance
        
        Args:
            text: Texte à analyser
            
        Returns:
            Tuple (émotion, confiance)
        """
        emotions = self.predict_emotion(text)
        # Exclure neutre pour trouver la vraie émotion
        non_neutral = {k: v for k, v in emotions.items() if k != 'neutre'}
        
        if non_neutral and max(non_neutral.values()) > 0:
            main_emotion = max(non_neutral.items(), key=lambda x: x[1])
            return main_emotion[0], main_emotion[1]
        else:
            return 'neutre', emotions.get('neutre', 0.0)


def get_emotion_detector(use_model: bool = True) -> EmotionDetector | SimpleEmotionDetector:
    """
    Factory function pour obtenir un détecteur d'émotions
    
    Args:
        use_model: Si True, utilise le modèle pré-entraîné, sinon utilise le détecteur simple
        
    Returns:
        Instance du détecteur d'émotions
    """
    if use_model:
        try:
            return EmotionDetector()
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            print("Utilisation du détecteur simple basé sur mots-clés")
            return SimpleEmotionDetector()
    else:
        return SimpleEmotionDetector()


if __name__ == "__main__":
    # Test
    detector = get_emotion_detector(use_model=False)  # Utiliser le simple pour le test
    
    test_texts = [
        "The food was amazing! I loved it!",
        "I'm so disappointed with the service. It was terrible.",
        "I'm really angry about the slow service!",
        "Wow! This restaurant is incredible!",
        "The food was okay, nothing special."
    ]
    
    print("=" * 60)
    print("TEST DETECTION D'EMOTIONS")
    print("=" * 60)
    
    for text in test_texts:
        emotion, conf = detector.get_main_emotion(text)
        print(f"\nTexte: {text}")
        print(f"Émotion principale: {emotion} ({conf*100:.1f}%)")
        all_emotions = detector.predict_emotion(text)
        print(f"Toutes les émotions: {all_emotions}")
