# 🐳 Test Docker Local - Avant Déploiement Azure

## ✅ Correction Appliquée

Le Dockerfile a été corrigé pour éviter l'erreur `--server.port requires an argument`.

**Changement:**
- ❌ Avant: `CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", ...]`
- ✅ Après: `CMD ["sh", "-c", "streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true"]`

---

## 🧪 Tester Localement Avant Azure

### Étape 1: Vérifier Docker

```powershell
docker --version
```

### Étape 2: Construire l'Image Docker

```powershell
cd C:\Users\LENOVO\Desktop\NLP

# Construire l'image (cela peut prendre 5-10 minutes)
docker build -t nlp-restau .
```

### Étape 3: Lancer le Conteneur

```powershell
# Lancer le conteneur
docker run -p 8501:8501 nlp-restau
```

### Étape 4: Accéder à l'Application

Ouvrez votre navigateur et allez à:
```
http://localhost:8501
```

---

## ✅ Vérifications

Si l'application fonctionne localement avec Docker, elle fonctionnera aussi sur Azure!

### Vérifier que Tout Fonctionne

1. ✅ L'application démarre sans erreur
2. ✅ Vous pouvez accéder à `http://localhost:8501`
3. ✅ Les modèles se chargent correctement
4. ✅ Vous pouvez analyser des avis

---

## 🚀 Après Test Local Réussi

Une fois que le test local fonctionne:

### Option 1: Déployer sur Azure

```powershell
# Utiliser le script PowerShell
.\deploy_azure.ps1
```

### Option 2: Déployer sur Streamlit Cloud

Suivez `deploy_streamlit_cloud.md`

---

## 🐛 Si Erreur Lors du Build

### Erreur: "Module not found"

**Solution:** Vérifier que `requirements.txt` contient toutes les dépendances

### Erreur: "File not found"

**Solution:** Vérifier que tous les fichiers sont présents:
- `streamlit_app.py`
- `emotion_detection.py`
- `requirements.txt`
- `TA_restaurants_balanced.csv` (optionnel)

### Erreur: "Port already in use"

**Solution:** Utiliser un autre port:
```powershell
docker run -p 8502:8501 nlp-restau
```
Puis accéder à: `http://localhost:8502`

---

## 📊 Commandes Utiles Docker

### Voir les Images Docker

```powershell
docker images
```

### Voir les Conteneurs en Cours

```powershell
docker ps
```

### Arrêter un Conteneur

```powershell
# Trouver l'ID du conteneur
docker ps

# Arrêter
docker stop <container-id>
```

### Voir les Logs

```powershell
docker logs <container-id>
```

### Supprimer l'Image

```powershell
docker rmi nlp-restau
```

---

## ✅ Checklist de Test

- [ ] Docker installé et lancé
- [ ] Image Docker construite sans erreur
- [ ] Conteneur démarre correctement
- [ ] Application accessible à `http://localhost:8501`
- [ ] Modèles se chargent (si utilisés)
- [ ] Analyse d'avis fonctionne
- [ ] Pas d'erreurs dans les logs

---

**Une fois le test local réussi, vous pouvez déployer sur Azure en toute confiance! 🚀**
