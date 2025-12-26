"""
Indian English Voice Module for Jarvis
Provides natural Indian English accent using Google TTS (gTTS)
"""

import os
import tempfile
from gtts import gTTS
import pygame
import threading
import queue

class IndianVoice:
    """
    Indian English Text-to-Speech using Google TTS
    Provides natural Indian accent with male-sounding voice
    """
    
    def __init__(self):
        pygame.mixer.init()
        self.audio_queue = queue.Queue()
        self.is_speaking = False
        
    def speak(self, text, slow=False):
        """
        Speak text with Indian English accent
        
        Args:
            text: Text to speak
            slow: If True, speaks slower (default: False)
        """
        try:
            # Create gTTS object with Indian English accent
            # tld='co.in' gives Indian English accent
            tts = gTTS(text=text, lang='en', tld='co.in', slow=slow)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_filename = temp_file.name
            temp_file.close()
            
            tts.save(temp_filename)
            
            # Play audio
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.music.unload()
            try:
                os.remove(temp_filename)
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"Indian voice error: {e}")
            return False
    
    def speak_async(self, text, slow=False):
        """
        Speak text asynchronously (non-blocking)
        """
        thread = threading.Thread(target=self.speak, args=(text, slow))
        thread.daemon = True
        thread.start()
        return thread


class HybridVoice:
    """
    Hybrid voice system that tries Indian accent first, falls back to Windows SAPI5
    """
    
    def __init__(self, prefer_indian=True):
        self.prefer_indian = prefer_indian
        self.indian_voice = None
        self.windows_voice = None
        
        # Try to initialize Indian voice
        if prefer_indian:
            try:
                self.indian_voice = IndianVoice()
                print("✅ Indian English voice initialized (gTTS)")
            except Exception as e:
                print(f"⚠️ Indian voice not available: {e}")
        
        # Initialize Windows voice as fallback
        try:
            import pyttsx3
            self.windows_voice = pyttsx3.init('sapi5')
            print("✅ Windows voice initialized (SAPI5)")
        except Exception as e:
            print(f"⚠️ Windows voice error: {e}")
    
    def speak(self, text, use_indian=None):
        """
        Speak with preferred voice
        
        Args:
            text: Text to speak
            use_indian: Override preference (True/False/None)
        """
        # Determine which voice to use
        should_use_indian = use_indian if use_indian is not None else self.prefer_indian
        
        # Try Indian voice first if preferred
        if should_use_indian and self.indian_voice:
            success = self.indian_voice.speak(text)
            if success:
                return
        
        # Fallback to Windows voice
        if self.windows_voice:
            try:
                self.windows_voice.say(text)
                self.windows_voice.runAndWait()
            except Exception as e:
                print(f"Windows voice error: {e}")
                print(f"Message: {text}")


# Quick test function
def test_indian_voice():
    """Test Indian English voice"""
    print("Testing Indian English voice...")
    
    voice = IndianVoice()
    
    test_phrases = [
        "Hello, I am Jarvis, your Indian voice assistant.",
        "Welcome to the future of voice technology.",
        "I can speak with a natural Indian English accent.",
        "How may I help you today?"
    ]
    
    for phrase in test_phrases:
        print(f"Speaking: {phrase}")
        voice.speak(phrase)
        print("✅ Done\n")


if __name__ == "__main__":
    test_indian_voice()
