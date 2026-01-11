# -*- coding: utf-8 -*-
"""
Script pour créer un dataset équilibré avec échantillonnage aléatoire
"""

import pandas as pd
import numpy as np
import random

def create_balanced_dataset(input_file, output_file, target_size_per_class=None, random_seed=42):
    """
    Crée un dataset équilibré avec échantillonnage aléatoire
    
    Args:
        input_file: Fichier CSV d'entrée
        output_file: Fichier CSV de sortie équilibré
        target_size_per_class: Nombre d'échantillons par classe (None = utiliser la classe la plus petite)
        random_seed: Seed pour la reproductibilité
    """
    print("=" * 60)
    print("CREATION D'UN DATASET EQUILIBRE")
    print("=" * 60)
    
    # Charger le dataset
    print(f"\nLecture du fichier: {input_file}")
    df = pd.read_csv(input_file, encoding='utf-8')
    print(f"   Shape initial: {df.shape}")
    
    # Vérifier les colonnes nécessaires
    required_cols = ['Review', 'Rating']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"[ERREUR] Colonnes manquantes: {missing_cols}")
        return None
    
    # Nettoyer et préparer les données
    print("\nNettoyage des donnees...")
    df = df[['Review', 'Rating']].copy()
    df = df.dropna()
    
    # Convertir Rating en numérique
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df = df.dropna(subset=['Rating'])
    
    # Créer les labels de sentiment
    def rating_to_label(r):
        if r <= 2:
            return 0  # Négatif
        elif r == 3:
            return 1  # Neutre
        else:
            return 2  # Positif
    
    df['label'] = df['Rating'].apply(rating_to_label)
    df['sentiment'] = df['label'].map({0: 'Négatif', 1: 'Neutre', 2: 'Positif'})
    
    # Nettoyer les reviews
    df['Review'] = df['Review'].astype(str).str.strip()
    df = df[df['Review'].str.len() > 10]  # Supprimer les reviews trop courtes
    df = df.drop_duplicates(subset=['Review']).reset_index(drop=True)
    
    print(f"   Après nettoyage: {df.shape}")
    
    # Afficher la distribution initiale
    print("\nDistribution initiale:")
    distribution = df['sentiment'].value_counts().sort_index()
    for sentiment, count in distribution.items():
        print(f"   {sentiment}: {count} echantillons")
    
    # Déterminer la taille cible
    if target_size_per_class is None:
        target_size_per_class = distribution.min()
        print(f"\nTaille cible par classe: {target_size_per_class} (basee sur la classe la plus petite)")
    else:
        print(f"\nTaille cible par classe: {target_size_per_class}")
    
    # Équilibrer le dataset
    print("\nEquilibrage du dataset...")
    balanced_dfs = []
    
    for sentiment in ['Négatif', 'Neutre', 'Positif']:
        sentiment_df = df[df['sentiment'] == sentiment].copy()
        
        if len(sentiment_df) >= target_size_per_class:
            # Sous-échantillonnage (downsampling) si nécessaire
            balanced_sentiment = sentiment_df.sample(
                n=target_size_per_class,
                random_state=random_seed
            ).reset_index(drop=True)
        else:
            # Sur-échantillonnage (upsampling) si nécessaire
            # Répéter les échantillons jusqu'à atteindre la taille cible
            n_repeats = (target_size_per_class // len(sentiment_df)) + 1
            balanced_sentiment = pd.concat([sentiment_df] * n_repeats, ignore_index=True)
            balanced_sentiment = balanced_sentiment.sample(
                n=target_size_per_class,
                random_state=random_seed
            ).reset_index(drop=True)
        
        balanced_dfs.append(balanced_sentiment)
        print(f"   {sentiment}: {len(balanced_sentiment)} echantillons")
    
    # Combiner les datasets équilibrés
    balanced_df = pd.concat(balanced_dfs, ignore_index=True)
    
    # Mélanger aléatoirement
    print("\nMelange aleatoire du dataset...")
    balanced_df = balanced_df.sample(frac=1, random_state=random_seed).reset_index(drop=True)
    
    # Afficher la distribution finale
    print("\nDistribution finale (equilibree):")
    final_distribution = balanced_df['sentiment'].value_counts().sort_index()
    for sentiment, count in final_distribution.items():
        print(f"   {sentiment}: {count} echantillons")
    
    # Sélectionner les colonnes à sauvegarder
    output_df = balanced_df[['Review', 'Rating', 'sentiment', 'label']].copy()
    
    # Sauvegarder
    print(f"\nSauvegarde dans: {output_file}")
    output_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n[OK] Dataset equilibre cree!")
    print(f"   Shape final: {output_df.shape}")
    print(f"   Total echantillons: {len(output_df)}")
    print(f"   Echantillons par classe: {target_size_per_class}")
    
    # Statistiques supplémentaires
    print("\nStatistiques supplementaires:")
    print(f"   Note moyenne: {output_df['Rating'].mean():.2f}")
    print(f"   Longueur moyenne des reviews: {output_df['Review'].str.len().mean():.1f} caracteres")
    
    return output_df

def create_multiple_sizes(input_file, base_name="TA_restaurants_balanced"):
    """
    Crée plusieurs versions du dataset avec différentes tailles
    """
    sizes = [
        (1000, "small"),      # 1000 par classe = 3000 total
        (5000, "medium"),    # 5000 par classe = 15000 total
        (10000, "large"),    # 10000 par classe = 30000 total
    ]
    
    datasets_created = []
    
    for size, name in sizes:
        output_file = f"{base_name}_{name}.csv"
        print(f"\n{'='*60}")
        print(f"Création dataset {name.upper()} ({size} par classe)")
        print(f"{'='*60}")
        
        try:
            df = create_balanced_dataset(
                input_file,
                output_file,
                target_size_per_class=size,
                random_seed=42
            )
            if df is not None:
                datasets_created.append((output_file, len(df)))
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la creation de {output_file}: {e}")
    
    return datasets_created

if __name__ == "__main__":
    input_file = "TA_restaurants_ML_clean_cleaned.csv"
    
    # Option 1: Créer un dataset équilibré avec taille automatique
    print("\n" + "="*60)
    print("OPTION 1: Dataset équilibré (taille automatique)")
    print("="*60)
    balanced_df = create_balanced_dataset(
        input_file,
        "TA_restaurants_balanced.csv",
        target_size_per_class=None,  # Utilise la classe la plus petite
        random_seed=42
    )
    
    # Option 2: Créer plusieurs tailles (désactivé par défaut)
    # Décommentez pour créer plusieurs tailles
    # print("\n\n" + "="*60)
    # print("OPTION 2: Création de plusieurs tailles")
    # print("="*60)
    # datasets = create_multiple_sizes(input_file)
    # 
    # print("\n" + "="*60)
    # print("RESUME DES DATASETS CREES")
    # print("="*60)
    # for filename, size in datasets:
    #     print(f"[OK] {filename}: {size} echantillons")
    
    print("\n" + "="*60)
    print("TERMINE!")
    print("="*60)
