# -*- coding: utf-8 -*-
"""
Application Streamlit - Projet NLP
Analyse de Sentiments et Détection d'Émotions sur les Avis de Restaurants
Auteur: Oumaima AYADI
"""

import streamlit as st
import pandas as pd
import numpy as np
from emotion_detection import SimpleEmotionDetector
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Configuration de la page
st.set_page_config(
    page_title="Analyse Sentiments & Émotions - Restaurants",
    page_icon="🍽️",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
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
st.markdown('<h1 class="main-title">🍽️ Analyse de Sentiments & Détection d\'Émotions</h1>', unsafe_allow_html=True)
st.markdown("**Projet NLP - Analyse des avis de restaurants**")
st.markdown("---")

# Initialisation du détecteur d'émotions
@st.cache_resource
def load_emotion_detector():
    """Charge le détecteur d'émotions"""
    return SimpleEmotionDetector()

emotion_detector = load_emotion_detector()

# Sidebar
st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown("### Options d'analyse")

# Onglets principaux
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Analyser un Avis",
    "📊 Statistiques Dataset",
    "🔍 Analyse par Émotions",
    "ℹ️ À Propos"
])

# ============================================
# ONGLET 1: ANALYSER UN AVIS
# ============================================
with tab1:
    st.header("📝 Analyse d'un Avis Individuel")
    
    # Zone de saisie
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_review = st.text_area(
            "✍️ Entrez un avis client:",
            height=150,
            placeholder="Ex: The food was amazing! The service was excellent and the atmosphere was perfect. I highly recommend this restaurant!"
        )
    
    with col2:
        st.markdown("### Exemples d'avis")
        examples = {
            "Exemple 1 - Positif": "The food was amazing! I loved every bite! The service was excellent!",
            "Exemple 2 - Négatif": "I'm very disappointed. The service was terrible and slow. The food was cold.",
            "Exemple 3 - Surprise": "Wow! This restaurant is incredible! I didn't expect such amazing food!",
            "Exemple 4 - Neutre": "The food was okay, nothing special really. The service was average."
        }
        
        for label, example in examples.items():
            if st.button(label, key=f"ex_{label}", use_container_width=True):
                user_review = example
                st.rerun()
    
    # Bouton d'analyse
    if st.button("🔍 Analyser l'avis", type="primary", use_container_width=True):
        if not user_review.strip():
            st.warning("⚠️ Veuillez entrer un avis à analyser.")
        else:
            with st.spinner("Analyse en cours..."):
                # Analyse d'émotions
                emotion_scores = emotion_detector.predict_emotion(user_review)
                main_emotion, emotion_conf = emotion_detector.get_main_emotion(user_review)
                
                # Analyse de sentiment basique (basée sur l'émotion)
                if main_emotion == "joie":
                    sentiment = "Positif"
                    sentiment_icon = "✅"
                    sentiment_color = "#10b981"
                elif main_emotion in ["tristesse", "colère"]:
                    sentiment = "Négatif"
                    sentiment_icon = "❌"
                    sentiment_color = "#ef4444"
                else:
                    sentiment = "Neutre"
                    sentiment_icon = "➖"
                    sentiment_color = "#f59e0b"
                
                # Affichage des résultats
                st.markdown("---")
                st.subheader("📌 Résultats de l'Analyse")
                
                # Métriques
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Sentiment",
                        f"{sentiment_icon} {sentiment}",
                        f"{emotion_conf*100:.1f}%"
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
                    if sentiment == "Positif":
                        satisfaction = "Satisfait ✅"
                    elif sentiment == "Négatif":
                        satisfaction = "Non satisfait ❌"
                    else:
                        satisfaction = "Moyen 🤝"
                    st.metric("Satisfaction", satisfaction)
                
                # Graphiques
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Distribution des Émotions")
                    emotions_list = list(emotion_scores.keys())
                    values_list = list(emotion_scores.values())
                    colors = ['#10b981', '#3b82f6', '#ef4444', '#f59e0b', '#6b7280']
                    
                    fig_emotion = go.Figure(data=[
                        go.Bar(
                            x=emotions_list,
                            y=values_list,
                            marker_color=colors[:len(emotions_list)],
                            text=[f"{v*100:.1f}%" for v in values_list],
                            textposition='auto'
                        )
                    ])
                    fig_emotion.update_layout(
                        yaxis_title="Score",
                        height=400,
                        showlegend=False,
                        xaxis_title="Émotions"
                    )
                    st.plotly_chart(fig_emotion, use_container_width=True)
                
                with col2:
                    st.subheader("📊 Graphique en Camembert")
                    fig_pie = px.pie(
                        values=values_list,
                        names=emotions_list,
                        title="Répartition des Émotions",
                        color_discrete_sequence=colors[:len(emotions_list)]
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Détails
                with st.expander("🔍 Détails de l'analyse"):
                    st.write("**Texte analysé:**")
                    st.code(user_review, language="text")
                    
                    st.write("**Scores d'émotions détaillés:**")
                    for emotion, score in emotion_scores.items():
                        st.write(f"- {emotion.capitalize()}: {score*100:.2f}%")
                    
                    st.write("**Interprétation:**")
                    if sentiment == "Positif":
                        st.success("Cet avis exprime une satisfaction claire. Le client est content de son expérience.")
                    elif sentiment == "Négatif":
                        st.error("Cet avis exprime une insatisfaction. Il serait important d'améliorer les points mentionnés.")
                    else:
                        st.info("Cet avis est neutre. L'expérience n'était ni exceptionnelle ni décevante.")

# ============================================
# ONGLET 2: STATISTIQUES DATASET
# ============================================
with tab2:
    st.header("📊 Statistiques du Dataset")
    
    # Charger le dataset
    @st.cache_data
    def load_dataset():
        try:
            df = pd.read_csv("TA_restaurants_balanced.csv")
            return df
        except FileNotFoundError:
            try:
                df = pd.read_csv("TA_restaurants_ML_clean_cleaned.csv")
                return df
            except:
                return None
    
    df = load_dataset()
    
    if df is not None:
        st.success(f"✅ Dataset chargé: {len(df)} avis")
        
        # Statistiques générales
        st.subheader("📈 Statistiques Générales")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total d'avis", len(df))
        
        with col2:
            if 'Name' in df.columns:
                st.metric("Restaurants uniques", df['Name'].nunique())
            else:
                st.metric("Colonnes", len(df.columns))
        
        with col3:
            if 'City' in df.columns:
                st.metric("Villes", df['City'].nunique())
            else:
                st.metric("Lignes", len(df))
        
        with col4:
            if 'Rating' in df.columns:
                avg_rating = df['Rating'].mean()
                st.metric("Note moyenne", f"{avg_rating:.2f}")
            else:
                st.metric("Dataset", "Équilibré")
        
        # Distribution des sentiments
        if 'sentiment' in df.columns:
            st.subheader("📊 Distribution des Sentiments")
            
            sentiment_counts = df['sentiment'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_bar = px.bar(
                    x=sentiment_counts.index,
                    y=sentiment_counts.values,
                    labels={'x': 'Sentiment', 'y': 'Nombre d\'avis'},
                    title="Distribution des Sentiments",
                    color=sentiment_counts.index,
                    color_discrete_map={
                        'Positif': '#10b981',
                        'Négatif': '#ef4444',
                        'Neutre': '#f59e0b'
                    }
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                fig_pie = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Répartition des Sentiments"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        # Distribution des notes
        if 'Rating' in df.columns:
            st.subheader("📊 Distribution des Notes")
            fig_rating = px.histogram(
                df,
                x='Rating',
                nbins=10,
                title="Distribution des Notes (1-5)",
                labels={'Rating': 'Note', 'count': 'Nombre d\'avis'}
            )
            st.plotly_chart(fig_rating, use_container_width=True)
        
        # Aperçu des données
        st.subheader("👀 Aperçu des Données")
        st.dataframe(df.head(10), use_container_width=True)
        
    else:
        st.error("❌ Impossible de charger le dataset. Vérifiez que les fichiers CSV sont présents.")

# ============================================
# ONGLET 3: ANALYSE PAR ÉMOTIONS
# ============================================
with tab3:
    st.header("🔍 Analyse par Émotions")
    
    df = load_dataset()
    
    if df is not None:
        st.info("💡 Cette fonctionnalité analyse les émotions dans le dataset. Cela peut prendre quelques secondes.")
        
        sample_size = st.slider(
            "Taille de l'échantillon à analyser",
            min_value=10,
            max_value=min(1000, len(df)),
            value=100,
            step=10
        )
        
        if st.button("🚀 Lancer l'analyse d'émotions", type="primary"):
            with st.spinner(f"Analyse de {sample_size} avis en cours..."):
                # Échantillonner
                sample_df = df.sample(min(sample_size, len(df)), random_state=42)
                
                # Analyser les émotions
                progress_bar = st.progress(0)
                emotions_list = []
                
                review_col = 'Review_clean' if 'Review_clean' in sample_df.columns else 'Review'
                
                for idx, row in sample_df.iterrows():
                    review = str(row.get(review_col, ''))
                    if review and review != 'nan' and len(review) > 10:
                        emotion, _ = emotion_detector.get_main_emotion(review)
                        emotions_list.append(emotion)
                    progress_bar.progress((idx + 1) / len(sample_df))
                
                # Statistiques des émotions
                emotion_counts = Counter(emotions_list)
                
                st.success(f"✅ Analyse terminée: {len(emotions_list)} avis analysés")
                
                # Graphiques
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Distribution des Émotions")
                    fig_bar = px.bar(
                        x=list(emotion_counts.keys()),
                        y=list(emotion_counts.values()),
                        labels={'x': 'Émotion', 'y': 'Nombre d\'avis'},
                        title="Nombre d'avis par Émotion",
                        color=list(emotion_counts.keys()),
                        color_discrete_map={
                            'joie': '#10b981',
                            'tristesse': '#3b82f6',
                            'colère': '#ef4444',
                            'surprise': '#f59e0b',
                            'neutre': '#6b7280'
                        }
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                with col2:
                    st.subheader("📊 Répartition en Pourcentage")
                    fig_pie = px.pie(
                        values=list(emotion_counts.values()),
                        names=list(emotion_counts.keys()),
                        title="Répartition des Émotions (%)"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Tableau récapitulatif
                st.subheader("📋 Résumé")
                summary_df = pd.DataFrame({
                    'Émotion': list(emotion_counts.keys()),
                    'Nombre': list(emotion_counts.values()),
                    'Pourcentage': [f"{v/len(emotions_list)*100:.1f}%" for v in emotion_counts.values()]
                })
                st.dataframe(summary_df, use_container_width=True)
    else:
        st.error("❌ Impossible de charger le dataset.")

# ============================================
# ONGLET 4: À PROPOS
# ============================================
with tab4:
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
       - Basée sur la détection d'émotions
    
    2. **Détection d'Émotions**
       - Joie/Excitation 😊
       - Tristesse/Déception 😢
       - Colère/Frustration 😠
       - Surprise/Étonnement 😲
       - Neutre 😐
    
    3. **Visualisations**
       - Graphiques en barres
       - Graphiques en camembert
       - Statistiques du dataset
    
    ### 🛠️ Technologies Utilisées
    
    - **Streamlit**: Interface utilisateur
    - **Plotly**: Visualisations interactives
    - **Pandas**: Traitement des données
    - **Emotion Detection**: Module personnalisé
    
    ### 📊 Dataset
    
    - **Source**: TripAdvisor Restaurant Reviews
    - **Taille**: ~71,000 avis (dataset complet) ou ~3,000 avis (dataset équilibré)
    - **Format**: CSV
    
    ### 📚 Structure du Projet
    
    - `streamlit_app.py`: Cette application
    - `emotion_detection.py`: Module de détection d'émotions
    - `TA_restaurants_balanced.csv`: Dataset équilibré
    - `TA_restaurants_ML_clean_cleaned.csv`: Dataset complet nettoyé
    
    ### 🚀 Utilisation
    
    1. **Analyser un avis**: Utilisez l'onglet "Analyser un Avis"
    2. **Voir les statistiques**: Consultez l'onglet "Statistiques Dataset"
    3. **Analyser les émotions**: Utilisez l'onglet "Analyse par Émotions"
    
    ### 📞 Support
    
    Pour plus d'informations, consultez:
    - `README.md`: Documentation complète
    - `QUICK_START.md`: Guide de démarrage rapide
    - `GUIDE_TEST.md`: Guide de test
    
    ---
    
    **Projet réalisé dans le cadre du cours NLP - 5ème Année**
    """)

# Footer
st.markdown("---")
st.caption("🍽️ Projet NLP - Analyse de Sentiments & Détection d'Émotions | Oumaima AYADI")
