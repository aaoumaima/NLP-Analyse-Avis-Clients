# 🚀 Démarrage Rapide - Application Streamlit

## ✅ Installation Terminée

- ✅ Streamlit installé (version 1.52.2)
- ✅ Plotly installé (version 6.5.1)
- ✅ Toutes les dépendances prêtes

---

## 🎯 Lancer l'Application

### Option 1: Application Principale (Recommandée)

```bash
streamlit run streamlit_app.py
```

### Option 2: Chatbot

```bash
streamlit run chatbot_app.py
```

### Option 3: Application Complète

```bash
streamlit run app_emotions.py
```

### Option 4: Application Simple

```bash
streamlit run app.py
```

---

## 📱 Ce qui va se passer

1. **L'application démarre** dans le terminal
2. **Le navigateur s'ouvre automatiquement** à l'adresse:
   ```
   http://localhost:8501
   ```
3. **Si le navigateur ne s'ouvre pas**, copiez cette adresse dans votre navigateur

---

## 🎨 Fonctionnalités Disponibles

### Avec `streamlit_app.py`:
- ✅ Analyser un avis individuel
- ✅ Voir les statistiques du dataset
- ✅ Analyser les émotions dans le dataset
- ✅ Graphiques interactifs

### Avec `chatbot_app.py`:
- ✅ Interface de chat
- ✅ Historique des conversations
- ✅ Analyse en temps réel

---

## ⚠️ Si vous avez des erreurs

### Erreur "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur "Dataset not found"
Vérifiez que les fichiers CSV sont dans le même dossier:
- `TA_restaurants_balanced.csv`
- `TA_restaurants_ML_clean_cleaned.csv`

### Port déjà utilisé
```bash
streamlit run chatbot_app.py --server.port 8502
```

---

## 🎉 C'est Prêt !

Lancez maintenant:
```bash
streamlit run chatbot_app.py
```

Ou:
```bash
streamlit run streamlit_app.py
```

**Bon test ! 🚀**
