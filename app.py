import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# -----------------------------
# CONFIG UI
# -----------------------------
st.set_page_config(page_title="Restaurant Reviews - Sentiment (BERT)", page_icon="🍽️", layout="centered")
st.title("🍽️ Sentiment Analysis - BERT (DistilBERT)")
st.write("Analyse automatique des avis clients (Négatif / Neutre / Positif).")

# -----------------------------
# SETTINGS
# -----------------------------
# 🔥 Modifie si besoin (Colab/Drive -> local)
DEFAULT_MODEL_PATH = "bert_sentiment_exam"  # ou "model" si tu as sauvegardé localement

MODEL_PATH = st.sidebar.text_input("Chemin du modèle", value=DEFAULT_MODEL_PATH)
MAX_LEN = st.sidebar.slider("Max length", 32, 256, 128, step=16)

# -----------------------------
# LOAD MODEL (cached)
# -----------------------------
@st.cache_resource
def load_model(model_path: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    model.eval()
    return tokenizer, model, device

def predict(text: str, tokenizer, model, device, max_len: int):
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

    # ✅ labels: 0 Negatif, 1 Neutre, 2 Positif (comme ton projet)
    label_map = {0: "Négatif", 1: "Neutre", 2: "Positif"}
    return label_map.get(pred_id, str(pred_id)), conf, probs.detach().cpu().numpy()

def satisfaction_and_loyalty(sentiment: str, conf: float):
    conf_pct = conf * 100
    if sentiment == "Positif" and conf_pct >= 60:
        return "Satisfait ✅", "Va probablement revenir ✅"
    if sentiment == "Négatif" and conf_pct >= 60:
        return "Non satisfait ❌", "Risque de ne pas revenir ❌"
    return "Moyen 🤝", "Incertain 🤔"

# -----------------------------
# APP
# -----------------------------
try:
    tokenizer, model, device = load_model(MODEL_PATH)
    st.sidebar.success("Modèle chargé ✅")
except Exception as e:
    st.sidebar.error("Erreur chargement modèle ❌")
    st.sidebar.write(str(e))
    st.stop()

text = st.text_area("✍️ Écris un avis client :", height=140, placeholder="Ex: The food was amazing but the service was slow...")

col1, col2 = st.columns([1, 1])
with col1:
    run_btn = st.button("🔍 Analyser")
with col2:
    st.caption("Astuce: teste en anglais ou français.")

if run_btn:
    if not text.strip():
        st.warning("Écris un avis d'abord.")
    else:
        sentiment, conf, probs = predict(text, tokenizer, model, device, MAX_LEN)
        sat, loy = satisfaction_and_loyalty(sentiment, conf)

        st.subheader("📌 Résultat")
        st.metric("Sentiment", sentiment, f"{conf*100:.2f}% confiance")

        st.write("**Satisfaction :**", sat)
        st.write("**Fidélité :**", loy)

        st.subheader("📊 Probabilités")
        st.write({
            "Négatif": float(probs[0]),
            "Neutre": float(probs[1]),
            "Positif": float(probs[2]),
        })

        st.subheader("🧾 Détails")
        st.code(text, language="text")

st.divider()
st.caption("Modèle: DistilBERT fine-tuné | Projet NLP19")
