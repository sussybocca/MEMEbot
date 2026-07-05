"""
MEMEBOT - Main Entry Point
Modular desktop character system with Lua skin support, Addons & Extensions
"""

from imports import *
from Src.vocab import build_vocabulary


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
        
        self.mod_menu = ModMenu(self.root, self.config, self.skin_loader, self)
        self.addon_manager = AddonManager(self.config, self)
        
        self._voice_channel = None
        
        # State
        self.auto_play_paused = False
        self._auto_counter = 0
        self._idle_counter = 0
        self._word_only_counter = 0
        self.is_running = False
        self._is_speaking = False
        self._speech_lock = threading.Lock()
        self._current_audio_type = None
        
        # Build vocabulary from vocab.py
        build_vocabulary(self)
        
        self._setup_bindings()
        if HAS_PYSTRAY:
            self.tray = TrayController(self)
    
    def _get_wav_duration(self, filepath):
        """Get duration of a WAV file in seconds"""
        try:
            with wave.open(filepath, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return frames / float(rate)
        except:
            return 0.5
    
    def _play_voice_file(self, voice_file):
        """Play a single voice file using dedicated channel and wait for it to finish"""
        if not voice_file or not self.is_running:
            return
        
        self._current_audio_type = 'voice'
        
        try:
            sound = pygame.mixer.Sound(voice_file)
            
            if self._voice_channel is None:
                self._voice_channel = pygame.mixer.Channel(0)
            
            self._voice_channel.stop()
            self._voice_channel.play(sound)
            
            while self._voice_channel.get_busy() and self.is_running:
                time.sleep(0.02)
            
            time.sleep(0.12)
            
        except Exception as e:
            print(f"[VOICE] pygame Sound failed, using fallback: {e}")
            duration = self._get_wav_duration(voice_file)
            self.audio_player.play(voice_file)
            time.sleep(max(duration, 0.5) + 0.2)
    
    def _speak_sentence_async(self, sentence: str):
        """Speak a sentence word by word asynchronously"""
        if self._is_speaking:
            return
        
        def speak_thread():
            with self._speech_lock:
                self._is_speaking = True
                try:
                    words = sentence.split()
                    for word in words:
                        if not self.is_running:
                            break
                        if word in self.available_words:
                            voice_file = self.voice_manager.get_file(word)
                            if voice_file:
                                self._play_voice_file(voice_file)
                finally:
                    self._is_speaking = False
                    self._current_audio_type = None
        
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
        
        self.root.bind('<Control-a>', lambda e: self._toggle_addons())
        self.root.bind('<Control-e>', lambda e: self._toggle_extensions())
        
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
        """Schedule automatic meme OR word playback depending on auto_play_paused"""
        def loop():
            meme_counter = 0
            word_counter = 0
            while self.is_running:
                time.sleep(1)
                if not self.is_running:
                    break
                
                if self.auto_play_paused:
                    if not self._is_speaking:
                        word_counter += 1
                        if word_counter >= 8:
                            word_counter = 0
                            self.root.after(0, self.say_random_sentence)
                else:
                    meme_counter += 1
                    if meme_counter >= interval and not self._is_speaking:
                        meme_counter = 0
                        self.root.after(0, self.play_random_meme)
        threading.Thread(target=loop, daemon=True).start()
    
    def _schedule_idle_chatter(self, interval=30):
        """Schedule random idle chatter"""
        def loop():
            counter = 0
            while self.is_running:
                time.sleep(1)
                if self.is_running and not self._is_speaking:
                    if self.character.state == "idle":
                        counter += 1
                        if counter >= interval:
                            counter = 0
                            self.root.after(0, self.say_random_chatter)
                else:
                    counter = 0
        threading.Thread(target=loop, daemon=True).start()
    
    def _startup_greeting(self):
        """Play startup greeting with random sentence"""
        self.character.state = "waving"
        self.character.add_particle(240, 300, "sparkle", 10)
        greeting = random.choice(self.greetings)
        self.character.say(greeting)
        self._speak_sentence_async(greeting)
        self.root.after(2000, lambda: setattr(self.character, 'state', 'idle'))
    
    def _toggle_addons(self):
        """Toggle addons on/off"""
        addons = self.addon_manager.get_addons()
        if not addons:
            self.say("No addons found")
            return
        active = self.addon_manager.active_addons
        if active:
            for name in active[:]:
                self.addon_manager.unload_addon(name)
            self.say("Addons unloaded")
        else:
            for addon in addons:
                if not addon.get("enabled", False):
                    self.addon_manager.load_addon(addon["name"])
                    break
    
    def _toggle_extensions(self):
        """Toggle extensions on/off"""
        extensions = self.addon_manager.get_extensions()
        if not extensions:
            self.say("No extensions found")
            return
        active = self.addon_manager.active_extensions
        if active:
            for name in active[:]:
                self.addon_manager.unload_extension(name)
            self.say("Extensions unloaded")
        else:
            for ext in extensions:
                if not ext.get("enabled", False):
                    self.addon_manager.load_extension(ext["name"])
                    break
    
    # ============================================
    # Event handlers
    # ============================================
    
    def on_click(self, event):
        self.character.move_to(event.x, event.y + 80)
        if self.auto_play_paused:
            if not self._is_speaking:
                sentence = random.choice(self.sentences)
                self.character.say(sentence)
                self._speak_sentence_async(sentence)
        else:
            if not self._is_speaking:
                self.play_random_meme()
    
    def on_double_click(self, event):
        self.say_hello()
    
    def on_right_click(self, event):
        self.character.state = "bouncing"
        self.character.add_particle(event.x, event.y, "music", 5)
        self.audio_player.stop_all()
        self.play_random_sound()
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
        self.audio_player.stop_all()
        time.sleep(0.15)
        greeting = random.choice(self.greetings)
        self.say_and_speak(greeting)
    
    def say_random_sentence(self):
        """Say a random sentence"""
        if self._is_speaking:
            return
        sentence = random.choice(self.sentences)
        self.say_and_speak(sentence)
    
    def say_random_chatter(self):
        """Say random idle chatter"""
        if not self._is_speaking:
            chatter = random.choice(self.idle_chatter)
            self.say_and_speak(chatter)
    
    def play_random_meme(self):
        """Play a random meme - speak reaction first, then meme"""
        if self._is_speaking:
            return
        
        self.character.set_dance("dancing")
        self.character.emotion = "happy"
        self.character.add_particle(self.character.x, self.character.y - 100, "sparkle", 10)
        self.character.add_particle(self.character.x, self.character.y - 100, "music", 5)
        
        reaction = random.choice(self.meme_reactions)
        self.character.say(reaction)
        
        def speak_then_play():
            with self._speech_lock:
                self._is_speaking = True
                try:
                    words = reaction.split()
                    for word in words:
                        if not self.is_running:
                            return
                        if word in self.available_words:
                            voice_file = self.voice_manager.get_file(word)
                            if voice_file:
                                self._play_voice_file(voice_file)
                    
                    time.sleep(0.2)
                    self.audio_player.stop_all()
                    if self.is_running:
                        result = self.media_manager.play_random_meme()
                        if not result:
                            self.root.after(0, lambda: self.character.say("No memes found"))
                finally:
                    self._is_speaking = False
                    self._current_audio_type = None
        
        threading.Thread(target=speak_then_play, daemon=True).start()
        self.root.after(5000, lambda: setattr(self.character, 'state', 'idle'))
    
    def play_random_sound(self):
        """Play a random sound effect"""
        self.media_manager.play_random_sound()
    
    def play_random_video(self):
        """Play a random video"""
        self.audio_player.stop_all()
        video = self.media_manager.play_random_video(show_window=True)
        if video:
            self.character.state = "video_dancing"
            self.character.video_playing = True
            self.character.add_particle(self.character.x, self.character.y - 100, "sparkle", 12)
            reaction = random.choice(self.video_reactions)
            self.character.say(reaction)
            self._speak_sentence_async(reaction)
            self.video_player.show(str(video), self.character.x, self.character.y)
        else:
            self.character.say("No videos found")
        self.root.after(4000, lambda: setattr(self.character, 'state', 'idle'))
    
    def play_random_gif(self):
        """Play a random GIF"""
        self.audio_player.stop_all()
        gif = self.media_manager.play_random_gif()
        if gif:
            self.character.state = "dancing"
            self.character.add_particle(self.character.x, self.character.y - 100, "sparkle", 8)
            reaction = random.choice(self.gif_reactions)
            self.character.say(reaction)
            self._speak_sentence_async(reaction)
            self.gif_player.show(str(gif), self.character.x, self.character.y)
        else:
            self.character.say("No GIFs found")
        self.root.after(4000, lambda: setattr(self.character, 'state', 'idle'))
    
    def play_file(self, file_path: str):
        """Play a specific file"""
        from pathlib import Path
        path = Path(file_path)
        if not path.exists():
            self.character.say("File not found")
            return
        
        is_video = path.suffix.lower() in ['.mp4', '.avi', '.mkv', '.mov', '.webm']
        is_gif = path.suffix.lower() == '.gif'
        
        self.character.state = "video_dancing" if (is_video or is_gif) else "dancing"
        self.character.is_talking = True
        self.character.say(f"Playing {path.name[:20]}")
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
        """Toggle auto-play on/off - OFF means words only, ON means memes"""
        self.auto_play_paused = not self.auto_play_paused
        self.audio_player.stop_all()
        time.sleep(0.15)
        
        if self.auto_play_paused:
            self.character.say("Auto-play OFF - Words mode")
        else:
            self.character.say("Auto-play ON - Memes mode")
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
        print("  CLICK anywhere to play memes (or words if auto-play OFF)")
        print("  DOUBLE-CLICK to hear voice greeting")
        print("  RIGHT-CLICK for sounds")
        print("  Ctrl+M = Open Mod Menu")
        print("  Ctrl+A = Toggle Addons")
        print("  Ctrl+E = Toggle Extensions")
        print("  M=meme  V=video  G=GIF  H=hello")
        print("  T=random sentence  Y=chatter")
        print("  Dance: 1=worm 2=moonwalk 3=thriller 4=robot 5=disco")
        print("  Water Survival: W (avoid rising water & meteors!)")
        print("  Space/X = Toggle auto-play (ON=memes, OFF=words only)")
        print("  ESC = Exit")
        print("=" * 60)
        
        interval = self.config.get("auto_play_interval", 15)
        if interval > 0:
            self._schedule_auto_play(interval)
        
        self._schedule_idle_chatter(45)
        self._animate()
        self.root.after(2000, self._startup_greeting)
        self.root.mainloop()
    
    def stop(self):
        """Stop the application"""
        print("\nStopping MEMEBOT...")
        self.is_running = False
        self.audio_player.stop_all()
        self.video_player.hide()
        self.gif_player.hide()
        self.mod_menu.hide()
        
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