# 🐳 Commandes Docker - Test Local

## ✅ Dockerfile Corrigé

Le Dockerfile utilise maintenant la syntaxe correcte:
```dockerfile
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true"]
```

---

## 🧪 Tester Localement

### Étape 1: Construire l'Image

```powershell
cd C:\Users\LENOVO\Desktop\NLP

docker build -t nlp-restau .
```

**Temps estimé:** 5-10 minutes (première fois)

---

### Étape 2: Lancer le Conteneur

```powershell
docker run -p 8501:8501 nlp-restau
```

---

### Étape 3: Accéder à l'Application

Ouvrez votre navigateur:
```
http://localhost:8501
```

---

## 🔄 Si Vous Modifiez le Code

Si vous modifiez le code, reconstruisez:

```powershell
# Arrêter le conteneur actuel (Ctrl+C)

# Reconstruire (plus rapide grâce au cache)
docker build -t nlp-restau .

# Relancer
docker run -p 8501:8501 nlp-restau
```

---

## 🛑 Arrêter le Conteneur

- **Dans le terminal:** Appuyez sur `Ctrl+C`

Ou trouver l'ID et arrêter:

```powershell
# Voir les conteneurs
docker ps

# Arrêter
docker stop <container-id>
```

---

## 📊 Commandes Utiles

### Voir les Images Docker

```powershell
docker images
```

### Supprimer une Image

```powershell
docker rmi nlp-restau
```

### Voir les Logs

```powershell
# Trouver l'ID du conteneur
docker ps

# Voir les logs
docker logs <container-id>
```

### Lancer en Mode Détaché (Background)

```powershell
docker run -d -p 8501:8501 nlp-restau
```

### Voir les Conteneurs (incluant arrêtés)

```powershell
docker ps -a
```

---

## ✅ Vérifications

Après le lancement, vérifiez:

1. ✅ Pas d'erreur `--server.port requires an argument`
2. ✅ L'application démarre
3. ✅ Accessible à `http://localhost:8501`
4. ✅ Les fonctionnalités marchent

---

## 🚀 Après Test Réussi

Une fois que le test local fonctionne, vous pouvez:

1. **Déployer sur Azure:**
   ```powershell
   .\deploy_azure.ps1
   ```

2. **Ou déployer sur Streamlit Cloud:**
   - Suivez `deploy_streamlit_cloud.md`

---

**Le Dockerfile est maintenant corrigé et prêt pour le déploiement! 🐳**
