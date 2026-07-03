"""
MEMEEngine - No-Code Game Creator for MEMEBOT
Main entry point - Launches the standalone editor
"""

import sys
import tkinter as tk
from pathlib import Path

from SRC.Editor.editor import MEMEEngineEditor


class StandaloneConfig:
    """Configuration for standalone mode"""
    def __init__(self):
        self.BASE_PATH = str(Path(__file__).parent.parent)
        self.GAMES_PATH = Path(self.BASE_PATH) / "games"
        self.GAMES_PATH.mkdir(exist_ok=True)


def main():
    """Main entry point"""
    config = StandaloneConfig()
    
    root = tk.Tk()
    root.title("MEMEEngine")
    root.geometry("400x350")
    root.configure(bg="#1a1a1a")
    root.resizable(False, False)
    
    tk.Label(root, text="🎮 MEMEEngine", bg="#1a1a1a", fg="#64B4FF", 
            font=("Arial", 24, "bold")).pack(pady=25)
    tk.Label(root, text="No-Code Game Creator", bg="#1a1a1a", fg="#CCCCCC",
            font=("Arial", 12)).pack()
    tk.Label(root, text="Drag & Drop • Premade Assets • Instant Play", bg="#1a1a1a", fg="#888888",
            font=("Arial", 9)).pack(pady=8)
    
    btn_frame = tk.Frame(root, bg="#1a1a1a")
    btn_frame.pack(pady=15)
    
    def launch_editor():
        root.withdraw()
        editor = MEMEEngineEditor(root, config, None)
        editor.show()
        def check_editor():
            if not editor.window or not editor.window.winfo_exists():
                root.deiconify()
            else:
                root.after(500, check_editor)
        root.after(1000, check_editor)
    
    tk.Button(btn_frame, text="🎮 Open Game Editor", command=launch_editor,
             bg="#1a7a1a", fg="white", font=("Arial", 14, "bold"),
             padx=30, pady=12, width=20).pack(pady=5)
    
    tk.Label(root, text="Games save to: MEMEEngine/games/", bg="#1a1a1a", fg="#555555",
            font=("Arial", 8)).pack(pady=5)
    
    tk.Label(root, text="Arrow Keys=Move | Space=Jump | P=Pause | R=Restart | ESC=Exit", 
            bg="#1a1a1a", fg="#666666", font=("Arial", 8)).pack(pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    main()