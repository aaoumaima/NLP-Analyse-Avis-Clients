# 📊 Accuracy du Modèle - Informations

## 🎯 Accuracy du Modèle de Sentiment

### Modèle Utilisé
**DistilBERT** (`distilbert-base-uncased`)

### Configuration d'Entraînement
- **Dataset:** Avis de restaurants (dataset nettoyé)
- **Classes:** 3 (Négatif, Neutre, Positif)
- **Split:** Train/Val/Test (80/10/10)
- **Époques:** 2
- **Learning Rate:** 2e-5

---

## 📈 Résultats Attendus

### Performance Typique de DistilBERT
- **Accuracy sur sentiment:** **85-95%** (selon le dataset)
- **F1-Score:** **80-90%** (weighted)

### Performance sur Dataset Équilibré
Avec un dataset équilibré (1,046 échantillons par classe):
- **Accuracy attendue:** **88-92%**
- **F1-Score attendu:** **85-90%**

---

## 🔍 Comment Vérifier l'Accuracy

### Option 1: Voir les Résultats d'Entraînement

Si vous avez déjà entraîné le modèle, les résultats sont dans `projet_nlp19 (7).py`:

```python
# Lignes 203, 286-287, 294-295
print("Accuracy =", round(accuracy_score(all_labels, all_preds)*100, 2), "%")
print(f"VAL Accuracy: {val_acc*100:.2f}%")
print(f"TEST Accuracy: {round(test_acc*100,2)}%")
```

### Option 2: Évaluer sur le Dataset Équilibré

Pour obtenir l'accuracy exacte, vous pouvez:

1. **Entraîner le modèle** (si pas déjà fait):
   ```bash
   python "projet_nlp19 (7).py"
   ```

2. **Ou utiliser le script d'évaluation**:
   ```bash
   pip install scikit-learn
   python evaluate_model.py
   ```

---

## 📊 Métriques de Performance

### Accuracy (Précision Globale)
- **Définition:** Pourcentage de prédictions correctes
- **Formule:** (Prédictions correctes / Total) × 100
- **Valeur attendue:** 85-95%

### F1-Score (Moyenne Harmonique)
- **Définition:** Moyenne harmonique de précision et rappel
- **Utilité:** Prend en compte les classes déséquilibrées
- **Valeur attendue:** 80-90%

### Par Classe
- **Positif:** Généralement la meilleure précision (90%+)
- **Négatif:** Bonne précision (85%+)
- **Neutre:** Plus difficile (75-85%)

---

## 🎯 Performance du Détecteur d'Émotions

### Détecteur Simple (Mots-clés)
- **Accuracy sur exemples de test:** **100%** (5/5 tests)
- **Précision:** Moyenne (dépend des mots-clés)
- **Avantage:** Rapide et fiable sur des cas clairs

### Modèle Avancé (DistilRoBERTa)
- **Accuracy attendue:** **85-90%**
- **Précision:** Élevée
- **Avantage:** Meilleure compréhension contextuelle

---

## 📝 Notes Importantes

### Facteurs Affectant l'Accuracy

1. **Qualité du Dataset**
   - ✅ Dataset équilibré: Meilleure accuracy
   - ⚠️ Dataset déséquilibré: Accuracy biaisée

2. **Fine-tuning**
   - ✅ Modèle fine-tuné: Meilleure accuracy
   - ⚠️ Modèle pré-entraîné seulement: Accuracy plus basse

3. **Taille du Dataset**
   - ✅ Plus de données: Meilleure généralisation
   - ⚠️ Peu de données: Risque de sur-apprentissage

### Votre Dataset

- **Dataset équilibré:** 3,138 échantillons (1,046 par classe)
- **Avantage:** Évaluation équitable
- **Accuracy attendue:** **88-92%** avec fine-tuning

---

## 🚀 Pour Obtenir l'Accuracy Exacte

### Méthode 1: Entraîner le Modèle

```bash
# Installer les dépendances
pip install scikit-learn transformers torch

# Lancer l'entraînement
python "projet_nlp19 (7).py"
```

Les résultats s'afficheront dans le terminal.

### Méthode 2: Évaluer le Modèle Existant

Si vous avez déjà un modèle entraîné:

```bash
# Installer scikit-learn
pip install scikit-learn

# Évaluer
python evaluate_model.py
```

---

## 📊 Résultats Typiques

### DistilBERT Non Fine-tuné
- **Accuracy:** ~70-75%
- **F1-Score:** ~65-70%

### DistilBERT Fine-tuné (2 époques)
- **Accuracy:** **88-92%**
- **F1-Score:** **85-90%**

### DistilBERT Fine-tuné (Plus d'époques)
- **Accuracy:** **90-95%**
- **F1-Score:** **88-93%**

---

## ✅ Conclusion

**Accuracy attendue de votre modèle:**
- **Avec fine-tuning:** **88-92%**
- **Sans fine-tuning:** **70-75%**

**Pour obtenir l'accuracy exacte:**
1. Entraînez le modèle avec `projet_nlp19 (7).py`
2. Les résultats s'afficheront automatiquement
3. Ou utilisez `evaluate_model.py` après installation de scikit-learn

---

**Note:** L'accuracy exacte dépend de votre entraînement spécifique. Les valeurs ci-dessus sont des estimations basées sur les performances typiques de DistilBERT.
