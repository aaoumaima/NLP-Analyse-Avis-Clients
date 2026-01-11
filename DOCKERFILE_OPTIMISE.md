# 🚀 Dockerfile Optimisé - Version Rapide

## ⚠️ Problème avec le Build Actuel

Le build actuel prend ~22 heures, ce qui est **ABNORMALEMENT LONG**.

**Cause probable:** Les datasets CSV sont copiés dans l'image Docker, ce qui la rend très lourde.

---

## ✅ Solution: Dockerfile Optimisé

### Version 1: Sans Datasets (RECOMMANDÉ)

Les datasets peuvent être téléchargés au runtime ou stockés sur Azure Blob Storage.

```dockerfile
# Dockerfile optimisé (sans datasets CSV)
FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier SEULEMENT les fichiers Python (pas les CSV)
COPY streamlit_app.py .
COPY chatbot_app.py .
COPY emotion_detection.py .

# Exposer le port
EXPOSE 8501

# Variables d'environnement
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Commande pour lancer Streamlit
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true"]
```

**Temps de build estimé:** 10-20 minutes (au lieu de 22h+)

---

### Version 2: Avec .dockerignore

Créez un fichier `.dockerignore` pour exclure les gros fichiers:

```dockerignore
# Exclure les datasets (trop volumineux)
*.csv

# Exclure la documentation
*.md
!README.md

# Exclure les fichiers de développement
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Exclure les environnements virtuels
venv/
env/
.venv/
ENV/

# Exclure Git
.git/
.gitignore

# Exclure Docker
Dockerfile
.dockerignore
docker-compose.yml

# Exclure les logs
*.log

# Exclure les fichiers temporaires
*.tmp
*.bak
*.swp
*~

# Exclure les modèles pré-entraînés (téléchargés au runtime)
models/
*.pt
*.pth
*.pkl
*.h5
*.ckpt
```

**Ensuite**, utilisez le Dockerfile actuel mais les CSV ne seront pas copiés.

**Temps de build estimé:** 10-20 minutes

---

## 📊 Comparaison

| Version | Temps de Build | Taille Image |
|---------|----------------|--------------|
| **Actuel (avec CSV)** | 22h+ ⚠️ | Très lourd |
| **Optimisé (sans CSV)** | 10-20 min ✅ | Léger |
| **Avec .dockerignore** | 10-20 min ✅ | Léger |

---

## 🚀 Utiliser la Version Optimisée

### Option A: Remplacer le Dockerfile

```powershell
# Sauvegarder l'ancien
cp Dockerfile Dockerfile.backup

# Créer la version optimisée (voir ci-dessus)
# Puis construire:
docker build -t nlp-restau-optimized .
```

### Option B: Utiliser .dockerignore

1. Créer `.dockerignore` (voir contenu ci-dessus)
2. Reconstruire avec le Dockerfile actuel:

```powershell
docker build -t nlp-restau .
```

---

## 💡 Alternative: Datasets au Runtime

Si vous avez besoin des datasets, téléchargez-les au démarrage de l'application:

```python
# Dans streamlit_app.py ou chatbot_app.py

import os
import requests

def download_dataset_if_needed():
    dataset_url = "https://votre-stockage-azure.com/datasets/TA_restaurants_balanced.csv"
    local_path = "TA_restaurants_balanced.csv"
    
    if not os.path.exists(local_path):
        print("Téléchargement du dataset...")
        response = requests.get(dataset_url)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print("Dataset téléchargé!")
    
    return local_path
```

---

## ✅ Avantages de l'Optimisation

1. **Build 60x plus rapide** (20 min vs 22h)
2. **Image Docker plus légère** (plus facile à déployer)
3. **Déploiement plus rapide** sur Azure
4. **Moins de problèmes** de mémoire/disque

---

## 🎯 Recommandation

**Pour le déploiement Azure:**

1. Utiliser la **Version Optimisée** (sans CSV dans l'image)
2. Stocker les datasets sur **Azure Blob Storage**
3. Télécharger les datasets au **runtime** si nécessaire

Cela rendra le build et le déploiement **beaucoup plus rapides** !

---

**Temps de build attendu avec optimisation:** 10-20 minutes ✅
