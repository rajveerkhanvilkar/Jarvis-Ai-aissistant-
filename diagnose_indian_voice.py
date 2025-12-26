#!/usr/bin/env python3
"""
Diagnostic script for Indian voice issues
"""

print("=" * 70)
print("🔍 JARVIS INDIAN VOICE DIAGNOSTIC")
print("=" * 70)
print()

# Test 1: Check gTTS installation
print("Test 1: Checking gTTS installation...")
try:
    import gtts
    print(f"✅ gTTS installed (version: {gtts.__version__})")
except ImportError as e:
    print(f"❌ gTTS NOT installed: {e}")
    print("   Fix: pip install gTTS")
    exit(1)

# Test 2: Check pygame
print("\nTest 2: Checking pygame...")
try:
    import pygame
    pygame.mixer.init()
    print(f"✅ Pygame installed and mixer initialized")
except Exception as e:
    print(f"❌ Pygame error: {e}")

# Test 3: Check internet connection
print("\nTest 3: Checking internet connection...")
try:
    import requests
    response = requests.get("https://www.google.com", timeout=3)
    print(f"✅ Internet connection OK (status: {response.status_code})")
except Exception as e:
    print(f"❌ No internet connection: {e}")
    print("   Indian voice REQUIRES internet!")

# Test 4: Check voice_config
print("\nTest 4: Checking voice_config.py...")
try:
    from backend import voice_config as vc
    print(f"✅ voice_config loaded")
    print(f"   USE_INDIAN_ACCENT = {vc.USE_INDIAN_ACCENT}")
    print(f"   INDIAN_VOICE_SLOW = {vc.INDIAN_VOICE_SLOW}")
    print(f"   FALLBACK_TO_WINDOWS = {vc.FALLBACK_TO_WINDOWS}")
except Exception as e:
    print(f"❌ voice_config error: {e}")

# Test 5: Check indian_voice module
print("\nTest 5: Checking indian_voice module...")
try:
    from backend.indian_voice import IndianVoice
    print(f"✅ indian_voice module loaded")
except Exception as e:
    print(f"❌ indian_voice module error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Try speaking
print("\nTest 6: Testing Indian voice speech...")
try:
    from backend.indian_voice import IndianVoice
    voice = IndianVoice()
    print("   Speaking: 'Testing Indian English accent'...")
    success = voice.speak("Testing Indian English accent")
    if success:
        print("✅ Indian voice works!")
    else:
        print("⚠️ Indian voice returned False")
except Exception as e:
    print(f"❌ Speech test failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
print()
print("Summary:")
print("- If all tests passed ✅, Indian voice should work in Jarvis")
print("- If any test failed ❌, fix that issue first")
print("- Check the error messages above for specific fixes")
print()
