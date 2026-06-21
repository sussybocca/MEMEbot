"""
MEMEBOT - Main Entry Point
Modular desktop character system with Lua skin support, Addons & Extensions
"""

import os
import sys
import threading
import time
import importlib
import random

# Add Src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Src'))

import tkinter as tk

# Import all modular components using importlib for hyphenated folder names
ConfigModule = importlib.import_module('Config.config')
MemeBotConfig = ConfigModule.MemeBotConfig

CharacterModule = importlib.import_module('Character-Drawing.2D.character_renderer')
CharacterRenderer = CharacterModule.CharacterRenderer

AudioPlayerModule = importlib.import_module('Player.AudioPlayer.audio_player')
AudioPlayer = AudioPlayerModule.AudioPlayer

VoiceModule = importlib.import_module('Audio.voice_manager')
VoiceManager = VoiceModule.VoiceManager

MediaModule = importlib.import_module('Media.media_manager')
MediaManager = MediaModule.MediaManager

VideoModule = importlib.import_module('Player.VideoPlayer.video_player')
VideoPlayerWindow = VideoModule.VideoPlayerWindow

GifModule = importlib.import_module('Player.GifPlayer.gif_player')
GifPlayer = GifModule.GifPlayer

TrayModule = importlib.import_module('UI.tray_controller')
TrayController = TrayModule.TrayController

ModMenuModule = importlib.import_module('UI.mod_menu')
ModMenu = ModMenuModule.ModMenu

SkinModule = importlib.import_module('Skin.skin_loader')
SkinLoader = SkinModule.SkinLoader

# Addon & Extension Manager
AddonManagerModule = importlib.import_module('Addons.addon_manager')
AddonManager = AddonManagerModule.AddonManager

# System tray check
try:
    import pystray
    HAS_PYSTRAY = True
except ImportError:
    HAS_PYSTRAY = False


class MemeBotApp:
    """Main MEMEBOT application"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.config = MemeBotConfig(base_path)
        self.skin_loader = SkinLoader(self.config)
        
        # Create transparent fullscreen window
        self.root = tk.Tk()
        self.root.title("MEMEBOT")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'black')
        self.root.configure(bg='black')
        self.root.overrideredirect(True)
        
        self.canvas = tk.Canvas(
            self.root, bg='black', highlightthickness=0,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight()
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Initialize components
        self.character = CharacterRenderer(self.canvas, self.config, self.skin_loader)
        self.character.root = self.root
        
        self.audio_player = AudioPlayer()
        self.voice_manager = VoiceManager(self.config.VOICE_PATH)
        self.media_manager = MediaManager(self.config)
        
        self.video_player = VideoPlayerWindow(self.root, self.config)
        self.gif_player = GifPlayer(self.root, self.config)
        
        # Mod menu (create AFTER character so it can reference it)
        self.mod_menu = ModMenu(self.root, self.config, self.skin_loader, self)
        
        # Addon & Extension Manager (create AFTER mod_menu for Lua access)
        self.addon_manager = AddonManager(self.config, self)
        
        # State
        self.auto_play_paused = False
        self._auto_counter = 0
        self.is_running = False  # Set to False until start() is called
        
        # Vocabulary / sentence building
        self._build_vocabulary()
        
        # Setup bindings and tray
        self._setup_bindings()
        if HAS_PYSTRAY:
            self.tray = TrayController(self)
    
    def _build_vocabulary(self):
        """Build sentence templates from available voice files"""
        # All available word files (without extension)
        self.available_words = []
        if os.path.exists(self.config.VOICE_PATH):
            for f in os.listdir(self.config.VOICE_PATH):
                if f.lower().endswith('.wav'):
                    word = os.path.splitext(f)[0]
                    self.available_words.append(word)
        
        # Greeting templates using available words
        self.greetings = [
            "hello welcome to memebot",
            "hey whats crackin",
            "heya friend",
            "bonjour",
            "greetings human",
            "well hello there",
            "hi hows it going",
            "hello im back",
            "hey youre back",
            "heya whats up",
            "well hello",
            "greetings friend",
            "hi there",
            "hello human",
            "hey friend",
        ]
        
        # Random sentence templates
        self.sentences = [
            "im so happy today",
            "what a beautiful day",
            "ive been waiting for you",
            "im ready for anything",
            "thats what im talking about",
            "you see that",
            "watch me",
            "looking good today",
            "some fun for you",
            "im going to have fun",
            "well thats beautiful",
            "so happy to see you",
            "whats going on today",
            "im ready for fun",
            "thats beautiful",
            "looking for fun",
            "ive been waiting",
            "watch this",
            "you see me",
            "what a day",
        ]
        
        # Reaction sentences for memes
        self.meme_reactions = [
            "watch this meme",
            "thats so funny",
            "im ready for this",
            "you see that meme",
            "what a meme",
            "looking good meme",
            "ive been waiting for this",
            "some fun meme",
            "whats this meme",
            "watch me meme",
        ]
        
        # Reaction sentences for videos
        self.video_reactions = [
            "watch this video",
            "im ready for video",
            "you see that video",
            "looking good video",
            "what a video",
            "ive been waiting for video",
            "some fun video",
            "watch me video",
        ]
        
        # Reaction sentences for GIFs
        self.gif_reactions = [
            "watch this gif",
            "thats so funny gif",
            "you see that gif",
            "looking good gif",
            "what a gif",
            "some fun gif",
            "watch me gif",
        ]
        
        # Random idle chatter
        self.idle_chatter = [
            "im so happy",
            "what a beautiful day",
            "ive been waiting",
            "im ready for anything",
            "looking good",
            "some fun today",
            "well hello",
            "so happy",
            "whats going on",
            "thats beautiful",
        ]
    
    def _speak_sentence(self, sentence: str):
        """Speak a sentence word by word using available voice files"""
        words = sentence.split()
        spoken_words = []
        
        for word in words:
            if word in self.available_words:
                spoken_words.append(word)
                voice_file = self.voice_manager.get_file(word)
                if voice_file:
                    self.audio_player.play(voice_file)
                    time.sleep(0.3)  # Small gap between words
        
        return " ".join(spoken_words)
    
    def _speak_sentence_async(self, sentence: str):
        """Speak a sentence asynchronously in a thread"""
        def speak_thread():
            words = sentence.split()
            for word in words:
                if word in self.available_words and self.is_running:
                    voice_file = self.voice_manager.get_file(word)
                    if voice_file:
                        self.audio_player.play(voice_file)
                        time.sleep(0.35)
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def _setup_bindings(self):
        """Setup all keyboard and mouse bindings"""
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Double-Button-1>', self.on_double_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
        
        self.root.bind('<Escape>', lambda e: self.stop())
        self.root.bind('m', lambda e: self.play_random_meme())
        self.root.bind('s', lambda e: self.play_random_sound())
        self.root.bind('h', lambda e: self.say_hello())
        self.root.bind('v', lambda e: self.play_random_video())
        self.root.bind('g', lambda e: self.play_random_gif())
        self.root.bind('<space>', lambda e: self.toggle_auto_play())
        self.root.bind('x', lambda e: self.toggle_auto_play())
        self.root.bind('<Control-m>', lambda e: self.mod_menu.toggle())
        self.root.bind('t', lambda e: self.say_random_sentence())
        self.root.bind('y', lambda e: self.say_random_chatter())
        
        # Addon/Extension keys
        self.root.bind('<Control-a>', lambda e: self._toggle_addons())
        self.root.bind('<Control-e>', lambda e: self._toggle_extensions())
        
        # Dance keys
        self.root.bind('1', lambda e: self.character.set_dance("worm"))
        self.root.bind('2', lambda e: self.character.set_dance("moonwalk"))
        self.root.bind('3', lambda e: self.character.set_dance("thriller"))
        self.root.bind('4', lambda e: self.character.set_dance("robot"))
        self.root.bind('5', lambda e: self.character.set_dance("disco"))
        self.root.bind('w', lambda e: self.character.set_dance("water_survival"))
    
    def _animate(self):
        """Main animation loop"""
        if self.is_running:
            self.character.animate()
            if self.video_player and self.video_player.is_visible:
                self.video_player.update_position(self.character.x, self.character.y)
            if self.gif_player and self.gif_player.is_visible:
                self.gif_player.update_position(self.character.x, self.character.y)
            self.root.after(33, self._animate)
    
    def _schedule_auto_play(self, interval):
        """Schedule automatic meme playback"""
        def loop():
            while self.is_running:
                time.sleep(1)
                if self.is_running and not self.auto_play_paused:
                    self._auto_counter += 1
                    if self._auto_counter >= interval:
                        self._auto_counter = 0
                        self.root.after(0, self.play_random_meme)
        threading.Thread(target=loop, daemon=True).start()
    
    def _schedule_idle_chatter(self, interval=30):
        """Schedule random idle chatter"""
        def loop():
            while self.is_running:
                time.sleep(1)
                if self.is_running and self.character.state == "idle":
                    self._auto_counter += 1
                    if self._auto_counter >= interval:
                        self._auto_counter = 0
                        self.root.after(0, self.say_random_chatter)
        threading.Thread(target=loop, daemon=True).start()
    
    def _startup_greeting(self):
        """Play startup greeting with random sentence"""
        self.character.state = "waving"
        self.character.add_particle(240, 300, "sparkle", 10)
        
        # Pick random greeting
        greeting = random.choice(self.greetings)
        self.character.say(greeting)
        self._speak_sentence_async(greeting)
        
        self.root.after(2000, lambda: setattr(self.character, 'state', 'idle'))
    
    def _toggle_addons(self):
        """Toggle addons on/off"""
        addons = self.addon_manager.get_addons()
        if not addons:
            self.say("No addons found! Create in Addons/ folder")
            return
        
        active = self.addon_manager.active_addons
        if active:
            # Unload all active addons
            for name in active[:]:
                self.addon_manager.unload_addon(name)
            self.say("All addons unloaded")
        else:
            # Load first available addon
            for addon in addons:
                if not addon.get("enabled", False):
                    success = self.addon_manager.load_addon(addon["name"])
                    if success:
                        break
    
    def _toggle_extensions(self):
        """Toggle extensions on/off"""
        extensions = self.addon_manager.get_extensions()
        if not extensions:
            self.say("No extensions found! Create in Extensions/ folder")
            return
        
        active = self.addon_manager.active_extensions
        if active:
            # Unload all active extensions
            for name in active[:]:
                self.addon_manager.unload_extension(name)
            self.say("All extensions unloaded")
        else:
            # Load first available extension
            for ext in extensions:
                if not ext.get("enabled", False):
                    success = self.addon_manager.load_extension(ext["name"])
                    if success:
                        break
    
    # ============================================
    # Event handlers
    # ============================================
    
    def on_click(self, event):
        self.character.move_to(event.x, event.y + 80)
        self.play_random_meme()
    
    def on_double_click(self, event):
        self.say_hello()
    
    def on_right_click(self, event):
        self.play_random_sound()
        self.character.state = "bouncing"
        self.character.add_particle(event.x, event.y, "music", 5)
        # Say random sentence on right click
        sentence = random.choice(self.sentences)
        self.character.say(sentence)
        self._speak_sentence_async(sentence)
        self.root.after(1000, lambda: setattr(self.character, 'state', 'idle'))
    
    # ============================================
    # Public API
    # ============================================
    
    def say(self, text: str):
        """Display text without speaking"""
        self.character.say(text)
        self.character.is_talking = True
        self.root.after(2000, lambda: setattr(self.character, 'is_talking', False))
    
    def say_and_speak(self, text: str):
        """Display text AND speak it"""
        self.character.say(text)
        self.character.is_talking = True
        self._speak_sentence_async(text)
        self.root.after(3000, lambda: setattr(self.character, 'is_talking', False))
    
    def say_hello(self):
        """Say a random greeting"""
        greeting = random.choice(self.greetings)
        self.say_and_speak(greeting)
    
    def say_random_sentence(self):
        """Say a random sentence"""
        sentence = random.choice(self.sentences)
        self.say_and_speak(sentence)
    
    def say_random_chatter(self):
        """Say random idle chatter"""
        if self.character.state == "idle" or self.character.state == "walking":
            chatter = random.choice(self.idle_chatter)
            self.say_and_speak(chatter)
    
    def play_random_meme(self):
        """Play a random meme with voice reaction"""
        self.character.set_dance("dancing")
        self.character.emotion = "happy"
        self.character.add_particle(self.character.x, self.character.y - 100, "sparkle", 10)
        self.character.add_particle(self.character.x, self.character.y - 100, "music", 5)
        
        # Random meme reaction
        reaction = random.choice(self.meme_reactions)
        self.character.say(reaction)
        self._speak_sentence_async(reaction)
        
        result = self.media_manager.play_random_meme()
        if not result:
            self.character.say("No memes found!")
        self.root.after(4000, lambda: setattr(self.character, 'state', 'idle'))
    
    def play_random_sound(self):
        """Play a random sound effect"""
        self.media_manager.play_random_sound()
    
    def play_random_video(self):
        """Play a random video with voice reaction"""
        video = self.media_manager.play_random_video(show_window=True)
        if video:
            self.character.state = "video_dancing"
            self.character.video_playing = True
            self.character.add_particle(self.character.x, self.character.y - 100, "sparkle", 12)
            
            # Random video reaction
            reaction = random.choice(self.video_reactions)
            self.character.say(reaction)
            self._speak_sentence_async(reaction)
            
            self.video_player.show(str(video), self.character.x, self.character.y)
        else:
            self.character.say("No videos found!")
        self.root.after(4000, lambda: setattr(self.character, 'state', 'idle'))
    
    def play_random_gif(self):
        """Play a random GIF with voice reaction"""
        gif = self.media_manager.play_random_gif()
        if gif:
            self.character.state = "dancing"
            self.character.add_particle(self.character.x, self.character.y - 100, "sparkle", 8)
            
            # Random GIF reaction
            reaction = random.choice(self.gif_reactions)
            self.character.say(reaction)
            self._speak_sentence_async(reaction)
            
            self.gif_player.show(str(gif), self.character.x, self.character.y)
        else:
            self.character.say("No GIFs found!")
        self.root.after(4000, lambda: setattr(self.character, 'state', 'idle'))
    
    def play_file(self, file_path: str):
        """Play a specific file"""
        from pathlib import Path
        path = Path(file_path)
        if not path.exists():
            self.character.say("File not found!")
            return
        
        is_video = path.suffix.lower() in ['.mp4', '.avi', '.mkv', '.mov', '.webm']
        is_gif = path.suffix.lower() == '.gif'
        
        self.character.state = "video_dancing" if (is_video or is_gif) else "dancing"
        self.character.is_talking = True
        self.character.say(f"Playing {path.name[:20]}!")
        self.character.add_particle(self.character.x, self.character.y - 100, "sparkle", 8)
        
        if is_gif:
            self.gif_player.show(str(path), self.character.x, self.character.y)
        elif is_video:
            self.character.video_playing = True
            self.media_manager.audio.play_video(path, str(self.config.FFPLAY_PATH))
            self.video_player.show(str(path), self.character.x, self.character.y)
        else:
            self.media_manager.play_file(file_path)
        
        self.root.after(4000, lambda: [setattr(self.character, 'state', 'idle'),
                                       setattr(self.character, 'is_talking', False),
                                       setattr(self.character, 'video_playing', False)])
    
    def toggle_auto_play(self):
        """Toggle auto-play on/off"""
        self.auto_play_paused = not self.auto_play_paused
        status = "OFF" if self.auto_play_paused else "ON"
        self.character.say(f"Auto-play {status}")
        # Say it with voice too
        if not self.auto_play_paused:
            self._speak_sentence_async("im ready for anything")
        else:
            self._speak_sentence_async("well see you later")
        self._auto_counter = 0
    
    # ============================================
    # Application lifecycle
    # ============================================
    
    def start(self):
        """Start the application"""
        self.is_running = True
        
        print("=" * 60)
        print("              MEMEBOT IS RUNNING!")
        print("=" * 60)
        print("  CLICK anywhere to play memes")
        print("  DOUBLE-CLICK to hear voice greeting")
        print("  RIGHT-CLICK for sounds")
        print("  Ctrl+M = Open Mod Menu")
        print("  Ctrl+A = Toggle Addons")
        print("  Ctrl+E = Toggle Extensions")
        print("  M=meme  V=video  G=GIF  H=hello")
        print("  T=random sentence  Y=chatter")
        print("  Dance: 1=worm 2=moonwalk 3=thriller 4=robot 5=disco")
        print("  Water Survival: W (avoid rising water & meteors!)")
        print("  Space/X = Toggle auto-play")
        print("  ESC = Exit")
        print("=" * 60)
        
        # Start auto-play
        interval = self.config.get("auto_play_interval", 15)
        if interval > 0:
            self._schedule_auto_play(interval)
        
        # Start idle chatter
        self._schedule_idle_chatter(45)
        
        # Start animation
        self._animate()
        
        # Play startup greeting after 2 seconds
        self.root.after(2000, self._startup_greeting)
        
        # Start tkinter main loop
        self.root.mainloop()
    
    def stop(self):
        """Stop the application"""
        print("\nStopping MEMEBOT...")
        self.is_running = False
        self.audio_player.stop_all()
        self.video_player.hide()
        self.gif_player.hide()
        self.mod_menu.hide()
        
        # Unload all addons and extensions
        for name in self.addon_manager.active_addons[:]:
            self.addon_manager.unload_addon(name)
        for name in self.addon_manager.active_extensions[:]:
            self.addon_manager.unload_extension(name)
        
        self.config.save_settings()
        
        if HAS_PYSTRAY and hasattr(self, 'tray') and hasattr(self.tray, 'icon'):
            try:
                self.tray.icon.stop()
            except:
                pass
        
        try:
            self.root.destroy()
        except:
            pass
        
        os._exit(0)


# ============================================
# Main entry point
# ============================================

def main():
    """Start MEMEBOT"""
    print("=" * 60)
    print("              MEMEBOT - Desktop Character")
    print("              Modular v3.0 - Addons & Extensions")
    print("=" * 60)
    print("  Plays WAV, MP3, MP4, GIF files")
    print("  Custom voice files supported")
    print("  Encrypted .MSK skin system")
    print("  Lua scripting for mods")
    print("  Addon system (Lua) - Ctrl+A")
    print("  Extension system (Python) - Ctrl+E")
    print("  Circular mod menu (Ctrl+M)")
    print("  Water Survival mini-game (W)")
    print("  Voice vocabulary system with 45+ words")
    print("=" * 60)
    print()
    
    try:
        # Get the directory where app.py is located
        base_path = os.path.dirname(os.path.abspath(__file__))
        app = MemeBotApp(base_path)
        app.start()
    except KeyboardInterrupt:
        print("\nMEMEBOT interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("MEMEBOT has exited.")


if __name__ == "__main__":
    main()