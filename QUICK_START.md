# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Vérifier que le dataset est présent

Le fichier `TA_restaurants_ML_clean_cleaned.csv` doit être dans le dossier.

### 3. Lancer l'application

```bash
streamlit run app_emotions.py
```

L'application s'ouvrira automatiquement dans votre navigateur !

---

## 🎯 Utilisation Rapide

### Analyser un avis

1. Ouvrez l'onglet **"📝 Analyse d'un Avis"**
2. Entrez un avis dans la zone de texte
3. Cliquez sur **"🔍 Analyser l'avis"**
4. Consultez les résultats :
   - Sentiment (Positif/Négatif/Neutre)
   - Émotion principale (joie, tristesse, colère, surprise)
   - Graphiques de probabilités

### Analyser le dataset

1. Ouvrez l'onglet **"📊 Analyse du Dataset"**
2. Choisissez le type d'analyse :
   - **Statistiques générales** : Vue d'ensemble du dataset
   - **Analyse par émotions** : Distribution des émotions
   - **Nuage de mots** : Mots les plus fréquents

---

## ⚙️ Configuration

Dans la barre latérale, vous pouvez :

- **Changer le modèle de sentiment** : Entrez le chemin vers votre modèle fine-tuné
- **Activer le modèle d'émotions avancé** : Cochez la case (nécessite internet)
- **Ajuster la longueur max** : Pour les textes longs

---

## 🐛 Problèmes Courants

### Erreur "Module not found"

```bash
pip install -r requirements.txt
```

### Le modèle ne se charge pas

- Vérifiez que vous avez une connexion internet (pour télécharger les modèles)
- Ou utilisez le détecteur simple (décochez "Utiliser modèle d'émotions avancé")

### L'application ne démarre pas

```bash
# Vérifiez que Streamlit est installé
pip install streamlit

# Vérifiez la version de Python (doit être >= 3.8)
python --version
```

---

## 📞 Besoin d'aide ?

Consultez le fichier `README.md` pour plus de détails.
