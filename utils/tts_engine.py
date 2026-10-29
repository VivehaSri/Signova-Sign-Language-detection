"""
Text-To-Speech (TTS) Engine Module
Part of Signova: AI-Based Sign Language Recognition System
"""

import os
import threading
import tempfile
from typing import Optional


class TTSEngine:
    """
    Text-to-Speech manager supporting:
    1. Background threaded pyttsx3 speech (non-blocking for UI/video).
    2. Audio file generation for Streamlit st.audio playback.
    3. Browser-side HTML5 Web Speech API integration.
    """

    def __init__(self, rate: int = 150, volume: float = 1.0):
        """
        Args:
            rate: Speech rate (words per minute). Default is 150.
            volume: Speech volume (0.0 to 1.0). Default is 1.0.
        """
        self.rate = rate
        self.volume = volume
        self._lock = threading.Lock()

    def _speak_worker(self, text: str):
        """Background worker thread to play speech without freezing the UI."""
        with self._lock:
            try:
                import pyttsx3
                # Initialize engine locally inside thread to avoid COM concurrency errors
                engine = pyttsx3.init()
                engine.setProperty("rate", self.rate)
                engine.setProperty("volume", self.volume)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print(f"[TTSEngine] Speech playback warning: {e}")

    def speak_async(self, text: str):
        """Speak the given text in a background thread."""
        if not text or not text.strip():
            return
        thread = threading.Thread(target=self._speak_worker, args=(text.strip(),), daemon=True)
        thread.start()

    def generate_audio_file(self, text: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Synthesize text into a .wav or .mp3 audio file for web playback.

        Args:
            text: Text to synthesize.
            output_path: Optional destination path. If None, uses a temporary file.

        Returns:
            Path to the generated audio file, or None if failed.
        """
        if not text or not text.strip():
            return None

        if output_path is None:
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, "signova_speech.wav")

        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", self.rate)
            engine.setProperty("volume", self.volume)
            engine.save_to_file(text.strip(), output_path)
            engine.runAndWait()
            engine.stop()
            if os.path.exists(output_path):
                return output_path
        except Exception as e:
            print(f"[TTSEngine] File synthesis warning: {e}")

        return None

    @staticmethod
    def get_browser_speech_html(text: str) -> str:
        """
        Returns a lightweight HTML/JS snippet to trigger native browser speech synthesis.
        Guarantees clear speech audio directly inside any modern web browser.
        """
        clean_text = text.replace('"', '\\"').replace("\n", " ").strip()
        return f"""
        <script>
            (function() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance("{clean_text}");
                    utterance.rate = 0.95;
                    utterance.pitch = 1.0;
                    window.speechSynthesis.speak(utterance);
                }}
            }})();
        </script>
        """
