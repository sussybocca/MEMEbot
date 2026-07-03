"""
MEMEEngine Core Game Engine
Main game logic, physics, and state management
"""

import os
import json
import logging
import random
import math
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from SRC.Core.game_assets import (
    GameAsset, GameCharacter, GameMap, GameCollectible,
    GameEnemy, GameSound, GameMeme, GameUIElement
)
from SRC.Core.templates import GAME_TEMPLATES
from SRC.Core.particle_system import ParticleSystem
from SRC.Characters.presets import PRESET_CHARACTERS
from SRC.Maps.presets import PRESET_MAPS
from SRC.Engine.renderer import GameRenderer


class MEMEEngine:
    """No-code game creation engine for MEMEBOT minigames."""
    
    def __init__(self, config):
        self.config = config
        self.games_path = Path(config.BASE_PATH) / "MEMEEngine" / "games"
        self.assets_path = Path(config.BASE_PATH) / "MEMEEngine" / "assets"
        self.games_path.mkdir(parents=True, exist_ok=True)
        self.assets_path.mkdir(parents=True, exist_ok=True)
        
        self.current_game: Optional[Dict[str, Any]] = None
        self.current_game_path: Optional[Path] = None
        
        self.player: Optional[GameCharacter] = None
        self.characters: List[GameCharacter] = []
        self.collectibles: List[GameCollectible] = []
        self.enemies: List[GameEnemy] = []
        self.platforms: List[Dict] = []
        self.hazards: List[Dict] = []
        self.ui_elements: List[GameUIElement] = []
        self.game_map: Optional[GameMap] = None
        self.particles = ParticleSystem()
        self.renderer = GameRenderer(self)
        
        self.is_playing = False
        self.is_paused = False
        self.is_editing = True
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.time_elapsed = 0
        self.game_timer = 0
        
        self.keys_pressed = set()
        self.key_bindings = {}
        
        self.game_canvas = None
        self.game_window = None
        
        self.animation_thread = None
        self.frame_count = 0
        self.fps = 60
        self.frame_delay = 1000 // self.fps
        
        self.combo_count = 0
        self.combo_timer = 0
        self.max_combo = 0
        
        self.available_characters = PRESET_CHARACTERS.copy()
        self.available_maps = PRESET_MAPS.copy()
    
    def create_new_game(self, template: str = None) -> Dict[str, Any]:
        """Create a new game from template or blank"""
        game_id = f"game_{int(time.time())}"
        
        if template and template in GAME_TEMPLATES:
            tpl = GAME_TEMPLATES[template]
            game_data = {
                "id": game_id,
                "name": f"My {tpl['name']}",
                "description": tpl["description"],
                "template": template,
                "version": "1.0",
                "author": "MEMEBOT User",
                "controls": tpl["default_controls"].copy(),
                "mechanics": tpl["mechanics"].copy(),
                "win_condition": tpl["win_condition"],
                "target_score": tpl["target_score"],
                "time_limit": 0,
                "lives": 3,
                "difficulty": "normal",
                "map": tpl.get("default_map", "grassy_hills"),
                "player_character": "memebot",
                "characters": [],
                "collectibles": [],
                "enemies": [],
                "platforms": [],
                "hazards": [],
                "sounds": [],
                "memes": [],
                "events": [],
                "ui_elements": [
                    {"type": "text", "text": "Score: {score}", "x": 10, "y": 10, "binding": "score"},
                    {"type": "text", "text": "Health: {health}", "x": 10, "y": 40, "binding": "health"},
                    {"type": "text", "text": "Lives: {lives}", "x": 10, "y": 70, "binding": "lives"},
                ]
            }
        else:
            game_data = {
                "id": game_id,
                "name": "My MEME Game",
                "description": "A custom MEMEBOT minigame",
                "template": template or "custom",
                "version": "1.0",
                "author": "MEMEBOT User",
                "controls": {
                    "Left": "move_left",
                    "Right": "move_right",
                    "Up": "jump",
                    "Space": "action"
                },
                "mechanics": ["gravity", "jumping"],
                "win_condition": "reach_end",
                "target_score": 0,
                "time_limit": 0,
                "lives": 3,
                "difficulty": "normal",
                "map": "grassy_hills",
                "player_character": "memebot",
                "characters": [],
                "collectibles": [],
                "enemies": [],
                "platforms": [],
                "hazards": [],
                "sounds": [],
                "memes": [],
                "events": [],
                "ui_elements": [
                    {"type": "text", "text": "Score: {score}", "x": 10, "y": 10, "binding": "score"},
                    {"type": "text", "text": "Health: {health}", "x": 10, "y": 40, "binding": "health"},
                ]
            }
        
        self.current_game = game_data
        self.current_game_path = None
        return game_data
    
    def load_game_runtime(self):
        """Load game data into runtime objects"""
        if not self.current_game:
            return False
        
        game = self.current_game
        
        # Clear existing runtime data
        self.characters.clear()
        self.collectibles.clear()
        self.enemies.clear()
        self.platforms.clear()
        self.hazards.clear()
        self.ui_elements.clear()
        self.particles.clear()
        
        # Load map
        map_id = game.get("map", "grassy_hills")
        map_data = PRESET_MAPS.get(map_id, PRESET_MAPS["grassy_hills"])
        
        self.game_map = GameMap(
            name=map_data["name"],
            background_color=map_data["background_color"],
            width=map_data["default_size"][0],
            height=map_data["default_size"][1],
            ground_y=map_data["ground_y"],
            gravity=map_data.get("gravity", 0.8),
            spawn_point=map_data["spawn_point"],
            end_point=map_data["end_point"],
        )
        
        # Load platforms - user platforms first, then map defaults
        user_platforms = game.get("platforms", [])
        if user_platforms:
            for plat in user_platforms:
                self.platforms.append(dict(plat))
        else:
            for plat in map_data.get("platforms", []):
                self.platforms.append(dict(plat))
        
        # Load collectibles
        user_collectibles = game.get("collectibles", [])
        if user_collectibles:
            source_collectibles = user_collectibles
        else:
            source_collectibles = map_data.get("collectibles", [])
        
        points_map = {"coin": 10, "gem": 25, "star": 50, "meme_coin": 30}
        for coll in source_collectibles:
            coll_type = coll.get("type", "coin")
            collectible = GameCollectible(
                id=f"coll_{len(self.collectibles)}",
                name=coll_type,
                asset_type="collectible",
                x=coll["x"],
                y=coll["y"],
                width=24,
                height=24,
                points=points_map.get(coll_type, 10),
            )
            self.collectibles.append(collectible)
        
        # Load enemies - merge user + map enemies
        user_enemies = game.get("enemies", [])
        map_enemies = map_data.get("enemies", [])
        all_enemies = user_enemies + map_enemies
        
        for ene in all_enemies:
            enemy_type = ene.get("type", "slime")
            enemy = GameEnemy(
                id=f"enemy_{len(self.enemies)}",
                name=enemy_type,
                asset_type="enemy",
                x=ene["x"],
                y=ene["y"],
                width=36,
                height=36,
                health=50 if not ene.get("is_boss") else 200,
                max_health=50 if not ene.get("is_boss") else 200,
                speed=ene.get("speed", 2),
                damage=ene.get("damage", 10),
                patrol_distance=ene.get("patrol", 100),
                patrol_start_x=ene["x"],
                is_boss=ene.get("is_boss", False),
            )
            self.enemies.append(enemy)
        
        # Load user-placed characters
        for char in game.get("characters", []):
            char_type = char.get("type", "memebot")
            char_data = PRESET_CHARACTERS.get(char_type, PRESET_CHARACTERS["memebot"])
            game_char = GameCharacter(
                id=f"char_{len(self.characters)}",
                name=char_data["name"],
                asset_type="character",
                x=char["x"],
                y=char["y"],
                width=char_data["width"],
                height=char_data["height"],
                speed=char_data["speed"],
                jump_power=char_data["jump_power"],
                health=char_data["health"],
                max_health=char_data["health"],
                attack_power=char_data["attack_power"],
            )
            self.characters.append(game_char)
        
        # Load hazards - merge user + map hazards
        user_hazards = game.get("hazards", [])
        map_hazards = map_data.get("hazards", [])
        all_hazards = user_hazards + map_hazards
        
        for haz in all_hazards:
            self.hazards.append(dict(haz))
        
        # Create player
        char_id = game.get("player_character", "memebot")
        char_data = PRESET_CHARACTERS.get(char_id, PRESET_CHARACTERS["memebot"])
        
        spawn = self.game_map.spawn_point
        self.player = GameCharacter(
            id="player",
            name=char_data["name"],
            asset_type="character",
            x=spawn[0],
            y=spawn[1],
            width=char_data["width"],
            height=char_data["height"],
            speed=char_data["speed"],
            jump_power=char_data["jump_power"],
            health=char_data["health"],
            max_health=char_data["health"],
            attack_power=char_data["attack_power"],
            lives=game.get("lives", 3),
            is_player=True,
        )
        
        # Load UI elements
        for ui in game.get("ui_elements", []):
            element = GameUIElement(
                element_type=ui.get("type", "text"),
                text=ui.get("text", ""),
                x=ui.get("x", 10),
                y=ui.get("y", 10),
                font_size=ui.get("font_size", 20),
                color=ui.get("color", "#FFFFFF"),
                binding=ui.get("binding", ""),
            )
            self.ui_elements.append(element)
        
        # Setup key bindings
        self.key_bindings = {}
        controls = game.get("controls", {})
        for key, action in controls.items():
            self.key_bindings[key.lower()] = action
        
        # Reset game state
        self.is_playing = True
        self.is_paused = False
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.time_elapsed = 0
        self.game_timer = 0
        self.combo_count = 0
        self.combo_timer = 0
        
        return True
    
    def update(self):
        """Main game update loop"""
        if not self.is_playing or self.is_paused:
            return
        
        self.frame_count += 1
        self.game_timer += 1
        self.time_elapsed = self.game_timer // self.fps
        
        self._update_player()
        self._update_enemies()
        self._update_collectibles()
        self._update_platforms()
        self._update_hazards()
        self.particles.update()
        
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo_count = 0
        
        self._update_camera()
        self._check_game_state()
    
    def _update_player(self):
        """Update player physics and input"""
        if not self.player or self.player.health <= 0:
            return
        
        p = self.player
        move_speed = p.speed
        
        # Horizontal movement
        if "move_left" in self.key_bindings.values():
            if self.keys_pressed.intersection({k for k, v in self.key_bindings.items() if v == "move_left"}):
                p.velocity_x = -move_speed
                p.facing_right = False
                p.animation_state = "walk"
            elif self.keys_pressed.intersection({k for k, v in self.key_bindings.items() if v == "move_right"}):
                p.velocity_x = move_speed
                p.facing_right = True
                p.animation_state = "walk"
            else:
                p.velocity_x *= 0.8
                if abs(p.velocity_x) < 0.1:
                    p.velocity_x = 0
                    p.animation_state = "idle"
        
        # Jumping
        if "jump" in self.key_bindings.values():
            jump_keys = {k for k, v in self.key_bindings.items() if v == "jump"}
            if self.keys_pressed.intersection(jump_keys) and p.on_ground and not p.is_jumping:
                p.velocity_y = p.jump_power
                p.is_jumping = True
                p.on_ground = False
                p.animation_state = "jump"
                self.particles.emit(p.x + p.width//2, p.y + p.height, 5, "sparkle")
        
        # Gravity
        if not p.on_ground:
            p.velocity_y += self.game_map.gravity
        
        # Apply velocity
        p.x += p.velocity_x
        p.y += p.velocity_y
        
        # Bounds check
        p.x = max(0, min(p.x, self.game_map.width - p.width))
        
        # Ground collision
        p.on_ground = False
        if p.y + p.height >= self.game_map.ground_y:
            p.y = self.game_map.ground_y - p.height
            p.velocity_y = 0
            p.on_ground = True
            p.is_jumping = False
            if p.animation_state == "jump":
                p.animation_state = "idle"
        
        # Platform collision
        for plat in self.platforms:
            if (p.x + p.width > plat["x"] and 
                p.x < plat["x"] + plat["width"] and
                p.velocity_y >= 0 and
                p.y + p.height >= plat["y"] and 
                p.y + p.height - p.velocity_y <= plat["y"]):
                p.y = plat["y"] - p.height
                p.velocity_y = 0
                p.on_ground = True
                p.is_jumping = False
                if p.animation_state == "jump":
                    p.animation_state = "idle"
                break
        
        # Fall death
        if p.y > self.game_map.height + 100:
            self._kill_player()
        
        # Invincibility timer
        if p.invincible:
            p.invincible_timer -= 1
            if p.invincible_timer <= 0:
                p.invincible = False
        
        # Animation
        p.animation_timer += 1
        if p.animation_timer > 10:
            p.animation_timer = 0
            p.animation_frame = (p.animation_frame + 1) % 4
    
    def _update_enemies(self):
        """Update enemy AI and behavior"""
        for enemy in self.enemies[:]:
            if enemy.is_dead:
                enemy.death_timer -= 1
                if enemy.death_timer <= 0:
                    self.enemies.remove(enemy)
                continue
            
            # Patrol movement
            if enemy.moving_right:
                enemy.x += enemy.speed
                if enemy.x > enemy.patrol_start_x + enemy.patrol_distance:
                    enemy.moving_right = False
            else:
                enemy.x -= enemy.speed
                if enemy.x < enemy.patrol_start_x - enemy.patrol_distance:
                    enemy.moving_right = True
            
            # Boss AI
            if enemy.is_boss:
                enemy.attack_timer += 1
                if enemy.attack_timer >= enemy.attack_cooldown:
                    enemy.attack_timer = 0
                    if enemy.boss_phase == 0 and self.player:
                        if self.player.x > enemy.x:
                            enemy.moving_right = True
                            enemy.speed = 8
                        else:
                            enemy.moving_right = False
                            enemy.speed = 8
                        if enemy.health < enemy.max_health * 0.5:
                            enemy.boss_phase = 1
                            enemy.attack_cooldown = 30
                            enemy.speed = 4
                    elif enemy.boss_phase == 1 and self.player:
                        if self.player.y < enemy.y - 50:
                            enemy.speed = 10
                        else:
                            enemy.speed = 3
            
            # Player collision
            if self.player and not self.player.invincible:
                if (abs(self.player.x + self.player.width//2 - enemy.x - enemy.width//2) < 
                    (self.player.width + enemy.width)//2 and
                    abs(self.player.y + self.player.height//2 - enemy.y - enemy.height//2) <
                    (self.player.height + enemy.height)//2):
                    
                    # Player jumping on enemy
                    if (self.player.velocity_y > 0 and 
                        self.player.y + self.player.height - enemy.y < 20):
                        enemy.health -= self.player.attack_power
                        self.player.velocity_y = -10
                        self.particles.emit(enemy.x + enemy.width//2, enemy.y, 15, "hit")
                        self.score += 50
                        self._add_combo()
                        
                        if enemy.health <= 0:
                            enemy.is_dead = True
                            enemy.death_timer = 30
                            self.score += 100 * (self.combo_count + 1)
                            self.particles.emit(enemy.x + enemy.width//2, 
                                              enemy.y + enemy.height//2, 30, "death")
                    else:
                        self._damage_player(enemy.damage)
    
    def _update_collectibles(self):
        """Update collectible animations and collection"""
        for coll in self.collectibles[:]:
            if coll.collected:
                continue
            
            # Bob animation
            coll.bob_offset = math.sin(self.frame_count * 0.05 + coll.x * 0.01) * 3
            
            # Sparkle effect
            coll.sparkle_timer += 1
            if coll.sparkle_timer > 30:
                coll.sparkle_timer = 0
                self.particles.emit(coll.x + coll.width//2, coll.y + coll.height//2, 2, coll.name)
            
            # Player collection
            if self.player:
                if (abs(self.player.x + self.player.width//2 - coll.x - coll.width//2) < 30 and
                    abs(self.player.y + self.player.height//2 - coll.y - coll.height//2) < 30):
                    coll.collected = True
                    self.score += coll.points
                    self.player.coins += 1
                    self._add_combo()
                    self.particles.emit(coll.x + coll.width//2, coll.y + coll.height//2, 
                                      15, coll.name)
                    self.collectibles.remove(coll)
    
    def _update_platforms(self):
        """Update moving, crumbling, sinking, and bouncy platforms"""
        for plat in self.platforms[:]:
            if plat.get("type") == "moving":
                if "move_x" in plat:
                    plat["x"] += plat.get("speed", 2) * (1 if plat.get("moving_right", True) else -1)
                    if plat["x"] > plat.get("start_x", plat["x"]) + plat.get("move_x", 100):
                        plat["moving_right"] = False
                    elif plat["x"] < plat.get("start_x", plat["x"]) - plat.get("move_x", 100):
                        plat["moving_right"] = True
                    if "start_x" not in plat:
                        plat["start_x"] = plat["x"]
                
                if "move_y" in plat:
                    plat["y"] += plat.get("speed", 2) * (1 if plat.get("moving_down", True) else -1)
                    if plat["y"] > plat.get("start_y", plat["y"]) + plat.get("move_y", 60):
                        plat["moving_down"] = False
                    elif plat["y"] < plat.get("start_y", plat["y"]) - plat.get("move_y", 60):
                        plat["moving_down"] = True
                    if "start_y" not in plat:
                        plat["start_y"] = plat["y"]
            
            elif plat.get("type") == "crumbling":
                if self.player and self.player.on_ground:
                    if (self.player.x + self.player.width > plat["x"] and 
                        self.player.x < plat["x"] + plat["width"] and
                        abs(self.player.y + self.player.height - plat["y"]) < 5):
                        plat["crumble_timer"] = plat.get("crumble_timer", 0) + 1
                        if plat["crumble_timer"] > 60:
                            self.platforms.remove(plat)
            
            elif plat.get("type") == "sinking":
                if self.player and self.player.on_ground:
                    if (self.player.x + self.player.width > plat["x"] and 
                        self.player.x < plat["x"] + plat["width"] and
                        abs(self.player.y + self.player.height - plat["y"]) < 5):
                        plat["y"] += 1
            
            elif plat.get("type") == "bouncy":
                if self.player and self.player.on_ground:
                    if (self.player.x + self.player.width > plat["x"] and 
                        self.player.x < plat["x"] + plat["width"] and
                        abs(self.player.y + self.player.height - plat["y"]) < 5):
                        self.player.velocity_y = -20
                        self.player.is_jumping = True
                        self.player.on_ground = False
                        self.particles.emit(self.player.x + self.player.width//2, 
                                          self.player.y + self.player.height, 10, "sparkle")
    
    def _update_hazards(self):
        """Update hazard behaviors"""
        for haz in self.hazards:
            if haz.get("type") == "meteor":
                haz["y"] += haz.get("fall_speed", 5)
                if haz["y"] > self.game_map.height:
                    haz["y"] = random.randint(-200, -50)
                    haz["x"] = random.randint(0, self.game_map.width - haz.get("width", 40))
                
                if self.player and not self.player.invincible:
                    if (abs(self.player.x + self.player.width//2 - haz["x"] - haz.get("width", 40)//2) < 30 and
                        abs(self.player.y + self.player.height//2 - haz["y"] - haz.get("height", 40)//2) < 30):
                        self._damage_player(25)
                        self.particles.emit(haz["x"], haz["y"], 20, "explosion")
                        haz["y"] = random.randint(-200, -50)
                        haz["x"] = random.randint(0, self.game_map.width)
            
            elif haz.get("type") == "lava":
                if self.player:
                    if self.player.y + self.player.height > haz["y"]:
                        self._damage_player(50)
                        self.particles.emit(self.player.x + self.player.width//2, 
                                          haz["y"], 20, "explosion")
                        if self.player.health > 0:
                            self.player.y = self.game_map.spawn_point[1]
                            self.player.x = self.game_map.spawn_point[0]
    
    def _damage_player(self, damage):
        """Apply damage to player"""
        if self.player.invincible or self.player.health <= 0:
            return
        
        self.player.health -= damage
        self.player.invincible = True
        self.player.invincible_timer = 60
        
        self.particles.emit(self.player.x + self.player.width//2, 
                          self.player.y + self.player.height//2, 10, "hit")
        
        if self.player.health <= 0:
            self._kill_player()
    
    def _kill_player(self):
        """Handle player death"""
        if self.player.health > 0:
            self.player.health = 0
        
        self.player.lives -= 1
        self.particles.emit(self.player.x + self.player.width//2, 
                          self.player.y + self.player.height//2, 40, "death")
        
        if self.player.lives > 0:
            self.player.health = self.player.max_health
            self.player.x = self.game_map.spawn_point[0]
            self.player.y = self.game_map.spawn_point[1]
            self.player.velocity_x = 0
            self.player.velocity_y = 0
            self.player.invincible = True
            self.player.invincible_timer = 120
            self.combo_count = 0
        else:
            self.game_over = True
            self.is_playing = False
    
    def _add_combo(self):
        """Increment combo counter"""
        self.combo_count += 1
        self.combo_timer = 120
        if self.combo_count > self.max_combo:
            self.max_combo = self.combo_count
    
    def _update_camera(self):
        """Update camera position to follow player"""
        if not self.player or not self.game_map:
            return
        
        target_x = self.player.x - 400 + self.player.width // 2
        target_y = self.player.y - 300 + self.player.height // 2
        
        self.game_map.camera_x += (target_x - self.game_map.camera_x) * 0.1
        self.game_map.camera_y += (target_y - self.game_map.camera_y) * 0.1
        
        self.game_map.camera_x = max(0, min(self.game_map.camera_x, 
                                           self.game_map.width - 800))
        self.game_map.camera_y = max(0, min(self.game_map.camera_y, 
                                           self.game_map.height - 600))
    
    def _check_game_state(self):
        """Check win/lose conditions"""
        if not self.current_game:
            return
        
        win_condition = self.current_game.get("win_condition", "")
        
        if win_condition == "reach_end":
            if self.player and self.player.x >= self.game_map.end_point[0]:
                self.game_won = True
                self.is_playing = False
        elif win_condition == "target_score":
            if self.score >= self.current_game.get("target_score", 100):
                self.game_won = True
                self.is_playing = False
        elif win_condition == "survival_time":
            target_time = self.current_game.get("time_limit", 60)
            if target_time > 0 and self.time_elapsed >= target_time:
                self.game_won = True
                self.is_playing = False
        elif win_condition == "defeat_boss":
            if not any(e.is_boss and not e.is_dead for e in self.enemies):
                self.game_won = True
                self.is_playing = False
    
    def handle_input(self, key, pressed):
        """Handle keyboard input"""
        key = key.lower()
        if pressed:
            self.keys_pressed.add(key)
            
            if key in self.key_bindings:
                action = self.key_bindings[key]
                if action == "action" and self.player:
                    self.player.animation_state = "attack"
                    self.particles.emit(self.player.x + self.player.width//2, 
                                      self.player.y + self.player.height//2, 5, "hit")
                    for enemy in self.enemies[:]:
                        if not enemy.is_dead:
                            if (abs(self.player.x + self.player.width//2 - enemy.x - enemy.width//2) < 60 and
                                abs(self.player.y + self.player.height//2 - enemy.y - enemy.height//2) < 60):
                                enemy.health -= self.player.attack_power
                                self.particles.emit(enemy.x + enemy.width//2, 
                                                  enemy.y + enemy.height//2, 10, "hit")
                                if enemy.health <= 0:
                                    enemy.is_dead = True
                                    enemy.death_timer = 30
                                    self.score += 100
                                    self.particles.emit(enemy.x, enemy.y, 30, "death")
        else:
            self.keys_pressed.discard(key)
    
    def render(self, canvas):
        """Render the game to canvas (delegates to renderer)"""
        self.renderer.render(canvas)
    
    def restart(self):
        """Restart the game"""
        self.load_game_runtime()
    
    def save_game(self, file_path: Path = None) -> bool:
        """Save current game to file"""
        if not self.current_game:
            return False
        
        if file_path is None:
            if self.current_game_path is None:
                file_path = self.games_path / f"{self.current_game.get('name', 'game')}.json"
            else:
                file_path = self.current_game_path
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_game, f, indent=2, ensure_ascii=False)
            self.current_game_path = file_path
            return True
        except Exception as e:
            logging.error(f"Failed to save game: {e}")
            return False
    
    def load_game(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load a game from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                game_data = json.load(f)
            self.current_game = game_data
            self.current_game_path = file_path
            return game_data
        except Exception as e:
            logging.error(f"Failed to load game: {e}")
            return None
    
    def get_available_games(self) -> List[Dict[str, str]]:
        """Get list of saved games"""
        games = []
        for file in self.games_path.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    games.append({
                        "name": data.get("name", file.stem),
                        "path": str(file),
                        "template": data.get("template", "custom"),
                        "author": data.get("author", "Unknown")
                    })
            except:
                pass
        return games