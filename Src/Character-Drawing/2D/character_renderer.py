"""
MEMEBOT 2D Character Renderer - Main Module
Handles core character state, animations, and particle systems
Part 1 of 3 - Character State & Core Animation
"""

import math
import random
from typing import List, Optional
from PIL import Image, ImageDraw, ImageTk

from io import BytesIO
import base64
# Import drawing modules with fallback
import sys
import os

# Add the current directory to sys.path to ensure imports work
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

try:
    from character_drawing import draw_standing_character, draw_laying_character
    from character_accessories import draw_speech_bubble
except ImportError as e:
    print(f"Failed to import drawing modules from {_current_dir}: {e}")
    print(f"Files in directory: {os.listdir(_current_dir)}")
    raise


class CharacterRenderer:
    """Renders the MEMEBOT character with full V4.0 body customization support"""
    
    # Dance states
    DANCE_IDLE = "idle"
    DANCE_WALKING = "walking"
    DANCE_RUNNING = "running"
    DANCE_WAVING = "waving"
    DANCE_BOUNCING = "bouncing"
    DANCE_DANCING = "dancing"
    DANCE_MEME = "meme"
    DANCE_VIDEO = "video_dancing"
    DANCE_WORM = "worm"
    DANCE_MOONWALK = "moonwalk"
    DANCE_THRILLER = "thriller"
    DANCE_ROBOT = "robot"
    DANCE_DISCO = "disco"
    DANCE_WATER_SURVIVAL = "water_survival"
    DANCE_DEAD = "dead"
    DANCE_DISCO_PARTY = "disco_party"
    
    # Idle animation types for meme reactions
    IDLE_NORMAL = "normal"
    IDLE_SHUFFLE = "shuffle"
    IDLE_BOUNCE = "bounce"
    IDLE_HEADBANG = "headbang"
    IDLE_SPIN = "spin"
    IDLE_DAB = "dab"
    IDLE_FLOSS = "floss"
    IDLE_HIT = "hit"
    IDLE_WAVE_ARMS = "wave_arms"
    IDLE_CHICKEN = "chicken"
    IDLE_SAXOPHONE = "saxophone"
    IDLE_BREAKDANCE = "breakdance"
    IDLE_SURF = "surf"
    IDLE_POGO = "pogo"
    IDLE_SNAKE = "snake"
    IDLE_KICK = "kick"
    IDLE_ARM_WAVE = "arm_wave"
    IDLE_TWERK = "twerk"
    IDLE_ROLL = "roll"
    IDLE_COSSACK = "cossack"
    IDLE_JUMPING_JACK = "jumping_jack"
    IDLE_GRIDDY = "griddy"
    IDLE_ORANGE_JUSTICE = "orange_justice"
    IDLE_TAKE_THE_L = "take_the_l"
    IDLE_ELECTRO_SHUFFLE = "electro_shuffle"
    IDLE_BEST_MATES = "best_mates"
    IDLE_FRESH = "fresh"
    IDLE_HYPE = "hype"
    IDLE_LAUGH = "laugh"
    IDLE_CHEER = "cheer"
    IDLE_FACE_PALM = "face_palm"
    IDLE_SHOULDER_BRUSH = "shoulder_brush"
    IDLE_MIC_DROP = "mic_drop"
    IDLE_AIR_GUITAR = "air_guitar"
    IDLE_DRUM = "drum"
    IDLE_PIANO = "piano"
    IDLE_CONDUCTOR = "conductor"
    IDLE_ZOMBIE = "zombie"
    IDLE_MIME = "mime"
    IDLE_MARTIAL_ARTS = "martial_arts"
    IDLE_BALLET = "ballet"
    IDLE_TAP_DANCE = "tap_dance"
    IDLE_SALSA = "salsa"
    IDLE_SWING = "swing"
    IDLE_TWIST = "twist"
    IDLE_WORM_DANCE = "worm_dance"
    IDLE_CRAWL = "crawl"
    IDLE_FISH_OUT_OF_WATER = "fish_out_of_water"
    IDLE_DISCO_FEVER = "disco_fever"
    IDLE_RAVE = "rave"
    IDLE_STROBE_DANCE = "strobe_dance"
    
    def __init__(self, canvas, config, skin_loader):
        self.canvas = canvas
        self.config = config
        self.skin_loader = skin_loader
        self.root = None
        
        # Position
        self.x = config.get("start_x", 500)
        self.y = config.get("start_y", 500)
        self.target_x = self.x
        self.target_y = self.y
        
        # State
        self.state = self.DANCE_IDLE
        self.idle_type = self.IDLE_NORMAL
        self.frame = 0
        self.walk_cycle = 0
        self.emotion = "happy"
        self.is_talking = False
        self.facing_right = True
        
        # Drawing
        self.sprite_id = None
        self.current_image = None
        self.blink_timer = random.randint(30, 70)
        self.is_blinking = False
        self.blink_frame = 0
        self.nose_twitch = 0
        
        # Screen bounds
        self.screen_width = canvas.winfo_screenwidth()
        self.screen_height = canvas.winfo_screenheight()
        
        # Particles
        self.particles = []
        self.speech_text = ""
        self.speech_timer = 0
        
        # Dance
        self.dance_timer = 0
        self.dance_override = False
        self.dance_start_x = self.x
        self.dance_start_y = self.y
        self.wander_timer = 0
        self.wander_interval = random.randint(4, 10)
        
        # Previous animation values
        self.prev_leg_swing = 0
        self.prev_arm_swing = 0
        self.prev_body_bob = 0
        self.prev_extra_spin = 0
        self.prev_arm_raise = 0
        
        # Video/lip sync
        self.video_playing = False
        self.lip_sync_intensity = 0
        self.audio_envelope = None
        self.audio_start_time = 0
        
        # Water survival state
        self.water_level = 0
        self.water_rising = True
        self.water_speed = 1.5
        self.water_float_y = 0
        self.is_dead = False
        self.death_timer = 0
        self.meteor_x = 0
        self.meteor_y = -100
        self.meteor_active = False
        self.survival_score = 0
        
        # Idle animation cycle
        self.idle_timer = 0
        self.idle_duration = 0
        self.current_idle_animation = 0
        
        # Extra animation state
        self.extra_bounce = 0
        self.extra_twist = 0
        self.extra_flail = 0
        
        # Animation sequence tracking
        self.idle_sequence_phase = 0
        self.idle_sequence_timer = 0
        
        # Disco party mode
        self.disco_party_active = False
        self.disco_party_timer = 0
        self.disco_party_duration = 600  # 20 seconds at 30fps
        self.disco_light_phase = 0
        self.disco_ball_x = 0
        self.disco_ball_y = 0
        self.disco_ball_rotation = 0
        self.disco_floor_tiles = []
        self.disco_strobe_on = True
        self.disco_strobe_timer = 0
        self.disco_color_index = 0
        self.disco_colors = [
            (255, 0, 0, 200), (0, 0, 255, 200), (255, 0, 255, 200),
            (0, 255, 255, 200), (255, 255, 0, 200), (0, 255, 0, 200),
            (255, 100, 0, 200), (100, 0, 255, 200), (255, 50, 150, 200),
            (50, 255, 200, 200)
        ]
        
        # 30-minute timer for disco party
        self.disco_party_cooldown = 1800  # 30 minutes in seconds (30 * 60)
        self.disco_party_available = True
        self.last_disco_party_time = 0
        
        # Music path
        self.disco_music_path = r"D:\MODZ4\music\[FREE] Trap Type Beat - _HUSH_ _ Freestyle Beat 2026 _ Melodic Type Beat _ Rap Type Dark [jWhSBxHxjgs].mp4"
        
        self.update_drawing()
    
    # ============================================
    # PARTICLE SYSTEM
    # ============================================
    
    def add_particle(self, x, y, ptype, count=3):
        """Add particles at position"""
        for _ in range(count):
            self.particles.append({
                'x': x + random.randint(-40, 40),
                'y': y + random.randint(-40, 40),
                'type': ptype,
                'life': 1.0,
                'vy': random.uniform(-4, -0.3),
                'vx': random.uniform(-3, 3)
            })
    
    def update_particles(self):
        """Update particle positions and lifetimes"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.06
            p['life'] -= 0.01
            if p['life'] <= 0:
                self.particles.remove(p)
    
    # ============================================
    # COMMANDS
    # ============================================
    
    def say(self, text: str):
        """Display speech bubble"""
        self.speech_text = text
        self.speech_timer = 120
        self.is_talking = True
    
    def move_to(self, x, y):
        """Move character to target position"""
        self.target_x = max(50, min(x, self.screen_width - 50))
        self.target_y = max(50, min(y, self.screen_height - 250))
    
    def set_dance(self, dance_state: str):
        """Set dance animation state"""
        self.state = dance_state
        self.dance_timer = 0
        self.dance_override = True
        self.dance_start_x = self.x
        self.dance_start_y = self.y
        
        if dance_state == self.DANCE_WATER_SURVIVAL:
            self._init_water_survival()
    
    # ============================================
    # DISCO PARTY MODE
    # ============================================
    
    def _check_disco_party(self):
        """Check if it's time for a disco party (every 30 minutes)"""
        import time
        current_time = time.time()
        
        if self.disco_party_available and (current_time - self.last_disco_party_time) >= self.disco_party_cooldown:
            self._start_disco_party()
    
    def _start_disco_party(self):
        """Start the disco party mode"""
        self.disco_party_active = True
        self.disco_party_timer = 0
        self.disco_party_duration = 600  # 20 seconds
        self.disco_ball_x = self.x
        self.disco_ball_y = self.y - 200
        self.disco_ball_rotation = 0
        self.disco_strobe_on = True
        self.disco_strobe_timer = 0
        self.disco_light_phase = 0
        self.disco_color_index = 0
        self.disco_party_available = False
        
        # Initialize disco floor tiles
        self.disco_floor_tiles = []
        for i in range(10):
            for j in range(6):
                self.disco_floor_tiles.append({
                    'x': i * 50 + random.randint(-5, 5),
                    'y': j * 50 + random.randint(-5, 5),
                    'color': random.choice(self.disco_colors),
                    'phase': random.uniform(0, 2 * math.pi),
                    'size': random.randint(30, 50)
                })
        
        # Set character to crazy disco mode
        self.state = self.DANCE_DISCO_PARTY
        self.idle_type = self.IDLE_DISCO_FEVER
        self.dance_timer = 0
        self.dance_override = True
        
        # Spawn particles
        self.add_particle(self.x, self.y, "sparkle", 50)
        self.add_particle(self.x, self.y, "music", 30)
        
        # Say something
        self.say("DISCO PARTY TIME!!!")
        
        # Play the music
        if self.root and hasattr(self.root, 'after'):
            # Notify app to play music
            import time
            self.last_disco_party_time = time.time()
    
    def _update_disco_party(self):
        """Update disco party effects"""
        if not self.disco_party_active:
            return
        
        self.disco_party_timer += 1
        self.disco_ball_rotation += 5
        self.disco_light_phase += 0.15
        
        # Strobe effect
        self.disco_strobe_timer += 1
        if self.disco_strobe_timer > random.randint(3, 10):
            self.disco_strobe_on = not self.disco_strobe_on
            self.disco_strobe_timer = 0
            if self.disco_strobe_on:
                self.disco_color_index = (self.disco_color_index + 1) % len(self.disco_colors)
        
        # Move disco ball
        self.disco_ball_x = self.x + math.sin(self.disco_light_phase * 2) * 50
        self.disco_ball_y = self.y - 200 + math.cos(self.disco_light_phase * 1.5) * 30
        
        # Update floor tiles
        for tile in self.disco_floor_tiles:
            tile['phase'] += 0.1
            tile['color'] = random.choice(self.disco_colors) if random.random() < 0.3 else tile['color']
        
        # Spawn disco particles
        if random.random() < 0.8:
            px = random.randint(0, self.screen_width)
            py = random.randint(0, self.screen_height)
            self.add_particle(px, py, "sparkle", 3)
        
        # Character goes crazy
        if self.idle_type == self.IDLE_DISCO_FEVER:
            if self.disco_party_timer % 60 < 30:
                self.idle_type = self.IDLE_RAVE
            else:
                self.idle_type = self.IDLE_STROBE_DANCE
        
        # End party
        if self.disco_party_timer >= self.disco_party_duration:
            self._end_disco_party()
    
    def _end_disco_party(self):
        """End the disco party"""
        self.disco_party_active = False
        self.state = self.DANCE_BOUNCING
        self.idle_type = self.IDLE_NORMAL
        self.dance_timer = 0
        self.dance_override = False
        self.disco_party_available = True
        
        # Final burst of particles
        self.add_particle(self.x, self.y, "sparkle", 30)
        self.say("That was CRAZY!")
    
    # ============================================
    # WATER SURVIVAL ANIMATION
    # ============================================
    
    def _init_water_survival(self):
        """Initialize water survival challenge"""
        self.water_level = self.screen_height
        self.water_rising = True
        self.water_speed = 1.5
        self.water_float_y = 0
        self.is_dead = False
        self.death_timer = 0
        self.meteor_x = random.randint(100, self.screen_width - 100)
        self.meteor_y = -100
        self.meteor_active = True
        self.survival_score = 0
        
        # Move character to center bottom
        self.x = self.screen_width // 2
        self.y = self.screen_height - 200
        
        self.add_particle(self.x, self.y, "water", 20)
    
    def _update_water_survival(self):
        """Update water survival animation state"""
        if not self.is_dead:
            # Rising water - stop when fully above screen
            if self.water_rising:
                self.water_level -= self.water_speed
                if self.water_level < -50:
                    self.water_rising = False
            
            # Character floating
            self.water_float_y = math.sin(self.dance_timer * 0.1) * 15
            
            # Move character to avoid water
            if self.water_level < self.y:
                self.y -= 2.5
                self.survival_score += 1
            
            # Falling meteor
            if self.meteor_active:
                self.meteor_y += 3
                
                # Check meteor collision with character
                meteor_dist = math.sqrt((self.meteor_x - self.x)**2 + (self.meteor_y - self.y)**2)
                if meteor_dist < 60:
                    self._kill_character()
                
                # Reset meteor if off screen
                if self.meteor_y > self.screen_height:
                    self.meteor_x = random.randint(100, self.screen_width - 100)
                    self.meteor_y = -100
                    self.survival_score += 50
            
            # Water splash particles near character
            if random.random() < 0.3:
                water_x = self.x + random.randint(-40, 40)
                water_y = self.y + 60
                self.add_particle(water_x, water_y, "water_drop", 2)
            
            # Death by drowning
            if self.y < self.water_level + 30:
                self._kill_character()
    
    def _kill_character(self):
        """Character death animation"""
        self.is_dead = True
        self.death_timer = 0
        self.emotion = "dead"
        self.add_particle(self.x, self.y, "sparkle", 30)
        self.add_particle(self.x, self.y, "water", 20)
        
        # Show score
        self.say(f"Score: {self.survival_score}!")
    
    def _respawn_character(self):
        """Respawn after death"""
        self.is_dead = False
        self.emotion = "happy"
        self.state = self.DANCE_BOUNCING
        self.dance_timer = 0
        self.dance_override = False
        
        # Move to safe position
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        
        self.add_particle(self.x, self.y, "sparkle", 20)
        self.say("I'm back!")
    
    # ============================================
    # IDLE ANIMATION CYCLING
    # ============================================
    
    def _cycle_idle_animation(self):
        """Cycle through idle animations when meme is playing"""
        if self.disco_party_active:
            return  # Don't cycle during disco party
        
        self.idle_timer += 1
        
        if self.idle_timer > self.idle_duration:
            # Pick new idle animation
            idle_anims = [
                self.IDLE_SHUFFLE, self.IDLE_BOUNCE, self.IDLE_HEADBANG,
                self.IDLE_SPIN, self.IDLE_DAB, self.IDLE_FLOSS,
                self.IDLE_HIT, self.IDLE_WAVE_ARMS, self.IDLE_CHICKEN,
                self.IDLE_SAXOPHONE, self.IDLE_SURF, self.IDLE_POGO,
                self.IDLE_SNAKE, self.IDLE_KICK, self.IDLE_ARM_WAVE,
                self.IDLE_TWERK, self.IDLE_ROLL, self.IDLE_COSSACK,
                self.IDLE_JUMPING_JACK, self.IDLE_GRIDDY, self.IDLE_ORANGE_JUSTICE,
                self.IDLE_TAKE_THE_L, self.IDLE_ELECTRO_SHUFFLE, self.IDLE_BEST_MATES,
                self.IDLE_FRESH, self.IDLE_HYPE, self.IDLE_LAUGH,
                self.IDLE_CHEER, self.IDLE_FACE_PALM, self.IDLE_SHOULDER_BRUSH,
                self.IDLE_MIC_DROP, self.IDLE_AIR_GUITAR, self.IDLE_DRUM,
                self.IDLE_PIANO, self.IDLE_CONDUCTOR, self.IDLE_ZOMBIE,
                self.IDLE_MIME, self.IDLE_MARTIAL_ARTS, self.IDLE_BALLET,
                self.IDLE_TAP_DANCE, self.IDLE_SALSA, self.IDLE_SWING,
                self.IDLE_TWIST, self.IDLE_WORM_DANCE, self.IDLE_CRAWL,
                self.IDLE_FISH_OUT_OF_WATER
            ]
            
            if self.state in [self.DANCE_DANCING, self.DANCE_MEME]:
                # More energetic animations during memes
                energetic = [self.IDLE_HEADBANG, self.IDLE_DAB, self.IDLE_FLOSS,
                           self.IDLE_BREAKDANCE, self.IDLE_POGO, self.IDLE_CHICKEN,
                           self.IDLE_GRIDDY, self.IDLE_ORANGE_JUSTICE, self.IDLE_TAKE_THE_L,
                           self.IDLE_ELECTRO_SHUFFLE, self.IDLE_FRESH, self.IDLE_HYPE,
                           self.IDLE_TWERK, self.IDLE_COSSACK, self.IDLE_JUMPING_JACK,
                           self.IDLE_AIR_GUITAR, self.IDLE_DRUM, self.IDLE_SHOULDER_BRUSH,
                           self.IDLE_MIC_DROP, self.IDLE_CHEER, self.IDLE_ROLL]
                self.idle_type = random.choice(energetic)
                self.idle_duration = random.randint(30, 90)
            else:
                self.idle_type = random.choice(idle_anims)
                self.idle_duration = random.randint(60, 180)
            
            self.idle_timer = 0
            self.idle_sequence_phase = 0
            self.idle_sequence_timer = 0
    
    def _get_idle_bonus_params(self):
        """Get extra animation parameters for idle animations"""
        bonus = {
            'extra_bounce': 0,
            'extra_twist': 0,
            'extra_flail': 0,
            'arm_specific': 0,
            'leg_specific': 0,
            'head_specific': 0,
        }
        
        t = self.idle_timer * 0.3
        
        if self.idle_type == self.IDLE_SHUFFLE:
            bonus['extra_bounce'] = math.sin(t * 2) * 15
            bonus['extra_twist'] = math.sin(t) * 10
        elif self.idle_type == self.IDLE_HEADBANG:
            bonus['head_specific'] = math.sin(t * 3) * 20
            bonus['extra_bounce'] = math.sin(t * 2) * 5
        elif self.idle_type == self.IDLE_DAB:
            if self.idle_timer < 40:
                bonus['arm_specific'] = min(self.idle_timer * 2, 60)
                bonus['head_specific'] = -self.idle_timer * 0.5
            else:
                bonus['arm_specific'] = 60
                bonus['head_specific'] = -20
        elif self.idle_type == self.IDLE_FLOSS:
            bonus['extra_twist'] = math.sin(t * 3) * 20
            bonus['arm_specific'] = math.sin(t * 4) * 30
        elif self.idle_type == self.IDLE_WAVE_ARMS:
            bonus['arm_specific'] = math.sin(t * 2) * 40
            bonus['extra_flail'] = math.cos(t * 1.5) * 15
        elif self.idle_type == self.IDLE_CHICKEN:
            bonus['arm_specific'] = math.sin(t * 5) * 25
            bonus['extra_bounce'] = math.sin(t * 3) * 10
        elif self.idle_type == self.IDLE_POGO:
            bonus['extra_bounce'] = abs(math.sin(t * 3)) * 30
        elif self.idle_type == self.IDLE_SNAKE:
            bonus['extra_twist'] = math.sin(t * 1.5) * 25
            bonus['head_specific'] = math.sin(t * 2) * 15
        elif self.idle_type == self.IDLE_KICK:
            if self.idle_timer % 40 < 20:
                bonus['leg_specific'] = math.sin(t * 4) * 40
            else:
                bonus['leg_specific'] = 0
        elif self.idle_type == self.IDLE_ARM_WAVE:
            bonus['arm_specific'] = math.sin(t * 2.5) * 45
            bonus['extra_twist'] = math.cos(t * 1.8) * 12
        elif self.idle_type == self.IDLE_TWERK:
            bonus['extra_bounce'] = math.sin(t * 5) * 20
            bonus['extra_twist'] = math.sin(t * 3) * 10
            bonus['leg_specific'] = abs(math.sin(t * 5)) * 25
        elif self.idle_type == self.IDLE_ROLL:
            bonus['extra_twist'] = t * 3 % 360
            bonus['extra_flail'] = 15
            bonus['head_specific'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_COSSACK:
            if self.idle_timer % 60 < 30:
                bonus['leg_specific'] = 35
                bonus['extra_bounce'] = 10
            else:
                bonus['leg_specific'] = 0
                bonus['extra_bounce'] = 0
        elif self.idle_type == self.IDLE_JUMPING_JACK:
            bonus['arm_specific'] = math.sin(t * 3) * 40
            bonus['leg_specific'] = abs(math.sin(t * 3)) * 20
            bonus['extra_bounce'] = abs(math.sin(t * 3)) * 15
        elif self.idle_type == self.IDLE_GRIDDY:
            bonus['extra_bounce'] = math.sin(t * 4) * 12
            bonus['arm_specific'] = math.sin(t * 2) * 25
            bonus['leg_specific'] = math.sin(t * 3) * 15
        elif self.idle_type == self.IDLE_ORANGE_JUSTICE:
            bonus['arm_specific'] = math.sin(t * 2) * 50
            bonus['extra_twist'] = math.sin(t * 3) * 15
            bonus['leg_specific'] = abs(math.sin(t * 4)) * 20
        elif self.idle_type == self.IDLE_TAKE_THE_L:
            if self.idle_timer < 30:
                bonus['arm_specific'] = 50
                bonus['head_specific'] = 15
            else:
                bonus['arm_specific'] = 50
                bonus['head_specific'] = 15
                bonus['extra_bounce'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_ELECTRO_SHUFFLE:
            bonus['extra_twist'] = math.sin(t * 4) * 18
            bonus['arm_specific'] = math.sin(t * 5) * 30
            bonus['leg_specific'] = math.sin(t * 3) * 20
        elif self.idle_type == self.IDLE_BEST_MATES:
            bonus['arm_specific'] = math.sin(t * 2) * 35
            bonus['extra_bounce'] = math.sin(t * 3) * 12
        elif self.idle_type == self.IDLE_FRESH:
            bonus['extra_twist'] = math.sin(t * 2) * 20
            bonus['arm_specific'] = math.cos(t * 1.5) * 25
            bonus['head_specific'] = math.sin(t * 2) * 8
        elif self.idle_type == self.IDLE_HYPE:
            bonus['extra_bounce'] = abs(math.sin(t * 4)) * 25
            bonus['arm_specific'] = math.sin(t * 5) * 30
            bonus['head_specific'] = math.sin(t * 6) * 10
        elif self.idle_type == self.IDLE_LAUGH:
            bonus['extra_bounce'] = math.sin(t * 3) * 10
            bonus['head_specific'] = math.sin(t * 4) * 15
            bonus['arm_specific'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_CHEER:
            bonus['arm_specific'] = abs(math.sin(t * 3)) * 50
            bonus['extra_bounce'] = abs(math.sin(t * 3)) * 15
        elif self.idle_type == self.IDLE_FACE_PALM:
            if self.idle_timer % 80 < 40:
                bonus['arm_specific'] = 40
                bonus['head_specific'] = -25
            else:
                bonus['arm_specific'] = 0
                bonus['head_specific'] = 0
        elif self.idle_type == self.IDLE_SHOULDER_BRUSH:
            bonus['arm_specific'] = math.sin(t * 2) * 30
            bonus['extra_twist'] = math.cos(t * 1.5) * 8
        elif self.idle_type == self.IDLE_MIC_DROP:
            if self.idle_timer < 20:
                bonus['arm_specific'] = self.idle_timer * 2
            elif self.idle_timer < 40:
                bonus['arm_specific'] = 60
            else:
                bonus['arm_specific'] = 0
                bonus['extra_bounce'] = 5
        elif self.idle_type == self.IDLE_AIR_GUITAR:
            bonus['arm_specific'] = math.sin(t * 4) * 35
            bonus['extra_bounce'] = math.sin(t * 2) * 10
            bonus['head_specific'] = math.sin(t * 3) * 15
        elif self.idle_type == self.IDLE_DRUM:
            bonus['arm_specific'] = abs(math.sin(t * 5)) * 40
            bonus['extra_bounce'] = math.sin(t * 2) * 8
        elif self.idle_type == self.IDLE_PIANO:
            bonus['arm_specific'] = math.sin(t * 3) * 25
            bonus['extra_twist'] = math.sin(t * 1.5) * 10
        elif self.idle_type == self.IDLE_CONDUCTOR:
            bonus['arm_specific'] = math.sin(t * 2) * 45
            bonus['extra_twist'] = math.cos(t * 1.2) * 10
        elif self.idle_type == self.IDLE_ZOMBIE:
            bonus['arm_specific'] = math.sin(t * 1.5) * 20
            bonus['leg_specific'] = math.sin(t * 1.2) * 15
            bonus['extra_flail'] = 10
            bonus['head_specific'] = math.sin(t * 0.8) * 8
        elif self.idle_type == self.IDLE_MIME:
            bonus['arm_specific'] = math.sin(t * 1.5) * 30
            bonus['extra_twist'] = math.sin(t * 0.8) * 5
        elif self.idle_type == self.IDLE_MARTIAL_ARTS:
            if self.idle_timer % 50 < 25:
                bonus['arm_specific'] = 50
                bonus['leg_specific'] = 40
            else:
                bonus['arm_specific'] = 10
                bonus['leg_specific'] = 5
        elif self.idle_type == self.IDLE_BALLET:
            bonus['arm_specific'] = math.sin(t * 2) * 25
            bonus['leg_specific'] = math.sin(t * 3) * 15
            bonus['extra_bounce'] = math.sin(t * 4) * 5
        elif self.idle_type == self.IDLE_TAP_DANCE:
            bonus['leg_specific'] = abs(math.sin(t * 6)) * 20
            bonus['arm_specific'] = math.sin(t * 3) * 10
        elif self.idle_type == self.IDLE_SALSA:
            bonus['extra_twist'] = math.sin(t * 3) * 20
            bonus['arm_specific'] = math.cos(t * 2) * 25
            bonus['leg_specific'] = math.sin(t * 4) * 15
        elif self.idle_type == self.IDLE_SWING:
            bonus['extra_twist'] = math.sin(t * 2) * 25
            bonus['arm_specific'] = math.sin(t * 3) * 30
            bonus['extra_bounce'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_TWIST:
            bonus['extra_twist'] = math.sin(t * 3) * 30
            bonus['arm_specific'] = math.sin(t * 2) * 15
            bonus['leg_specific'] = math.sin(t * 2.5) * 10
        elif self.idle_type == self.IDLE_WORM_DANCE:
            bonus['extra_bounce'] = math.sin(t * 2) * 20
            bonus['extra_twist'] = math.sin(t * 1.5) * 15
            bonus['arm_specific'] = math.sin(t * 3) * 25
        elif self.idle_type == self.IDLE_CRAWL:
            bonus['extra_flail'] = 20
            bonus['leg_specific'] = math.sin(t * 2) * 10
            bonus['arm_specific'] = math.sin(t * 2.5) * 10
        elif self.idle_type == self.IDLE_FISH_OUT_OF_WATER:
            bonus['extra_bounce'] = abs(math.sin(t * 3)) * 25
            bonus['extra_flail'] = 20
            bonus['arm_specific'] = math.sin(t * 4) * 30
            bonus['leg_specific'] = math.sin(t * 4) * 25
        elif self.idle_type == self.IDLE_DISCO_FEVER:
            bonus['extra_bounce'] = abs(math.sin(t * 6)) * 30
            bonus['extra_twist'] = math.sin(t * 5) * 25
            bonus['arm_specific'] = math.sin(t * 7) * 40
            bonus['leg_specific'] = math.cos(t * 6) * 30
            bonus['head_specific'] = math.sin(t * 8) * 15
        elif self.idle_type == self.IDLE_RAVE:
            bonus['extra_bounce'] = abs(math.sin(t * 8)) * 35
            bonus['arm_specific'] = math.sin(t * 9) * 50
            bonus['extra_twist'] = t * 5 % 360
            bonus['head_specific'] = math.sin(t * 10) * 20
        elif self.idle_type == self.IDLE_STROBE_DANCE:
            bonus['extra_bounce'] = abs(math.sin(t * 4)) * 40
            bonus['extra_twist'] = math.sin(t * 3) * 35
            bonus['arm_specific'] = math.sin(t * 6) * 45
            bonus['leg_specific'] = math.cos(t * 5) * 35
        
        return bonus
    
    # ============================================
    # CONFIG HELPERS
    # ============================================
    
    def _get_body_config(self):
        """Get full body configuration from MSK skin data"""
        skin = self.skin_loader.get_current_skin()
        return {
            "scale": skin.get("body_scale", {
                "height": 1.0, "width": 1.0,
                "head_size": 1.0, "limb_length": 1.0
            }),
            "shape": skin.get("body_shape", {
                "type": "default", "torso_width": 1.0, "torso_height": 1.0,
                "belly_size": 0.0, "shoulder_width": 1.0, "hip_width": 1.0,
                "custom_points": []
            }),
            "limbs": skin.get("limbs", {
                "arm_style": "default", "arm_length": 1.0, "arm_width": 1.0,
                "leg_style": "default", "leg_length": 1.0, "leg_width": 1.0,
                "hand_style": "default", "foot_style": "default"
            }),
            "head_cfg": skin.get("head", {
                "shape": "round", "size": 1.0,
                "face_position": 0.0, "ear_style": "default", "ear_size": 1.0
            }),
            "hair_cfg": skin.get("hair", {
                "style": "default", "length": 1.0, "volume": 1.0,
                "bangs": True, "custom_points": []
            }),
            "outfit_cfg": skin.get("outfit", {
                "type": "default",
                "top_color": [100, 180, 255, 255],
                "bottom_color": [50, 130, 200, 255],
                "custom_shapes": []
            }),
            "colors": skin.get("colors", {}),
            "clothing": skin.get("clothing", {}),
            "accessories": skin.get("accessories", {}),
            "sprite_data": skin.get("sprite_data", {}),
        }
    
    def _get_skin_colors(self):
        """Get colors from MSK skin data with fallback defaults"""
        skin = self.skin_loader.get_current_skin()
        colors = skin.get("colors", {})
        return {
            "body": tuple(colors.get("body", [100, 180, 255, 255])),
            "body_outline": tuple(colors.get("body_outline", [50, 130, 200, 255])),
            "skin": tuple(colors.get("skin", [255, 220, 180, 255])),
            "skin_outline": tuple(colors.get("skin_outline", [200, 170, 140, 255])),
            "hair": tuple(colors.get("hair", [80, 60, 40, 255])),
            "hair_outline": tuple(colors.get("hair_outline", [60, 40, 20, 255])),
            "eyes": tuple(colors.get("eyes", [100, 180, 255, 255])),
            "pupils": tuple(colors.get("pupils", [30, 30, 30, 255])),
            "mouth": tuple(colors.get("mouth", [200, 100, 100, 255])),
            "tongue": tuple(colors.get("tongue", [255, 150, 150, 255])),
            "cheeks": tuple(colors.get("cheeks", [255, 180, 180, 80])),
            "feet": tuple(colors.get("feet", [50, 50, 50, 255])),
            "hands": tuple(colors.get("hands", [255, 220, 180, 255])),
            "tag_bg": tuple(colors.get("name_tag_bg", [50, 50, 50, 200])),
            "tag_text": tuple(colors.get("name_tag_text", [255, 255, 255, 255])),
            "outfit_primary": tuple(colors.get("outfit_primary", [100, 180, 255, 255])),
            "outfit_secondary": tuple(colors.get("outfit_secondary", [50, 130, 200, 255])),
            "ears_inner": tuple(colors.get("ears_inner", [255, 180, 200, 255])),
        }
    
    def _get_dance_params(self):
        """Get dance parameters from dance engine"""
        self.dance_timer += 1
        import importlib
        DanceEngine = importlib.import_module('Animations.DanceMoves.dance_engine').DanceEngine
        return DanceEngine.get_params(self)
    
    def _draw_msk_sprites(self, draw, cfg):
        """Draw character using MSK sprite data from Drawer-created skins"""
        sprite_data = cfg.get("sprite_data", None)
        if not sprite_data:
            return None
        
        layers = sprite_data.get("layers", {})
        if not layers:
            return None
        
        layer_order = [
            "tail", "wings", "legs", "body", "arms", "outfit",
            "accessories", "head", "hair", "eyes", "mouth",
            "hat", "glasses",
        ]
        
        composite = Image.new('RGBA', (480, 620), (0, 0, 0, 0))
        
        for layer_name in layer_order:
            if layer_name in layers:
                try:
                    layer_data = base64.b64decode(layers[layer_name])
                    layer_img = Image.open(BytesIO(layer_data)).convert('RGBA')
                    composite = Image.alpha_composite(composite, layer_img)
                except Exception:
                    pass
        
        return composite
    
    # ============================================
    # MAIN DRAWING UPDATE
    # ============================================
    
    def update_drawing(self):
        """Main drawing update - creates character image"""
        img = Image.new('RGBA', (480, 620), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        self.update_particles()
        
        # Check for disco party trigger
        self._check_disco_party()
        
        # Update disco party
        if self.disco_party_active:
            self._update_disco_party()
        
        # Handle water survival state
        if self.state == self.DANCE_WATER_SURVIVAL:
            self._update_water_survival()
        
        # Handle death state
        if self.is_dead:
            self.death_timer += 1
            if self.death_timer > 90:  # Respawn after ~3 seconds
                self._respawn_character()
        
        cfg = self._get_body_config()
        c = self._get_skin_colors()
        
        scale = cfg["scale"]
        height_mult = scale.get("height", 1.0)
        width_mult = scale.get("width", 1.0)
        head_size_mult = scale.get("head_size", 1.0)
        
        cx, cy = 240, 300
        ground_y = 530
        
        # Blinking
        self.blink_timer -= 1
        if self.blink_timer <= 0:
            self.is_blinking = True
            self.blink_timer = random.randint(50, 120)
        if self.is_blinking:
            self.blink_frame += 1
            if self.blink_frame > 6:
                self.is_blinking = False
                self.blink_frame = 0
        
        self.nose_twitch = (self.nose_twitch + 0.08) % (2 * math.pi)
        
        # Get dance parameters
        leg_swing, arm_swing, body_bob, extra_spin, arm_raise, head_bob, body_squash, laying_down = self._get_dance_params()
        
        # Apply water float
        if self.state == self.DANCE_WATER_SURVIVAL:
            body_bob += self.water_float_y
        
        # Cycle idle animations
        self._cycle_idle_animation()
        idle_bonus = self._get_idle_bonus_params()
        
        # Draw disco party effects
        if self.disco_party_active:
            self._draw_disco_effects(draw, c, cx, ground_y)
        
        # Draw shadow
        shadow_w = int((80 if laying_down else 50) * width_mult)
        if not self.state == self.DANCE_WATER_SURVIVAL:
            draw.ellipse([cx - shadow_w, ground_y - 5, cx + shadow_w, ground_y + 15], fill=(0, 0, 0, 30))
        
        # Draw water if in survival mode
        if self.state == self.DANCE_WATER_SURVIVAL:
            self._draw_water_level(draw, c)
        
        # Try MSK sprite-based rendering first
        sprite_composite = self._draw_msk_sprites(draw, cfg)
        
        if sprite_composite is not None and not self.state == self.DANCE_WATER_SURVIVAL:
            # Use sprite-based rendering (from Drawer-created skins)
            img.paste(sprite_composite, (0, 0), sprite_composite)
        else:
            # Fall back to procedural drawing
            if laying_down:
                draw_laying_character(self, draw, c, cfg, cx, ground_y, body_bob)
            else:
                draw_standing_character(self, draw, c, cfg, cx, ground_y, leg_swing, arm_swing, 
                                       body_bob, extra_spin, arm_raise, head_bob, idle_bonus)
        
        # Draw death effects
        if self.is_dead:
            self._draw_death_effects(draw, cx, ground_y)
        
        # Draw meteor
        if self.meteor_active and self.state == self.DANCE_WATER_SURVIVAL:
            self._draw_meteor(draw)
        
        # Draw disco ball
        if self.disco_party_active:
            self._draw_disco_ball(draw, c)
        
        # Draw speech bubble
        if self.speech_timer > 0:
            self.speech_timer -= 1
            if self.state == self.DANCE_WATER_SURVIVAL:
                draw_speech_bubble(self, draw, cx, ground_y - 300)
            else:
                draw_speech_bubble(self, draw, cx, ground_y - 200 if laying_down else ground_y - 250)
        
        # Draw particles
        for p in self.particles:
            alpha = int(255 * p['life'])
            if p['type'] == 'water' or p['type'] == 'water_drop':
                color = (50, 150, 255, alpha)
            elif p['type'] == 'music':
                color = (255, 200, 50, alpha)
            elif p['type'] == 'heart':
                color = (255, 100, 150, alpha)
            else:
                color = (255, 200, 200, alpha)
            draw.ellipse([int(p['x']-4), int(p['y']-4), int(p['x']+4), int(p['y']+4)], fill=color)
        
        self.current_image = ImageTk.PhotoImage(img)
        if self.sprite_id:
            self.canvas.delete(self.sprite_id)
        self.sprite_id = self.canvas.create_image(self.x, self.y - 80, image=self.current_image, anchor='center')
    
    def _draw_disco_effects(self, draw, c, cx, ground_y):
        """Draw disco party lighting effects"""
        # Disco floor tiles
        for tile in self.disco_floor_tiles:
            tile_alpha = 100 + int(50 * math.sin(tile['phase'] + self.disco_light_phase))
            tile_color = list(tile['color'])
            tile_color[3] = tile_alpha
            draw.rectangle([tile['x'], tile['y'], tile['x'] + tile['size'], tile['y'] + tile['size']], 
                         fill=tuple(tile_color), outline=None)
        
        # Red and blue strobe lights
        if self.disco_strobe_on:
            current_color = self.disco_colors[self.disco_color_index]
            
            # Left red/blue light beam
            for i in range(5):
                beam_alpha = 100 - i * 20
                beam_color = list(current_color)
                beam_color[3] = max(0, beam_alpha)
                draw.ellipse([50 - i * 30, 0, 150 + i * 30, 620], fill=tuple(beam_color), outline=None)
            
            # Right red/blue light beam
            for i in range(5):
                beam_alpha = 100 - i * 20
                beam_color2 = list(self.disco_colors[(self.disco_color_index + 1) % len(self.disco_colors)])
                beam_color2[3] = max(0, beam_alpha)
                draw.ellipse([330 - i * 30, 0, 430 + i * 30, 620], fill=tuple(beam_color2), outline=None)
        
        # Light rays from center
        for i in range(12):
            angle = i * (math.pi / 6) + self.disco_light_phase
            ray_length = 200 + math.sin(self.disco_light_phase * 2 + i) * 50
            ray_color = self.disco_colors[i % len(self.disco_colors)]
            ray_color_list = list(ray_color)
            ray_color_list[3] = 50
            end_x = cx + int(ray_length * math.cos(angle))
            end_y = ground_y - 200 + int(ray_length * math.sin(angle))
            draw.line([cx, ground_y - 200, end_x, end_y], fill=tuple(ray_color_list), width=3)
    
    def _draw_disco_ball(self, draw, c):
        """Draw the disco ball"""
        # Ball body
        ball_size = 30
        draw.ellipse([self.disco_ball_x - ball_size, self.disco_ball_y - ball_size,
                     self.disco_ball_x + ball_size, self.disco_ball_y + ball_size],
                    fill=(200, 200, 200, 255), outline=(150, 150, 150, 255), width=2)
        
        # Mirror tiles on ball
        for i in range(8):
            angle = i * (math.pi / 4) + self.disco_ball_rotation * 0.05
            tile_x = self.disco_ball_x + int(ball_size * 0.7 * math.cos(angle))
            tile_y = self.disco_ball_y + int(ball_size * 0.7 * math.sin(angle))
            draw.ellipse([tile_x - 4, tile_y - 4, tile_x + 4, tile_y + 4],
                        fill=(255, 255, 255, 200), outline=(200, 200, 200, 255), width=1)
        
        # Light reflections from ball
        for i in range(16):
            angle = i * (math.pi / 8) + self.disco_ball_rotation * 0.03
            reflect_color = self.disco_colors[i % len(self.disco_colors)]
            reflect_color_list = list(reflect_color)
            reflect_color_list[3] = 80
            reflect_length = 40 + random.randint(-10, 10)
            end_x = self.disco_ball_x + int(reflect_length * math.cos(angle))
            end_y = self.disco_ball_y + int(reflect_length * math.sin(angle))
            draw.line([self.disco_ball_x, self.disco_ball_y, end_x, end_y],
                     fill=tuple(reflect_color_list), width=2)
        
        # String/rope
        draw.line([self.disco_ball_x, self.disco_ball_y - ball_size,
                  self.disco_ball_x, self.disco_ball_y - ball_size - 80],
                 fill=(255, 255, 255, 200), width=2)
    
    def _draw_water_level(self, draw, c):
        """Draw rising water"""
        for i in range(3):
            wave_offset = math.sin(self.dance_timer * 0.1 + i * 2) * 15
            water_y = self.water_level + wave_offset
            
            # Clamp water_y to valid range for PIL drawing
            water_y = max(0, min(water_y, 620))
            
            water_alpha = 150 - i * 30
            
            # Only draw if water_y is within the canvas bounds
            if water_y < 620:
                # Water body
                draw.rectangle([0, int(water_y), 480, 620], fill=(30, 100, 200, max(0, water_alpha)))
                
                # Wave lines
                for x in range(0, 480, 30):
                    wave_h = math.sin((x + self.dance_timer * 5) * 0.05 + i) * 8
                    wave_y_top = max(0, water_y - 20 + wave_h)
                    wave_y_bottom = min(620, water_y + 20 + wave_h)
                    if wave_y_top < wave_y_bottom:
                        draw.arc([x - 15, wave_y_top, x + 15, wave_y_bottom], 
                                0, 180, fill=(100, 180, 255, max(0, 100)), width=2)
    
    def _draw_meteor(self, draw):
        """Draw falling heart meteor"""
        if self.meteor_active:
            # Meteor trail
            for i in range(5):
                trail_y = self.meteor_y - i * 15
                alpha = 200 - i * 40
                size = 15 - i * 2
                draw.ellipse([self.meteor_x - size, trail_y - size, 
                             self.meteor_x + size, trail_y + size], 
                            fill=(255, 100, 50, alpha))
            
            # Heart meteor
            self._draw_heart(draw, self.meteor_x, self.meteor_y, 20, (255, 50, 50, 255))
    
    def _draw_heart(self, draw, cx, cy, size, color):
        """Draw a heart shape"""
        # Left lobe
        draw.ellipse([cx - size, cy - size//2, cx, cy + size//2], fill=color)
        # Right lobe
        draw.ellipse([cx, cy - size//2, cx + size, cy + size//2], fill=color)
        # Bottom point
        draw.polygon([(cx - size, cy), (cx + size, cy), (cx, cy + size)], fill=color)
    
    def _draw_death_effects(self, draw, cx, ground_y):
        """Draw death cross eyes and effects"""
        # Cross eyes effect
        eye_y = ground_y - 250
        for es in [-1, 1]:
            ex = cx - 20 * es
            # Cross mark
            draw.line([ex - 8, eye_y - 8, ex + 8, eye_y + 8], fill=(255, 0, 0, 255), width=3)
            draw.line([ex + 8, eye_y - 8, ex - 8, eye_y + 8], fill=(255, 0, 0, 255), width=3)
        
        # Ghost leaving body
        ghost_y = ground_y - 200 - self.death_timer * 2
        if self.death_timer < 60:
            ghost_alpha = max(0, 200 - self.death_timer * 3)
            draw.ellipse([cx - 20, ghost_y - 10, cx + 20, ghost_y + 20], 
                        fill=(255, 255, 255, ghost_alpha), outline=(200, 200, 200, ghost_alpha))
            draw.ellipse([cx - 10, ghost_y + 5, cx + 10, ghost_y + 25], 
                        fill=(255, 255, 255, ghost_alpha))
    
    # ============================================
    # MOVEMENT & ANIMATION
    # ============================================
    
    def update_movement(self):
        """Update character movement"""
        if self.dance_override:
            if self.state == self.DANCE_WATER_SURVIVAL:
                # Auto-move during water survival
                self.x += math.sin(self.dance_timer * 0.05) * 2
                self.x = max(80, min(self.x, self.screen_width - 80))
            elif self.disco_party_active:
                # Crazy dance movement during disco party
                self.x += math.sin(self.dance_timer * 0.15) * 8
                self.y += math.cos(self.dance_timer * 0.12) * 5
                self.x = max(100, min(self.x, self.screen_width - 100))
                self.y = max(200, min(self.y, self.screen_height - 300))
            return
        
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        if abs(dx) > 5 or abs(dy) > 5:
            speed = self.config.get("run_speed", 6) if abs(dx) > 40 else self.config.get("walk_speed", 3)
            self.x += max(-speed, min(speed, dx * 0.1))
            self.y += max(-speed, min(speed, dy * 0.1))
            self.state = self.DANCE_RUNNING if abs(dx) > 40 else self.DANCE_WALKING
        elif self.state in [self.DANCE_WALKING, self.DANCE_RUNNING]:
            self.state = self.DANCE_IDLE
        
        self.x = max(80, min(self.x, self.screen_width - 80))
        self.y = max(80, min(self.y, self.screen_height - 250))
        
        if self.config.get("auto_walk", True) and self.state == self.DANCE_IDLE:
            self.wander_timer += 1
            if self.wander_timer > self.wander_interval * 60:
                self.wander_timer = 0
                self.wander_interval = random.randint(4, 10)
                new_x = random.randint(150, self.screen_width - 150)
                new_y = random.randint(100, self.screen_height - 350)
                self.move_to(new_x, new_y)
    
    def animate(self):
        """Main animation frame"""
        self.frame += 1
        self.update_drawing()
        self.update_movement()
        return self.frame