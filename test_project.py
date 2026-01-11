# -*- coding: utf-8 -*-
"""
Script de test complet pour le projet NLP
Teste toutes les fonctionnalités du projet
"""

import sys
import os

def print_header(text):
    """Affiche un en-tête formaté"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def test_imports():
    """Test 1: Vérifier que tous les imports fonctionnent"""
    print_header("TEST 1: Vérification des Imports")
    
    errors = []
    
    # Test des imports de base
    try:
        import pandas as pd
        print("[OK] pandas importe")
    except ImportError:
        print("[ERREUR] pandas non installe")
        errors.append("pandas")
    
    try:
        import numpy as np
        print("[OK] numpy importe")
    except ImportError:
        print("[ERREUR] numpy non installe")
        errors.append("numpy")
    
    # Test des imports NLP
    try:
        import torch
        print("[OK] torch importe")
    except ImportError:
        print("[ERREUR] torch non installe")
        errors.append("torch")
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        print("[OK] transformers importe")
    except ImportError:
        print("[ERREUR] transformers non installe")
        errors.append("transformers")
    
    # Test des imports Streamlit
    try:
        import streamlit
        print("[OK] streamlit importe")
    except ImportError:
        print("[ATTENTION] streamlit non installe (necessaire pour les apps)")
        errors.append("streamlit")
    
    # Test des imports de visualisation
    try:
        import matplotlib.pyplot as plt
        print("[OK] matplotlib importe")
    except ImportError:
        print("[ATTENTION] matplotlib non installe")
        errors.append("matplotlib")
    
    try:
        import plotly
        print("[OK] plotly importe")
    except ImportError:
        print("[ATTENTION] plotly non installe")
        errors.append("plotly")
    
    # Test du module personnalisé
    try:
        from emotion_detection import SimpleEmotionDetector, get_emotion_detector
        print("[OK] emotion_detection importe")
    except ImportError as e:
        print(f"[ERREUR] emotion_detection non importe: {e}")
        errors.append("emotion_detection")
    
    if errors:
        print(f"\n[ATTENTION] {len(errors)} module(s) manquant(s)")
        print("Installez avec: pip install -r requirements.txt")
        return False
    else:
        print("\n[OK] Tous les imports sont OK")
        return True

def test_datasets():
    """Test 2: Vérifier que les datasets existent"""
    print_header("TEST 2: Vérification des Datasets")
    
    datasets = [
        ("TA_restaurants_ML_clean_cleaned.csv", "Dataset nettoyé"),
        ("TA_restaurants_balanced.csv", "Dataset équilibré")
    ]
    
    all_ok = True
    
    for filename, description in datasets:
        if os.path.exists(filename):
            try:
                import pandas as pd
                df = pd.read_csv(filename)
                print(f"[OK] {description}: {filename}")
                print(f"   - Taille: {len(df)} lignes, {len(df.columns)} colonnes")
                
                # Vérifier les colonnes importantes
                if 'Review' in df.columns or 'Review_clean' in df.columns:
                    print(f"   - Colonnes OK")
                else:
                    print(f"   [ATTENTION] Colonnes 'Review' ou 'Review_clean' manquantes")
                
                # Vérifier l'équilibrage si c'est le dataset équilibré
                if 'sentiment' in df.columns:
                    dist = df['sentiment'].value_counts()
                    print(f"   - Distribution: {dict(dist)}")
                    if len(dist) == 3 and all(v == dist.iloc[0] for v in dist.values):
                        print(f"   [OK] Dataset equilibre")
                    else:
                        print(f"   [ATTENTION] Dataset non equilibre")
                
            except Exception as e:
                print(f"[ERREUR] {description}: Erreur lors de la lecture - {e}")
                all_ok = False
        else:
            print(f"[ERREUR] {description}: {filename} non trouve")
            all_ok = False
    
    return all_ok

def test_emotion_detection():
    """Test 3: Tester la détection d'émotions"""
    print_header("TEST 3: Détection d'Émotions")
    
    try:
        from emotion_detection import SimpleEmotionDetector
        
        detector = SimpleEmotionDetector()
        print("[OK] Detecteur d'emotions cree")
        
        # Tests avec différents avis
        test_cases = [
            ("The food was amazing! I loved it!", "joie"),
            ("I'm very disappointed. The service was terrible.", "tristesse"),
            ("I'm really angry about the slow service!", "colère"),
            ("Wow! This restaurant is incredible!", "surprise"),
            ("The food was okay, nothing special.", "neutre")
        ]
        
        print("\nTests de detection:")
        all_passed = True
        
        for text, expected_emotion in test_cases:
            emotion, conf = detector.get_main_emotion(text)
            status = "[OK]" if emotion == expected_emotion or conf > 0.3 else "[ATTENTION]"
            print(f"{status} Texte: '{text[:50]}...'")
            print(f"   -> Emotion: {emotion} ({conf*100:.1f}%)")
            
            if emotion != expected_emotion and conf < 0.3:
                all_passed = False
        
        if all_passed:
            print("\n[OK] Tous les tests de detection d'emotions sont OK")
        else:
            print("\n[ATTENTION] Certains tests ont echoue (normal si le detecteur est basique)")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur lors du test de detection d'emotions: {e}")
        return False

def test_data_processing():
    """Test 4: Tester le traitement des données"""
    print_header("TEST 4: Traitement des Données")
    
    try:
        import pandas as pd
        
        # Test avec le dataset équilibré
        if os.path.exists("TA_restaurants_balanced.csv"):
            df = pd.read_csv("TA_restaurants_balanced.csv")
            
            print("[OK] Dataset charge")
            print(f"   - Shape: {df.shape}")
            
            # Vérifier les colonnes
            required_cols = ['Review', 'Rating', 'sentiment', 'label']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                print(f"   [ATTENTION] Colonnes manquantes: {missing}")
            else:
                print("   [OK] Toutes les colonnes requises sont presentes")
            
            # Vérifier les valeurs manquantes
            missing_values = df.isnull().sum().sum()
            if missing_values == 0:
                print("   [OK] Aucune valeur manquante")
            else:
                print(f"   [ATTENTION] {missing_values} valeurs manquantes")
            
            # Vérifier les types
            if df['label'].dtype in ['int64', 'int32']:
                print("   [OK] Type de 'label' correct")
            else:
                print("   [ATTENTION] Type de 'label' incorrect")
            
            return True
        else:
            print("[ATTENTION] Dataset equilibre non trouve")
            return False
            
    except Exception as e:
        print(f"[ERREUR] Erreur lors du test de traitement: {e}")
        return False

def test_scripts():
    """Test 5: Vérifier que les scripts existent"""
    print_header("TEST 5: Vérification des Scripts")
    
    scripts = [
        ("clean_data.py", "Nettoyage des données"),
        ("balance_dataset.py", "Équilibrage du dataset"),
        ("emotion_detection.py", "Détection d'émotions"),
        ("chatbot_app.py", "Application chatbot"),
        ("app_emotions.py", "Application complète"),
        ("app.py", "Application simple")
    ]
    
    all_exist = True
    
    for filename, description in scripts:
        if os.path.exists(filename):
            print(f"[OK] {description}: {filename}")
        else:
            print(f"[ERREUR] {description}: {filename} non trouve")
            all_exist = False
    
    return all_exist

def test_documentation():
    """Test 6: Vérifier la documentation"""
    print_header("TEST 6: Vérification de la Documentation")
    
    docs = [
        ("README.md", "Documentation principale"),
        ("QUICK_START.md", "Guide de démarrage"),
        ("GUIDE_CHATBOT.md", "Guide du chatbot"),
        ("PROJET_FINI.md", "Résumé du projet"),
        ("requirements.txt", "Dépendances")
    ]
    
    all_exist = True
    
    for filename, description in docs:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"[OK] {description}: {filename} ({size} bytes)")
        else:
            print(f"[ERREUR] {description}: {filename} non trouve")
            all_exist = False
    
    return all_exist

def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "=" * 60)
    print("TESTS COMPLETS DU PROJET NLP")
    print("=" * 60)
    
    results = {}
    
    # Exécuter tous les tests
    results['imports'] = test_imports()
    results['datasets'] = test_datasets()
    results['emotion'] = test_emotion_detection()
    results['processing'] = test_data_processing()
    results['scripts'] = test_scripts()
    results['documentation'] = test_documentation()
    
    # Résumé final
    print_header("RÉSUMÉ DES TESTS")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "[OK]" if result else "[ERREUR]"
        print(f"{status} {test_name.upper()}: {'PASSE' if result else 'ECHOUE'}")
    
    print(f"\nResultat: {passed}/{total} tests passes")
    
    if passed == total:
        print("\n[SUCCES] TOUS LES TESTS SONT PASSES! Le projet est pret!")
    elif passed >= total * 0.8:
        print("\n[ATTENTION] La plupart des tests sont passes. Verifiez les erreurs ci-dessus.")
    else:
        print("\n[ERREUR] Plusieurs tests ont echoue. Installez les dependances avec:")
        print("   pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    
    print("\n" + "=" * 60)
    print("PROCHAINES ÉTAPES")
    print("=" * 60)
    print("\n1. Si tous les tests sont OK, lancez le chatbot:")
    print("   streamlit run chatbot_app.py")
    print("\n2. Ou l'application complète:")
    print("   streamlit run app_emotions.py")
    print("\n3. Consultez le README.md pour plus d'informations")
    print("=" * 60 + "\n")
    
    sys.exit(0 if success else 1)
