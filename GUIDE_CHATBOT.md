# 🤖 Guide d'Utilisation du Chatbot

## 🚀 Lancement du Chatbot

### Étape 1: Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 2: Lancer l'application

```bash
streamlit run chatbot_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

---

## 📖 Comment Utiliser le Chatbot

### 1. Charger les Modèles

1. Dans la barre latérale (sidebar), cliquez sur le bouton **"🔄 Charger/Recharger les Modèles"**
2. Attendez que les modèles se chargent (vous verrez des messages de succès ✅)
3. Les modèles sont maintenant prêts à être utilisés

### 2. Analyser un Avis

#### Option A: Utiliser un Exemple
- Cliquez sur l'un des boutons "Exemple 1", "Exemple 2", "Exemple 3" ou "Exemple 4"
- L'avis sera automatiquement rempli dans la zone de texte

#### Option B: Entrer Votre Propre Avis
1. Tapez votre avis dans la zone de texte "✍️ Votre avis:"
2. Cliquez sur le bouton **"🔍 Analyser"**
3. Le chatbot analysera votre avis et affichera les résultats

### 3. Consulter les Résultats

Le chatbot affiche :
- **Sentiment** : Positif ✅, Négatif ❌, ou Neutre ➖ avec le pourcentage de confiance
- **Émotion principale** : 😊 Joie, 😢 Tristesse, 😠 Colère, 😲 Surprise, ou 😐 Neutre
- **Réponse personnalisée** : Une explication adaptée selon l'analyse

### 4. Historique des Conversations

- Tous vos avis et les analyses sont sauvegardés dans l'historique
- Vous pouvez voir toute la conversation dans la zone de chat
- Cliquez sur **"🗑️ Effacer l'historique"** pour recommencer

---

## ⚙️ Configuration

### Modèle de Sentiment

Dans la barre latérale, vous pouvez :
- **Changer le chemin du modèle** : Entrez le chemin vers votre modèle fine-tuné
- Par défaut : `distilbert-base-uncased` (modèle HuggingFace)

### Détecteur d'Émotions

- **Cocher "Utiliser modèle d'émotions avancé"** : Utilise un modèle pré-entraîné (nécessite internet)
- **Décocher** : Utilise un détecteur simple basé sur mots-clés (fonctionne hors ligne)

### Longueur Maximum

- Ajustez le slider "Longueur max du texte" selon vos besoins (32-256 caractères)
- Par défaut : 128 caractères

---

## 💡 Exemples d'Avis à Tester

### Avis Positif avec Joie
```
The food was amazing! I loved every bite! The service was excellent and the atmosphere was perfect. I highly recommend this restaurant!
```

### Avis Négatif avec Colère
```
I'm very disappointed. The service was terrible and slow. The food was cold and overpriced. I will never come back!
```

### Avis avec Surprise
```
Wow! This place is incredible! I didn't expect such amazing food. The presentation was beautiful and the taste was outstanding!
```

### Avis Neutre
```
The food was okay, nothing special really. The service was average. It's a decent place but nothing to write home about.
```

---

## 🎯 Fonctionnalités du Chatbot

### ✅ Analyse de Sentiment
- Classification en 3 catégories : Positif, Négatif, Neutre
- Score de confiance pour chaque prédiction
- Utilise un modèle DistilBERT fine-tuné

### ✅ Détection d'Émotions
- Identification de l'émotion principale
- 5 émotions possibles : joie, tristesse, colère, surprise, neutre
- Scores pour chaque émotion

### ✅ Interface Chat
- Historique des conversations
- Messages formatés avec icônes
- Horodatage des messages
- Design moderne et intuitif

### ✅ Réponses Personnalisées
- Le chatbot génère une réponse adaptée selon l'analyse
- Explications claires et compréhensibles
- Suggestions basées sur le sentiment et l'émotion

---

## 🐛 Résolution de Problèmes

### Erreur "Modèles non chargés"

**Solution** : Cliquez sur le bouton "🔄 Charger/Recharger les Modèles" dans la barre latérale

### Erreur "Module not found"

**Solution** :
```bash
pip install -r requirements.txt
```

### Le chatbot ne répond pas

**Vérifications** :
1. Les modèles sont-ils chargés ? (voir la barre latérale)
2. Avez-vous entré un texte dans la zone de saisie ?
3. Avez-vous cliqué sur le bouton "🔍 Analyser" ?

### Erreur lors du chargement du modèle

**Solutions** :
- Vérifiez votre connexion internet (pour télécharger les modèles)
- Vérifiez que le chemin du modèle est correct
- Essayez de décocher "Utiliser modèle d'émotions avancé" pour utiliser le détecteur simple

---

## 📊 Comprendre les Résultats

### Sentiment Positif ✅
- Indique que l'avis est globalement positif
- Le client est satisfait
- Probabilité élevée de retour

### Sentiment Négatif ❌
- Indique que l'avis est globalement négatif
- Le client n'est pas satisfait
- Risque de ne pas revenir

### Sentiment Neutre ➖
- Indique que l'avis est neutre
- Ni positif ni négatif
- Expérience moyenne

### Émotions

- **😊 Joie** : Le client exprime du bonheur et de la satisfaction
- **😢 Tristesse** : Le client exprime de la déception
- **😠 Colère** : Le client exprime de la frustration ou de la colère
- **😲 Surprise** : Le client exprime de l'étonnement (positif ou négatif)
- **😐 Neutre** : Aucune émotion particulière détectée

---

## 🎨 Personnalisation

Vous pouvez personnaliser le chatbot en modifiant le fichier `chatbot_app.py` :

- **Couleurs** : Modifiez les classes CSS dans la section `<style>`
- **Réponses** : Modifiez la fonction qui génère les réponses personnalisées
- **Exemples** : Ajoutez ou modifiez les exemples d'avis

---

## 📞 Support

Pour toute question ou problème :
1. Consultez le fichier `README.md` pour plus d'informations
2. Vérifiez que toutes les dépendances sont installées
3. Assurez-vous que les modèles sont correctement chargés

---

**Bon test ! 🚀**
