# 🤖 Modèles Utilisés dans le Projet

## 📋 Vue d'Ensemble

Votre projet utilise **2 types de modèles** pour analyser les avis de restaurants:

1. **Modèle de Sentiment Analysis** (Analyse de sentiments)
2. **Modèle de Détection d'Émotions** (Détection d'émotions)

---

## 1. 🎯 Modèle de Sentiment Analysis

### Nom du Modèle
**`distilbert-base-uncased`**

### Type
**DistilBERT** - Version légère de BERT

### Source
**HuggingFace Transformers** (modèle pré-entraîné)

### Description
- **DistilBERT** est une version compacte et rapide de BERT
- Entraîné sur un large corpus de texte en anglais
- Optimisé pour être plus rapide tout en gardant de bonnes performances

### Fonctionnalité
- **Classification en 3 classes:**
  - ✅ **Positif** (rating 4-5)
  - ➖ **Neutre** (rating 3)
  - ❌ **Négatif** (rating 1-2)

### Utilisation dans le Projet
- Utilisé dans: `chatbot_app.py`, `app_emotions.py`, `app.py`
- Fine-tuné sur votre dataset d'avis de restaurants (dans `projet_nlp19 (7).py`)

### Avantages
- ✅ Rapide et efficace
- ✅ Bonne précision
- ✅ Modèle pré-entraîné (pas besoin d'entraîner from scratch)
- ✅ Léger (moins de mémoire que BERT complet)

---

## 2. 😊 Modèle de Détection d'Émotions

### Option A: Modèle Avancé (Optionnel)

#### Nom du Modèle
**`j-hartmann/emotion-english-distilroberta-base`**

#### Type
**DistilRoBERTa** - Version légère de RoBERTa

#### Source
**HuggingFace Transformers** (modèle pré-entraîné)

#### Description
- Modèle spécialement entraîné pour la détection d'émotions
- Basé sur DistilRoBERTa (version optimisée de RoBERTa)
- Entraîné sur des données d'émotions en anglais

#### Émotions Détectées
- 😊 **Joy** (Joie)
- 😢 **Sadness** (Tristesse)
- 😠 **Anger** (Colère)
- 😲 **Surprise**
- 😐 **Neutral** (Neutre)
- Et d'autres (fear, disgust)

#### Utilisation
- Activé en cochant "Utiliser modèle d'émotions avancé" dans l'interface
- Nécessite une connexion internet pour le téléchargement

---

### Option B: Détecteur Simple (Par Défaut)

#### Type
**Détecteur basé sur mots-clés** (SimpleEmotionDetector)

#### Description
- Détecteur personnalisé créé dans `emotion_detection.py`
- Utilise des dictionnaires de mots-clés pour chaque émotion
- Fonctionne **sans internet** et **sans modèle lourd**

#### Émotions Détectées
- 😊 **Joie** - Mots: amazing, wonderful, great, love, perfect...
- 😢 **Tristesse** - Mots: disappointed, sad, bad, terrible, awful...
- 😠 **Colère** - Mots: angry, frustrated, annoyed, horrible, hate...
- 😲 **Surprise** - Mots: surprised, unexpected, wow, incredible...
- 😐 **Neutre** - Aucune émotion particulière

#### Avantages
- ✅ Rapide (pas de calculs lourds)
- ✅ Fonctionne hors ligne
- ✅ Pas besoin de télécharger de modèle
- ✅ Facile à comprendre et modifier

#### Utilisation
- **Activé par défaut** dans l'application
- Utilisé quand "Utiliser modèle d'émotions avancé" est **décoché**

---

## 📊 Comparaison des Modèles

| Caractéristique | DistilBERT (Sentiment) | DistilRoBERTa (Émotions) | Détecteur Simple |
|----------------|------------------------|--------------------------|------------------|
| **Type** | Transformer | Transformer | Mots-clés |
| **Taille** | ~260 MB | ~260 MB | Quelques KB |
| **Vitesse** | Rapide | Rapide | Très rapide |
| **Précision** | Élevée | Très élevée | Moyenne |
| **Internet requis** | Oui (première fois) | Oui (première fois) | Non |
| **Fine-tuning** | Oui (sur dataset) | Non | Non |

---

## 🔧 Configuration dans l'Application

### Dans la Barre Latérale

1. **Chemin du modèle de sentiment:**
   - Par défaut: `distilbert-base-uncased`
   - Vous pouvez changer pour un modèle fine-tuné si vous en avez un

2. **Utiliser modèle d'émotions avancé:**
   - ✅ **Coché**: Utilise `j-hartmann/emotion-english-distilroberta-base`
   - ❌ **Décoché**: Utilise le détecteur simple (recommandé)

---

## 📝 Fichiers du Projet Utilisant les Modèles

### Modèle de Sentiment
- `chatbot_app.py` - Ligne 90-94
- `app_emotions.py` - Ligne 15-16
- `app.py` - Ligne 16
- `projet_nlp19 (7).py` - Ligne 129 (entraînement)

### Modèle d'Émotions
- `emotion_detection.py` - Tout le fichier
- `chatbot_app.py` - Ligne 124
- `app_emotions.py` - Ligne 20

---

## 🎓 Détails Techniques

### DistilBERT (Sentiment)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
```

**Architecture:**
- 6 couches (vs 12 pour BERT)
- 66 millions de paramètres (vs 110M pour BERT)
- 60% plus rapide que BERT
- 97% de la performance de BERT

### DistilRoBERTa (Émotions Avancé)

```python
model_name = "j-hartmann/emotion-english-distilroberta-base"
```

**Architecture:**
- Basé sur RoBERTa (version optimisée de BERT)
- Entraîné spécifiquement pour les émotions
- 7 classes d'émotions

### Détecteur Simple

```python
emotion_keywords = {
    'joie': ['amazing', 'wonderful', 'great', 'love', ...],
    'tristesse': ['disappointed', 'sad', 'bad', ...],
    'colère': ['angry', 'frustrated', 'hate', ...],
    'surprise': ['wow', 'incredible', 'unexpected', ...]
}
```

**Fonctionnement:**
- Compte les occurrences de mots-clés
- Calcule les probabilités
- Retourne l'émotion avec le score le plus élevé

---

## 🚀 Recommandations

### Pour une Utilisation Générale
👉 **Utilisez:**
- DistilBERT pour le sentiment (par défaut)
- Détecteur simple pour les émotions (décoché)

### Pour une Précision Maximale
👉 **Utilisez:**
- DistilBERT pour le sentiment
- DistilRoBERTa pour les émotions (coché)

### Pour une Utilisation Hors Ligne
👉 **Utilisez:**
- DistilBERT (téléchargé une fois)
- Détecteur simple pour les émotions

---

## 📚 Références

- **DistilBERT:** https://huggingface.co/distilbert-base-uncased
- **Emotion Model:** https://huggingface.co/j-hartmann/emotion-english-distilroberta-base
- **HuggingFace Transformers:** https://huggingface.co/transformers/

---

## ✅ Résumé

**Modèle Principal (Sentiment):**
- **DistilBERT** (`distilbert-base-uncased`)
- Classification: Positif / Neutre / Négatif

**Modèle Secondaire (Émotions):**
- **Option 1:** DistilRoBERTa (avancé, nécessite internet)
- **Option 2:** Détecteur simple (par défaut, fonctionne hors ligne)

**Tous les modèles sont pré-entraînés et prêts à l'emploi !** 🎉
