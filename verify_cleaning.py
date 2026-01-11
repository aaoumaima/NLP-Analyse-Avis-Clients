# -*- coding: utf-8 -*-
import pandas as pd

print("=" * 60)
print("VERIFICATION DU NETTOYAGE DES DONNEES")
print("=" * 60)

# Lire les deux fichiers
df_orig = pd.read_csv('TA_restaurants_ML_clean.csv')
df_clean = pd.read_csv('TA_restaurants_ML_clean_cleaned.csv')

print("\n=== FICHIER ORIGINAL ===")
print(f"  Shape: {df_orig.shape}")
print(f"  Colonnes: {len(df_orig.columns)}")
print(f"  Colonne 'Unnamed: 0' existe: {'Unnamed: 0' in df_orig.columns}")
print(f"  Valeurs manquantes Review_clean: {df_orig['Review_clean'].isna().sum()}")
print(f"  Doublons: {df_orig.duplicated().sum()}")

print("\n=== FICHIER NETTOYE ===")
print(f"  Shape: {df_clean.shape}")
print(f"  Colonnes: {len(df_clean.columns)}")
print(f"  Colonne 'Unnamed: 0' existe: {'Unnamed: 0' in df_clean.columns}")
print(f"  Valeurs manquantes Review_clean: {df_clean['Review_clean'].isna().sum()}")
print(f"  Doublons: {df_clean.duplicated().sum()}")

print("\n=== AMELIORATIONS ===")
if 'Unnamed: 0' not in df_clean.columns:
    print("  [OK] Colonne 'Unnamed: 0' supprimee")
if df_clean['Review_clean'].isna().sum() == 0:
    print("  [OK] Plus de valeurs manquantes dans Review_clean")
if df_clean.duplicated().sum() == 0:
    print("  [OK] Pas de doublons")
    
print("\n=== COLONNES NETTOYEES ===")
print(f"  {', '.join(df_clean.columns.tolist()[:5])}...")

print("\n" + "=" * 60)
print("VERIFICATION TERMINEE")
print("=" * 60)
