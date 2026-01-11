# 🚀 Déploiement sur Streamlit Community Cloud (GRATUIT et SIMPLE!)

## ⚡ Option la Plus Simple - 5 Minutes!

### Étape 1: Créer un Dépôt GitHub

1. Aller sur **https://github.com**
2. Cliquer sur **"New repository"**
3. Nom: `nlp-sentiment-analysis` (ou autre nom)
4. **Important:** Ne pas cocher "Add a README file"
5. Cliquer sur **"Create repository"**

### Étape 2: Initialiser Git et Pousser le Code

Dans PowerShell, depuis `C:\Users\LENOVO\Desktop\NLP`:

```powershell
# Initialiser git (si pas déjà fait)
git init

# Ajouter les fichiers nécessaires
git add *.py requirements.txt .streamlit/ *.md Dockerfile

# Commit
git commit -m "NLP Sentiment Analysis App - Ready for Streamlit Cloud"

# Ajouter le remote GitHub (remplacez par votre URL)
git remote add origin https://github.com/VOTRE-USERNAME/nlp-sentiment-analysis.git

# Pousser
git branch -M main
git push -u origin main
```

**Note:** Les fichiers CSV peuvent être trop gros pour GitHub. Vous pouvez:
- Utiliser Git LFS pour les gros fichiers
- Ou stocker les datasets ailleurs (Azure Blob Storage)
- Ou ne pas les inclure si l'app peut fonctionner sans

### Étape 3: Déployer sur Streamlit Cloud

1. **Aller sur:** https://share.streamlit.io/
2. **Cliquer sur "Sign in"** (connectez-vous avec GitHub)
3. **Cliquer sur "New app"**
4. **Remplir le formulaire:**
   - **Repository:** `votre-username/nlp-sentiment-analysis`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py` (ou `chatbot_app.py`)
   - **App URL:** (optionnel, laissez par défaut)
5. **Cliquer sur "Deploy"**

### Étape 4: Attendre le Déploiement

- ⏳ Le déploiement prend 2-5 minutes
- ✅ Vous verrez "Your app is live!"
- 🌐 Votre URL sera: `https://nlp-sentiment-analysis.streamlit.app`

---

## 📝 Fichiers Nécessaires sur GitHub

### ✅ Fichiers à Inclure

```
nlp-sentiment-analysis/
├── streamlit_app.py          ✅ Application principale
├── chatbot_app.py            ✅ Application chatbot
├── emotion_detection.py      ✅ Module d'émotions
├── requirements.txt          ✅ Dépendances
├── .streamlit/
│   └── config.toml           ✅ Configuration
├── README.md                 ✅ Documentation
└── *.py                      ✅ Autres scripts
```

### ⚠️ Fichiers à Exclure (Gros Fichiers)

Si les CSV sont trop gros (>100MB), créez un `.gitignore`:

```gitignore
# Datasets (trop gros pour GitHub)
*.csv
TA_restaurants_*.csv

# Ou utilisez Git LFS pour les gros fichiers
# Installer Git LFS: git lfs install
# Puis: git lfs track "*.csv"
```

### Option: Stocker les Datasets sur Azure Blob Storage

Si vous ne pouvez pas inclure les CSV sur GitHub, modifiez `streamlit_app.py` pour télécharger depuis Azure Blob Storage.

---

## 🔧 Configuration Avancée

### Utiliser un Dataset Externe

Si les CSV sont trop gros, modifiez `streamlit_app.py`:

```python
# Au lieu de charger depuis le fichier local
@st.cache_data
def load_dataset():
    # Option 1: Depuis Azure Blob Storage
    from azure.storage.blob import BlobServiceClient
    # ... code pour télécharger depuis Azure
    
    # Option 2: Depuis une URL publique
    # return pd.read_csv("https://votre-url.com/dataset.csv")
    
    # Option 3: Utiliser un échantillon seulement
    # return pd.read_csv("TA_restaurants_balanced.csv", nrows=1000)
```

---

## ✅ Checklist de Déploiement Streamlit Cloud

- [ ] Compte GitHub créé
- [ ] Dépôt GitHub créé
- [ ] Code poussé sur GitHub
- [ ] `requirements.txt` à jour
- [ ] `.streamlit/config.toml` créé
- [ ] Fichiers CSV gérés (inclus ou stockés ailleurs)
- [ ] Application testée localement
- [ ] Déploiement sur Streamlit Cloud effectué
- [ ] Application accessible en ligne

---

## 🎉 Après le Déploiement

### Votre Application Sera Accessible à:
```
https://nlp-sentiment-analysis.streamlit.app
```

### Gestion de l'Application

- **Modifier le code:** Push sur GitHub → Redéploiement automatique
- **Voir les logs:** Streamlit Cloud Dashboard
- **Gérer l'app:** https://share.streamlit.io/ → Your apps

---

## 🚀 Avantages de Streamlit Cloud

- ✅ **Gratuit**
- ✅ **HTTPS automatique**
- ✅ **Redéploiement automatique** (chaque push)
- ✅ **Pas de configuration complexe**
- ✅ **URL personnalisable**
- ✅ **Logs intégrés**

---

## 📞 Support

- **Documentation Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **Forum Streamlit:** https://discuss.streamlit.io/

---

**C'est la méthode la plus simple! Bon déploiement! 🚀**
