"""
MEMEBOT System Tray Controller
Manages system tray icon and menu
"""

import threading
import logging
from PIL import Image, ImageDraw

try:
    import pystray
    HAS_PYSTRAY = True
except ImportError:
    HAS_PYSTRAY = False


class TrayController:
    """System tray icon for controlling MEMEBOT"""
    
    def __init__(self, app):
        self.app = app
        self.icon = None
        if HAS_PYSTRAY:
            self._create_tray()
    
    def _create_tray(self):
        """Create system tray icon with menu"""
        try:
            icon_img = Image.new('RGB', (64, 64), color=(100, 200, 255))
            d = ImageDraw.Draw(icon_img)
            d.ellipse([10, 10, 54, 54], fill=(255, 220, 180))
            d.ellipse([22, 22, 30, 30], fill=(30, 30, 30))
            d.ellipse([34, 22, 42, 30], fill=(30, 30, 30))
            d.arc([22, 34, 42, 46], 0, 180, fill=(150, 50, 50), width=2)
            
            menu = (
                pystray.MenuItem('Random Meme', self._on_meme),
                pystray.MenuItem('Random Sound', self._on_sound),
                pystray.MenuItem('Random Video', self._on_video),
                pystray.MenuItem('Random GIF', self._on_gif),
                pystray.MenuItem('Say Hello', self._on_hello),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem('Toggle Auto-Play', self._on_toggle_auto),
                pystray.MenuItem('Quit', self._on_quit),
            )
            
            self.icon = pystray.Icon("MEMEBOT", icon_img, "MEMEBOT", menu)
            threading.Thread(target=self.icon.run, daemon=True).start()
            logging.info("System tray icon created")
        except Exception as e:
            logging.error(f"Failed to create tray: {e}")
    
    def _on_meme(self, icon, item):
        self.app.root.after(0, self.app.play_random_meme)
    
    def _on_sound(self, icon, item):
        self.app.root.after(0, self.app.play_random_sound)
    
    def _on_video(self, icon, item):
        self.app.root.after(0, self.app.play_random_video)
    
    def _on_gif(self, icon, item):
        self.app.root.after(0, self.app.play_random_gif)
    
    def _on_hello(self, icon, item):
        self.app.root.after(0, self.app.say_hello)
    
    def _on_toggle_auto(self, icon, item):
        self.app.root.after(0, self.app.toggle_auto_play)
    
    def _on_quit(self, icon, item):
        self.app.root.after(0, self.app.stop)
        icon.stop()