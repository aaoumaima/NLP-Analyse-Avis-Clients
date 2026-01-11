# Script PowerShell pour déploiement Azure avec Docker Hub (sans ACR)
# Usage: .\deploy_azure_dockerhub.ps1
# 
# AVANT DE LANCER:
# 1. Créer un compte Docker Hub: https://hub.docker.com/signup
# 2. Se connecter: docker login
# 3. Modifier DOCKERHUB_USERNAME ci-dessous avec votre nom d'utilisateur Docker Hub

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DEPLOIEMENT AZURE - DOCKER HUB (SANS ACR)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# ⚠️ MODIFIEZ CECI avec votre nom d'utilisateur Docker Hub
$DOCKERHUB_USERNAME = "VOTRE_USERNAME_DOCKERHUB"  # ⚠️ À MODIFIER!

# Variables
$RESOURCE_GROUP = "rg-nlp-sentiment-analysis"
$CONTAINER_NAME = "nlp-streamlit-app"
$LOCATION = "eastus"  # Essayons East US
$DNS_LABEL = "nlp-sentiment-app" + (Get-Random -Maximum 999)
$IMAGE_NAME = "${DOCKERHUB_USERNAME}/nlp-sentiment-app:latest"

Write-Host "`nConfiguration:" -ForegroundColor Yellow
Write-Host "  Resource Group: $RESOURCE_GROUP"
Write-Host "  Container Name: $CONTAINER_NAME"
Write-Host "  Location: $LOCATION"
Write-Host "  Docker Hub Image: $IMAGE_NAME"
Write-Host "  DNS Label: $DNS_LABEL"
Write-Host ""
Write-Host "⚠️  IMPORTANT: Modifiez DOCKERHUB_USERNAME dans le script!" -ForegroundColor Red

if ($DOCKERHUB_USERNAME -eq "VOTRE_USERNAME_DOCKERHUB") {
    Write-Host "`n❌ ERREUR: Vous devez modifier DOCKERHUB_USERNAME dans le script!" -ForegroundColor Red
    Write-Host "1. Créez un compte sur https://hub.docker.com/signup" -ForegroundColor Yellow
    Write-Host "2. Modifiez la ligne 9 du script avec votre username" -ForegroundColor Yellow
    Write-Host "3. Exécutez: docker login" -ForegroundColor Yellow
    exit 1
}

# Vérifier Azure CLI
Write-Host "`n1. Verification d'Azure CLI..." -ForegroundColor Green
$azVersion = az --version 2>$null
if (-not $azVersion) {
    Write-Host "Azure CLI non trouve. Installation necessaire." -ForegroundColor Red
    Write-Host "Telechargez depuis: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}
Write-Host "Azure CLI OK" -ForegroundColor Green

# Connexion à Azure
Write-Host "`n2. Connexion a Azure..." -ForegroundColor Green
az login
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de la connexion Azure" -ForegroundColor Red
    exit 1
}

# Créer le Resource Group
Write-Host "`n3. Creation du Resource Group..." -ForegroundColor Green
az group create --name $RESOURCE_GROUP --location "$LOCATION" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Resource Group existe deja ou erreur" -ForegroundColor Yellow
} else {
    Write-Host "Resource Group cree" -ForegroundColor Green
}

# Vérifier Docker
Write-Host "`n4. Verification de Docker..." -ForegroundColor Green
$dockerVersion = docker --version 2>$null
if (-not $dockerVersion) {
    Write-Host "Docker non trouve. Installation necessaire." -ForegroundColor Red
    Write-Host "Telechargez depuis: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}
Write-Host "Docker OK" -ForegroundColor Green

# Vérifier connexion Docker Hub
Write-Host "`n5. Verification de la connexion Docker Hub..." -ForegroundColor Green
$dockerLogin = docker info 2>&1 | Select-String -Pattern "Username"
if (-not $dockerLogin) {
    Write-Host "⚠️  Vous n'etes pas connecte a Docker Hub" -ForegroundColor Yellow
    Write-Host "Executez: docker login" -ForegroundColor Yellow
    Write-Host "Voulez-vous continuer quand meme? (O/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -ne "O" -and $response -ne "o") {
        exit 1
    }
}

# Construire l'image Docker
Write-Host "`n6. Construction de l'image Docker..." -ForegroundColor Green
Write-Host "Cela peut prendre plusieurs minutes..." -ForegroundColor Yellow
docker build -t $IMAGE_NAME .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de la construction de l'image" -ForegroundColor Red
    exit 1
}
Write-Host "Image construite" -ForegroundColor Green

# Pousser l'image vers Docker Hub
Write-Host "`n7. Envoi de l'image vers Docker Hub..." -ForegroundColor Green
Write-Host "Cela peut prendre plusieurs minutes..." -ForegroundColor Yellow
docker push $IMAGE_NAME
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de l'envoi de l'image" -ForegroundColor Red
    Write-Host "Verifiez que vous etes connecte: docker login" -ForegroundColor Yellow
    exit 1
}
Write-Host "Image envoyee vers Docker Hub" -ForegroundColor Green

# Créer l'instance de conteneur (sans ACR, directement depuis Docker Hub)
Write-Host "`n8. Creation de l'instance de conteneur Azure..." -ForegroundColor Green
Write-Host "Cela peut prendre 2-3 minutes..." -ForegroundColor Yellow

# Essayer plusieurs régions si nécessaire
$regions = @("eastus", "westus2", "centralus", "southcentralus")
$containerCreated = $false

# Demander le mot de passe Docker Hub une seule fois
Write-Host "`n   Entrez votre mot de passe Docker Hub:" -ForegroundColor Yellow
$securePassword = Read-Host "Password" -AsSecureString
$DOCKERHUB_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))

foreach ($region in $regions) {
    Write-Host "`n   Tentative dans la region: $region" -ForegroundColor Yellow
    
    az container create `
      --resource-group $RESOURCE_GROUP `
      --name $CONTAINER_NAME `
      --image $IMAGE_NAME `
      --dns-name-label $DNS_LABEL `
      --ports 8501 `
      --cpu 2 `
      --memory 4 `
      --location "$region" `
      --registry-login-server "docker.io" `
      --registry-username $DOCKERHUB_USERNAME `
      --registry-password $DOCKERHUB_PASSWORD
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Conteneur cree dans $region" -ForegroundColor Green
        $containerCreated = $true
        $LOCATION = $region
        break
    } else {
        Write-Host "   ❌ Echec dans $region, essai suivant..." -ForegroundColor Red
    }
}

if (-not $containerCreated) {
    Write-Host "`n❌ Erreur: Impossible de creer le conteneur dans toutes les regions testees" -ForegroundColor Red
    Write-Host "Essayez manuellement avec une region specifique" -ForegroundColor Yellow
    exit 1
}

# Obtenir l'URL publique
Write-Host "`n9. Recuperation de l'URL publique..." -ForegroundColor Green
$FQDN = az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn -o tsv

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "DEPLOIEMENT TERMINE AVEC SUCCES!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Votre application est accessible a:" -ForegroundColor Yellow
Write-Host "http://$FQDN:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Resource Group: $RESOURCE_GROUP" -ForegroundColor White
Write-Host "Container Name: $CONTAINER_NAME" -ForegroundColor White
Write-Host "Region: $LOCATION" -ForegroundColor White
Write-Host ""
Write-Host "Pour arreter l'instance:" -ForegroundColor Yellow
Write-Host "az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --yes" -ForegroundColor Gray
Write-Host ""
Write-Host "Pour voir les logs:" -ForegroundColor Yellow
Write-Host "az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME" -ForegroundColor Gray
Write-Host ""
