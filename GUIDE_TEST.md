# 🧪 Guide Complet de Test du Projet

## 📋 Table des Matières

1. [Tests Automatiques](#tests-automatiques)
2. [Tests Manuels](#tests-manuels)
3. [Test du Chatbot](#test-du-chatbot)
4. [Test de l'Application](#test-de-lapplication)
5. [Vérification des Données](#vérification-des-données)
6. [Résolution de Problèmes](#résolution-de-problèmes)

---

## 🤖 Tests Automatiques

### Étape 1: Lancer le Script de Test

```bash
python test_project.py
```

Ce script teste automatiquement:
- ✅ Les imports de tous les modules
- ✅ L'existence des datasets
- ✅ La détection d'émotions
- ✅ Le traitement des données
- ✅ L'existence des scripts
- ✅ La documentation

### Résultat Attendu

```
============================================================
TESTS COMPLETS DU PROJET NLP
============================================================

TEST 1: Vérification des Imports
✅ pandas importé
✅ numpy importé
✅ torch importé
✅ transformers importé
✅ streamlit importé
...

🎉 TOUS LES TESTS SONT PASSÉS! Le projet est prêt!
```

---

## 🧪 Tests Manuels

### Test 1: Vérifier les Datasets

```bash
python -c "import pandas as pd; df = pd.read_csv('TA_restaurants_balanced.csv'); print(f'Dataset: {len(df)} lignes'); print(df['sentiment'].value_counts())"
```

**Résultat attendu:**
- Dataset équilibré: 3,138 lignes
- Distribution: 1,046 par classe (Négatif, Neutre, Positif)

### Test 2: Tester la Détection d'Émotions

```bash
python emotion_detection.py
```

**Résultat attendu:**
- Détecteur créé avec succès
- Tests sur plusieurs avis
- Émotions détectées correctement

### Test 3: Vérifier le Nettoyage des Données

```bash
python verify_cleaning.py
```

**Résultat attendu:**
- Comparaison dataset original vs nettoyé
- Vérification des améliorations

---

## 🤖 Test du Chatbot

### Étape 1: Lancer le Chatbot

```bash
streamlit run chatbot_app.py
```

### Étape 2: Tests à Effectuer

#### Test A: Charger les Modèles
1. Ouvrir la barre latérale (☰)
2. Cliquer sur "🔄 Charger/Recharger les Modèles"
3. ✅ Vérifier que les modèles se chargent (messages ✅)

#### Test B: Analyser un Avis Positif
1. Entrer: "The food was amazing! I loved every bite!"
2. Cliquer sur "🔍 Analyser"
3. ✅ Vérifier:
   - Sentiment: Positif ✅
   - Émotion: Joie 😊
   - Score de confiance > 50%

#### Test C: Analyser un Avis Négatif
1. Entrer: "I'm very disappointed. The service was terrible."
2. Cliquer sur "🔍 Analyser"
3. ✅ Vérifier:
   - Sentiment: Négatif ❌
   - Émotion: Tristesse 😢 ou Colère 😠
   - Score de confiance > 50%

#### Test D: Utiliser les Exemples
1. Cliquer sur "Exemple 1", "Exemple 2", etc.
2. ✅ Vérifier que l'avis se remplit automatiquement
3. Analyser et vérifier les résultats

#### Test E: Historique
1. Analyser plusieurs avis
2. ✅ Vérifier que l'historique s'affiche
3. ✅ Vérifier l'horodatage
4. Tester "🗑️ Effacer l'historique"

---

## 🎨 Test de l'Application Complète

### Étape 1: Lancer l'Application

```bash
streamlit run app_emotions.py
```

### Étape 2: Tests par Onglet

#### Onglet 1: Analyse d'un Avis
1. Entrer un avis
2. Cliquer sur "🔍 Analyser l'avis"
3. ✅ Vérifier:
   - Métriques (Sentiment, Émotion, Satisfaction)
   - Graphiques de probabilités
   - Graphique de distribution des émotions
   - Détails de l'analyse

#### Onglet 2: Analyse du Dataset
1. Sélectionner "Statistiques générales"
2. ✅ Vérifier:
   - Nombre total d'avis
   - Restaurants uniques
   - Note moyenne
   - Graphiques de distribution

3. Sélectionner "Analyse par émotions"
4. Cliquer sur "🚀 Lancer l'analyse"
5. ✅ Vérifier le graphique en camembert

6. Sélectionner "Nuage de mots"
7. ✅ Vérifier le nuage de mots généré

#### Onglet 3: À Propos
1. ✅ Vérifier que les informations s'affichent correctement

---

## 📊 Vérification des Données

### Vérifier le Dataset Équilibré

```python
import pandas as pd

# Charger le dataset
df = pd.read_csv('TA_restaurants_balanced.csv')

# Vérifications
print(f"Total: {len(df)} échantillons")
print(f"Colonnes: {list(df.columns)}")
print(f"\nDistribution:")
print(df['sentiment'].value_counts())
print(f"\nValeurs manquantes: {df.isnull().sum().sum()}")
print(f"Doublons: {df.duplicated().sum()}")
```

**Résultats attendus:**
- Total: 3,138 échantillons
- Distribution équilibrée: 1,046 par classe
- Aucune valeur manquante
- Aucun doublon

### Vérifier le Dataset Nettoyé

```python
import pandas as pd

df = pd.read_csv('TA_restaurants_ML_clean_cleaned.csv')

print(f"Total: {len(df)} échantillons")
print(f"Colonnes: {len(df.columns)}")
print(f"Valeurs manquantes Review_clean: {df['Review_clean'].isna().sum()}")
```

**Résultats attendus:**
- Total: ~71,369 échantillons
- 13 colonnes
- 0 valeur manquante dans Review_clean

---

## 🔧 Tests Avancés

### Test 1: Performance du Modèle

```python
from emotion_detection import SimpleEmotionDetector
import time

detector = SimpleEmotionDetector()

# Test de performance
start = time.time()
for i in range(100):
    detector.get_main_emotion("The food was amazing!")
end = time.time()

print(f"100 analyses en {end-start:.2f} secondes")
print(f"Moyenne: {(end-start)/100*1000:.2f} ms par analyse")
```

### Test 2: Cohérence des Résultats

```python
from emotion_detection import SimpleEmotionDetector

detector = SimpleEmotionDetector()

# Test avec le même texte plusieurs fois
text = "The food was amazing!"
results = [detector.get_main_emotion(text) for _ in range(10)]

# Vérifier la cohérence
emotions = [r[0] for r in results]
print(f"Émotions détectées: {set(emotions)}")
print(f"Cohérence: {len(set(emotions)) == 1}")
```

---

## 🐛 Résolution de Problèmes

### Problème 1: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problème 2: "Dataset non trouvé"

**Solution:**
```bash
# Créer le dataset équilibré
python balance_dataset.py
```

### Problème 3: "Modèles non chargés" dans Streamlit

**Solution:**
1. Vérifier la connexion internet
2. Cliquer sur "🔄 Charger/Recharger les Modèles"
3. Attendre le chargement complet

### Problème 4: Erreur d'encodage

**Solution:**
- Vérifier que les fichiers CSV sont en UTF-8
- Utiliser Python 3.8+

### Problème 5: Streamlit ne démarre pas

**Solution:**
```bash
# Vérifier l'installation
pip install streamlit --upgrade

# Vérifier le port
streamlit run chatbot_app.py --server.port 8501
```

---

## ✅ Checklist de Test Complète

### Avant la Présentation

- [ ] Tous les tests automatiques passent
- [ ] Le chatbot fonctionne correctement
- [ ] L'application complète fonctionne
- [ ] Les datasets sont accessibles
- [ ] Les visualisations s'affichent
- [ ] Les exemples fonctionnent
- [ ] L'historique fonctionne
- [ ] La documentation est complète

### Tests Fonctionnels

- [ ] Analyse de sentiment fonctionne
- [ ] Détection d'émotions fonctionne
- [ ] Visualisations s'affichent
- [ ] Nuage de mots se génère
- [ ] Statistiques sont correctes
- [ ] Exemples se chargent

### Tests de Performance

- [ ] Analyse rapide (< 2 secondes)
- [ ] Interface réactive
- [ ] Pas d'erreurs dans la console

---

## 📝 Rapport de Test

Après avoir effectué tous les tests, créez un rapport:

```markdown
# Rapport de Test - Projet NLP

Date: [DATE]
Testeur: [NOM]

## Résultats des Tests

### Tests Automatiques
- ✅/❌ Imports
- ✅/❌ Datasets
- ✅/❌ Détection d'émotions
- ✅/❌ Traitement des données
- ✅/❌ Scripts
- ✅/❌ Documentation

### Tests Manuels
- ✅/❌ Chatbot
- ✅/❌ Application complète
- ✅/❌ Visualisations

## Problèmes Rencontrés
[Liste des problèmes]

## Solutions Appliquées
[Liste des solutions]
```

---

## 🎯 Tests Recommandés pour la Présentation

### Test Rapide (5 minutes)

1. Lancer le chatbot
2. Tester 3 exemples différents
3. Vérifier les visualisations
4. Montrer l'historique

### Test Complet (15 minutes)

1. Tous les tests automatiques
2. Tous les onglets de l'application
3. Différents types d'avis
4. Vérification des données

---

**Bon test ! 🚀**

Pour toute question, consultez le `README.md` ou `QUICK_START.md`.
