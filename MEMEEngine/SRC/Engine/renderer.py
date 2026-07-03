"""
MEMEEngine Renderer
Handles all drawing operations for the game
"""

import math
import tkinter as tk


class GameRenderer:
    """Renders all game objects to a tkinter Canvas"""
    
    def __init__(self, engine):
        self.engine = engine
    
    def render(self, canvas):
        """Main render function - draws entire game state"""
        if not self.engine.game_map:
            return
        
        cam_x = int(self.engine.game_map.camera_x)
        cam_y = int(self.engine.game_map.camera_y)
        
        canvas.delete("all")
        
        # Draw background
        canvas.create_rectangle(0, 0, 800, 600, 
                               fill=self.engine.game_map.background_color, outline="")
        
        self._draw_background(canvas, cam_x, cam_y)
        self._draw_platforms(canvas, cam_x, cam_y)
        self._draw_hazards(canvas, cam_x, cam_y)
        self._draw_collectibles(canvas, cam_x, cam_y)
        self._draw_enemies(canvas, cam_x, cam_y)
        self._draw_characters(canvas, cam_x, cam_y)
        
        # Draw player
        if self.engine.player and self.engine.player.health > 0:
            px = self.engine.player.x - cam_x
            py = self.engine.player.y - cam_y
            
            if not self.engine.player.invincible or self.engine.frame_count % 4 < 2:
                self._draw_character(canvas, self.engine.player, px, py)
        
        self.engine.particles.draw(canvas, cam_x, cam_y)
        self._draw_ui(canvas)
        self._draw_overlay(canvas)
    
    def _draw_background(self, canvas, cam_x, cam_y):
        """Draw parallax background elements"""
        # Clouds
        for i in range(0, self.engine.game_map.width + 400, 200):
            cloud_x = i - (cam_x * 0.3) % (self.engine.game_map.width + 400)
            cloud_y = 50 + math.sin(i * 0.01 + self.engine.frame_count * 0.001) * 10
            
            if -100 < cloud_x < 900:
                canvas.create_oval(cloud_x, cloud_y, cloud_x + 60, cloud_y + 30, 
                                  fill="#FFFFFF", outline="")
                canvas.create_oval(cloud_x + 20, cloud_y - 10, cloud_x + 50, cloud_y + 20, 
                                  fill="#FFFFFF", outline="")
        
        # Mountains
        for i in range(0, self.engine.game_map.width + 600, 300):
            mx = i - (cam_x * 0.5) % (self.engine.game_map.width + 600)
            my = self.engine.game_map.ground_y - 100
            
            if -200 < mx < 1000:
                canvas.create_polygon(mx, my, mx + 150, my - 200, mx + 300, my,
                                     fill="#4A7C59", outline="#3A6C49")
                canvas.create_polygon(mx + 150, my - 200, mx + 200, my - 250, mx + 250, my - 200,
                                     fill="#FFFFFF", outline="#DDDDDD")
    
    def _draw_platforms(self, canvas, cam_x, cam_y):
        """Draw all platforms"""
        for plat in self.engine.platforms:
            px = plat["x"] - cam_x
            py = plat["y"] - cam_y
            
            if -100 < px < 900 and -100 < py < 700:
                plat_type = plat.get("type", "static")
                colors = {
                    "static": ("#8B4513", "#654321"),
                    "moving": ("#4169E1", "#1E90FF"),
                    "crumbling": ("#A0522D", "#8B4513"),
                    "sinking": ("#DAA520", "#B8860B"),
                    "bouncy": ("#FF69B4", "#FF1493"),
                }
                color1, color2 = colors.get(plat_type, ("#808080", "#606060"))
                
                canvas.create_rectangle(px, py, px + plat["width"], py + plat["height"],
                                       fill=color1, outline=color2, width=2)
    
    def _draw_hazards(self, canvas, cam_x, cam_y):
        """Draw all hazards"""
        for haz in self.engine.hazards:
            hx = haz["x"] - cam_x
            hy = haz["y"] - cam_y
            
            if haz.get("type") == "lava":
                if -100 < hx < 900:
                    canvas.create_rectangle(hx, hy, hx + haz["width"], hy + haz["height"],
                                           fill="#FF4500", outline="#FF0000", width=3)
                    # Animated lava surface
                    for i in range(0, haz["width"], 30):
                        wave_y = hy + math.sin((self.engine.frame_count + i) * 0.05) * 5
                        canvas.create_arc(hx + i, wave_y - 15, hx + i + 30, wave_y + 15,
                                        start=0, extent=180, fill="#FF6347", outline="")
            
            elif haz.get("type") == "meteor":
                if -100 < hx < 900 and -100 < hy < 700:
                    for i in range(3):
                        size = haz.get("width", 40) - i * 5
                        canvas.create_oval(
                            hx + i*5, hy - i*15, 
                            hx + size, hy + size - i*15,
                            fill="#FF4500", outline="#FF0000"
                        )
    
    def _draw_collectibles(self, canvas, cam_x, cam_y):
        """Draw all collectibles"""
        for coll in self.engine.collectibles:
            if coll.collected:
                continue
            cx = coll.x - cam_x
            cy = coll.y + coll.bob_offset - cam_y
            
            if -50 < cx < 850 and -50 < cy < 650:
                coll_type = coll.name
                if coll_type == "coin":
                    canvas.create_oval(cx, cy, cx + 24, cy + 24, fill="#FFD700", 
                                      outline="#FFA500", width=2)
                    canvas.create_text(cx + 12, cy + 12, text="$", fill="#FFA500", 
                                      font=("Arial", 12, "bold"))
                elif coll_type == "gem":
                    canvas.create_polygon(cx + 12, cy, cx + 24, cy + 8, cx + 24, cy + 16, 
                                         cx + 12, cy + 24, cx, cy + 16, cx, cy + 8,
                                         fill="#00FFFF", outline="#00CED1", width=2)
                elif coll_type == "star":
                    self._draw_star(canvas, cx + 12, cy + 12, 12, "#FFFF00", "#FFD700")
                elif coll_type == "meme_coin":
                    canvas.create_oval(cx, cy, cx + 24, cy + 24, fill="#FF69B4", 
                                      outline="#FF1493", width=2)
                    canvas.create_text(cx + 12, cy + 12, text="M", fill="#FFFFFF", 
                                      font=("Arial", 10, "bold"))
    
    def _draw_enemies(self, canvas, cam_x, cam_y):
        """Draw all enemies"""
        for enemy in self.engine.enemies:
            if enemy.is_dead and enemy.death_timer <= 0:
                continue
            
            ex = enemy.x - cam_x
            ey = enemy.y - cam_y
            
            if -50 < ex < 850 and -50 < ey < 650:
                if enemy.is_dead:
                    canvas.create_oval(ex, ey, ex + enemy.width, ey + enemy.height,
                                      fill="#FF0000", outline="#8B0000", stipple="gray50")
                else:
                    self._draw_enemy(canvas, enemy, ex, ey)
    
    def _draw_characters(self, canvas, cam_x, cam_y):
        """Draw non-player characters"""
        for char in self.engine.characters:
            cx = char.x - cam_x
            cy = char.y - cam_y
            if -50 < cx < 850 and -50 < cy < 650:
                self._draw_character(canvas, char, cx, cy)
    
    def _draw_character(self, canvas, char, x, y):
        """Draw a character sprite"""
        body_color = "#64B4FF" if char.name == "MEMEBOT" else \
                    "#C0C0C0" if char.name == "Pixel Knight" else \
                    "#FF8C00" if char.name == "Ninja Cat" else \
                    "#00FF00" if char.name == "Space Blob" else \
                    "#808080"
        
        outline_color = "#3282C8" if char.name == "MEMEBOT" else "#808080"
        
        if char.animation_state == "jump":
            # Jumping pose
            canvas.create_oval(x + 5, y + 5, x + char.width - 5, y + char.height - 5,
                             fill=body_color, outline=outline_color, width=2)
            canvas.create_line(x + 5, y + 15, x - 5, y, fill=body_color, width=4)
            canvas.create_line(x + char.width - 5, y + 15, x + char.width + 5, y, 
                             fill=body_color, width=4)
        else:
            # Normal/idle/walk pose
            canvas.create_oval(x + 5, y + 5, x + char.width - 5, y + char.height - 5,
                             fill=body_color, outline=outline_color, width=2)
            
            if char.animation_state == "walk":
                leg_offset = math.sin(self.engine.frame_count * 0.2) * 5
                canvas.create_line(x + char.width//2, y + char.height - 5,
                                 x + char.width//2 - leg_offset, y + char.height + 10,
                                 fill=body_color, width=4)
                canvas.create_line(x + char.width//2, y + char.height - 5,
                                 x + char.width//2 + leg_offset, y + char.height + 10,
                                 fill=body_color, width=4)
            else:
                canvas.create_line(x + char.width//2, y + char.height - 5,
                                 x + char.width//2 - 5, y + char.height + 8,
                                 fill=body_color, width=4)
                canvas.create_line(x + char.width//2, y + char.height - 5,
                                 x + char.width//2 + 5, y + char.height + 8,
                                 fill=body_color, width=4)
        
        # Eyes
        eye_y = y + char.height//3
        if char.facing_right:
            canvas.create_oval(x + char.width - 15, eye_y, x + char.width - 5, eye_y + 10,
                             fill="#FFFFFF", outline="#000000")
            canvas.create_oval(x + char.width - 12, eye_y + 2, x + char.width - 8, eye_y + 8,
                             fill="#000000")
        else:
            canvas.create_oval(x + 5, eye_y, x + 15, eye_y + 10,
                             fill="#FFFFFF", outline="#000000")
            canvas.create_oval(x + 8, eye_y + 2, x + 12, eye_y + 8,
                             fill="#000000")
        
        # Mouth
        mouth_y = y + char.height//2
        canvas.create_arc(x + char.width//2 - 5, mouth_y, x + char.width//2 + 5, mouth_y + 10,
                         start=0, extent=-180, fill="#FF0000", outline="")
        
        # Name label
        canvas.create_text(x + char.width//2, y - 10, text=char.name, fill="#FFFFFF", 
                          font=("Arial", 8), anchor="s")
        
        # Health bar for player
        if char.is_player:
            bar_width = char.width
            bar_height = 4
            bar_x = x
            bar_y = y - 20
            
            canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                   fill="#333333", outline="")
            health_ratio = char.health / char.max_health
            health_color = "#00FF00" if health_ratio > 0.5 else \
                          "#FFFF00" if health_ratio > 0.25 else "#FF0000"
            canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width * health_ratio, 
                                   bar_y + bar_height, fill=health_color, outline="")
    
    def _draw_enemy(self, canvas, enemy, x, y):
        """Draw an enemy sprite based on type"""
        enemy_type = enemy.name
        
        if enemy_type == "slime":
            canvas.create_oval(x + 2, y + enemy.height//2, x + enemy.width - 2, y + enemy.height,
                             fill="#32CD32", outline="#228B22", width=2)
            canvas.create_oval(x + 8, y + 5, x + 16, y + 13, fill="#FFFFFF")
            canvas.create_oval(x + 20, y + 5, x + 28, y + 13, fill="#FFFFFF")
            canvas.create_oval(x + 10, y + 7, x + 14, y + 11, fill="#000000")
            canvas.create_oval(x + 22, y + 7, x + 26, y + 11, fill="#000000")
        
        elif enemy_type == "skeleton":
            canvas.create_rectangle(x + 8, y + 5, x + enemy.width - 8, y + enemy.height - 5,
                                  fill="#F5F5DC", outline="#D2B48C", width=2)
            canvas.create_oval(x + 8, y, x + enemy.width - 8, y + 20, 
                             fill="#F5F5DC", outline="#D2B48C", width=2)
            canvas.create_oval(x + 12, y + 5, x + 16, y + 9, fill="#FF0000")
            canvas.create_oval(x + 20, y + 5, x + 24, y + 9, fill="#FF0000")
        
        elif enemy_type == "ghost":
            canvas.create_oval(x + 2, y, x + enemy.width - 2, y + enemy.height - 5,
                             fill="#DDA0DD", outline="#BA55D3", width=2)
            canvas.create_oval(x + 8, y + 8, x + 14, y + 14, fill="#FFFFFF")
            canvas.create_oval(x + 20, y + 8, x + 26, y + 14, fill="#FFFFFF")
            canvas.create_oval(x + 10, y + 10, x + 12, y + 12, fill="#000000")
            canvas.create_oval(x + 22, y + 10, x + 24, y + 12, fill="#000000")
        
        elif enemy_type == "robot_enemy":
            canvas.create_rectangle(x + 4, y + 4, x + enemy.width - 4, y + enemy.height - 4,
                                  fill="#808080", outline="#606060", width=2)
            canvas.create_oval(x + 8, y + 8, x + 14, y + 14, fill="#00FFFF")
            canvas.create_oval(x + 20, y + 8, x + 26, y + 14, fill="#00FFFF")
            canvas.create_rectangle(x + 12, y + 18, x + 22, y + 22, fill="#00FFFF")
        
        elif enemy_type == "meme_troll":
            canvas.create_oval(x, y, x + enemy.width, y + enemy.height,
                             fill="#FF6347", outline="#FF4500", width=2)
            canvas.create_oval(x + 6, y + 8, x + 14, y + 16, fill="#FFFFFF")
            canvas.create_oval(x + 20, y + 8, x + 28, y + 16, fill="#FFFFFF")
            canvas.create_text(x + enemy.width//2, y + enemy.height//2, text=">:)",
                             fill="#FFFFFF", font=("Arial", 8, "bold"))
        
        elif enemy_type == "boss_slime":
            boss_size = enemy.width * 2
            canvas.create_oval(x - boss_size//4, y - boss_size//4, 
                             x + boss_size*3//4, y + boss_size*3//4,
                             fill="#8B0000", outline="#FF0000", width=3)
            canvas.create_oval(x + boss_size//8, y + boss_size//8,
                             x + boss_size//4, y + boss_size//4, fill="#FFFF00")
            canvas.create_oval(x + boss_size*3//8, y + boss_size//8,
                             x + boss_size//2, y + boss_size//4, fill="#FFFF00")
            # Boss health bar
            bar_width = boss_size
            bar_height = 8
            canvas.create_rectangle(x - boss_size//4, y - boss_size//4 - 20,
                                   x + boss_size*3//4, y - boss_size//4 - 12,
                                   fill="#333333", outline="")
            health_ratio = enemy.health / enemy.max_health
            canvas.create_rectangle(x - boss_size//4, y - boss_size//4 - 20,
                                   x - boss_size//4 + bar_width * health_ratio, 
                                   y - boss_size//4 - 12,
                                   fill="#FF0000", outline="")
        
        # Regular enemy health bar
        if not enemy.is_boss:
            bar_width = enemy.width
            bar_height = 3
            bar_y = y - 8
            canvas.create_rectangle(x, bar_y, x + bar_width, bar_y + bar_height,
                                   fill="#333333", outline="")
            health_ratio = enemy.health / enemy.max_health
            canvas.create_rectangle(x, bar_y, x + bar_width * health_ratio, bar_y + bar_height,
                                   fill="#FF4444", outline="")
    
    def _draw_star(self, canvas, cx, cy, size, fill_color, outline_color):
        """Draw a star shape"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            r = size if i % 2 == 0 else size * 0.4
            points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
        canvas.create_polygon(points, fill=fill_color, outline=outline_color, width=2)
    
    def _draw_ui(self, canvas):
        """Draw HUD elements"""
        for ui in self.engine.ui_elements:
            if not ui.visible:
                continue
            
            text = ui.text
            if ui.binding == "score":
                text = text.replace("{score}", str(self.engine.score))
            elif ui.binding == "health":
                text = text.replace("{health}", 
                    str(self.engine.player.health if self.engine.player else 0))
            elif ui.binding == "lives":
                text = text.replace("{lives}", 
                    str(self.engine.player.lives if self.engine.player else 0))
            elif ui.binding == "time":
                text = text.replace("{time}", str(self.engine.time_elapsed))
            elif ui.binding == "combo":
                text = text.replace("{combo}", 
                    f"{self.engine.combo_count}x" if self.engine.combo_count > 1 else "")
            
            canvas.create_text(ui.x, ui.y, text=text, fill=ui.color,
                             font=("Arial", ui.font_size, "bold"), anchor="nw")
        
        # Combo display
        if self.engine.combo_count > 1:
            canvas.create_text(400, 500, text=f"{self.engine.combo_count}x COMBO!",
                             fill="#FFD700", font=("Arial", 24, "bold"))
    
    def _draw_overlay(self, canvas):
        """Draw game over / win overlays"""
        if self.engine.game_over:
            canvas.create_rectangle(0, 0, 800, 600, fill="#000000", stipple="gray50")
            canvas.create_text(400, 250, text="GAME OVER", fill="#FF0000", 
                             font=("Arial", 48, "bold"))
            canvas.create_text(400, 320, text=f"Score: {self.engine.score}", 
                             fill="#FFFFFF", font=("Arial", 24))
            canvas.create_text(400, 360, text="Press R to Restart", 
                             fill="#FFFF00", font=("Arial", 18))
        
        if self.engine.game_won:
            canvas.create_rectangle(0, 0, 800, 600, fill="#000000", stipple="gray25")
            canvas.create_text(400, 250, text="YOU WIN!", fill="#FFD700", 
                             font=("Arial", 48, "bold"))
            canvas.create_text(400, 320, text=f"Score: {self.engine.score}", 
                             fill="#FFFFFF", font=("Arial", 24))
            canvas.create_text(400, 360, text=f"Max Combo: {self.engine.max_combo}x", 
                             fill="#FF69B4", font=("Arial", 18))
            canvas.create_text(400, 400, text="Press R to Restart", 
                             fill="#FFFF00", font=("Arial", 18))