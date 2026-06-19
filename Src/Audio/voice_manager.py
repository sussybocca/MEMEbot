"""
MEMEBOT Voice Manager
Loads and plays custom voice files
"""

import time
import threading
import logging
from pathlib import Path
from typing import Optional, List

class VoiceManager:
    """Loads and plays your custom voice WAV/MP3 files"""
    
    def __init__(self, voice_path: Path):
        self.voice_path = Path(voice_path)
        self.voice_map = {}
        self._load()
        logging.info(f"Voice Manager loaded {len(self.voice_map)} voice files")
    
    def _load(self):
        """Scan directory and load all voice files"""
        if not self.voice_path.exists():
            logging.warning(f"Voice path not found: {self.voice_path}")
            return
        
        audio_exts = {'.wav', '.mp3', '.ogg', '.flac'}
        for file in self.voice_path.iterdir():
            if file.is_file() and file.suffix.lower() in audio_exts:
                word = file.stem.lower().strip()
                self.voice_map[word] = file
                logging.debug(f"Loaded voice: '{word}' -> {file.name}")
    
    def get_file(self, word: str) -> Optional[Path]:
        """Get voice file for a word"""
        return self.voice_map.get(word.lower().strip())
    
    def speak(self, sentence: str, audio_player, delay: float = 0.15):
        """Speak a sentence using voice files"""
        words = sentence.lower().split()
        
        def speak_thread():
            for word in words:
                clean = word.strip('.,!?;:"\'()[]{}')
                if clean:
                    f = self.get_file(clean)
                    if f:
                        audio_player.play_sound(f)
                        time.sleep(delay)
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def list_words(self) -> List[str]:
        """List all available voice words"""
        return sorted(list(self.voice_map.keys()))