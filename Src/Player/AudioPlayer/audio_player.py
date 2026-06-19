"""
MEMEBOT Audio Player
Handles all audio playback with stop capability
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Union
import pygame
from pygame import mixer

class AudioPlayer:
    """Plays real audio files with full stop capability"""
    
    def __init__(self):
        try:
            mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            self.volume = 0.8
            self.ffplay_proc = None
            logging.info("Audio player initialized successfully")
        except Exception as e:
            logging.error(f"Audio init error: {e}")
            self.volume = 0.8
    
    def play(self, file_path: Union[str, Path]) -> bool:
        """Play an audio file through music channel"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logging.warning(f"Audio file not found: {file_path}")
                return False
            
            mixer.music.stop()
            mixer.music.unload()
            mixer.music.load(str(file_path))
            mixer.music.set_volume(self.volume)
            mixer.music.play()
            
            logging.info(f"NOW PLAYING: {file_path.name}")
            return True
        except Exception as e:
            logging.error(f"Play error for {file_path}: {e}")
            return False
    
    def play_sound(self, file_path: Union[str, Path]) -> bool:
        """Play a sound effect (can overlap with music)"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
            
            sound = mixer.Sound(str(file_path))
            sound.set_volume(self.volume)
            sound.play()
            return True
        except Exception as e:
            logging.error(f"Sound play error: {e}")
            return False
    
    def play_video(self, file_path: Union[str, Path], ffplay: str = "ffplay.exe") -> bool:
        """Play video with ffplay (shows video window)"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
            
            # Kill existing ffplay
            if self.ffplay_proc:
                try:
                    self.ffplay_proc.kill()
                    self.ffplay_proc.wait(timeout=1)
                except:
                    pass
                self.ffplay_proc = None
            
            cmd = [ffplay, "-autoexit", "-volume", str(int(self.volume * 100)), str(file_path)]
            self.ffplay_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            logging.info(f"NOW PLAYING VIDEO: {file_path.name}")
            return True
        except Exception as e:
            logging.error(f"Video play error: {e}")
            return False
    
    def play_video_audio_only(self, file_path: Union[str, Path], ffplay: str = "ffplay.exe") -> bool:
        """Play video audio only (hidden window)"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
            
            cmd = [ffplay, "-nodisp", "-autoexit", "-volume", str(int(self.volume * 100)), str(file_path)]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            logging.info(f"NOW PLAYING VIDEO (audio only): {file_path.name}")
            return True
        except Exception as e:
            logging.error(f"Video audio error: {e}")
            return False
    
    def stop_all(self):
        """Stop all audio and video playback completely"""
        try:
            mixer.music.stop()
            mixer.music.unload()
            mixer.stop()
        except Exception as e:
            logging.debug(f"Mixer stop: {e}")
        
        if self.ffplay_proc:
            try:
                self.ffplay_proc.kill()
                self.ffplay_proc.wait(timeout=2)
            except Exception as e:
                logging.debug(f"ffplay kill: {e}")
            finally:
                self.ffplay_proc = None
        
        # Force kill any remaining ffplay processes
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'ffplay.exe'], capture_output=True, timeout=5)
        except Exception as e:
            logging.debug(f"taskkill: {e}")
    
    def set_volume(self, v: float):
        """Set volume level (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, v))
        try:
            mixer.music.set_volume(self.volume)
        except:
            pass