# 🚀 Comment Lancer l'Application Streamlit

## 📋 Prérequis

1. **Python 3.8+** installé
2. **Toutes les dépendances** installées

## 🔧 Installation

### Étape 1: Installer les dépendances

```bash
pip install -r requirements.txt
```

Ou installer manuellement:

```bash
pip install streamlit pandas numpy plotly
```

### Étape 2: Vérifier que les fichiers sont présents

Assurez-vous d'avoir:
- ✅ `streamlit_app.py` (application principale)
- ✅ `emotion_detection.py` (module de détection)
- ✅ `TA_restaurants_balanced.csv` (dataset équilibré)
- ✅ `TA_restaurants_ML_clean_cleaned.csv` (dataset complet - optionnel)

## 🚀 Lancement

### Option 1: Application Principale (Recommandée)

```bash
streamlit run streamlit_app.py
```

### Option 2: Chatbot

```bash
streamlit run chatbot_app.py
```

### Option 3: Application Complète

```bash
streamlit run app_emotions.py
```

### Option 4: Application Simple

```bash
streamlit run app.py
```

## 🌐 Accès

Une fois lancé, l'application s'ouvrira automatiquement dans votre navigateur à:

**http://localhost:8501**

Si le navigateur ne s'ouvre pas automatiquement, copiez cette adresse dans votre navigateur.

## 📱 Fonctionnalités de l'Application

### Onglet 1: Analyser un Avis
- Saisir un avis client
- Obtenir l'analyse de sentiment
- Voir la détection d'émotions
- Visualiser les résultats avec des graphiques

### Onglet 2: Statistiques Dataset
- Voir les statistiques générales
- Distribution des sentiments
- Distribution des notes
- Aperçu des données

### Onglet 3: Analyse par Émotions
- Analyser un échantillon du dataset
- Voir la distribution des émotions
- Graphiques interactifs

### Onglet 4: À Propos
- Informations sur le projet
- Documentation

## 🛠️ Résolution de Problèmes

### Erreur "Module not found"

```bash
pip install streamlit pandas numpy plotly
```

### Erreur "Dataset not found"

Vérifiez que les fichiers CSV sont dans le même dossier que `streamlit_app.py`

### L'application ne démarre pas

```bash
# Vérifier la version de Python
python --version

# Réinstaller Streamlit
pip install --upgrade streamlit
```

### Port déjà utilisé

```bash
# Utiliser un autre port
streamlit run streamlit_app.py --server.port 8502
```

## 📊 Exemples d'Utilisation

### Exemple 1: Analyser un avis positif

1. Ouvrir l'onglet "Analyser un Avis"
2. Cliquer sur "Exemple 1 - Positif"
3. Cliquer sur "Analyser l'avis"
4. Voir les résultats

### Exemple 2: Voir les statistiques

1. Ouvrir l'onglet "Statistiques Dataset"
2. Consulter les métriques
3. Voir les graphiques

### Exemple 3: Analyser les émotions

1. Ouvrir l'onglet "Analyse par Émotions"
2. Choisir la taille de l'échantillon (ex: 100)
3. Cliquer sur "Lancer l'analyse"
4. Voir les résultats

## 🎯 Commandes Utiles

### Arrêter l'application
Appuyez sur `Ctrl+C` dans le terminal

### Recharger l'application
Appuyez sur `R` dans l'interface Streamlit ou cliquez sur "Rerun"

### Voir les logs
Les logs s'affichent dans le terminal où vous avez lancé l'application

## 📝 Notes

- L'application utilise le cache pour améliorer les performances
- Les graphiques sont interactifs (zoom, pan, etc.)
- Vous pouvez télécharger les graphiques en cliquant sur l'icône de téléchargement

---

**Bon test ! 🚀**
