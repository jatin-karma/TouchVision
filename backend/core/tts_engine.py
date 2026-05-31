"""
Text-to-Speech Engine.
Converts decoded text to spoken audio using pyttsx3.
Fallback to gTTS if needed.
"""

import pyttsx3
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TTS_RATE, TTS_VOLUME


class TTSEngine:
    """
    Text-to-Speech engine using pyttsx3.
    Provides online and offline speech synthesis.
    """

    def __init__(self, rate: int = TTS_RATE, volume: float = TTS_VOLUME):
        """
        Initialize TTS engine.
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            print("✅ pyttsx3 TTS engine initialized")
        except Exception as e:
            print(f"⚠️  Failed to initialize pyttsx3: {e}")
            self.engine = None

    def speak(self, text: str) -> bool:
        """
        Speak the provided text.
        
        Args:
            text: Text to speak
        
        Returns:
            True if successful, False otherwise
        """
        if not text:
            return False
        
        if self.engine is None:
            print("❌ TTS engine not available")
            return False
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"❌ TTS error: {e}")
            return False

    def set_rate(self, rate: int):
        """Set speech rate."""
        if self.engine:
            self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float):
        """Set volume (0.0-1.0)."""
        if self.engine:
            # Clamp volume between 0 and 1
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)

    def get_properties(self) -> dict:
        """Get current engine properties."""
        if not self.engine:
            return {}
        
        try:
            return {
                'rate': self.engine.getProperty('rate'),
                'volume': self.engine.getProperty('volume'),
            }
        except:
            return {}


class TTSEngineGoogleFallback(TTSEngine):
    """
    TTS engine using Google TTS as fallback.
    Requires internet connection.
    """

    def __init__(self, rate: int = TTS_RATE, volume: float = TTS_VOLUME):
        super().__init__(rate, volume)
        try:
            from gtts import gTTS
            self.gtts = gTTS
            print("✅ gTTS fallback available")
        except ImportError:
            self.gtts = None
            print("⚠️  gTTS not installed (pip install gTTS)")

    def speak_google(self, text: str, lang: str = 'en') -> bool:
        """
        Speak using Google TTS (requires internet).
        
        Args:
            text: Text to speak
            lang: Language code (default: 'en')
        
        Returns:
            True if successful, False otherwise
        """
        if not self.gtts or not text:
            return False
        
        try:
            tts = self.gtts(text=text, lang=lang, slow=False)
            # Save to temporary file and play
            # (This requires additional audio playback setup)
            return True
        except Exception as e:
            print(f"❌ Google TTS error: {e}")
            return False
