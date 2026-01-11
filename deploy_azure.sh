#!/bin/bash
# Script de déploiement Azure pour l'application Streamlit
# Usage: bash deploy_azure.sh

echo "=========================================="
echo "DEPLOIEMENT AZURE - APPLICATION STREAMLIT"
echo "=========================================="

# Variables (modifiez selon vos besoins)
RESOURCE_GROUP="nlp-streamlit-rg"
ACR_NAME="nlpstreamlitregistry"
CONTAINER_NAME="nlp-streamlit-app"
APP_NAME="nlp-streamlit-app"
LOCATION="westeurope"

echo ""
echo "1. Connexion à Azure..."
az login

echo ""
echo "2. Création du Resource Group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo ""
echo "3. Création de l'Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

echo ""
echo "4. Connexion à ACR..."
az acr login --name $ACR_NAME

echo ""
echo "5. Construction de l'image Docker..."
docker build -t $ACR_NAME.azurecr.io/$APP_NAME:latest .

echo ""
echo "6. Envoi de l'image vers ACR..."
docker push $ACR_NAME.azurecr.io/$APP_NAME:latest

echo ""
echo "7. Récupération du mot de passe ACR..."
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

echo ""
echo "8. Création de l'instance de conteneur..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $ACR_NAME.azurecr.io/$APP_NAME:latest \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --registry-password $ACR_PASSWORD \
  --dns-name-label $APP_NAME \
  --ports 8501 \
  --cpu 2 \
  --memory 4

echo ""
echo "9. Récupération de l'URL publique..."
FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn -o tsv)

echo ""
echo "=========================================="
echo "DEPLOIEMENT TERMINE!"
echo "=========================================="
echo ""
echo "Votre application est accessible à:"
echo "http://$FQDN:8501"
echo ""
echo "Pour arrêter l'instance:"
echo "az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --yes"
echo ""
