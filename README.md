# 🍽️ Analyse de Sentiments & Détection d'Émotions - Avis Restaurants

**Projet NLP - 5ème Année**  
**Auteur:** Oumaima AYADI  
**Date:** 2024

---

## 📋 Description du Projet

Ce projet réalise une analyse fine des avis clients pour des restaurants, en détectant non seulement si un avis est positif ou négatif, mais aussi quelle émotion principale ressort. Les émotions ciblées incluent : **joie/excitation**, **tristesse/déception**, **colère/frustration**, et **surprise/étonnement**.

### 🎯 Objectifs

1. **Analyse de Sentiments**: Classification des avis en Positif / Négatif / Neutre
2. **Détection d'Émotions**: Identification de l'émotion principale dans chaque avis
3. **Visualisation**: Graphiques et nuages de mots pour une analyse visuelle
4. **Interface Utilisateur**: Application web interactive avec Streamlit

---

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Téléchargement des modèles

Les modèles seront téléchargés automatiquement lors du premier lancement :
- **DistilBERT** pour l'analyse de sentiments
- **Emotion Detection Model** (optionnel) pour la détection d'émotions avancée

---

## 📁 Structure du Projet

```
NLP/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── TA_restaurants_ML_clean_cleaned.csv  # Dataset nettoyé
├── clean_data.py                      # Script de nettoyage des données
├── emotion_detection.py              # Module de détection d'émotions
├── app.py                            # Application Streamlit (version simple)
├── app_emotions.py                   # Application Streamlit (version complète)
├── projet_nlp19 (7).py               # Script d'entraînement du modèle
└── verify_cleaning.py                # Script de vérification du nettoyage
```

---

## 🎮 Utilisation

### 1. Lancer l'application Streamlit complète

```bash
streamlit run app_emotions.py
```

L'application s'ouvrira dans votre navigateur à l'adresse `http://localhost:8501`

### 2. Lancer l'application Streamlit simple

```bash
streamlit run app.py
```

### 3. Nettoyer les données

```bash
python clean_data.py
```

### 4. Tester la détection d'émotions

```bash
python emotion_detection.py
```

---

## 📊 Fonctionnalités de l'Application

### Onglet 1: Analyse d'un Avis Individuel

- **Saisie d'un avis**: Zone de texte pour entrer un avis client
- **Analyse de sentiment**: Classification Positif/Négatif/Neutre avec probabilités
- **Détection d'émotions**: Identification de l'émotion principale (joie, tristesse, colère, surprise)
- **Visualisations**: 
  - Graphique en barres des probabilités de sentiment
  - Graphique en barres des scores d'émotions
- **Détails**: Affichage des probabilités détaillées

### Onglet 2: Analyse du Dataset

- **Statistiques générales**:
  - Nombre total d'avis
  - Nombre de restaurants uniques
  - Note moyenne
  - Distribution des notes
  - Top 10 restaurants par nombre d'avis

- **Analyse par émotions**:
  - Distribution des émotions dans un échantillon d'avis
  - Graphique en camembert des émotions

- **Nuage de mots**:
  - Visualisation des mots les plus fréquents dans les avis

### Onglet 3: À Propos

- Description du projet
- Technologies utilisées
- Informations sur le dataset

---

## 🔧 Technologies Utilisées

### NLP & Machine Learning
- **Transformers (HuggingFace)**: Modèles NLP pré-entraînés
- **PyTorch**: Framework de deep learning
- **DistilBERT**: Modèle de sentiment analysis
- **scikit-learn**: Métriques et évaluation

### Interface & Visualisation
- **Streamlit**: Framework pour applications web interactives
- **Plotly**: Graphiques interactifs
- **Matplotlib/Seaborn**: Visualisations statiques
- **WordCloud**: Nuages de mots

### Traitement de Données
- **Pandas**: Manipulation de données
- **NumPy**: Calculs numériques

---

## 📈 Modèles Utilisés

### 1. Analyse de Sentiments

- **Modèle**: DistilBERT (distilbert-base-uncased)
- **Fine-tuning**: Sur le dataset d'avis de restaurants
- **Classes**: 3 (Négatif, Neutre, Positif)
- **Performance**: Accuracy et F1-score mesurés sur un set de test

### 2. Détection d'Émotions

**Option A - Modèle Pré-entraîné** (recommandé):
- **Modèle**: `j-hartmann/emotion-english-distilroberta-base`
- **Émotions**: joy, sadness, anger, surprise, fear, disgust, neutral
- **Mapping**: Vers nos catégories (joie, tristesse, colère, surprise, neutre)

**Option B - Détecteur par Mots-clés** (fallback):
- Basé sur des dictionnaires de mots-clés
- Fonctionne sans connexion internet
- Moins précis mais plus rapide

---

## 📊 Dataset

### Source
- **Dataset**: TripAdvisor Restaurant Reviews
- **Taille**: ~71,369 avis
- **Format**: CSV (UTF-8)

### Colonnes
- `Name`: Nom du restaurant
- `City`: Ville
- `Cuisine Style`: Style de cuisine
- `Ranking`: Classement
- `Rating`: Note (1-5)
- `Price Range`: Fourchette de prix
- `Number of Reviews`: Nombre d'avis
- `Review`: Avis original
- `Review_clean`: Avis nettoyé (pour NLP)

### Nettoyage Effectué
- Suppression de la colonne d'index inutile
- Correction des valeurs manquantes
- Normalisation du texte (minuscules, suppression dates)
- Suppression des doublons

---

## 🧪 Évaluation du Modèle

### Métriques Utilisées

- **Accuracy**: Taux de prédictions correctes
- **F1-Score**: Moyenne harmonique de précision et rappel
- **Precision**: Proportion de prédictions positives correctes
- **Recall**: Proportion de vrais positifs détectés
- **Matrice de Confusion**: Visualisation des erreurs de classification

### Résultats

Les résultats d'évaluation sont affichés dans le script d'entraînement (`projet_nlp19 (7).py`).

---

## 🛠️ Développement

### Structure du Code

1. **`emotion_detection.py`**: 
   - Classe `EmotionDetector`: Utilise un modèle pré-entraîné
   - Classe `SimpleEmotionDetector`: Détecteur basé sur mots-clés
   - Factory function pour choisir le détecteur

2. **`app_emotions.py`**:
   - Interface Streamlit complète
   - Intégration des deux modèles (sentiment + émotions)
   - Visualisations interactives

3. **`clean_data.py`**:
   - Script de nettoyage des données
   - Normalisation du texte
   - Gestion des valeurs manquantes

---

## 📝 Prochaines Étapes / Améliorations Possibles

### Court Terme
- [ ] Ajouter support multilingue (français/anglais)
- [ ] Améliorer la détection d'émotions avec fine-tuning
- [ ] Ajouter analyse par aspect (nourriture, service, prix, ambiance)

### Moyen Terme
- [ ] Déployer l'application sur Streamlit Cloud
- [ ] Ajouter export des résultats (PDF, Excel)
- [ ] Créer API REST pour intégration

### Long Terme
- [ ] Modèle de détection d'émotions fine-tuné sur le dataset
- [ ] Analyse temporelle des tendances
- [ ] Recommandations automatiques pour les restaurants

---

## 📚 Références

### Articles & Documentation
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [DistilBERT Paper](https://arxiv.org/abs/1910.01108)

### Datasets
- [Kaggle Restaurant Reviews](https://www.kaggle.com/datasets/archaeocharlie/restaurant-reviews)
- [Yelp Dataset](https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset)

### Modèles
- [DistilBERT Base Uncased](https://huggingface.co/distilbert-base-uncased)
- [Emotion Detection Model](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base)

---

## 👤 Auteur

**Oumaima AYADI**  
Projet réalisé dans le cadre du cours NLP - 5ème Année

---

## 📄 Licence

Ce projet est à des fins éducatives uniquement.

---

## 🙏 Remerciements

- HuggingFace pour les modèles pré-entraînés
- La communauté Streamlit
- Les contributeurs des datasets utilisés

---

## ❓ Support

Pour toute question ou problème, veuillez ouvrir une issue sur le dépôt du projet.

---

**Dernière mise à jour:** 2024
