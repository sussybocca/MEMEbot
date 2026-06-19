"""
MEMEBOT Media Manager
Manages memes, sounds, videos, and GIFs
"""

import random
import logging
from pathlib import Path
from typing import Optional, List, Union

# Import AudioAnalyzer using importlib
import importlib
AudioAnalyzerModule = importlib.import_module('Audio.audio_analyzer')
AudioAnalyzer = AudioAnalyzerModule.AudioAnalyzer

# Import AudioPlayer using importlib
AudioPlayerModule = importlib.import_module('Player.AudioPlayer.audio_player')
AudioPlayer = AudioPlayerModule.AudioPlayer


class MediaManager:
    """Manages all media files - memes, sounds, videos, GIFs"""
    
    def __init__(self, config):
        self.config = config
        self.audio = AudioPlayer()
        self.analyzer = AudioAnalyzer(str(config.FFMPEG_PATH))
    
    def _get_files(self, path: Path, exts: List[str]) -> List[Path]:
        """Get all files with specified extensions"""
        files = []
        if path.exists():
            for ext in exts:
                files.extend(path.glob(f"*.{ext}"))
                files.extend(path.glob(f"*.{ext.upper()}"))
        return files
    
    def play_random_meme(self) -> bool:
        """Play a random meme file"""
        files = self._get_files(self.config.MEMES_PATH, ['mp3', 'wav', 'ogg', 'flac'])
        if files:
            f = random.choice(files)
            logging.info(f"Playing meme: {f.name}")
            return self.audio.play(f)
        logging.warning("No memes found!")
        return False
    
    def play_random_sound(self) -> bool:
        """Play a random sound effect"""
        files = self._get_files(self.config.SOUNDS_PATH, ['mp3', 'wav', 'ogg', 'flac'])
        if files:
            f = random.choice(files)
            logging.info(f"Playing sound: {f.name}")
            return self.audio.play_sound(f)
        logging.warning("No sounds found!")
        return False
    
    def play_random_video(self, show_window: bool = False) -> Optional[Path]:
        """Play a random video, returns file path if successful"""
        files = self._get_files(self.config.VIDEOS_PATH, ['mp4', 'avi', 'mkv', 'webm', 'mov'])
        if files:
            f = random.choice(files)
            logging.info(f"Playing video: {f.name}")
            if show_window:
                self.audio.play_video(f, str(self.config.FFPLAY_PATH))
            else:
                self.audio.play_video_audio_only(f, str(self.config.FFPLAY_PATH))
            return f
        logging.warning("No videos found!")
        return None
    
    def play_random_gif(self) -> Optional[Path]:
        """Get a random GIF file path"""
        files = self._get_files(self.config.GIFS_PATH, ['gif'])
        if files:
            f = random.choice(files)
            logging.info(f"Playing GIF: {f.name}")
            return f
        logging.warning("No GIFs found!")
        return None
    
    def play_file(self, file_path: Union[str, Path]) -> bool:
        """Play any audio or video file"""
        path = Path(file_path)
        if not path.exists():
            return False
        if path.suffix.lower() in ['.mp4', '.avi', '.mkv', '.mov', '.webm']:
            return self.audio.play_video_audio_only(path, str(self.config.FFPLAY_PATH))
        if path.suffix.lower() == '.gif':
            return True  # Handled by GifPlayer
        return self.audio.play(path)
    
    def get_audio_envelope(self, file_path: str, fps: int = 30) -> Optional[List[float]]:
        """Get audio envelope for lip-sync"""
        return self.analyzer.get_envelope(file_path, fps)