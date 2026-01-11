# -*- coding: utf-8 -*-
"""
Script pour télécharger/partager les données nettoyées
"""

import os
import shutil
from pathlib import Path

def show_file_info():
    """Affiche les informations sur le fichier"""
    file_path = "TA_restaurants_ML_clean_cleaned.csv"
    
    if not os.path.exists(file_path):
        print(f"ERREUR: Le fichier {file_path} n'existe pas!")
        return
    
    # Informations du fichier
    size = os.path.getsize(file_path)
    abs_path = os.path.abspath(file_path)
    
    print("=" * 60)
    print("INFORMATIONS SUR LE FICHIER NETTOYE")
    print("=" * 60)
    print(f"\nNom du fichier: {file_path}")
    print(f"Chemin complet: {abs_path}")
    print(f"Taille: {size / (1024*1024):.2f} MB ({size:,} bytes)")
    
    # Vérifier le contenu
    import pandas as pd
    try:
        df = pd.read_csv(file_path, nrows=1)
        print(f"Colonnes: {len(df.columns)}")
        print(f"Format: CSV (UTF-8)")
        print("\nColonnes disponibles:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
    except Exception as e:
        print(f"Erreur lors de la lecture: {e}")
    
    print("\n" + "=" * 60)
    print("METHODES DE TELECHARGEMENT")
    print("=" * 60)
    print("\n1. COPIER LE FICHIER:")
    print(f"   - Ouvrez l'explorateur Windows")
    print(f"   - Allez dans: {os.path.dirname(abs_path)}")
    print(f"   - Copiez le fichier: {file_path}")
    
    print("\n2. UTILISER LA LIGNE DE COMMANDE:")
    print(f"   - Ouvrez PowerShell ou CMD")
    print(f"   - Exécutez: copy \"{abs_path}\" [destination]")
    
    print("\n3. PARTAGER VIA CLOUD:")
    print("   - Google Drive: Uploadez le fichier")
    print("   - OneDrive: Glissez-déposez le fichier")
    print("   - Dropbox: Ajoutez le fichier")
    
    print("\n4. ENVOYER PAR EMAIL:")
    print("   - Le fichier fait 28.91 MB")
    print("   - Certains emails limitent à 25 MB")
    print("   - Utilisez WeTransfer ou Google Drive pour les gros fichiers")
    
    return abs_path

def copy_to_desktop():
    """Copie le fichier sur le Bureau pour faciliter l'accès"""
    source = "TA_restaurants_ML_clean_cleaned.csv"
    desktop = Path.home() / "Desktop"
    destination = desktop / source
    
    if not os.path.exists(source):
        print(f"ERREUR: Le fichier {source} n'existe pas!")
        return False
    
    try:
        shutil.copy2(source, destination)
        print(f"\n[OK] Fichier copié sur le Bureau: {destination}")
        return True
    except Exception as e:
        print(f"\n[ERREUR] Impossible de copier: {e}")
        return False

if __name__ == "__main__":
    abs_path = show_file_info()
    
    print("\n" + "=" * 60)
    response = input("\nVoulez-vous copier le fichier sur le Bureau? (o/n): ")
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        copy_to_desktop()
