# 🚀 Guide Simple de Déploiement sur Azure

## 📋 Avant de Commencer

### ✅ Vérifications Préalables

1. **Azure CLI installé** ? 
   ```powershell
   az --version
   ```
   Si non installé: https://aka.ms/installazurecliwindows

2. **Docker Desktop lancé** ?
   ```powershell
   docker --version
   ```
   Si non installé: https://www.docker.com/products/docker-desktop

3. **Fichiers présents** ?
   - ✅ `Dockerfile` (corrigé)
   - ✅ `streamlit_app.py`
   - ✅ `chatbot_app.py`
   - ✅ `emotion_detection.py`
   - ✅ `requirements.txt`

---

## 🎯 Méthode 1: Déploiement Automatique (RECOMMANDÉ) ⭐

### ✅ Le Plus Simple - Script Automatique

```powershell
cd C:\Users\LENOVO\Desktop\NLP

# Activer l'exécution de scripts (si nécessaire)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Lancer le script de déploiement
.\deploy_azure.ps1
```

**C'est tout !** Le script fait tout automatiquement:
1. ✅ Connexion à Azure
2. ✅ Création du Resource Group
3. ✅ Création de l'Azure Container Registry
4. ✅ Construction de l'image Docker
5. ✅ Envoi vers Azure
6. ✅ Création du conteneur
7. ✅ Affichage de l'URL

**Temps total:** 15-30 minutes

À la fin, vous obtiendrez une URL comme:
```
http://nlp-sentiment-app123.westeurope.azurecontainer.io:8501
```

---

## 🔧 Méthode 2: Déploiement Manuel

Si vous préférez faire chaque étape manuellement:

### Étape 1: Se Connecter à Azure

```powershell
az login
```
Une fenêtre de navigateur s'ouvrira pour la connexion.

### Étape 2: Créer un Resource Group

```powershell
az group create --name rg-nlp-sentiment --location "West Europe"
```

### Étape 3: Créer Azure Container Registry

```powershell
# Le nom doit être unique (ajoutez des chiffres si nécessaire)
az acr create --resource-group rg-nlp-sentiment --name nlpregistry123 --sku Basic
```

### Étape 4: Se Connecter au Registry

```powershell
az acr login --name nlpregistry123
```

### Étape 5: Construire l'Image Docker

```powershell
cd C:\Users\LENOVO\Desktop\NLP

docker build -t nlpregistry123.azurecr.io/nlp-app:latest .
```

**Temps:** 10-20 minutes

### Étape 6: Envoyer l'Image vers Azure

```powershell
docker push nlpregistry123.azurecr.io/nlp-app:latest
```

**Temps:** 5-10 minutes

### Étape 7: Créer le Conteneur

```powershell
# Obtenir le mot de passe
$PWD = az acr credential show --name nlpregistry123 --query "passwords[0].value" -o tsv

# Créer le conteneur
az container create `
  --resource-group rg-nlp-sentiment `
  --name nlp-app `
  --image nlpregistry123.azurecr.io/nlp-app:latest `
  --registry-login-server nlpregistry123.azurecr.io `
  --registry-username nlpregistry123 `
  --registry-password $PWD `
  --dns-name-label nlp-app-123 `
  --ports 8501 `
  --cpu 2 `
  --memory 4 `
  --location "West Europe"
```

### Étape 8: Obtenir l'URL

```powershell
az container show --resource-group rg-nlp-sentiment --name nlp-app --query ipAddress.fqdn -o tsv
```

Copiez l'URL et ajoutez `:8501` à la fin!

---

## 📊 Commandes Utiles Après Déploiement

### Voir les Logs

```powershell
az container logs --resource-group rg-nlp-sentiment --name nlp-app
```

### Voir l'État

```powershell
az container show --resource-group rg-nlp-sentiment --name nlp-app --query instanceView.state
```

### Arrêter le Conteneur (pour économiser)

```powershell
az container stop --resource-group rg-nlp-sentiment --name nlp-app
```

### Redémarrer

```powershell
az container start --resource-group rg-nlp-sentiment --name nlp-app
```

### Supprimer Tout

```powershell
az group delete --name rg-nlp-sentiment --yes
```

---

## 🐛 Dépannage

### Erreur: "ACR name already exists"

**Solution:** Utilisez un nom unique avec des chiffres:
```powershell
az acr create --resource-group rg-nlp-sentiment --name nlpregistry$(Get-Random -Maximum 9999) --sku Basic
```

### Erreur: "Docker build failed"

**Solutions:**
1. Vérifiez que Docker Desktop est lancé
2. Vérifiez que tous les fichiers sont présents
3. Vérifiez le Dockerfile

### L'Application ne Fonctionne Pas

**Vérifications:**
1. Voir les logs:
   ```powershell
   az container logs --resource-group rg-nlp-sentiment --name nlp-app
   ```
2. Vérifier l'état:
   ```powershell
   az container show --resource-group rg-nlp-sentiment --name nlp-app
   ```
3. Vérifier que vous utilisez le bon port (`:8501`)

---

## 💰 Coûts

- **Azure Container Registry (Basic):** ~$5/mois
- **Azure Container Instances (2 CPU, 4GB RAM):** 
  - Si actif 24/7: ~$31/mois
  - Si actif 8h/jour: ~$10/mois

**Recommandation:** Arrêtez le conteneur quand vous ne l'utilisez pas pour économiser!

---

## ✅ Checklist

Avant le déploiement:
- [ ] Azure CLI installé
- [ ] Docker Desktop installé et lancé
- [ ] Compte Azure actif
- [ ] Tous les fichiers présents
- [ ] Application testée localement

Pendant le déploiement:
- [ ] Script exécuté ou commandes manuelles complétées
- [ ] URL obtenue

Après le déploiement:
- [ ] Application accessible via l'URL
- [ ] Fonctionnalités testées
- [ ] Logs vérifiés (pas d'erreurs)

---

## 🎯 Recommandation

**Pour un déploiement rapide et sans erreur:**

👉 **Utilisez la Méthode 1 (Script Automatique)** 

Le script `deploy_azure.ps1` fait tout pour vous!

---

## 📚 Documentation Complète

Pour plus de détails, consultez:
- `GUIDE_DEPLOIEMENT_AZURE.md` - Guide complet détaillé

---

**Bon déploiement! ☁️🚀**
