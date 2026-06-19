"""
MEMEBOT Video Player
Floating window for video display
"""

import tkinter as tk
from pathlib import Path

class VideoPlayerWindow:
    """A floating window that displays video playback status"""
    
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.video_window = None
        self.video_label = None
        self.is_visible = False
        self.current_file = None
        
        self.vw = config.get("video_window_width", 320)
        self.vh = config.get("video_window_height", 240)
    
    def show(self, file_path: str, x: int, y: int):
        """Show video player window"""
        self.hide()
        
        self.video_window = tk.Toplevel(self.root)
        self.video_window.title("MEMEBOT Video")
        self.video_window.attributes('-topmost', True)
        self.video_window.overrideredirect(True)
        self.video_window.configure(bg='black')
        
        win_x = int(x + 150)
        win_y = int(y - 200)
        self.video_window.geometry(f"{self.vw}x{self.vh}+{win_x}+{win_y}")
        
        self.video_label = tk.Label(
            self.video_window, bg='black', fg='white',
            text="▶ VIDEO PLAYING", font=('Arial', 14)
        )
        self.video_label.pack(expand=True, fill='both')
        
        # Close button
        close_btn = tk.Label(
            self.video_window, text="✕", bg='red', fg='white',
            font=('Arial', 12, 'bold'), cursor='hand2'
        )
        close_btn.place(x=self.vw - 25, y=0)
        close_btn.bind('<Button-1>', lambda e: self.hide())
        
        self.is_visible = True
        self.current_file = file_path
        
        # Auto-hide after 30 seconds
        self.root.after(30000, self.hide)
    
    def hide(self):
        """Hide video player window"""
        if self.video_window:
            try:
                self.video_window.destroy()
            except:
                pass
            self.video_window = None
            self.video_label = None
        self.is_visible = False
        self.current_file = None
    
    def update_position(self, x: int, y: int):
        """Update window position to follow character"""
        if self.video_window and self.is_visible:
            try:
                win_x = int(x + 150)
                win_y = int(y - 200)
                self.video_window.geometry(f"+{win_x}+{win_y}")
            except:
                pass