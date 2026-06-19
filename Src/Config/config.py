"""
MEMEBOT Configuration System
Handles all settings, paths, and configuration management
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Union

class MemeBotConfig:
    """MEMEBOT Configuration Manager"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.BASE_PATH = Path(base_path)
        
        # Source paths
        self.SRC_PATH = self.BASE_PATH / "Src"
        self.CHARACTER_PATH = self.SRC_PATH / "Character-Drawing"
        self.ANIMATIONS_PATH = self.CHARACTER_PATH / "Animations"
        self.DANCE_PATH = self.ANIMATIONS_PATH / "DanceMoves"
        self.MOVEMENT_PATH = self.ANIMATIONS_PATH / "Movements"
        self.RENDERER_PATH = self.CHARACTER_PATH / "2D"
        self.PLAYER_PATH = self.SRC_PATH / "Player"
        self.AUDIO_PATH = self.SRC_PATH / "Audio"
        self.MEDIA_PATH = self.SRC_PATH / "Media"
        self.UI_PATH = self.SRC_PATH / "UI"
        self.SKIN_PATH = self.SRC_PATH / "Skin"
        
        # Data paths
        self.VOICE_PATH = self.BASE_PATH / "vocabulary_voice"
        self.MEMES_PATH = self.BASE_PATH / "memes"
        self.SOUNDS_PATH = self.BASE_PATH / "sounds"
        self.VIDEOS_PATH = self.BASE_PATH / "videos"
        self.GIFS_PATH = self.BASE_PATH / "gifs"
        self.SCRIPTS_PATH = self.BASE_PATH / "scripts"
        self.CONFIG_PATH = self.BASE_PATH / "config"
        self.MODS_PATH = self.BASE_PATH / "mods"
        self.SKINS_PATH = self.BASE_PATH / "skins"
        self.ASSETS_PATH = self.BASE_PATH / "assets"
        self.LOGS_PATH = self.BASE_PATH / "logs"
        
        # External tools
        self.FFMPEG_PATH = self.BASE_PATH / "ffmpeg.exe"
        self.FFPLAY_PATH = self.BASE_PATH / "ffplay.exe"
        self.FFPROBE_PATH = self.BASE_PATH / "ffprobe.exe"
        
        # Create all directories
        self._create_directories()
        
        # Load settings
        self.settings = self._load_settings()
        
        # Setup logging
        self._setup_logging()
    
    def _create_directories(self):
        """Create all necessary directories"""
        directories = [
            self.SRC_PATH, self.CHARACTER_PATH, self.ANIMATIONS_PATH,
            self.DANCE_PATH, self.MOVEMENT_PATH, self.RENDERER_PATH,
            self.PLAYER_PATH, self.AUDIO_PATH, self.MEDIA_PATH,
            self.UI_PATH, self.SKIN_PATH,
            self.VOICE_PATH, self.MEMES_PATH, self.SOUNDS_PATH,
            self.VIDEOS_PATH, self.GIFS_PATH, self.SCRIPTS_PATH,
            self.CONFIG_PATH, self.MODS_PATH, self.SKINS_PATH,
            self.ASSETS_PATH, self.LOGS_PATH
        ]
        for d in directories:
            d.mkdir(parents=True, exist_ok=True)
    
    def _load_settings(self) -> dict:
        """Load settings from JSON file"""
        settings_file = self.CONFIG_PATH / "settings.json"
        defaults = {
            "volume": 0.8,
            "start_x": 500,
            "start_y": 500,
            "fps": 30,
            "auto_play_interval": 15,
            "character_size": 256,
            "idle_movement": True,
            "walk_speed": 3,
            "run_speed": 6,
            "auto_walk": True,
            "current_skin": "default",
            "video_window_width": 320,
            "video_window_height": 240,
            "show_video_player": False,
            "mod_menu_enabled": True,
            "lua_scripts_enabled": True,
            "play_history": []
        }
        
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    defaults.update(loaded)
            except Exception as e:
                logging.error(f"Error loading settings: {e}")
        else:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(defaults, f, indent=4)
        
        return defaults
    
    def _setup_logging(self):
        """Setup logging"""
        log_file = self.LOGS_PATH / f"memebot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def save_settings(self):
        """Save settings to file"""
        settings_file = self.CONFIG_PATH / "settings.json"
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()