# 🚀 Déploiement Simple - Guide Rapide

## 🎯 Option la Plus Simple: Streamlit Community Cloud (GRATUIT!)

### ⚡ En 5 Étapes

#### Étape 1: Créer un Dépôt GitHub

1. Aller sur https://github.com
2. Créer un nouveau dépôt (ex: `nlp-sentiment-analysis`)
3. **Important:** Ne pas initialiser avec README

#### Étape 2: Pousser Votre Code vers GitHub

Dans PowerShell, depuis votre dossier NLP:

```bash
# Initialiser git
git init

# Ajouter tous les fichiers (sauf les gros CSV si nécessaire)
git add *.py *.md *.txt .streamlit/

# Commit
git commit -m "NLP Sentiment Analysis App - Ready for deployment"

# Ajouter le remote GitHub (remplacez par votre URL)
git remote add origin https://github.com/VOTRE-USERNAME/nlp-sentiment-analysis.git

# Pousser
git branch -M main
git push -u origin main
```

**Note:** Si vos fichiers CSV sont trop gros (>100MB), utilisez Git LFS ou stockez-les ailleurs.

#### Étape 3: Créer le Fichier de Configuration Streamlit

Le fichier `.streamlit/config.toml` a déjà été créé ✅

#### Étape 4: Déployer sur Streamlit Cloud

1. **Aller sur:** https://share.streamlit.io/
2. **Cliquer sur "Sign in"** et se connecter avec GitHub
3. **Cliquer sur "New app"**
4. **Remplir le formulaire:**
   - Repository: `votre-username/nlp-sentiment-analysis`
   - Branch: `main`
   - Main file path: `streamlit_app.py` (ou `chatbot_app.py`)
5. **Cliquer sur "Deploy"**

#### Étape 5: Attendre le Déploiement

- ⏳ Le déploiement prend 2-5 minutes
- ✅ Vous verrez "Your app is live!"
- 🌐 Votre URL sera: `https://nlp-sentiment-analysis.streamlit.app`

---

## 🔧 Pour Azure Container Instances

### Prérequis
- Compte Azure (gratuit pendant 12 mois)
- Azure CLI installé
- Docker installé

### Commandes Rapides

```bash
# 1. Connexion à Azure
az login

# 2. Créer un Resource Group
az group create --name nlp-streamlit-rg --location westeurope

# 3. Créer un Container Registry
az acr create --resource-group nlp-streamlit-rg --name nlpstreamlitregistry --sku Basic

# 4. Se connecter à ACR
az acr login --name nlpstreamlitregistry

# 5. Construire et pousser l'image
docker build -t nlpstreamlitregistry.azurecr.io/nlp-app:latest .
docker push nlpstreamlitregistry.azurecr.io/nlp-app:latest

# 6. Obtenir le mot de passe ACR
az acr credential show --name nlpstreamlitregistry --query "passwords[0].value" -o tsv

# 7. Créer l'instance de conteneur
az container create \
  --resource-group nlp-streamlit-rg \
  --name nlp-streamlit-app \
  --image nlpstreamlitregistry.azurecr.io/nlp-app:latest \
  --registry-login-server nlpstreamlitregistry.azurecr.io \
  --registry-username nlpstreamlitregistry \
  --registry-password <mot-de-passe-ACR> \
  --dns-name-label nlp-streamlit-app \
  --ports 8501 \
  --cpu 2 \
  --memory 4

# 8. Obtenir l'URL
az container show --resource-group nlp-streamlit-rg --name nlp-streamlit-app --query ipAddress.fqdn -o tsv
```

---

## 📋 Fichiers Nécessaires pour le Déploiement

### ✅ Déjà Créés
- ✅ `Dockerfile` - Configuration Docker
- ✅ `.dockerignore` - Fichiers à ignorer
- ✅ `.streamlit/config.toml` - Configuration Streamlit
- ✅ `requirements.txt` - Dépendances Python

### ⚠️ À Vérifier
- [ ] `requirements.txt` contient toutes les dépendances
- [ ] Les datasets CSV sont accessibles (ou dans le dépôt)
- [ ] Les fichiers `.py` sont tous présents

---

## 🌐 URLs après Déploiement

### Streamlit Cloud
```
https://nlp-sentiment-analysis.streamlit.app
```

### Azure Container Instances
```
http://nlp-streamlit-app.westeurope.azurecontainer.io:8501
```

---

## 🎯 Recommandation Finale

**Pour commencer rapidement:**
👉 **Streamlit Community Cloud** (GRATUIT et SIMPLE)

**Pour production professionnelle:**
👉 **Azure Container Instances** (Plus de contrôle)

---

## 📞 Besoin d'Aide?

Consultez le fichier complet: `AZURE_DEPLOYMENT.md`

---

**Prêt à déployer! 🚀**
