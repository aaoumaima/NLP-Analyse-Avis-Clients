# -*- coding: utf-8 -*-
"""
Script de test pour le chatbot
Teste les fonctions principales sans interface Streamlit
"""

from emotion_detection import SimpleEmotionDetector
import sys

def test_emotion_detection():
    """Teste la détection d'émotions"""
    print("=" * 60)
    print("TEST DE DETECTION D'EMOTIONS")
    print("=" * 60)
    
    detector = SimpleEmotionDetector()
    
    test_cases = [
        ("The food was amazing! I loved every bite!", "joie"),
        ("I'm very disappointed. The service was terrible.", "tristesse"),
        ("I'm really angry about the slow service!", "colère"),
        ("Wow! This restaurant is incredible!", "surprise"),
        ("The food was okay, nothing special.", "neutre")
    ]
    
    print("\nTest des avis:\n")
    for i, (text, expected_emotion) in enumerate(test_cases, 1):
        emotion, conf = detector.get_main_emotion(text)
        status = "✅" if emotion == expected_emotion else "⚠️"
        print(f"{status} Test {i}:")
        print(f"   Texte: {text}")
        print(f"   Émotion détectée: {emotion} ({conf*100:.1f}%)")
        print(f"   Émotion attendue: {expected_emotion}")
        print()
    
    print("=" * 60)
    print("TEST TERMINE")
    print("=" * 60)

def test_imports():
    """Teste que tous les imports fonctionnent"""
    print("Test des imports...")
    
    try:
        import streamlit
        print("✅ Streamlit importé")
    except ImportError:
        print("❌ Streamlit non installé - installez avec: pip install streamlit")
        return False
    
    try:
        import torch
        print("✅ PyTorch importé")
    except ImportError:
        print("❌ PyTorch non installé - installez avec: pip install torch")
        return False
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        print("✅ Transformers importé")
    except ImportError:
        print("❌ Transformers non installé - installez avec: pip install transformers")
        return False
    
    try:
        from emotion_detection import get_emotion_detector
        print("✅ Module emotion_detection importé")
    except ImportError as e:
        print(f"❌ Erreur import emotion_detection: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTS DU CHATBOT")
    print("=" * 60 + "\n")
    
    # Test des imports
    if test_imports():
        print("\n✅ Tous les imports sont OK\n")
    else:
        print("\n❌ Certains imports ont échoué\n")
        print("Installez les dépendances avec:")
        print("  pip install -r requirements.txt\n")
        sys.exit(1)
    
    # Test de la détection d'émotions
    test_emotion_detection()
    
    print("\n" + "=" * 60)
    print("POUR LANCER LE CHATBOT:")
    print("  streamlit run chatbot_app.py")
    print("=" * 60 + "\n")
