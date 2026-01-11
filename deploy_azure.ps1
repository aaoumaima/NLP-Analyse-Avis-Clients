# Script PowerShell pour déploiement Azure
# Usage: .\deploy_azure.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DEPLOIEMENT AZURE - APPLICATION STREAMLIT" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Variables (modifiez selon vos besoins)
$RESOURCE_GROUP = "rg-nlp-sentiment-analysis"
$ACR_NAME = "nlpstreamlitregistry" + (Get-Random -Maximum 9999)
$CONTAINER_NAME = "nlp-streamlit-app"
$LOCATION = "East US"
$DNS_LABEL = "nlp-sentiment-app" + (Get-Random -Maximum 999)

Write-Host "`nConfiguration:" -ForegroundColor Yellow
Write-Host "  Resource Group: $RESOURCE_GROUP"
Write-Host "  ACR Name: $ACR_NAME"
Write-Host "  Container Name: $CONTAINER_NAME"
Write-Host "  Location: $LOCATION"
Write-Host "  DNS Label: $DNS_LABEL"

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

# Créer Azure Container Registry
Write-Host "`n4. Creation de l'Azure Container Registry..." -ForegroundColor Green
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --location "$LOCATION"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de la creation de l'ACR" -ForegroundColor Red
    exit 1
}
Write-Host "ACR cree: $ACR_NAME" -ForegroundColor Green

# Connexion à ACR
Write-Host "`n5. Connexion a ACR..." -ForegroundColor Green
az acr login --name $ACR_NAME
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de la connexion ACR" -ForegroundColor Red
    exit 1
}

# Vérifier Docker
Write-Host "`n6. Verification de Docker..." -ForegroundColor Green
$dockerVersion = docker --version 2>$null
if (-not $dockerVersion) {
    Write-Host "Docker non trouve. Installation necessaire." -ForegroundColor Red
    Write-Host "Telechargez depuis: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}
Write-Host "Docker OK" -ForegroundColor Green

# Construire l'image Docker
Write-Host "`n7. Construction de l'image Docker..." -ForegroundColor Green
Write-Host "Cela peut prendre plusieurs minutes..." -ForegroundColor Yellow
docker build -t ${ACR_NAME}.azurecr.io/${CONTAINER_NAME}:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de la construction de l'image" -ForegroundColor Red
    exit 1
}
Write-Host "Image construite" -ForegroundColor Green

# Pousser l'image vers ACR
Write-Host "`n8. Envoi de l'image vers ACR..." -ForegroundColor Green
Write-Host "Cela peut prendre plusieurs minutes..." -ForegroundColor Yellow
docker push ${ACR_NAME}.azurecr.io/${CONTAINER_NAME}:latest
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de l'envoi de l'image" -ForegroundColor Red
    exit 1
}
Write-Host "Image envoyee" -ForegroundColor Green

# Obtenir le mot de passe ACR
Write-Host "`n9. Recuperation du mot de passe ACR..." -ForegroundColor Green
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
if (-not $ACR_PASSWORD) {
    Write-Host "Erreur lors de la recuperation du mot de passe" -ForegroundColor Red
    exit 1
}

# Créer l'instance de conteneur
Write-Host "`n10. Creation de l'instance de conteneur Azure..." -ForegroundColor Green
Write-Host "Cela peut prendre 2-3 minutes..." -ForegroundColor Yellow

az container create `
  --resource-group $RESOURCE_GROUP `
  --name $CONTAINER_NAME `
  --image ${ACR_NAME}.azurecr.io/${CONTAINER_NAME}:latest `
  --registry-login-server ${ACR_NAME}.azurecr.io `
  --registry-username $ACR_NAME `
  --registry-password $ACR_PASSWORD `
  --dns-name-label $DNS_LABEL `
  --ports 8501 `
  --cpu 2 `
  --memory 4 `
  --location "$LOCATION"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de la creation du conteneur" -ForegroundColor Red
    exit 1
}

# Obtenir l'URL publique
Write-Host "`n11. Recuperation de l'URL publique..." -ForegroundColor Green
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
Write-Host ""
Write-Host "Pour arreter l'instance:" -ForegroundColor Yellow
Write-Host "az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --yes" -ForegroundColor Gray
Write-Host ""
Write-Host "Pour voir les logs:" -ForegroundColor Yellow
Write-Host "az container logs --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME" -ForegroundColor Gray
Write-Host ""
