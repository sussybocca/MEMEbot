"""
MEMEBOT Skin Loader
Loads and manages .MSK skin files for the character
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

# Use absolute import via importlib to match how main.py imports it
import importlib
SkinEncryptor = importlib.import_module('Skin.skin_encryptor').SkinEncryptor


class SkinLoader:
    """Manages loading and applying skins to MEMEBOT"""
    
    def __init__(self, config):
        self.config = config
        self.encryptor = SkinEncryptor()
        self.current_skin = None
        self.available_skins = []
        self._scan_skins()
    
    def _scan_skins(self):
        """Scan skins directory for available .MSK files"""
        self.available_skins = []
        skins_path = self.config.SKINS_PATH
        
        if skins_path.exists():
            for file in skins_path.glob("*.msk"):
                # Skip preview temp file
                if file.name == "_preview.msk":
                    continue
                skin_data = self.encryptor.load_skin_file(file)
                if skin_data:
                    self.available_skins.append({
                        "name": skin_data.get("name", file.stem),
                        "path": str(file),
                        "author": skin_data.get("author", "Unknown"),
                        "version": skin_data.get("version", "1.0")
                    })
        
        # Add default skin if not already present
        if not any(s["name"] == "Default" for s in self.available_skins):
            self.available_skins.insert(0, {
                "name": "Default",
                "path": None,
                "author": "MEMEBOT",
                "version": "1.0"
            })
    
    def load_skin(self, skin_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Load a skin from file or use default
        
        Args:
            skin_path: Path to .MSK file, or None for default
        
        Returns:
            Skin data dictionary
        """
        if skin_path is None:
            # Try loading Default.msk first
            default_path = self.config.SKINS_PATH / "Default.msk"
            if default_path.exists():
                skin_data = self.encryptor.load_skin_file(default_path)
                if skin_data:
                    self.current_skin = skin_data
                    logging.info(f"Loaded default skin from Default.msk")
                    return skin_data
            
            # Fallback to built-in default
            self.current_skin = self.encryptor.create_default_skin("Default")
            logging.info("Using built-in default skin")
            return self.current_skin
        
        path = Path(skin_path)
        if not path.exists():
            logging.warning(f"Skin file not found: {skin_path}")
            return None
        
        skin_data = self.encryptor.load_skin_file(path)
        if skin_data:
            self.current_skin = skin_data
            logging.info(f"Loaded skin: {skin_data.get('name', 'Unknown')} from {path.name}")
        return skin_data
    
    def get_current_skin(self) -> Dict[str, Any]:
        """Get currently loaded skin data"""
        if self.current_skin is None:
            self.load_skin(None)
        return self.current_skin
    
    def get_available_skins(self) -> List[Dict[str, str]]:
        """Get list of available skins"""
        self._scan_skins()
        return self.available_skins
    
    def save_skin(self, name: str, skin_data: Dict[str, Any]) -> bool:
        """Save a new skin file"""
        file_path = self.config.SKINS_PATH / f"{name}.msk"
        return self.encryptor.save_skin_file(file_path, skin_data)
    
    def delete_skin(self, skin_path: str) -> bool:
        """Delete a skin file"""
        try:
            path = Path(skin_path)
            if path.exists():
                path.unlink()
                self._scan_skins()
                return True
        except Exception as e:
            logging.error(f"Failed to delete skin: {e}")
        return False