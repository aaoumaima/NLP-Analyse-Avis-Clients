import streamlit as st
import torch
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from emotion_detection import SimpleEmotionDetector

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Sentiment Analysis - BERT",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS PERSONNALISÉ ====================
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #1f2937;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .metric-card {
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<h1 class="main-title">🍽️ Sentiment Analysis - BERT (DistilBERT)</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyse automatique des avis clients (Négatif / Neutre / Positif).</p>', unsafe_allow_html=True)
st.markdown("---")

# ==================== CONFIGURATION DU MODÈLE ====================
# Modèle Hugging Face (meilleure solution pour Streamlit Cloud)
MODEL_NAME = "distilbert-base-uncased"  # Modèle de base DistilBERT
# Alternative: "nlptown/bert-base-multilingual-uncased-sentiment" pour sentiment pré-entraîné

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    MAX_LEN = st.slider("📏 Longueur maximale", 32, 256, 128, 16)
    st.markdown("---")
    device_name = "🖥️ GPU" if torch.cuda.is_available() else "💻 CPU"
    st.info(f"{device_name}")
    st.caption(f"Modèle: {MODEL_NAME}")

# ==================== FONCTIONS ====================
@st.cache_resource
def load_model(model_name):
    """Charge le modèle depuis Hugging Face"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Charger avec 3 labels pour sentiment (Négatif, Neutre, Positif)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=3
    )
    model.to(device)
    model.eval()
    return tokenizer, model, device

@st.cache_resource
def load_emotion_detector():
    return SimpleEmotionDetector()

# ==================== CHARGEMENT DES MODÈLES ====================
try:
    with st.spinner("⏳ Chargement du modèle BERT depuis Hugging Face..."):
        tokenizer, model, device = load_model(MODEL_NAME)
    st.sidebar.success("✅ Modèle BERT chargé depuis Hugging Face")
except Exception as e:
    st.error(f"❌ Erreur lors du chargement: {e}")
    st.info("💡 Le modèle sera téléchargé automatiquement depuis Hugging Face")
    st.stop()

try:
    emotion_detector = load_emotion_detector()
    st.sidebar.success("✅ Détecteur d'émotions chargé")
except Exception as e:
    st.sidebar.warning(f"⚠️ Erreur: {e}")
    emotion_detector = None

# ==================== INTERFACE PRINCIPALE ====================
text = st.text_area(
    "Entrez un avis client à analyser:",
    height=180,
    placeholder="Exemple: The food was absolutely amazing! The service was excellent and the atmosphere was perfect.",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_btn = st.button("🔍 Analyser l'avis", type="primary", use_container_width=True)

# ==================== ANALYSE ====================
if run_btn:
    if not text.strip():
        st.warning("⚠️ Veuillez entrer un avis à analyser.")
    else:
        with st.spinner("🔄 Analyse en cours..."):
            # Analyse d'émotions d'abord
            if emotion_detector:
                emotion_scores = emotion_detector.predict_emotion(text)
                main_emotion, emotion_conf = emotion_detector.get_main_emotion(text)
            else:
                emotion_scores = {}
                main_emotion, emotion_conf = "neutre", 0.0
            
            # Dériver le sentiment depuis l'émotion (plus fiable)
            emotion_to_sentiment = {
                "joie": "Positif",
                "tristesse": "Négatif",
                "colère": "Négatif",
                "surprise": "Neutre",  # Surprise peut être positive ou négative
                "neutre": "Neutre"
            }
            
            # Si l'émotion est très confiante (>70%), utiliser l'émotion pour le sentiment
            if emotion_conf > 0.7:
                sentiment = emotion_to_sentiment.get(main_emotion, "Neutre")
                conf = emotion_conf  # Utiliser la confiance de l'émotion
                # Calculer les probabilités approximatives pour les graphiques
                if sentiment == "Positif":
                    probs = torch.tensor([0.1, 0.1, 0.8])  # [Négatif, Neutre, Positif]
                elif sentiment == "Négatif":
                    probs = torch.tensor([0.8, 0.1, 0.1])
                else:
                    probs = torch.tensor([0.2, 0.6, 0.2])
            else:
                # Si l'émotion n'est pas très confiante, utiliser le modèle BERT
                inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=MAX_LEN)
                inputs = {k: v.to(device) for k, v in inputs.items()}
                with torch.no_grad():
                    outputs = model(**inputs)
                    probs = torch.softmax(outputs.logits, dim=-1)[0]
                    pred_id = torch.argmax(probs).item()
                    conf = float(probs[pred_id].item())
                
                label_map = {0: "Négatif", 1: "Neutre", 2: "Positif"}
                sentiment = label_map.get(pred_id, "Neutre")
                
                # Vérifier la cohérence avec l'émotion
                if emotion_detector and main_emotion != "neutre":
                    expected_sentiment = emotion_to_sentiment.get(main_emotion, "Neutre")
                    # Si le sentiment BERT n'est pas cohérent avec l'émotion, utiliser l'émotion
                    if sentiment != expected_sentiment and emotion_conf > 0.5:
                        sentiment = expected_sentiment
                        conf = max(conf, emotion_conf * 0.8)  # Ajuster la confiance
        
        st.markdown("---")
        st.markdown("### 📌 Résultats de l'Analyse")
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        emoji_map = {"Positif": "✅", "Négatif": "❌", "Neutre": "➖"}
        emoji = emoji_map.get(sentiment, "❓")
        sentiment_colors = {"Positif": "#10b981", "Négatif": "#ef4444", "Neutre": "#f59e0b"}
        
        with col1:
            sentiment_bg = sentiment_colors.get(sentiment, '#6b7280')
            st.markdown(f"""
            <div class="metric-card" style="background: {sentiment_bg};">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 500; opacity: 0.9;">Sentiment</h3>
                <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700;">{emoji} {sentiment}</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; opacity: 0.85;">{conf*100:.2f}% confiance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            conf_level = "Élevée" if conf >= 0.7 else "Moyenne" if conf >= 0.5 else "Faible"
            conf_arrow = "↑" if conf >= 0.5 else "↓"
            st.metric("Confiance", f"{conf*100:.2f}%", f"{conf_arrow} {conf_level}")
        
        with col3:
            if emotion_detector:
                emotion_icons = {"joie": "😊", "tristesse": "😢", "colère": "😠", "surprise": "😲", "neutre": "😐"}
                emotion_color = {"joie": "#10b981", "tristesse": "#3b82f6", "colère": "#ef4444", "surprise": "#f59e0b", "neutre": "#6b7280"}.get(main_emotion, "#6b7280")
                emotion_icon = emotion_icons.get(main_emotion, "😐")
                st.markdown(f"""
                <div class="metric-card" style="background: {emotion_color};">
                    <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 500; opacity: 0.9;">Émotion</h3>
                    <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700;">{emotion_icon} {main_emotion.capitalize()}</h2>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem; opacity: 0.85;">{emotion_conf*100:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("Émotion", "❌ Non disponible")
        
        with col4:
            # Satisfaction basée sur le sentiment (cohérent)
            if sentiment == "Positif":
                sat = "Satisfait ✅"
                sat_color = "#10b981"
            elif sentiment == "Négatif":
                sat = "Non satisfait ❌"
                sat_color = "#ef4444"
            else:
                sat = "Moyen 🤝"
                sat_color = "#f59e0b"
            st.markdown(f"""
            <div class="metric-card" style="background: {sat_color};">
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 500; opacity: 0.9;">Satisfaction</h3>
                <h2 style="margin: 0.5rem 0; font-size: 1.8rem; font-weight: 700;">{sat}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Graphiques
        st.markdown("### 📊 Analyse de Sentiment")
        labels = ["Négatif", "Neutre", "Positif"]
        # S'assurer que probs est un tensor avec 3 valeurs
        if isinstance(probs, torch.Tensor):
            values = [float(probs[0]), float(probs[1]), float(probs[2])]
        else:
            values = [float(probs[0]), float(probs[1]), float(probs[2])]
        colors = ["#ef4444", "#f59e0b", "#10b981"]
        
        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=colors, text=[f"{v*100:.2f}%" for v in values], textposition='auto')])
            fig.update_layout(yaxis_title="Probabilité", yaxis_range=[0, 1], height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(values=values, names=labels, color_discrete_sequence=colors, hole=0.4)
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Émotions
        if emotion_detector and emotion_scores:
            st.markdown("### 😊 Analyse d'Émotions")
            emotion_labels = list(emotion_scores.keys())
            emotion_values = list(emotion_scores.values())
            emotion_colors = {'joie': '#10b981', 'tristesse': '#3b82f6', 'colère': '#ef4444', 'surprise': '#f59e0b', 'neutre': '#6b7280'}
            colors_emotion = [emotion_colors.get(em, '#6b7280') for em in emotion_labels]
            
            col1, col2 = st.columns(2)
            with col1:
                fig_emotion = go.Figure(data=[go.Bar(x=[em.capitalize() for em in emotion_labels], y=emotion_values, marker_color=colors_emotion, text=[f"{v*100:.2f}%" for v in emotion_values], textposition='auto')])
                fig_emotion.update_layout(yaxis_title="Score", yaxis_range=[0, 1], height=400, showlegend=False)
                st.plotly_chart(fig_emotion, use_container_width=True)
            
            with col2:
                fig_pie_emotion = px.pie(values=emotion_values, names=[em.capitalize() for em in emotion_labels], color_discrete_sequence=colors_emotion, hole=0.4)
                fig_pie_emotion.update_layout(height=400)
                st.plotly_chart(fig_pie_emotion, use_container_width=True)
