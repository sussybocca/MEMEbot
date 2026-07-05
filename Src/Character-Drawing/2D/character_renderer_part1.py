"""
MEMEBOT 2D Character Renderer - Main Module Part 1
Character state, particles, config, disco party, water survival, idle animations
Part 1 of 2 - Lines 1-500
"""

import math
import random
from typing import List, Optional
from PIL import Image, ImageDraw, ImageTk
from io import BytesIO
import base64
import sys
import os
import time as time_module

_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

try:
    from character_drawing_part2 import draw_standing_character, draw_laying_character
    from character_renderer_accessories_part1 import draw_speech_bubble
except ImportError as e:
    print(f"Failed to import drawing modules from {_current_dir}: {e}")
    raise


class CharacterRenderer:
    """Renders the MEMEBOT character with full V4.0 body customization support"""
    
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
    
    STATE_TO_ANIM_KEY = {
        "idle": "idle", "walking": "walking", "running": "running",
        "waving": "waving", "bouncing": "bouncing", "dancing": "dancing",
        "meme": "dancing", "video_dancing": "dancing",
        "worm": "dancing", "moonwalk": "dancing", "thriller": "dancing",
        "robot": "dancing", "disco": "dancing", "disco_party": "dancing",
    }
    
    def __init__(self, canvas, config, skin_loader):
        self.canvas = canvas
        self.config = config
        self.skin_loader = skin_loader
        self.root = None
        self.x = config.get("start_x", 500)
        self.y = config.get("start_y", 500)
        self.target_x = self.x
        self.target_y = self.y
        self.state = self.DANCE_IDLE
        self.idle_type = self.IDLE_NORMAL
        self.frame = 0
        self.walk_cycle = 0
        self.emotion = "happy"
        self.is_talking = False
        self.facing_right = True
        self.sprite_id = None
        self.current_image = None
        self.blink_timer = random.randint(30, 70)
        self.is_blinking = False
        self.blink_frame = 0
        self.nose_twitch = 0
        self.screen_width = canvas.winfo_screenwidth()
        self.screen_height = canvas.winfo_screenheight()
        self.particles = []
        self.speech_text = ""
        self.speech_timer = 0
        self.dance_timer = 0
        self.dance_override = False
        self.dance_start_x = self.x
        self.dance_start_y = self.y
        self.wander_timer = 0
        self.wander_interval = random.randint(4, 10)
        self.prev_leg_swing = 0
        self.prev_arm_swing = 0
        self.prev_body_bob = 0
        self.prev_extra_spin = 0
        self.prev_arm_raise = 0
        self.video_playing = False
        self.lip_sync_intensity = 0
        self.audio_envelope = None
        self.audio_start_time = 0
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
        self.idle_timer = 0
        self.idle_duration = 0
        self.current_idle_animation = 0
        self.extra_bounce = 0
        self.extra_twist = 0
        self.extra_flail = 0
        self.idle_sequence_phase = 0
        self.idle_sequence_timer = 0
        self.disco_party_active = False
        self.disco_party_timer = 0
        self.disco_party_duration = 600
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
        self.disco_party_cooldown = 1800
        self.disco_party_available = True
        self.last_disco_party_time = 0
        self.disco_music_path = r"D:\MODZ4\music\[FREE] Trap Type Beat - _HUSH_ _ Freestyle Beat 2026 _ Melodic Type Beat _ Rap Type Dark [jWhSBxHxjgs].mp4"
        self.custom_anim_frame = 0
        self.custom_anim_timer = 0
        self.custom_anim_speed = 8
        self.update_drawing()
    
    def add_particle(self, x, y, ptype, count=3):
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
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.06
            p['life'] -= 0.01
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def say(self, text: str):
        self.speech_text = text
        self.speech_timer = 120
        self.is_talking = True
    
    def move_to(self, x, y):
        self.target_x = max(50, min(x, self.screen_width - 50))
        self.target_y = max(50, min(y, self.screen_height - 250))
    
    def set_dance(self, dance_state: str):
        self.state = dance_state
        self.dance_timer = 0
        self.dance_override = True
        self.dance_start_x = self.x
        self.dance_start_y = self.y
        self.custom_anim_frame = 0
        self.custom_anim_timer = 0
        if dance_state == self.DANCE_WATER_SURVIVAL:
            self._init_water_survival()
    
    def _check_disco_party(self):
        current_time = time_module.time()
        if self.disco_party_available and (current_time - self.last_disco_party_time) >= self.disco_party_cooldown:
            self._start_disco_party()
    
    def _start_disco_party(self):
        self.disco_party_active = True
        self.disco_party_timer = 0
        self.disco_party_duration = 600
        self.disco_ball_x = self.x
        self.disco_ball_y = self.y - 200
        self.disco_ball_rotation = 0
        self.disco_strobe_on = True
        self.disco_strobe_timer = 0
        self.disco_light_phase = 0
        self.disco_color_index = 0
        self.disco_party_available = False
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
        self.state = self.DANCE_DISCO_PARTY
        self.idle_type = self.IDLE_DISCO_FEVER
        self.dance_timer = 0
        self.dance_override = True
        self.custom_anim_frame = 0
        self.custom_anim_timer = 0
        self.add_particle(self.x, self.y, "sparkle", 50)
        self.add_particle(self.x, self.y, "music", 30)
        self.say("DISCO PARTY TIME!!!")
        if self.root and hasattr(self.root, 'after'):
            self.last_disco_party_time = time_module.time()
    
    def _update_disco_party(self):
        if not self.disco_party_active:
            return
        self.disco_party_timer += 1
        self.disco_ball_rotation += 5
        self.disco_light_phase += 0.15
        self.disco_strobe_timer += 1
        if self.disco_strobe_timer > random.randint(3, 10):
            self.disco_strobe_on = not self.disco_strobe_on
            self.disco_strobe_timer = 0
            if self.disco_strobe_on:
                self.disco_color_index = (self.disco_color_index + 1) % len(self.disco_colors)
        self.disco_ball_x = self.x + math.sin(self.disco_light_phase * 2) * 50
        self.disco_ball_y = self.y - 200 + math.cos(self.disco_light_phase * 1.5) * 30
        for tile in self.disco_floor_tiles:
            tile['phase'] += 0.1
            tile['color'] = random.choice(self.disco_colors) if random.random() < 0.3 else tile['color']
        if random.random() < 0.8:
            px = random.randint(0, self.screen_width)
            py = random.randint(0, self.screen_height)
            self.add_particle(px, py, "sparkle", 3)
        if self.idle_type == self.IDLE_DISCO_FEVER:
            if self.disco_party_timer % 60 < 30:
                self.idle_type = self.IDLE_RAVE
            else:
                self.idle_type = self.IDLE_STROBE_DANCE
        if self.disco_party_timer >= self.disco_party_duration:
            self._end_disco_party()
    
    def _end_disco_party(self):
        self.disco_party_active = False
        self.state = self.DANCE_BOUNCING
        self.idle_type = self.IDLE_NORMAL
        self.dance_timer = 0
        self.dance_override = False
        self.disco_party_available = True
        self.custom_anim_frame = 0
        self.custom_anim_timer = 0
        self.add_particle(self.x, self.y, "sparkle", 30)
        self.say("That was CRAZY!")
    
    def _init_water_survival(self):
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
        self.x = self.screen_width // 2
        self.y = self.screen_height - 200
        self.add_particle(self.x, self.y, "water", 20)
    
    def _update_water_survival(self):
        if not self.is_dead:
            if self.water_rising:
                self.water_level -= self.water_speed
                if self.water_level < -50:
                    self.water_rising = False
            self.water_float_y = math.sin(self.dance_timer * 0.1) * 15
            if self.water_level < self.y:
                self.y -= 2.5
                self.survival_score += 1
            if self.meteor_active:
                self.meteor_y += 3
                meteor_dist = math.sqrt((self.meteor_x - self.x)**2 + (self.meteor_y - self.y)**2)
                if meteor_dist < 60:
                    self._kill_character()
                if self.meteor_y > self.screen_height:
                    self.meteor_x = random.randint(100, self.screen_width - 100)
                    self.meteor_y = -100
                    self.survival_score += 50
            if random.random() < 0.3:
                water_x = self.x + random.randint(-40, 40)
                water_y = self.y + 60
                self.add_particle(water_x, water_y, "water_drop", 2)
            if self.y < self.water_level + 30:
                self._kill_character()
    
    def _kill_character(self):
        self.is_dead = True
        self.death_timer = 0
        self.emotion = "dead"
        self.add_particle(self.x, self.y, "sparkle", 30)
        self.add_particle(self.x, self.y, "water", 20)
        self.say(f"Score: {self.survival_score}!")
    
    def _respawn_character(self):
        self.is_dead = False
        self.emotion = "happy"
        self.state = self.DANCE_BOUNCING
        self.dance_timer = 0
        self.dance_override = False
        self.custom_anim_frame = 0
        self.custom_anim_timer = 0
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        self.add_particle(self.x, self.y, "sparkle", 20)
        self.say("I'm back!")
    
    def _cycle_idle_animation(self):
        if self.disco_party_active:
            return
        self.idle_timer += 1
        if self.idle_timer > self.idle_duration:
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
    
    def _get_body_config(self):
        skin = self.skin_loader.get_current_skin()
        return {
            "scale": skin.get("body_scale", {"height": 1.0, "width": 1.0, "head_size": 1.0, "limb_length": 1.0}),
            "shape": skin.get("body_shape", {"type": "default", "torso_width": 1.0, "torso_height": 1.0, "belly_size": 0.0, "shoulder_width": 1.0, "hip_width": 1.0, "custom_points": []}),
            "limbs": skin.get("limbs", {"arm_style": "default", "arm_length": 1.0, "arm_width": 1.0, "leg_style": "default", "leg_length": 1.0, "leg_width": 1.0, "hand_style": "default", "foot_style": "default"}),
            "head_cfg": skin.get("head", {"shape": "round", "size": 1.0, "face_position": 0.0, "ear_style": "default", "ear_size": 1.0}),
            "hair_cfg": skin.get("hair", {"style": "default", "length": 1.0, "volume": 1.0, "bangs": True, "custom_points": []}),
            "outfit_cfg": skin.get("outfit", {"type": "default", "top_color": [100, 180, 255, 255], "bottom_color": [50, 130, 200, 255], "custom_shapes": []}),
            "colors": skin.get("colors", {}),
            "clothing": skin.get("clothing", {}),
            "accessories": skin.get("accessories", {}),
            "sprite_data": skin.get("sprite_data", {}),
            "animation_frames": skin.get("animation_frames", {}),
            "name": skin.get("name", "Default"),
            "version": skin.get("version", "4.0"),
            "author": skin.get("author", "MEMEBOT User"),
            "description": skin.get("description", ""),
        }
    
    def _get_skin_colors(self):
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