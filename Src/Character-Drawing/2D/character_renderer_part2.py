"""
MEMEBOT 2D Character Renderer - Main Module Part 2
Idle bonus params, MSK sprite drawing, main update_drawing, effects, movement, animate
Part 2 of 2
"""

import math
import random
from PIL import Image, ImageDraw, ImageTk
from io import BytesIO
import base64
import importlib
import sys
import os

_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)


def _extend_character_renderer(cls):
    
    def _get_idle_bonus_params(self):
        bonus = {'extra_bounce': 0, 'extra_twist': 0, 'extra_flail': 0, 'arm_specific': 0, 'leg_specific': 0, 'head_specific': 0}
        t = self.idle_timer * 0.3
        if self.idle_type == self.IDLE_SHUFFLE:
            bonus['extra_bounce'] = math.sin(t * 2) * 15; bonus['extra_twist'] = math.sin(t) * 10
        elif self.idle_type == self.IDLE_HEADBANG:
            bonus['head_specific'] = math.sin(t * 3) * 20; bonus['extra_bounce'] = math.sin(t * 2) * 5
        elif self.idle_type == self.IDLE_DAB:
            if self.idle_timer < 40: bonus['arm_specific'] = min(self.idle_timer * 2, 60); bonus['head_specific'] = -self.idle_timer * 0.5
            else: bonus['arm_specific'] = 60; bonus['head_specific'] = -20
        elif self.idle_type == self.IDLE_FLOSS:
            bonus['extra_twist'] = math.sin(t * 3) * 20; bonus['arm_specific'] = math.sin(t * 4) * 30
        elif self.idle_type == self.IDLE_WAVE_ARMS:
            bonus['arm_specific'] = math.sin(t * 2) * 40; bonus['extra_flail'] = math.cos(t * 1.5) * 15
        elif self.idle_type == self.IDLE_CHICKEN:
            bonus['arm_specific'] = math.sin(t * 5) * 25; bonus['extra_bounce'] = math.sin(t * 3) * 10
        elif self.idle_type == self.IDLE_POGO:
            bonus['extra_bounce'] = abs(math.sin(t * 3)) * 30
        elif self.idle_type == self.IDLE_SNAKE:
            bonus['extra_twist'] = math.sin(t * 1.5) * 25; bonus['head_specific'] = math.sin(t * 2) * 15
        elif self.idle_type == self.IDLE_KICK:
            if self.idle_timer % 40 < 20: bonus['leg_specific'] = math.sin(t * 4) * 40
            else: bonus['leg_specific'] = 0
        elif self.idle_type == self.IDLE_ARM_WAVE:
            bonus['arm_specific'] = math.sin(t * 2.5) * 45; bonus['extra_twist'] = math.cos(t * 1.8) * 12
        elif self.idle_type == self.IDLE_TWERK:
            bonus['extra_bounce'] = math.sin(t * 5) * 20; bonus['extra_twist'] = math.sin(t * 3) * 10; bonus['leg_specific'] = abs(math.sin(t * 5)) * 25
        elif self.idle_type == self.IDLE_ROLL:
            bonus['extra_twist'] = t * 3 % 360; bonus['extra_flail'] = 15; bonus['head_specific'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_COSSACK:
            if self.idle_timer % 60 < 30: bonus['leg_specific'] = 35; bonus['extra_bounce'] = 10
            else: bonus['leg_specific'] = 0; bonus['extra_bounce'] = 0
        elif self.idle_type == self.IDLE_JUMPING_JACK:
            bonus['arm_specific'] = math.sin(t * 3) * 40; bonus['leg_specific'] = abs(math.sin(t * 3)) * 20; bonus['extra_bounce'] = abs(math.sin(t * 3)) * 15
        elif self.idle_type == self.IDLE_GRIDDY:
            bonus['extra_bounce'] = math.sin(t * 4) * 12; bonus['arm_specific'] = math.sin(t * 2) * 25; bonus['leg_specific'] = math.sin(t * 3) * 15
        elif self.idle_type == self.IDLE_ORANGE_JUSTICE:
            bonus['arm_specific'] = math.sin(t * 2) * 50; bonus['extra_twist'] = math.sin(t * 3) * 15; bonus['leg_specific'] = abs(math.sin(t * 4)) * 20
        elif self.idle_type == self.IDLE_TAKE_THE_L:
            bonus['arm_specific'] = 50; bonus['head_specific'] = 15; bonus['extra_bounce'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_ELECTRO_SHUFFLE:
            bonus['extra_twist'] = math.sin(t * 4) * 18; bonus['arm_specific'] = math.sin(t * 5) * 30; bonus['leg_specific'] = math.sin(t * 3) * 20
        elif self.idle_type == self.IDLE_BEST_MATES:
            bonus['arm_specific'] = math.sin(t * 2) * 35; bonus['extra_bounce'] = math.sin(t * 3) * 12
        elif self.idle_type == self.IDLE_FRESH:
            bonus['extra_twist'] = math.sin(t * 2) * 20; bonus['arm_specific'] = math.cos(t * 1.5) * 25; bonus['head_specific'] = math.sin(t * 2) * 8
        elif self.idle_type == self.IDLE_HYPE:
            bonus['extra_bounce'] = abs(math.sin(t * 4)) * 25; bonus['arm_specific'] = math.sin(t * 5) * 30; bonus['head_specific'] = math.sin(t * 6) * 10
        elif self.idle_type == self.IDLE_LAUGH:
            bonus['extra_bounce'] = math.sin(t * 3) * 10; bonus['head_specific'] = math.sin(t * 4) * 15; bonus['arm_specific'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_CHEER:
            bonus['arm_specific'] = abs(math.sin(t * 3)) * 50; bonus['extra_bounce'] = abs(math.sin(t * 3)) * 15
        elif self.idle_type == self.IDLE_FACE_PALM:
            if self.idle_timer % 80 < 40: bonus['arm_specific'] = 40; bonus['head_specific'] = -25
            else: bonus['arm_specific'] = 0; bonus['head_specific'] = 0
        elif self.idle_type == self.IDLE_SHOULDER_BRUSH:
            bonus['arm_specific'] = math.sin(t * 2) * 30; bonus['extra_twist'] = math.cos(t * 1.5) * 8
        elif self.idle_type == self.IDLE_MIC_DROP:
            if self.idle_timer < 20: bonus['arm_specific'] = self.idle_timer * 2
            elif self.idle_timer < 40: bonus['arm_specific'] = 60
            else: bonus['arm_specific'] = 0; bonus['extra_bounce'] = 5
        elif self.idle_type == self.IDLE_AIR_GUITAR:
            bonus['arm_specific'] = math.sin(t * 4) * 35; bonus['extra_bounce'] = math.sin(t * 2) * 10; bonus['head_specific'] = math.sin(t * 3) * 15
        elif self.idle_type == self.IDLE_DRUM:
            bonus['arm_specific'] = abs(math.sin(t * 5)) * 40; bonus['extra_bounce'] = math.sin(t * 2) * 8
        elif self.idle_type == self.IDLE_PIANO:
            bonus['arm_specific'] = math.sin(t * 3) * 25; bonus['extra_twist'] = math.sin(t * 1.5) * 10
        elif self.idle_type == self.IDLE_CONDUCTOR:
            bonus['arm_specific'] = math.sin(t * 2) * 45; bonus['extra_twist'] = math.cos(t * 1.2) * 10
        elif self.idle_type == self.IDLE_ZOMBIE:
            bonus['arm_specific'] = math.sin(t * 1.5) * 20; bonus['leg_specific'] = math.sin(t * 1.2) * 15; bonus['extra_flail'] = 10; bonus['head_specific'] = math.sin(t * 0.8) * 8
        elif self.idle_type == self.IDLE_MIME:
            bonus['arm_specific'] = math.sin(t * 1.5) * 30; bonus['extra_twist'] = math.sin(t * 0.8) * 5
        elif self.idle_type == self.IDLE_MARTIAL_ARTS:
            if self.idle_timer % 50 < 25: bonus['arm_specific'] = 50; bonus['leg_specific'] = 40
            else: bonus['arm_specific'] = 10; bonus['leg_specific'] = 5
        elif self.idle_type == self.IDLE_BALLET:
            bonus['arm_specific'] = math.sin(t * 2) * 25; bonus['leg_specific'] = math.sin(t * 3) * 15; bonus['extra_bounce'] = math.sin(t * 4) * 5
        elif self.idle_type == self.IDLE_TAP_DANCE:
            bonus['leg_specific'] = abs(math.sin(t * 6)) * 20; bonus['arm_specific'] = math.sin(t * 3) * 10
        elif self.idle_type == self.IDLE_SALSA:
            bonus['extra_twist'] = math.sin(t * 3) * 20; bonus['arm_specific'] = math.cos(t * 2) * 25; bonus['leg_specific'] = math.sin(t * 4) * 15
        elif self.idle_type == self.IDLE_SWING:
            bonus['extra_twist'] = math.sin(t * 2) * 25; bonus['arm_specific'] = math.sin(t * 3) * 30; bonus['extra_bounce'] = math.sin(t * 2) * 10
        elif self.idle_type == self.IDLE_TWIST:
            bonus['extra_twist'] = math.sin(t * 3) * 30; bonus['arm_specific'] = math.sin(t * 2) * 15; bonus['leg_specific'] = math.sin(t * 2.5) * 10
        elif self.idle_type == self.IDLE_WORM_DANCE:
            bonus['extra_bounce'] = math.sin(t * 2) * 20; bonus['extra_twist'] = math.sin(t * 1.5) * 15; bonus['arm_specific'] = math.sin(t * 3) * 25
        elif self.idle_type == self.IDLE_CRAWL:
            bonus['extra_flail'] = 20; bonus['leg_specific'] = math.sin(t * 2) * 10; bonus['arm_specific'] = math.sin(t * 2.5) * 10
        elif self.idle_type == self.IDLE_FISH_OUT_OF_WATER:
            bonus['extra_bounce'] = abs(math.sin(t * 3)) * 25; bonus['extra_flail'] = 20; bonus['arm_specific'] = math.sin(t * 4) * 30; bonus['leg_specific'] = math.sin(t * 4) * 25
        elif self.idle_type == self.IDLE_DISCO_FEVER:
            bonus['extra_bounce'] = abs(math.sin(t * 6)) * 30; bonus['extra_twist'] = math.sin(t * 5) * 25; bonus['arm_specific'] = math.sin(t * 7) * 40; bonus['leg_specific'] = math.cos(t * 6) * 30; bonus['head_specific'] = math.sin(t * 8) * 15
        elif self.idle_type == self.IDLE_RAVE:
            bonus['extra_bounce'] = abs(math.sin(t * 8)) * 35; bonus['arm_specific'] = math.sin(t * 9) * 50; bonus['extra_twist'] = t * 5 % 360; bonus['head_specific'] = math.sin(t * 10) * 20
        elif self.idle_type == self.IDLE_STROBE_DANCE:
            bonus['extra_bounce'] = abs(math.sin(t * 4)) * 40; bonus['extra_twist'] = math.sin(t * 3) * 35; bonus['arm_specific'] = math.sin(t * 6) * 45; bonus['leg_specific'] = math.cos(t * 5) * 35
        return bonus
    
    def _get_dance_params(self):
        self.dance_timer += 1
        DanceEngine = importlib.import_module('Animations.DanceMoves.dance_engine').DanceEngine
        return DanceEngine.get_params(self)
    
    def _draw_msk_sprites(self, draw, cfg):
        sprite_data = cfg.get("sprite_data", None)
        if not sprite_data: return None
        layers = sprite_data.get("layers", {})
        if not layers: return None
        layer_order = ["tail", "wings", "legs", "body", "arms", "outfit", "accessories", "head", "hair", "eyes", "mouth", "hat", "glasses"]
        composite = Image.new('RGBA', (480, 620), (0, 0, 0, 0))
        for layer_name in layer_order:
            if layer_name in layers:
                try:
                    layer_data = base64.b64decode(layers[layer_name])
                    layer_img = Image.open(BytesIO(layer_data)).convert('RGBA')
                    composite = Image.alpha_composite(composite, layer_img)
                except Exception: pass
        return composite
    
    def _get_custom_animation_frame(self, cfg):
        animation_frames = cfg.get("animation_frames", {})
        if not animation_frames: return None
        anim_key = self.STATE_TO_ANIM_KEY.get(self.state, self.state)
        if anim_key not in animation_frames or not animation_frames[anim_key]:
            if self.state in [self.DANCE_WALKING, self.DANCE_RUNNING]:
                anim_key = "walking" if "walking" in animation_frames else "running"
            if anim_key not in animation_frames or not animation_frames[anim_key]:
                anim_key = "idle"
        if anim_key not in animation_frames: return None
        frames = animation_frames[anim_key]
        if not frames or len(frames) < 1: return None
        self.custom_anim_timer += 1
        if self.custom_anim_timer >= self.custom_anim_speed:
            self.custom_anim_timer = 0
            self.custom_anim_frame = (self.custom_anim_frame + 1) % len(frames)
        frame_idx = min(self.custom_anim_frame, len(frames) - 1)
        frame_data = frames[frame_idx]
        if not frame_data: return None
        layer_order = ["tail", "wings", "legs", "body", "arms", "outfit", "accessories", "head", "hair", "eyes", "mouth", "hat", "glasses"]
        composite = Image.new('RGBA', (480, 620), (0, 0, 0, 0))
        for layer_name in layer_order:
            if layer_name in frame_data:
                try:
                    layer_b64 = frame_data[layer_name]
                    layer_bytes = base64.b64decode(layer_b64)
                    layer_img = Image.open(BytesIO(layer_bytes)).convert('RGBA')
                    composite = Image.alpha_composite(composite, layer_img)
                except Exception: pass
        return composite
    
    def _draw_disco_effects(self, draw, c, cx, ground_y):
        for tile in self.disco_floor_tiles:
            tile_alpha = 100 + int(50 * math.sin(tile['phase'] + self.disco_light_phase))
            tile_color = list(tile['color']); tile_color[3] = tile_alpha
            draw.rectangle([tile['x'], tile['y'], tile['x'] + tile['size'], tile['y'] + tile['size']], fill=tuple(tile_color), outline=None)
        if self.disco_strobe_on:
            current_color = self.disco_colors[self.disco_color_index]
            for i in range(5):
                beam_alpha = 100 - i * 20
                beam_color = list(current_color); beam_color[3] = max(0, beam_alpha)
                draw.ellipse([50 - i * 30, 0, 150 + i * 30, 620], fill=tuple(beam_color), outline=None)
            for i in range(5):
                beam_alpha = 100 - i * 20
                beam_color2 = list(self.disco_colors[(self.disco_color_index + 1) % len(self.disco_colors)])
                beam_color2[3] = max(0, beam_alpha)
                draw.ellipse([330 - i * 30, 0, 430 + i * 30, 620], fill=tuple(beam_color2), outline=None)
        for i in range(12):
            angle = i * (math.pi / 6) + self.disco_light_phase
            ray_length = 200 + math.sin(self.disco_light_phase * 2 + i) * 50
            ray_color = self.disco_colors[i % len(self.disco_colors)]
            ray_color_list = list(ray_color); ray_color_list[3] = 50
            end_x = cx + int(ray_length * math.cos(angle))
            end_y = ground_y - 200 + int(ray_length * math.sin(angle))
            draw.line([cx, ground_y - 200, end_x, end_y], fill=tuple(ray_color_list), width=3)
    
    def _draw_disco_ball(self, draw, c):
        ball_size = 30
        draw.ellipse([self.disco_ball_x - ball_size, self.disco_ball_y - ball_size, self.disco_ball_x + ball_size, self.disco_ball_y + ball_size], fill=(200, 200, 200, 255), outline=(150, 150, 150, 255), width=2)
        for i in range(8):
            angle = i * (math.pi / 4) + self.disco_ball_rotation * 0.05
            tile_x = self.disco_ball_x + int(ball_size * 0.7 * math.cos(angle))
            tile_y = self.disco_ball_y + int(ball_size * 0.7 * math.sin(angle))
            draw.ellipse([tile_x - 4, tile_y - 4, tile_x + 4, tile_y + 4], fill=(255, 255, 255, 200), outline=(200, 200, 200, 255), width=1)
        for i in range(16):
            angle = i * (math.pi / 8) + self.disco_ball_rotation * 0.03
            reflect_color = self.disco_colors[i % len(self.disco_colors)]
            reflect_color_list = list(reflect_color); reflect_color_list[3] = 80
            reflect_length = 40 + random.randint(-10, 10)
            end_x = self.disco_ball_x + int(reflect_length * math.cos(angle))
            end_y = self.disco_ball_y + int(reflect_length * math.sin(angle))
            draw.line([self.disco_ball_x, self.disco_ball_y, end_x, end_y], fill=tuple(reflect_color_list), width=2)
        draw.line([self.disco_ball_x, self.disco_ball_y - ball_size, self.disco_ball_x, self.disco_ball_y - ball_size - 80], fill=(255, 255, 255, 200), width=2)
    
    def _draw_water_level(self, draw, c):
        for i in range(3):
            wave_offset = math.sin(self.dance_timer * 0.1 + i * 2) * 15
            water_y = max(0, min(self.water_level + wave_offset, 620))
            water_alpha = 150 - i * 30
            if water_y < 620:
                draw.rectangle([0, int(water_y), 480, 620], fill=(30, 100, 200, max(0, water_alpha)))
                for x in range(0, 480, 30):
                    wave_h = math.sin((x + self.dance_timer * 5) * 0.05 + i) * 8
                    wave_y_top = max(0, water_y - 20 + wave_h)
                    wave_y_bottom = min(620, water_y + 20 + wave_h)
                    if wave_y_top < wave_y_bottom:
                        draw.arc([x - 15, wave_y_top, x + 15, wave_y_bottom], 0, 180, fill=(100, 180, 255, max(0, 100)), width=2)
    
    def _draw_meteor(self, draw):
        if self.meteor_active:
            for i in range(5):
                trail_y = self.meteor_y - i * 15
                alpha = 200 - i * 40
                size = 15 - i * 2
                draw.ellipse([self.meteor_x - size, trail_y - size, self.meteor_x + size, trail_y + size], fill=(255, 100, 50, alpha))
            self._draw_heart(draw, self.meteor_x, self.meteor_y, 20, (255, 50, 50, 255))
    
    def _draw_heart(self, draw, cx, cy, size, color):
        draw.ellipse([cx - size, cy - size//2, cx, cy + size//2], fill=color)
        draw.ellipse([cx, cy - size//2, cx + size, cy + size//2], fill=color)
        draw.polygon([(cx - size, cy), (cx + size, cy), (cx, cy + size)], fill=color)
    
    def _draw_death_effects(self, draw, cx, ground_y):
        eye_y = ground_y - 250
        for es in [-1, 1]:
            ex = cx - 20 * es
            draw.line([ex - 8, eye_y - 8, ex + 8, eye_y + 8], fill=(255, 0, 0, 255), width=3)
            draw.line([ex + 8, eye_y - 8, ex - 8, eye_y + 8], fill=(255, 0, 0, 255), width=3)
        ghost_y = ground_y - 200 - self.death_timer * 2
        if self.death_timer < 60:
            ghost_alpha = max(0, 200 - self.death_timer * 3)
            draw.ellipse([cx - 20, ghost_y - 10, cx + 20, ghost_y + 20], fill=(255, 255, 255, ghost_alpha), outline=(200, 200, 200, ghost_alpha))
            draw.ellipse([cx - 10, ghost_y + 5, cx + 10, ghost_y + 25], fill=(255, 255, 255, ghost_alpha))
    
    def update_drawing(self):
        img = Image.new('RGBA', (480, 620), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        self.update_particles()
        self._check_disco_party()
        if self.disco_party_active: self._update_disco_party()
        if self.state == self.DANCE_WATER_SURVIVAL: self._update_water_survival()
        if self.is_dead:
            self.death_timer += 1
            if self.death_timer > 90: self._respawn_character()
        cfg = self._get_body_config()
        c = self._get_skin_colors()
        height_mult = cfg["scale"].get("height", 1.0)
        width_mult = cfg["scale"].get("width", 1.0)
        cx, cy = 240, 300
        ground_y = 530
        self.blink_timer -= 1
        if self.blink_timer <= 0:
            self.is_blinking = True; self.blink_timer = random.randint(50, 120)
        if self.is_blinking:
            self.blink_frame += 1
            if self.blink_frame > 6: self.is_blinking = False; self.blink_frame = 0
        self.nose_twitch = (self.nose_twitch + 0.08) % (2 * math.pi)
        leg_swing, arm_swing, body_bob, extra_spin, arm_raise, head_bob, body_squash, laying_down = self._get_dance_params()
        if self.state == self.DANCE_WATER_SURVIVAL: body_bob += self.water_float_y
        self._cycle_idle_animation()
        idle_bonus = self._get_idle_bonus_params()
        if self.disco_party_active: self._draw_disco_effects(draw, c, cx, ground_y)
        shadow_w = int((80 if laying_down else 50) * width_mult)
        if not self.state == self.DANCE_WATER_SURVIVAL:
            draw.ellipse([cx - shadow_w, ground_y - 5, cx + shadow_w, ground_y + 15], fill=(0, 0, 0, 30))
        if self.state == self.DANCE_WATER_SURVIVAL: self._draw_water_level(draw, c)
        custom_frame = self._get_custom_animation_frame(cfg)
        if custom_frame is not None and not self.state == self.DANCE_WATER_SURVIVAL:
            img.paste(custom_frame, (0, 0), custom_frame)
        else:
            sprite_composite = self._draw_msk_sprites(draw, cfg)
            if sprite_composite is not None and not self.state == self.DANCE_WATER_SURVIVAL:
                img.paste(sprite_composite, (0, 0), sprite_composite)
            else:
                if laying_down:
                    from character_drawing_part2 import draw_laying_character
                    draw_laying_character(self, draw, c, cfg, cx, ground_y, body_bob)
                else:
                    from character_drawing_part2 import draw_standing_character
                    draw_standing_character(self, draw, c, cfg, cx, ground_y, leg_swing, arm_swing, body_bob, extra_spin, arm_raise, head_bob, idle_bonus)
        if self.is_dead: self._draw_death_effects(draw, cx, ground_y)
        if self.meteor_active and self.state == self.DANCE_WATER_SURVIVAL: self._draw_meteor(draw)
        if self.disco_party_active: self._draw_disco_ball(draw, c)
        if self.speech_timer > 0:
            self.speech_timer -= 1
            from character_renderer_accessories_part1 import draw_speech_bubble
            if self.state == self.DANCE_WATER_SURVIVAL:
                draw_speech_bubble(self, draw, cx, ground_y - 300)
            else:
                draw_speech_bubble(self, draw, cx, ground_y - 200 if laying_down else ground_y - 250)
        for p in self.particles:
            alpha = int(255 * p['life'])
            if p['type'] == 'water' or p['type'] == 'water_drop': color = (50, 150, 255, alpha)
            elif p['type'] == 'music': color = (255, 200, 50, alpha)
            elif p['type'] == 'heart': color = (255, 100, 150, alpha)
            else: color = (255, 200, 200, alpha)
            draw.ellipse([int(p['x']-4), int(p['y']-4), int(p['x']+4), int(p['y']+4)], fill=color)
        self.current_image = ImageTk.PhotoImage(img)
        if self.sprite_id: self.canvas.delete(self.sprite_id)
        self.sprite_id = self.canvas.create_image(self.x, self.y - 80, image=self.current_image, anchor='center')
    
    def update_movement(self):
        if self.dance_override:
            if self.state == self.DANCE_WATER_SURVIVAL:
                self.x += math.sin(self.dance_timer * 0.05) * 2
                self.x = max(80, min(self.x, self.screen_width - 80))
            elif self.disco_party_active:
                self.x += math.sin(self.dance_timer * 0.15) * 8
                self.y += math.cos(self.dance_timer * 0.12) * 5
                self.x = max(100, min(self.x, self.screen_width - 100))
                self.y = max(200, min(self.y, self.screen_height - 300))
            return
        dx = self.target_x - self.x; dy = self.target_y - self.y
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
                self.wander_timer = 0; self.wander_interval = random.randint(4, 10)
                new_x = random.randint(150, self.screen_width - 150)
                new_y = random.randint(100, self.screen_height - 350)
                self.move_to(new_x, new_y)
    
    def animate(self):
        self.frame += 1
        self.update_drawing()
        self.update_movement()
        return self.frame
    
    cls._get_idle_bonus_params = _get_idle_bonus_params
    cls._get_dance_params = _get_dance_params
    cls._draw_msk_sprites = _draw_msk_sprites
    cls._get_custom_animation_frame = _get_custom_animation_frame
    cls._draw_disco_effects = _draw_disco_effects
    cls._draw_disco_ball = _draw_disco_ball
    cls._draw_water_level = _draw_water_level
    cls._draw_meteor = _draw_meteor
    cls._draw_heart = _draw_heart
    cls._draw_death_effects = _draw_death_effects
    cls.update_drawing = update_drawing
    cls.update_movement = update_movement
    cls.animate = animate