# 🚀 Alternatives de Déploiement - Azure for Students

## ❌ Problème Rencontré

Votre abonnement **Azure for Students** a des restrictions sur les régions autorisées pour créer des ressources comme **Azure Container Registry (ACR)**.

**Erreur:** `RequestDisallowedByAzure - This policy maintains a set of best available regions...`

---

## ✅ Solution 1: Docker Hub (RECOMMANDÉ pour Azure)

Utiliser **Docker Hub** (gratuit) au lieu d'Azure Container Registry.

### Avantages
- ✅ Gratuit
- ✅ Pas de restrictions de région
- ✅ Simple à utiliser
- ✅ Compatible avec Azure Container Instances

### Étapes

#### 1. Créer un compte Docker Hub

1. Aller sur: https://hub.docker.com/signup
2. Créer un compte gratuit
3. Noter votre **username**

#### 2. Se connecter à Docker Hub

```powershell
docker login
```

Entrez votre username et mot de passe Docker Hub.

#### 3. Modifier le script

Ouvrez `deploy_azure_dockerhub.ps1` et modifiez la ligne 9:

```powershell
$DOCKERHUB_USERNAME = "VOTRE_USERNAME_DOCKERHUB"  # Remplacez par votre username
```

#### 4. Lancer le déploiement

```powershell
.\deploy_azure_dockerhub.ps1
```

Le script va:
1. Construire l'image Docker
2. L'envoyer vers Docker Hub
3. Créer le conteneur Azure depuis Docker Hub
4. Vous donner l'URL

---

## ✅ Solution 2: Streamlit Community Cloud (LE PLUS SIMPLE!)

### Avantages
- ✅ **100% GRATUIT**
- ✅ Pas besoin de Docker
- ✅ Pas besoin d'Azure
- ✅ Déploiement en 5 minutes
- ✅ URL automatique

### Étapes

#### 1. Créer un compte GitHub (si vous n'en avez pas)

https://github.com/signup

#### 2. Créer un nouveau dépôt

1. Aller sur https://github.com/new
2. Nom: `nlp-sentiment-analysis`
3. **Ne pas** cocher "Initialize with README"
4. Cliquer "Create repository"

#### 3. Pousser votre code vers GitHub

```powershell
cd C:\Users\LENOVO\Desktop\NLP

# Initialiser git (si pas déjà fait)
git init

# Ajouter les fichiers
git add *.py requirements.txt .streamlit/

# Commit
git commit -m "NLP Sentiment Analysis App"

# Ajouter le remote (remplacez USERNAME par votre username GitHub)
git remote add origin https://github.com/USERNAME/nlp-sentiment-analysis.git

# Pousser
git branch -M main
git push -u origin main
```

**Note:** Si vos fichiers CSV sont trop gros (>100MB), utilisez Git LFS ou stockez-les ailleurs.

#### 4. Déployer sur Streamlit Cloud

1. Aller sur: https://share.streamlit.io/
2. Cliquer "Sign in" et se connecter avec GitHub
3. Cliquer "New app"
4. Remplir:
   - **Repository:** `votre-username/nlp-sentiment-analysis`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Cliquer "Deploy"

#### 5. Attendre 2-5 minutes

Votre application sera accessible à:
```
https://nlp-sentiment-analysis.streamlit.app
```

---

## ✅ Solution 3: Déploiement Manuel Azure (Sans ACR)

Si vous voulez absolument utiliser Azure, vous pouvez déployer manuellement:

### Étape 1: Construire et pousser vers Docker Hub

```powershell
# Se connecter à Docker Hub
docker login

# Construire l'image
docker build -t VOTRE_USERNAME/nlp-app:latest .

# Pousser vers Docker Hub
docker push VOTRE_USERNAME/nlp-app:latest
```

### Étape 2: Créer le conteneur Azure

```powershell
# Se connecter à Azure
az login

# Créer Resource Group (essayez plusieurs régions)
az group create --name rg-nlp-sentiment --location eastus

# Créer le conteneur depuis Docker Hub
az container create `
  --resource-group rg-nlp-sentiment `
  --name nlp-app `
  --image VOTRE_USERNAME/nlp-app:latest `
  --dns-name-label nlp-app-123 `
  --ports 8501 `
  --cpu 2 `
  --memory 4 `
  --registry-login-server docker.io `
  --registry-username VOTRE_USERNAME `
  --registry-password VOTRE_MOT_DE_PASSE_DOCKERHUB
```

### Étape 3: Obtenir l'URL

```powershell
az container show --resource-group rg-nlp-sentiment --name nlp-app --query ipAddress.fqdn -o tsv
```

---

## 📊 Comparaison des Solutions

| Solution | Coût | Complexité | Temps | Recommandation |
|----------|------|------------|-------|----------------|
| **Streamlit Cloud** | Gratuit | ⭐ Très Simple | 5 min | ⭐⭐⭐⭐⭐ |
| **Docker Hub + Azure** | ~$5-30/mois | ⭐⭐ Moyen | 20 min | ⭐⭐⭐⭐ |
| **Azure ACR** | ~$5-30/mois | ⭐⭐⭐ Complexe | 30 min | ❌ Bloqué |

---

## 🎯 Recommandation Finale

### Pour un Projet Universitaire / Démo:

👉 **Streamlit Community Cloud** (Solution 1)

**Pourquoi?**
- ✅ Gratuit
- ✅ Le plus simple
- ✅ Pas de configuration complexe
- ✅ URL permanente
- ✅ Mise à jour automatique depuis GitHub

### Pour Production Professionnelle:

👉 **Docker Hub + Azure Container Instances** (Solution 2)

**Pourquoi?**
- ✅ Plus de contrôle
- ✅ Intégration Azure
- ✅ Scalabilité
- ✅ Pas de restrictions de région

---

## 🐛 Dépannage

### Erreur: "Docker login failed"

**Solution:**
```powershell
docker logout
docker login
```

### Erreur: "Image push failed"

**Solutions:**
1. Vérifier que vous êtes connecté: `docker login`
2. Vérifier que l'image existe: `docker images`
3. Réessayer: `docker push VOTRE_USERNAME/nlp-app:latest`

### Erreur: "Container creation failed"

**Solutions:**
1. Essayer une autre région
2. Vérifier les logs: `az container logs --resource-group rg-nlp-sentiment --name nlp-app`
3. Vérifier que l'image existe sur Docker Hub

---

## 📝 Checklist

### Pour Streamlit Cloud:
- [ ] Compte GitHub créé
- [ ] Dépôt GitHub créé
- [ ] Code poussé vers GitHub
- [ ] Compte Streamlit Cloud créé
- [ ] Application déployée

### Pour Docker Hub + Azure:
- [ ] Compte Docker Hub créé
- [ ] `docker login` exécuté
- [ ] Script `deploy_azure_dockerhub.ps1` modifié
- [ ] Image construite et poussée
- [ ] Conteneur Azure créé

---

## ✅ Prêt à Déployer?

**Option Rapide (5 min):**
```powershell
# Suivez Solution 2: Streamlit Cloud
```

**Option Azure (20 min):**
```powershell
# Modifiez deploy_azure_dockerhub.ps1
# Puis: .\deploy_azure_dockerhub.ps1
```

---

**Bon déploiement! ☁️🚀**
