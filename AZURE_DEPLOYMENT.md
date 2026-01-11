# ☁️ Guide de Déploiement Azure - Application Streamlit

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Option 1: Azure Container Instances (ACI)](#option-1-azure-container-instances)
3. [Option 2: Azure App Service](#option-2-azure-app-service)
4. [Option 3: Azure Machine Learning](#option-3-azure-machine-learning)
5. [Option 4: Streamlit Community Cloud](#option-4-streamlit-community-cloud)
6. [Configuration des Fichiers](#configuration-des-fichiers)
7. [Dépannage](#dépannage)

---

## 📋 Prérequis

### 1. Compte Azure
- Créer un compte Azure gratuit: https://azure.microsoft.com/free/
- Activer Azure CLI (optionnel mais recommandé)

### 2. Outils Nécessaires
- **Azure CLI** installé
- **Docker** (pour Option 1)
- **Git** (pour certaines options)

### 3. Installation Azure CLI

```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'

# Ou télécharger depuis: https://aka.ms/installazurecliwindows
```

Vérifier l'installation:
```bash
az --version
```

---

## 🚀 Option 1: Azure Container Instances (ACI) - RECOMMANDÉ

### Avantages
- ✅ Simple et rapide
- ✅ Pas besoin de serveur permanent
- ✅ Pay-as-you-go
- ✅ Parfait pour les démos

### Étape 1: Créer un Dockerfile

Créez un fichier `Dockerfile` dans le dossier du projet:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application
COPY *.py .
COPY *.csv .
COPY *.md .

# Exposer le port Streamlit
EXPOSE 8501

# Variables d'environnement
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Commande pour lancer Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Étape 2: Créer un fichier .dockerignore

```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.git
.gitignore
*.md
*.ipynb
.ipynb_checkpoints
```

### Étape 3: Créer un Container Registry Azure

```bash
# Connexion à Azure
az login

# Créer un resource group
az group create --name nlp-streamlit-rg --location westeurope

# Créer un Azure Container Registry (ACR)
az acr create --resource-group nlp-streamlit-rg --name nlpstreamlitregistry --sku Basic

# Se connecter à ACR
az acr login --name nlpstreamlitregistry
```

### Étape 4: Construire et Pousser l'Image Docker

```bash
# Aller dans le dossier du projet
cd C:\Users\LENOVO\Desktop\NLP

# Construire l'image
docker build -t nlpstreamlitregistry.azurecr.io/nlp-app:latest .

# Pousser l'image vers ACR
docker push nlpstreamlitregistry.azurecr.io/nlp-app:latest
```

### Étape 5: Déployer sur Azure Container Instances

```bash
# Créer l'instance de conteneur
az container create \
  --resource-group nlp-streamlit-rg \
  --name nlp-streamlit-app \
  --image nlpstreamlitregistry.azurecr.io/nlp-app:latest \
  --registry-login-server nlpstreamlitregistry.azurecr.io \
  --registry-username nlpstreamlitregistry \
  --registry-password <votre-mot-de-passe-ACR> \
  --dns-name-label nlp-streamlit-app \
  --ports 8501 \
  --cpu 2 \
  --memory 4
```

### Étape 6: Accéder à l'Application

```bash
# Obtenir l'URL publique
az container show --resource-group nlp-streamlit-rg --name nlp-streamlit-app --query ipAddress.fqdn
```

L'application sera accessible à: `http://<dns-name-label>.<region>.azurecontainer.io:8501`

---

## 🌐 Option 2: Azure App Service

### Avantages
- ✅ Intégration facile avec Azure
- ✅ Scaling automatique
- ✅ HTTPS inclus
- ✅ Custom domain

### Étape 1: Préparer les Fichiers

Créez un fichier `.deployment`:

```ini
[config]
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

Créez un fichier `startup.sh`:

```bash
#!/bin/bash
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port=8000 --server.address=0.0.0.0
```

### Étape 2: Créer l'App Service

```bash
# Créer un App Service Plan
az appservice plan create \
  --name nlp-streamlit-plan \
  --resource-group nlp-streamlit-rg \
  --sku B1 \
  --is-linux

# Créer l'application web
az webapp create \
  --resource-group nlp-streamlit-rg \
  --plan nlp-streamlit-plan \
  --name nlp-streamlit-app \
  --runtime "PYTHON|3.9"

# Configurer le démarrage
az webapp config set \
  --resource-group nlp-streamlit-rg \
  --name nlp-streamlit-app \
  --startup-file "startup.sh"

# Déployer depuis un dossier local
az webapp up \
  --resource-group nlp-streamlit-rg \
  --name nlp-streamlit-app \
  --runtime "PYTHON|3.9"
```

---

## 🤖 Option 3: Azure Machine Learning (Recommandé pour Production)

### Avantages
- ✅ Optimisé pour le ML
- ✅ Gestion des modèles
- ✅ Monitoring intégré
- ✅ Auto-scaling

### Étape 1: Créer un Workspace Azure ML

```bash
# Installer Azure ML CLI
az extension add -n azure-cli-ml

# Créer un workspace
az ml workspace create \
  --resource-group nlp-streamlit-rg \
  --workspace-name nlp-ml-workspace \
  --location westeurope
```

### Étape 2: Déployer avec Azure ML

Créer un fichier `deployment.yml`:

```yaml
name: streamlit-app
computeType: aci
codePath: .
scoringScript: streamlit_app.py
environment:
  condaFile: conda.yml
  dockerImage: python:3.9
```

---

## 🎯 Option 4: Streamlit Community Cloud (PLUS SIMPLE!)

### Avantages
- ✅ Gratuit
- ✅ Très simple
- ✅ Pas de configuration complexe
- ✅ HTTPS automatique

### Étape 1: Préparer le Projet

1. **Créer un compte GitHub** (si vous n'en avez pas)
   - Aller sur: https://github.com

2. **Créer un dépôt GitHub**
   - Nom suggéré: `nlp-sentiment-analysis`

3. **Ajouter un fichier `packages.txt`** (si besoin de packages système)

4. **Vérifier `requirements.txt`** est à jour

### Étape 2: Créer un Fichier `.streamlit/config.toml`

```toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Étape 3: Pousser vers GitHub

```bash
# Initialiser git (si pas déjà fait)
git init
git add .
git commit -m "Initial commit - NLP Sentiment Analysis App"

# Ajouter le remote GitHub
git remote add origin https://github.com/votre-username/nlp-sentiment-analysis.git
git branch -M main
git push -u origin main
```

### Étape 4: Déployer sur Streamlit Cloud

1. **Aller sur:** https://share.streamlit.io/
2. **Se connecter avec GitHub**
3. **Cliquer sur "New app"**
4. **Sélectionner le dépôt:** `nlp-sentiment-analysis`
5. **Sélectionner le fichier principal:** `streamlit_app.py` (ou `chatbot_app.py`)
6. **Cliquer sur "Deploy"**

### Étape 5: Accéder à l'Application

L'application sera accessible à:
```
https://nlp-sentiment-analysis.streamlit.app
```

---

## 📁 Configuration des Fichiers

### Fichier: `requirements.txt`

Assurez-vous qu'il contient:

```txt
streamlit>=1.28.0
transformers>=4.30.0
torch>=2.0.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
wordcloud>=1.9.0
scikit-learn>=1.3.0
datasets>=2.14.0
accelerate>=0.20.0
evaluate>=0.4.0
tqdm>=4.65.0
```

### Fichier: `.streamlit/config.toml` (pour Streamlit Cloud)

Créez un dossier `.streamlit` et un fichier `config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Fichier: `.gitignore`

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
*.csv
*.pt
*.pth
*.pkl
*.h5
*.ckpt
.ipynb_checkpoints/
.DS_Store
*.log
.env
.secrets
```

---

## 🐳 Option Docker Simple (Recommandée pour Débutants)

### Créer un Dockerfile Simplifié

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY *.py .
COPY TA_restaurants_balanced.csv .

# Exposer le port
EXPOSE 8501

# Lancer Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Tester Localement

```bash
# Construire l'image
docker build -t nlp-app .

# Lancer le conteneur
docker run -p 8501:8501 nlp-app

# Accéder à: http://localhost:8501
```

---

## 🔧 Dépannage

### Problème: Module not found après déploiement

**Solution:**
- Vérifier que tous les modules sont dans `requirements.txt`
- Vérifier que les fichiers Python sont bien copiés

### Problème: Dataset not found

**Solution:**
- Inclure les fichiers CSV dans le Dockerfile ou le dépôt Git
- Ou utiliser un stockage Azure Blob Storage

### Problème: Modèle trop lourd

**Solution:**
- Utiliser Azure Blob Storage pour stocker les modèles
- Télécharger les modèles au démarrage (cache)

### Problème: Timeout

**Solution:**
- Augmenter le timeout dans la configuration
- Optimiser le chargement des modèles (cache)

---

## 💰 Coûts Estimés

### Azure Container Instances
- **B1 (1 CPU, 1.5 GB RAM):** ~$15/mois
- **B2 (2 CPU, 3.5 GB RAM):** ~$30/mois

### Azure App Service
- **Basic B1:** ~$13/mois
- **Standard S1:** ~$55/mois

### Streamlit Community Cloud
- **Gratuit!** ✅

---

## 🎯 Recommandation

**Pour commencer:** Utilisez **Streamlit Community Cloud** (Option 4)
- ✅ Gratuit
- ✅ Simple
- ✅ Rapide à déployer
- ✅ Pas de configuration complexe

**Pour production:** Utilisez **Azure Container Instances** (Option 1)
- ✅ Professionnel
- ✅ Scalable
- ✅ Contrôle total

---

## 📝 Checklist de Déploiement

### Avant le Déploiement
- [ ] Tous les fichiers sont prêts
- [ ] `requirements.txt` est à jour
- [ ] Les datasets sont inclus ou accessibles
- [ ] Les tests passent localement
- [ ] L'application fonctionne en local

### Pour Streamlit Cloud
- [ ] Compte GitHub créé
- [ ] Dépôt GitHub créé
- [ ] Code poussé sur GitHub
- [ ] `.streamlit/config.toml` créé
- [ ] `requirements.txt` vérifié

### Pour Azure
- [ ] Compte Azure créé
- [ ] Azure CLI installé
- [ ] Docker installé (si Option 1)
- [ ] Dockerfile créé
- [ ] Resource Group créé

---

## 🚀 Démarrage Rapide - Streamlit Cloud

```bash
# 1. Créer un dépôt GitHub et pousser le code
git init
git add .
git commit -m "NLP Sentiment Analysis App"
git remote add origin https://github.com/votre-username/nlp-sentiment-analysis.git
git push -u origin main

# 2. Aller sur https://share.streamlit.io/
# 3. Se connecter avec GitHub
# 4. Cliquer sur "New app"
# 5. Sélectionner le dépôt et streamlit_app.py
# 6. Cliquer sur "Deploy"

# C'est tout! 🎉
```

---

## 📞 Support

Pour toute question sur le déploiement Azure:
- Documentation Azure: https://docs.microsoft.com/azure/
- Documentation Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud

---

**Bon déploiement ! ☁️🚀**
