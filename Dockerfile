# Dockerfile pour déploiement Azure
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application
COPY streamlit_app.py .
COPY chatbot_app.py .
COPY emotion_detection.py .

# Copier les datasets (optionnel, peut aussi utiliser Azure Blob Storage)
COPY TA_restaurants_balanced.csv .
COPY TA_restaurants_ML_clean_cleaned.csv .

# Exposer le port Streamlit
EXPOSE 8501

# Variables d'environnement
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Commande pour lancer Streamlit
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true"]
