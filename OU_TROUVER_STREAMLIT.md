# 📍 Où Trouver les Applications Streamlit

## 🎯 Fichiers Streamlit dans le Projet

Votre projet contient **4 applications Streamlit** dans le dossier :

**`C:\Users\LENOVO\Desktop\NLP\`**

---

## 📁 Liste des Applications Streamlit

### 1. 🎨 **streamlit_app.py** (RECOMMANDÉ)
**Chemin:** `C:\Users\LENOVO\Desktop\NLP\streamlit_app.py`

**Description:** Application principale avec 4 onglets
- ✅ Analyser un Avis
- ✅ Statistiques Dataset
- ✅ Analyse par Émotions
- ✅ À Propos

**Pour lancer:**
```bash
streamlit run streamlit_app.py
```

---

### 2. 🤖 **chatbot_app.py**
**Chemin:** `C:\Users\LENOVO\Desktop\NLP\chatbot_app.py`

**Description:** Interface de type chatbot
- ✅ Historique des conversations
- ✅ Analyse en temps réel
- ✅ Réponses personnalisées

**Pour lancer:**
```bash
streamlit run chatbot_app.py
```

---

### 3. 🎯 **app_emotions.py**
**Chemin:** `C:\Users\LENOVO\Desktop\NLP\app_emotions.py`

**Description:** Application complète avec modèle BERT
- ✅ Analyse de sentiment (DistilBERT)
- ✅ Détection d'émotions
- ✅ Visualisations avancées

**Pour lancer:**
```bash
streamlit run app_emotions.py
```

---

### 4. 📱 **app.py**
**Chemin:** `C:\Users\LENOVO\Desktop\NLP\app.py`

**Description:** Application simple
- ✅ Analyse de sentiment basique
- ✅ Interface minimaliste

**Pour lancer:**
```bash
streamlit run app.py
```

---

## 🚀 Comment Lancer une Application

### Étape 1: Ouvrir le Terminal

1. Ouvrez PowerShell ou CMD
2. Naviguez vers le dossier du projet:
```bash
cd C:\Users\LENOVO\Desktop\NLP
```

### Étape 2: Installer Streamlit (si nécessaire)

```bash
pip install streamlit
```

### Étape 3: Lancer l'Application

Choisissez une des applications ci-dessus et lancez-la avec:

```bash
streamlit run [nom_du_fichier].py
```

**Exemple:**
```bash
streamlit run streamlit_app.py
```

### Étape 4: Accéder à l'Application

L'application s'ouvrira automatiquement dans votre navigateur à:

**http://localhost:8501**

---

## 📊 Comparaison des Applications

| Application | Complexité | Fonctionnalités | Recommandé pour |
|-------------|------------|-----------------|----------------|
| **streamlit_app.py** | ⭐⭐⭐ | Complète | Démonstration générale |
| **chatbot_app.py** | ⭐⭐⭐⭐ | Chat interactif | Démo interactive |
| **app_emotions.py** | ⭐⭐⭐⭐⭐ | Avec BERT | Analyse avancée |
| **app.py** | ⭐ | Basique | Test rapide |

---

## 🎯 Quelle Application Choisir ?

### Pour une Démonstration Générale
👉 **Utilisez `streamlit_app.py`**
- Interface complète
- 4 onglets
- Facile à utiliser

### Pour une Démonstration Interactive
👉 **Utilisez `chatbot_app.py`**
- Interface de chat
- Historique des conversations
- Plus engageant

### Pour une Analyse Avancée
👉 **Utilisez `app_emotions.py`**
- Modèle BERT
- Analyse plus précise
- Nécessite le modèle entraîné

### Pour un Test Rapide
👉 **Utilisez `app.py`**
- Simple et rapide
- Fonctionnalités de base

---

## 📂 Structure des Fichiers

```
C:\Users\LENOVO\Desktop\NLP\
│
├── streamlit_app.py          ← Application principale ⭐
├── chatbot_app.py            ← Application chatbot 🤖
├── app_emotions.py           ← Application complète 🎯
├── app.py                    ← Application simple 📱
│
├── emotion_detection.py      ← Module de détection d'émotions
├── TA_restaurants_balanced.csv  ← Dataset équilibré
│
└── requirements.txt          ← Dépendances (inclut streamlit)
```

---

## ⚙️ Prérequis

Avant de lancer une application Streamlit, assurez-vous d'avoir:

1. **Python 3.8+** installé
2. **Streamlit** installé:
   ```bash
   pip install streamlit
   ```
3. **Autres dépendances** (optionnel):
   ```bash
   pip install -r requirements.txt
   ```

---

## 🐛 Problèmes Courants

### Erreur "streamlit not found"

**Solution:**
```bash
pip install streamlit
```

### Erreur "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### L'application ne s'ouvre pas

**Solution:**
1. Vérifiez que le port 8501 n'est pas utilisé
2. Ouvrez manuellement: http://localhost:8501
3. Ou utilisez un autre port:
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

---

## 📝 Exemple Complet

```bash
# 1. Ouvrir le terminal
# 2. Aller dans le dossier
cd C:\Users\LENOVO\Desktop\NLP

# 3. Installer streamlit (si nécessaire)
pip install streamlit

# 4. Lancer l'application
streamlit run streamlit_app.py

# 5. L'application s'ouvre dans le navigateur
# URL: http://localhost:8501
```

---

## 🎉 Résumé

**Tous les fichiers Streamlit sont dans:**
```
C:\Users\LENOVO\Desktop\NLP\
```

**Application recommandée pour commencer:**
```
streamlit_app.py
```

**Commande pour lancer:**
```bash
streamlit run streamlit_app.py
```

---

**Bon test ! 🚀**
