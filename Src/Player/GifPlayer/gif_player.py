"""
MEMEBOT GIF Player
Displays animated GIFs in a floating window
"""

import tkinter as tk
import logging
from pathlib import Path
from PIL import Image, ImageSequence, ImageTk

class GifPlayer:
    """Plays GIF animations in a floating window"""
    
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.gif_window = None
        self.gif_label = None
        self.is_visible = False
        self.current_file = None
        self.gif_frames = []
        self.gif_index = 0
        self.gif_anim_id = None
        
        self.vw = config.get("video_window_width", 320)
        self.vh = config.get("video_window_height", 240)
    
    def show(self, file_path: str, x: int, y: int):
        """Show GIF animation"""
        self.hide()
        
        self.gif_window = tk.Toplevel(self.root)
        self.gif_window.title("MEMEBOT GIF")
        self.gif_window.attributes('-topmost', True)
        self.gif_window.overrideredirect(True)
        self.gif_window.configure(bg='black')
        
        win_x = int(x + 150)
        win_y = int(y - 200)
        self.gif_window.geometry(f"{self.vw}x{self.vh}+{win_x}+{win_y}")
        
        self.gif_label = tk.Label(self.gif_window, bg='black')
        self.gif_label.pack(expand=True, fill='both')
        
        # Close button
        close_btn = tk.Label(
            self.gif_window, text="✕", bg='red', fg='white',
            font=('Arial', 12, 'bold'), cursor='hand2'
        )
        close_btn.place(x=self.vw - 25, y=0)
        close_btn.bind('<Button-1>', lambda e: self.hide())
        
        self.is_visible = True
        self.current_file = file_path
        
        # Load and animate GIF
        self._load_gif(file_path)
        self._animate_gif()
        
        # Auto-hide after 30 seconds
        self.root.after(30000, self.hide)
    
    def _load_gif(self, file_path: str):
        """Load GIF frames"""
        try:
            img = Image.open(file_path)
            self.gif_frames = []
            for frame in ImageSequence.Iterator(img):
                frame_rgba = frame.convert('RGBA')
                frame_resized = frame_rgba.resize((self.vw, self.vh), Image.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(frame_resized))
            self.gif_index = 0
            logging.info(f"Loaded GIF: {Path(file_path).name} ({len(self.gif_frames)} frames)")
        except Exception as e:
            logging.error(f"Failed to load GIF: {e}")
            self.gif_frames = []
    
    def _animate_gif(self):
        """Animate GIF frames"""
        if not self.is_visible or not self.gif_frames:
            return
        if self.gif_label:
            try:
                self.gif_label.config(image=self.gif_frames[self.gif_index])
                self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            except:
                pass
        self.gif_anim_id = self.root.after(50, self._animate_gif)  # ~20 fps
    
    def hide(self):
        """Hide GIF window"""
        if self.gif_anim_id:
            self.root.after_cancel(self.gif_anim_id)
            self.gif_anim_id = None
        if self.gif_window:
            try:
                self.gif_window.destroy()
            except:
                pass
            self.gif_window = None
            self.gif_label = None
        self.is_visible = False
        self.current_file = None
        self.gif_frames = []
    
    def update_position(self, x: int, y: int):
        """Update window position"""
        if self.gif_window and self.is_visible:
            try:
                win_x = int(x + 150)
                win_y = int(y - 200)
                self.gif_window.geometry(f"+{win_x}+{win_y}")
            except:
                pass