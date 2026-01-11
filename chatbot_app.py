# -*- coding: utf-8 -*-
"""
Application Streamlit - Chatbot d'Analyse de Sentiments et Émotions
Projet NLP: Analyse des avis de restaurants avec détection d'émotions spécifiques
Auteur: Oumaima AYADI
"""

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from emotion_detection import get_emotion_detector, SimpleEmotionDetector
import time
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Chatbot - Analyse Sentiments & Émotions",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour le chatbot
st.markdown("""
    <style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .message-content {
        flex: 1;
    }
    .message-time {
        font-size: 0.75rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .sentiment-positive {
        color: #10b981;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #ef4444;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #f59e0b;
        font-weight: bold;
    }
    .emotion-joy {
        color: #10b981;
    }
    .emotion-sadness {
        color: #3b82f6;
    }
    .emotion-anger {
        color: #ef4444;
    }
    .emotion-surprise {
        color: #f59e0b;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation de la session
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'sentiment_model' not in st.session_state:
    st.session_state.sentiment_model = None
    st.session_state.tokenizer = None
    st.session_state.device = None
    st.session_state.emotion_detector = None

# Sidebar - Configuration
st.sidebar.header("⚙️ Configuration")

# Choix du modèle de sentiment
SENTIMENT_MODEL_PATH = st.sidebar.text_input(
    "Chemin du modèle de sentiment",
    value="distilbert-base-uncased",
    help="Chemin vers le modèle fine-tuné ou nom du modèle HuggingFace"
)

# Choix du détecteur d'émotions
USE_EMOTION_MODEL = st.sidebar.checkbox(
    "Utiliser modèle d'émotions avancé",
    value=False,
    help="Si désactivé, utilise un détecteur basé sur mots-clés"
)

MAX_LENGTH = st.sidebar.slider("Longueur max du texte", 32, 256, 128, step=16)

# Bouton pour charger les modèles
if st.sidebar.button("🔄 Charger/Recharger les Modèles"):
    with st.sidebar.spinner("Chargement des modèles..."):
        try:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_PATH)
            model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_PATH)
            model.to(device)
            model.eval()
            
            st.session_state.tokenizer = tokenizer
            st.session_state.sentiment_model = model
            st.session_state.device = device
            
            st.sidebar.success("✅ Modèle de sentiment chargé")
        except Exception as e:
            st.sidebar.error(f"❌ Erreur: {e}")
        
        try:
            emotion_detector = get_emotion_detector(use_model=USE_EMOTION_MODEL)
            st.session_state.emotion_detector = emotion_detector
            st.sidebar.success("✅ Détecteur d'émotions chargé")
        except Exception as e:
            st.sidebar.warning(f"⚠️ Erreur détecteur d'émotions: {e}")
            st.session_state.emotion_detector = SimpleEmotionDetector()

# Vérification que les modèles sont chargés
if st.session_state.sentiment_model is None:
    st.warning("⚠️ Veuillez charger les modèles depuis la barre latérale (bouton 'Charger/Recharger les Modèles')")
    st.stop()

# Fonction de prédiction de sentiment
def predict_sentiment(text: str):
    """Prédit le sentiment (Positif/Négatif/Neutre)"""
    tokenizer = st.session_state.tokenizer
    model = st.session_state.sentiment_model
    device = st.session_state.device
    
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0]
        pred_id = torch.argmax(probs).item()
        conf = float(probs[pred_id].item())
    
    label_map = {0: "Négatif", 1: "Neutre", 2: "Positif"}
    sentiment = label_map.get(pred_id, "Neutre")
    
    return sentiment, conf, probs.detach().cpu().numpy()

# Fonction pour obtenir l'icône d'émotion
def get_emotion_icon(emotion: str) -> str:
    """Retourne l'icône correspondant à l'émotion"""
    icons = {
        "joie": "😊",
        "tristesse": "😢",
        "colère": "😠",
        "surprise": "😲",
        "neutre": "😐"
    }
    return icons.get(emotion, "😐")

# Fonction pour obtenir l'icône de sentiment
def get_sentiment_icon(sentiment: str) -> str:
    """Retourne l'icône correspondant au sentiment"""
    icons = {
        "Positif": "✅",
        "Négatif": "❌",
        "Neutre": "➖"
    }
    return icons.get(sentiment, "➖")

# Titre principal
st.title("🤖 Chatbot d'Analyse de Sentiments & Émotions")
st.markdown("**Analysez vos avis de restaurants en temps réel**")
st.markdown("---")

# Zone de chat
chat_container = st.container()

# Afficher l'historique du chat
with chat_container:
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-content">
                        <strong>Vous:</strong><br>
                        {message['content']}
                        <div class="message-time">{message['time']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Message du bot avec analyse
            sentiment = message.get('sentiment', 'N/A')
            emotion = message.get('emotion', 'N/A')
            emotion_conf = message.get('emotion_conf', 0)
            sent_conf = message.get('sentiment_conf', 0)
            
            sentiment_icon = get_sentiment_icon(sentiment)
            emotion_icon = get_emotion_icon(emotion)
            
            # Afficher la réponse détaillée du bot
            bot_response = message.get('content', '')
            
            # Afficher les métriques
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <div class="message-content">
                        <strong>🤖 Assistant:</strong><br>
                        <b>Sentiment:</b> {sentiment_icon} <span class="sentiment-{sentiment.lower()}">{sentiment}</span> ({sent_conf*100:.1f}%)<br>
                        <b>Émotion:</b> {emotion_icon} <span class="emotion-{emotion}">{emotion.capitalize()}</span> ({emotion_conf*100:.1f}%)<br>
                        <div class="message-time">{message['time']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Afficher la réponse détaillée avec markdown
            st.markdown("""
                <div style="margin: 10px 0; padding: 15px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #1f77b4;">
            """, unsafe_allow_html=True)
            st.markdown(bot_response)
            st.markdown("</div>", unsafe_allow_html=True)

# Zone de saisie
st.markdown("---")
st.subheader("💬 Entrez un avis à analyser")

# Exemples d'avis
col1, col2, col3, col4 = st.columns(4)
example_reviews = [
    "The food was amazing! I loved every bite!",
    "I'm very disappointed. The service was terrible.",
    "Wow! This place is incredible! Best restaurant ever!",
    "The food was okay, nothing special really."
]

with col1:
    if st.button("Exemple 1", use_container_width=True):
        st.session_state.example_input = example_reviews[0]
        st.session_state.auto_analyze = True
        st.rerun()

with col2:
    if st.button("Exemple 2", use_container_width=True):
        st.session_state.example_input = example_reviews[1]
        st.session_state.auto_analyze = True
        st.rerun()

with col3:
    if st.button("Exemple 3", use_container_width=True):
        st.session_state.example_input = example_reviews[2]
        st.session_state.auto_analyze = True
        st.rerun()

with col4:
    if st.button("Exemple 4", use_container_width=True):
        st.session_state.example_input = example_reviews[3]
        st.session_state.auto_analyze = True
        st.rerun()

# Zone de texte pour l'avis avec analyse automatique
user_input = st.text_area(
    "✍️ Votre avis:",
    value=st.session_state.get('example_input', ''),
    height=100,
    placeholder="Ex: The food was amazing but the service was slow...",
    key="user_input_text"
)

# Option pour activer/désactiver l'analyse automatique
auto_analyze_option = st.checkbox(
    "🔄 Analyser automatiquement lors de la saisie",
    value=st.session_state.get('auto_analyze_enabled', False),
    help="Si activé, l'analyse se lance automatiquement quand vous entrez un avis"
)

st.session_state.auto_analyze_enabled = auto_analyze_option

# Bouton d'analyse manuel
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🔍 Analyser", type="primary", use_container_width=True)

# Déterminer si on doit analyser
should_analyze = False

# Si l'analyse automatique est activée et qu'il y a du texte
if auto_analyze_option and user_input.strip():
    # Vérifier si c'est un nouveau texte (pas déjà analysé)
    last_analyzed = st.session_state.get('last_analyzed_text', '')
    if user_input != last_analyzed:
        should_analyze = True
        st.session_state.last_analyzed_text = user_input

# Ou si le bouton a été cliqué
if analyze_button and user_input.strip():
    should_analyze = True

# Ou si auto_analyze est activé (depuis les exemples)
if st.session_state.get('auto_analyze', False) and user_input.strip():
    should_analyze = True
    st.session_state.auto_analyze = False

# Traitement de l'analyse
if should_analyze and user_input.strip():
    # Ajouter le message de l'utilisateur à l'historique
    current_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input,
        'time': current_time
    })
    
    # Analyser l'avis
    with st.spinner("🤔 Analyse en cours..."):
        # Analyse de sentiment
        sentiment, sent_conf, sent_probs = predict_sentiment(user_input)
        
        # Analyse d'émotions
        if st.session_state.emotion_detector:
            emotion_scores = st.session_state.emotion_detector.predict_emotion(user_input)
            main_emotion, emotion_conf = st.session_state.emotion_detector.get_main_emotion(user_input)
        else:
            emotion_detector = SimpleEmotionDetector()
            emotion_scores = emotion_detector.predict_emotion(user_input)
            main_emotion, emotion_conf = emotion_detector.get_main_emotion(user_input)
        
        # Générer une réponse personnalisée et détaillée
        if sentiment == "Positif" and main_emotion == "joie":
            response = f"""Excellent ! 🎉 Votre avis exprime une satisfaction claire. 

**Analyse détaillée:**
- **Sentiment:** {sentiment} ({sent_conf*100:.1f}% de confiance)
- **Émotion principale:** {main_emotion.capitalize()} ({emotion_conf*100:.1f}% de confiance)
- **Interprétation:** L'émotion de joie indique que vous avez vraiment apprécié votre expérience. C'est un excellent signe pour le restaurant !

**Recommandation:** Le restaurant devrait continuer dans cette direction et peut-être mettre en avant ces points positifs dans sa communication."""
        
        elif sentiment == "Négatif" and main_emotion == "colère":
            response = f"""Je comprends votre frustration. 😔

**Analyse détaillée:**
- **Sentiment:** {sentiment} ({sent_conf*100:.1f}% de confiance)
- **Émotion principale:** {main_emotion.capitalize()} ({emotion_conf*100:.1f}% de confiance)
- **Interprétation:** Votre avis exprime de la colère, ce qui indique une insatisfaction importante. Il serait crucial d'améliorer les points mentionnés.

**Recommandation pour le restaurant:** 
- Analyser les points spécifiques mentionnés
- Prendre des mesures correctives immédiates
- Contacter le client pour s'excuser et proposer une solution"""
        
        elif sentiment == "Négatif" and main_emotion == "tristesse":
            response = f"""Je comprends votre déception. 😢

**Analyse détaillée:**
- **Sentiment:** {sentiment} ({sent_conf*100:.1f}% de confiance)
- **Émotion principale:** {main_emotion.capitalize()} ({emotion_conf*100:.1f}% de confiance)
- **Interprétation:** Votre avis montre une déception. Nous comprenons votre frustration et espérons pouvoir améliorer votre expérience.

**Recommandation pour le restaurant:**
- Identifier les causes de la déception
- Améliorer les processus concernés
- Proposer une compensation si approprié"""
        
        elif sentiment == "Positif" and main_emotion == "surprise":
            response = f"""Fantastique ! Votre avis exprime une surprise positive ! 😲✨

**Analyse détaillée:**
- **Sentiment:** {sentiment} ({sent_conf*100:.1f}% de confiance)
- **Émotion principale:** {main_emotion.capitalize()} ({emotion_conf*100:.1f}% de confiance)
- **Interprétation:** C'est excellent de voir que l'expérience a dépassé vos attentes ! La surprise positive est un indicateur très fort de satisfaction.

**Recommandation:** Le restaurant devrait capitaliser sur ces éléments qui ont créé cette surprise positive."""
        
        elif sentiment == "Positif":
            response = f"""Très bien ! Votre avis est positif. 👍

**Analyse détaillée:**
- **Sentiment:** {sentiment} ({sent_conf*100:.1f}% de confiance)
- **Émotion principale:** {main_emotion.capitalize()} ({emotion_conf*100:.1f}% de confiance)
- **Interprétation:** Vous semblez satisfait de votre expérience. C'est un bon signe pour le restaurant.

**Recommandation:** Continuer à maintenir la qualité du service."""
        
        elif sentiment == "Négatif":
            response = f"""Je comprends votre insatisfaction. 😞

**Analyse détaillée:**
- **Sentiment:** {sentiment} ({sent_conf*100:.1f}% de confiance)
- **Émotion principale:** {main_emotion.capitalize()} ({emotion_conf*100:.1f}% de confiance)
- **Interprétation:** Votre avis indique une insatisfaction. Il serait important d'améliorer les points mentionnés.

**Recommandation pour le restaurant:**
- Analyser les problèmes mentionnés
- Mettre en place des actions correctives
- Suivre avec le client"""
        
        else:
            response = f"""Votre avis a été analysé. 📊

**Analyse détaillée:**
- **Sentiment:** {sentiment} ({sent_conf*100:.1f}% de confiance)
- **Émotion principale:** {main_emotion.capitalize()} ({emotion_conf*100:.1f}% de confiance)
- **Interprétation:** Votre avis est neutre, ni particulièrement positif ni négatif.

**Recommandation:** Le restaurant pourrait chercher à améliorer l'expérience pour créer plus d'émotions positives."""
        
        # Ajouter la réponse du bot à l'historique
        st.session_state.chat_history.append({
            'role': 'bot',
            'content': response,
            'sentiment': sentiment,
            'emotion': main_emotion,
            'sentiment_conf': sent_conf,
            'emotion_conf': emotion_conf,
            'time': current_time
        })
        
        # Réinitialiser l'input
        st.session_state.example_input = ''
        
        # Recharger la page pour afficher le nouveau message
        st.rerun()

# Bouton pour effacer l'historique
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🗑️ Effacer l'historique", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Informations supplémentaires
with st.expander("ℹ️ Informations sur l'analyse"):
    st.markdown("""
    ### 📊 Comment fonctionne l'analyse ?
    
    1. **Analyse de Sentiment** :
       - Utilise un modèle DistilBERT fine-tuné
       - Classifie l'avis en : Positif, Négatif ou Neutre
       - Donne un score de confiance
    
    2. **Détection d'Émotions** :
       - Identifie l'émotion principale : joie, tristesse, colère, surprise
       - Utilise soit un modèle pré-entraîné, soit un détecteur basé sur mots-clés
       - Fournit un score pour chaque émotion
    
    3. **Réponse Personnalisée** :
       - Génère une réponse adaptée selon le sentiment et l'émotion détectés
       - Aide à comprendre l'analyse
    """)

# Footer
st.markdown("---")
st.caption("🤖 Chatbot NLP - Analyse de Sentiments & Détection d'Émotions | Projet Oumaima AYADI")
