# -*- coding: utf-8 -*-
"""
Application Streamlit - Analyse de Sentiments et Détection d'Émotions
Projet NLP: Analyse des avis de restaurants avec détection d'émotions spécifiques
Auteur: Oumaima AYADI
"""

import streamlit as st
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from emotion_detection import get_emotion_detector, SimpleEmotionDetector

# Configuration de la page
st.set_page_config(
    page_title="Analyse Sentiments & Émotions - Restaurants",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">🍽️ Analyse de Sentiments & Détection d\'Émotions</h1>', unsafe_allow_html=True)
st.markdown("---")

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

# Chargement des modèles
@st.cache_resource
def load_sentiment_model(model_path: str):
    """Charge le modèle de sentiment"""
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        model.to(device)
        model.eval()
        return tokenizer, model, device
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle: {e}")
        return None, None, None

@st.cache_resource
def load_emotion_detector(use_model: bool):
    """Charge le détecteur d'émotions"""
    try:
        return get_emotion_detector(use_model=use_model)
    except Exception as e:
        st.warning(f"Erreur lors du chargement du détecteur d'émotions: {e}")
        return SimpleEmotionDetector()

# Chargement
with st.spinner("Chargement des modèles..."):
    tokenizer, sentiment_model, device = load_sentiment_model(SENTIMENT_MODEL_PATH)
    emotion_detector = load_emotion_detector(USE_EMOTION_MODEL)

if tokenizer is None or sentiment_model is None:
    st.error("❌ Impossible de charger le modèle de sentiment. Vérifiez le chemin.")
    st.stop()

st.sidebar.success("✅ Modèles chargés")

# Fonctions de prédiction
def predict_sentiment(text: str, tokenizer, model, device, max_len: int):
    """Prédit le sentiment (Positif/Négatif/Neutre)"""
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=max_len
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0]
        pred_id = torch.argmax(probs).item()
        conf = float(probs[pred_id].item())
    
    label_map = {0: "Négatif", 1: "Neutre", 2: "Positif"}
    return label_map.get(pred_id, "Neutre"), conf, probs.detach().cpu().numpy()

# Interface principale
tab1, tab2, tab3 = st.tabs(["📝 Analyse d'un Avis", "📊 Analyse du Dataset", "ℹ️ À Propos"])

# TAB 1: Analyse d'un avis
with tab1:
    st.header("Analyse d'un Avis Individuel")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        text_input = st.text_area(
            "✍️ Entrez un avis client:",
            height=150,
            placeholder="Ex: The food was amazing! The service was excellent and the atmosphere was perfect. I highly recommend this restaurant!"
        )
    
    with col2:
        st.write("**Exemples d'avis:**")
        example_reviews = [
            "The food was amazing! I loved every bite!",
            "I'm very disappointed. The service was terrible and slow.",
            "Wow! This place is incredible! Best restaurant ever!",
            "The food was okay, nothing special really."
        ]
        for i, example in enumerate(example_reviews, 1):
            if st.button(f"Exemple {i}", key=f"ex_{i}"):
                text_input = example
                st.rerun()
    
    analyze_btn = st.button("🔍 Analyser l'avis", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not text_input.strip():
            st.warning("⚠️ Veuillez entrer un avis à analyser.")
        else:
            with st.spinner("Analyse en cours..."):
                # Analyse de sentiment
                sentiment, sent_conf, sent_probs = predict_sentiment(
                    text_input, tokenizer, sentiment_model, device, MAX_LENGTH
                )
                
                # Analyse d'émotions
                emotion_scores = emotion_detector.predict_emotion(text_input)
                main_emotion, emotion_conf = emotion_detector.get_main_emotion(text_input)
                
                # Affichage des résultats
                st.markdown("---")
                st.subheader("📌 Résultats de l'Analyse")
                
                # Métriques principales
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    sentiment_color = {
                        "Positif": "🟢",
                        "Négatif": "🔴",
                        "Neutre": "🟡"
                    }
                    st.metric(
                        "Sentiment",
                        f"{sentiment_color.get(sentiment, '⚪')} {sentiment}",
                        f"{sent_conf*100:.1f}%"
                    )
                
                with col2:
                    emotion_icons = {
                        "joie": "😊",
                        "tristesse": "😢",
                        "colère": "😠",
                        "surprise": "😲",
                        "neutre": "😐"
                    }
                    st.metric(
                        "Émotion Principale",
                        f"{emotion_icons.get(main_emotion, '😐')} {main_emotion.capitalize()}",
                        f"{emotion_conf*100:.1f}%"
                    )
                
                with col3:
                    # Satisfaction
                    if sentiment == "Positif" and sent_conf >= 0.6:
                        satisfaction = "Satisfait ✅"
                    elif sentiment == "Négatif" and sent_conf >= 0.6:
                        satisfaction = "Non satisfait ❌"
                    else:
                        satisfaction = "Moyen 🤝"
                    st.metric("Satisfaction", satisfaction)
                
                # Graphiques
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Probabilités de Sentiment")
                    fig_sent = go.Figure(data=[
                        go.Bar(
                            x=["Négatif", "Neutre", "Positif"],
                            y=[sent_probs[0], sent_probs[1], sent_probs[2]],
                            marker_color=['#ef4444', '#f59e0b', '#10b981']
                        )
                    ])
                    fig_sent.update_layout(
                        yaxis_title="Probabilité",
                        height=300,
                        showlegend=False
                    )
                    st.plotly_chart(fig_sent, use_container_width=True)
                
                with col2:
                    st.subheader("📊 Distribution des Émotions")
                    emotions_list = list(emotion_scores.keys())
                    values_list = list(emotion_scores.values())
                    colors = ['#10b981', '#3b82f6', '#ef4444', '#f59e0b', '#6b7280']
                    
                    fig_emotion = go.Figure(data=[
                        go.Bar(
                            x=emotions_list,
                            y=values_list,
                            marker_color=colors[:len(emotions_list)]
                        )
                    ])
                    fig_emotion.update_layout(
                        yaxis_title="Score",
                        height=300,
                        showlegend=False
                    )
                    st.plotly_chart(fig_emotion, use_container_width=True)
                
                # Détails
                with st.expander("🔍 Détails de l'analyse"):
                    st.write("**Texte analysé:**")
                    st.code(text_input, language="text")
                    
                    st.write("**Probabilités de sentiment:**")
                    st.json({
                        "Négatif": f"{sent_probs[0]*100:.2f}%",
                        "Neutre": f"{sent_probs[1]*100:.2f}%",
                        "Positif": f"{sent_probs[2]*100:.2f}%"
                    })
                    
                    st.write("**Scores d'émotions:**")
                    st.json({k: f"{v*100:.2f}%" for k, v in emotion_scores.items()})

# TAB 2: Analyse du dataset
with tab2:
    st.header("📊 Analyse du Dataset Complet")
    
    # Chargement du dataset
    @st.cache_data
    def load_dataset():
        try:
            df = pd.read_csv("TA_restaurants_ML_clean_cleaned.csv")
            return df
        except FileNotFoundError:
            st.error("Fichier dataset non trouvé!")
            return None
    
    df = load_dataset()
    
    if df is not None:
        st.success(f"✅ Dataset chargé: {len(df)} avis")
        
        # Options d'analyse
        analysis_option = st.radio(
            "Type d'analyse:",
            ["Statistiques générales", "Analyse par émotions", "Nuage de mots"],
            horizontal=True
        )
        
        if analysis_option == "Statistiques générales":
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total d'avis", len(df))
            with col2:
                st.metric("Restaurants uniques", df['Name'].nunique())
            with col3:
                st.metric("Villes", df['City'].nunique())
            with col4:
                avg_rating = df['Rating'].mean()
                st.metric("Note moyenne", f"{avg_rating:.2f}")
            
            # Distribution des notes
            st.subheader("Distribution des Notes")
            fig_rating = px.histogram(
                df,
                x='Rating',
                nbins=10,
                title="Distribution des notes (1-5)",
                labels={'Rating': 'Note', 'count': 'Nombre d\'avis'}
            )
            st.plotly_chart(fig_rating, use_container_width=True)
            
            # Top restaurants
            st.subheader("Top 10 Restaurants par Nombre d'Avis")
            top_restaurants = df['Name'].value_counts().head(10)
            fig_top = px.bar(
                x=top_restaurants.values,
                y=top_restaurants.index,
                orientation='h',
                labels={'x': 'Nombre d\'avis', 'y': 'Restaurant'}
            )
            st.plotly_chart(fig_top, use_container_width=True)
        
        elif analysis_option == "Analyse par émotions":
            st.info("💡 Cette fonctionnalité nécessite d'analyser tous les avis. Cela peut prendre du temps.")
            
            if st.button("🚀 Lancer l'analyse d'émotions sur un échantillon"):
                sample_size = st.slider("Taille de l'échantillon", 10, 1000, 100)
                sample_df = df.sample(min(sample_size, len(df)))
                
                progress_bar = st.progress(0)
                emotions_list = []
                
                for idx, row in sample_df.iterrows():
                    review = str(row.get('Review_clean', row.get('Review', '')))
                    if review and review != 'nan':
                        emotion, _ = emotion_detector.get_main_emotion(review)
                        emotions_list.append(emotion)
                    progress_bar.progress((idx + 1) / len(sample_df))
                
                # Graphique de distribution
                emotion_counts = Counter(emotions_list)
                fig_emotions = px.pie(
                    values=list(emotion_counts.values()),
                    names=list(emotion_counts.keys()),
                    title="Distribution des Émotions dans les Avis"
                )
                st.plotly_chart(fig_emotions, use_container_width=True)
        
        elif analysis_option == "Nuage de mots":
            st.subheader("Nuage de Mots des Avis")
            
            # Collecter tous les textes
            all_texts = " ".join(df['Review_clean'].dropna().astype(str).tolist())
            
            if all_texts:
                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    max_words=100
                ).generate(all_texts)
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)

# TAB 3: À propos
with tab3:
    st.header("ℹ️ À Propos du Projet")
    
    st.markdown("""
    ### 📋 Description du Projet
    
    **Projet NLP: Analyse de sentiments sur les avis de restaurants avec détection d'émotions spécifiques**
    
    **Auteur:** Oumaima AYADI
    
    **Objectif:** 
    Réaliser une analyse fine des avis clients pour un restaurant ou un service, en détectant non seulement 
    si un avis est positif ou négatif, mais aussi quelle émotion principale ressort.
    
    ### 🎯 Fonctionnalités
    
    1. **Analyse de Sentiments**
       - Classification: Positif / Négatif / Neutre
       - Utilise un modèle DistilBERT fine-tuné
    
    2. **Détection d'Émotions**
       - Joie/Excitation 😊
       - Tristesse/Déception 😢
       - Colère/Frustration 😠
       - Surprise/Étonnement 😲
       - Neutre 😐
    
    3. **Visualisations**
       - Graphiques de probabilités
       - Distribution des émotions
       - Nuage de mots
       - Statistiques du dataset
    
    ### 🛠️ Technologies Utilisées
    
    - **Transformers (HuggingFace)**: Modèles NLP pré-entraînés
    - **PyTorch**: Framework de deep learning
    - **Streamlit**: Interface utilisateur
    - **Plotly**: Visualisations interactives
    - **WordCloud**: Nuages de mots
    
    ### 📊 Dataset
    
    - **Source**: TripAdvisor Restaurant Reviews
    - **Taille**: ~71,000 avis
    - **Colonnes**: Name, City, Rating, Review, Review_clean, etc.
    
    ### 📚 Références
    
    - HuggingFace Transformers: https://huggingface.co/transformers/
    - Streamlit: https://streamlit.io/
    - Dataset: Kaggle Restaurant Reviews
    """)

# Footer
st.markdown("---")
st.caption("Projet NLP - Analyse de Sentiments & Détection d'Émotions | Oumaima AYADI")
