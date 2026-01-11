# -*- coding: utf-8 -*-
"""
Script de nettoyage des données TA_restaurants_ML_clean.csv
"""

import pandas as pd
import numpy as np
import re

def clean_data(input_file, output_file):
    """
    Nettoie le fichier CSV des restaurants
    """
    print(f"Lecture du fichier: {input_file}")
    df = pd.read_csv(input_file, encoding='utf-8')
    
    print(f"   Shape initial: {df.shape}")
    
    # 1. Supprimer la colonne d'index "Unnamed: 0"
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        print("[OK] Colonne 'Unnamed: 0' supprimee")
    
    # 2. Nettoyer les colonnes de texte (supprimer les espaces en début/fin)
    text_columns = ['Name', 'City', 'Cuisine Style', 'Price Range', 'Review', 'Review_clean']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    # 3. Gérer les valeurs manquantes dans Review_clean
    # Si Review_clean est vide ou NaN, utiliser Review (nettoyé) comme fallback
    mask_missing = (df['Review_clean'].isna()) | (df['Review_clean'].astype(str).str.strip() == '') | (df['Review_clean'].astype(str).str.strip() == 'nan')
    if mask_missing.sum() > 0:
        print(f"[INFO] {mask_missing.sum()} valeurs manquantes dans Review_clean detectees")
        # Utiliser Review comme fallback, en le nettoyant
        df.loc[mask_missing, 'Review_clean'] = df.loc[mask_missing, 'Review'].astype(str).str.lower().str.strip()
        # Nettoyer les dates et caractères spéciaux
        df.loc[mask_missing, 'Review_clean'] = df.loc[mask_missing, 'Review_clean'].apply(
            lambda x: re.sub(r'\d{2}/\d{2}/\d{4}', '', str(x)).strip() if pd.notna(x) else ''
        )
        print("[OK] Valeurs manquantes dans Review_clean corrigees")
    
    # 4. Nettoyer Review_clean (supprimer les dates, normaliser)
    def clean_review_text(text):
        if pd.isna(text) or str(text).strip() == '':
            return ''
        text = str(text).lower().strip()
        # Supprimer les dates (format MM/DD/YYYY)
        text = re.sub(r'\d{2}/\d{2}/\d{4}', '', text)
        # Supprimer les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        # Supprimer les caractères spéciaux en fin de texte
        text = text.strip('.,!?;:')
        return text.strip()
    
    df['Review_clean'] = df['Review_clean'].apply(clean_review_text)
    
    # 5. Supprimer les lignes où Review_clean est vide après nettoyage
    before_drop = len(df)
    df = df[df['Review_clean'].astype(str).str.strip() != '']
    after_drop = len(df)
    if before_drop != after_drop:
        print(f"[OK] {before_drop - after_drop} lignes avec Review_clean vide supprimees")
    
    # 6. Nettoyer les valeurs numériques
    numeric_columns = ['Ranking', 'Rating', 'Number of Reviews']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 7. Supprimer les lignes avec Rating manquant (critique pour l'analyse)
    before_drop = len(df)
    df = df.dropna(subset=['Rating'])
    after_drop = len(df)
    if before_drop != after_drop:
        print(f"[OK] {before_drop - after_drop} lignes avec Rating manquant supprimees")
    
    # 8. Nettoyer les noms de restaurants (supprimer les espaces multiples)
    if 'Name' in df.columns:
        df['Name'] = df['Name'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # 9. Nettoyer Cuisine Style (supprimer les espaces multiples)
    if 'Cuisine Style' in df.columns:
        df['Cuisine Style'] = df['Cuisine Style'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # 10. Réinitialiser l'index
    df = df.reset_index(drop=True)
    
    # 11. Vérifier les doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"[INFO] {duplicates} doublons detectes")
        df = df.drop_duplicates().reset_index(drop=True)
        print("[OK] Doublons supprimes")
    
    print(f"\nShape final: {df.shape}")
    print(f"[OK] Donnees nettoyees sauvegardees dans: {output_file}")
    
    # Sauvegarder
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Afficher un résumé
    print("\nResume du nettoyage:")
    print(f"   - Lignes: {df.shape[0]}")
    print(f"   - Colonnes: {df.shape[1]}")
    print(f"   - Valeurs manquantes:")
    missing = df.isnull().sum()
    for col, count in missing[missing > 0].items():
        print(f"     * {col}: {count}")
    
    return df

if __name__ == "__main__":
    input_file = r"C:\Users\LENOVO\Desktop\NLP\TA_restaurants_ML_clean.csv"
    output_file = r"C:\Users\LENOVO\Desktop\NLP\TA_restaurants_ML_clean_cleaned.csv"
    
    print("=" * 60)
    print("NETTOYAGE DES DONNEES")
    print("=" * 60)
    
    df_cleaned = clean_data(input_file, output_file)
    
    print("\n" + "=" * 60)
    print("NETTOYAGE TERMINE!")
    print("=" * 60)
