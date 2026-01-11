# -*- coding: utf-8 -*-
"""
Script pour évaluer l'accuracy du modèle sur le dataset équilibré
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from emotion_detection import SimpleEmotionDetector

def evaluate_sentiment_model():
    """Évalue le modèle de sentiment sur le dataset équilibré"""
    print("=" * 60)
    print("EVALUATION DU MODELE DE SENTIMENT")
    print("=" * 60)
    
    # Charger le dataset équilibré
    print("\nChargement du dataset equilibre...")
    df = pd.read_csv("TA_restaurants_balanced.csv")
    print(f"Dataset charge: {len(df)} echantillons")
    
    # Préparer les données
    texts = df['Review'].astype(str).tolist()
    labels = df['label'].astype(int).tolist()
    
    # Split train/test
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )
    
    print(f"\nTrain: {len(train_texts)} echantillons")
    print(f"Test: {len(test_texts)} echantillons")
    
    # Charger le modèle
    print("\nChargement du modele DistilBERT...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = "distilbert-base-uncased"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=3
        )
        model.to(device)
        model.eval()
        print("Modele charge avec succes")
    except Exception as e:
        print(f"Erreur lors du chargement du modele: {e}")
        print("Utilisation d'une evaluation basique...")
        return evaluate_basic_accuracy(df)
    
    # Prédire sur le test set
    print("\nPrediction sur le test set...")
    predictions = []
    batch_size = 32
    
    for i in range(0, len(test_texts), batch_size):
        batch_texts = test_texts[i:i+batch_size]
        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model(**inputs)
            preds = torch.argmax(outputs.logits, dim=1)
            predictions.extend(preds.cpu().numpy())
    
    # Calculer les métriques
    accuracy = accuracy_score(test_labels, predictions)
    f1 = f1_score(test_labels, predictions, average='weighted')
    
    print("\n" + "=" * 60)
    print("RESULTATS")
    print("=" * 60)
    print(f"\nAccuracy: {accuracy*100:.2f}%")
    print(f"F1-Score (weighted): {f1*100:.2f}%")
    
    # Rapport de classification
    print("\nRapport de classification:")
    print(classification_report(
        test_labels,
        predictions,
        target_names=["Negatif", "Neutre", "Positif"]
    ))
    
    # Matrice de confusion
    print("\nMatrice de confusion:")
    cm = confusion_matrix(test_labels, predictions)
    print(cm)
    
    return accuracy, f1

def evaluate_basic_accuracy(df):
    """Évaluation basique basée sur les ratings"""
    print("\n" + "=" * 60)
    print("EVALUATION BASIQUE")
    print("=" * 60)
    
    # Distribution des labels
    print("\nDistribution des labels:")
    print(df['sentiment'].value_counts())
    
    # Accuracy basique (si on prédit toujours la classe majoritaire)
    label_counts = df['label'].value_counts()
    majority_class_accuracy = label_counts.max() / len(df)
    
    print(f"\nAccuracy si on predit toujours la classe majoritaire: {majority_class_accuracy*100:.2f}%")
    print(f"Accuracy aleatoire (3 classes): {1/3*100:.2f}%")
    
    return majority_class_accuracy, 0

def evaluate_emotion_detector():
    """Évalue le détecteur d'émotions"""
    print("\n" + "=" * 60)
    print("EVALUATION DU DETECTEUR D'EMOTIONS")
    print("=" * 60)
    
    detector = SimpleEmotionDetector()
    
    # Tests sur des exemples connus
    test_cases = [
        ("The food was amazing! I loved it!", "joie"),
        ("I'm very disappointed. The service was terrible.", "tristesse"),
        ("I'm really angry about the slow service!", "colère"),
        ("Wow! This restaurant is incredible!", "surprise"),
        ("The food was okay, nothing special.", "neutre")
    ]
    
    correct = 0
    total = len(test_cases)
    
    print("\nTests sur exemples connus:")
    for text, expected in test_cases:
        emotion, conf = detector.get_main_emotion(text)
        is_correct = emotion == expected
        if is_correct:
            correct += 1
        status = "[OK]" if is_correct else "[ERREUR]"
        print(f"{status} Texte: '{text[:40]}...'")
        print(f"   Attendu: {expected}, Obtenu: {emotion} ({conf*100:.1f}%)")
    
    accuracy = correct / total
    print(f"\nAccuracy sur exemples de test: {accuracy*100:.2f}% ({correct}/{total})")
    
    return accuracy

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE DU PROJET")
    print("=" * 60)
    
    # Évaluer le modèle de sentiment
    try:
        sent_accuracy, sent_f1 = evaluate_sentiment_model()
    except Exception as e:
        print(f"\nErreur lors de l'evaluation du modele de sentiment: {e}")
        print("Evaluation basique...")
        df = pd.read_csv("TA_restaurants_balanced.csv")
        sent_accuracy, sent_f1 = evaluate_basic_accuracy(df)
    
    # Évaluer le détecteur d'émotions
    try:
        emotion_accuracy = evaluate_emotion_detector()
    except Exception as e:
        print(f"\nErreur lors de l'evaluation du detecteur d'emotions: {e}")
        emotion_accuracy = 0
    
    # Résumé final
    print("\n" + "=" * 60)
    print("RESUME FINAL")
    print("=" * 60)
    print(f"\nModele de Sentiment:")
    print(f"  - Accuracy: {sent_accuracy*100:.2f}%")
    print(f"  - F1-Score: {sent_f1*100:.2f}%")
    print(f"\nDetecteur d'Emotions:")
    print(f"  - Accuracy: {emotion_accuracy*100:.2f}%")
    print("\n" + "=" * 60)
