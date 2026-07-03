"""
MEMEEngine Particle System
Particle effects for games
"""

import random
import math


class ParticleSystem:
    """Particle effects system for MEMEEngine games"""
    
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, count=10, particle_type="sparkle"):
        for _ in range(count):
            particle = {
                "x": x + random.randint(-10, 10),
                "y": y + random.randint(-10, 10),
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-5, -1),
                "life": 1.0,
                "decay": random.uniform(0.02, 0.05),
                "size": random.randint(2, 6),
                "type": particle_type,
                "color": self._get_particle_color(particle_type)
            }
            self.particles.append(particle)
    
    def _get_particle_color(self, ptype):
        colors = {
            "sparkle": (255, 255, 100),
            "coin": (255, 215, 0),
            "gem": (100, 255, 255),
            "star": (255, 255, 255),
            "hit": (255, 100, 50),
            "death": (255, 50, 50),
            "explosion": (255, 150, 0),
            "heal": (100, 255, 100),
            "powerup": (200, 100, 255),
        }
        return colors.get(ptype, (255, 255, 255))
    
    def update(self):
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.1
            p["life"] -= p["decay"]
            if p["life"] <= 0:
                self.particles.remove(p)
    
    def draw(self, canvas, camera_x=0, camera_y=0):
        for p in self.particles:
            alpha = int(255 * p["life"])
            if alpha > 0:
                color = p["color"]
                size = int(p["size"] * p["life"])
                if size > 0:
                    x = p["x"] - camera_x
                    y = p["y"] - camera_y
                    try:
                        hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
                        canvas.create_oval(
                            x - size, y - size, x + size, y + size,
                            fill=hex_color,
                            stipple="gray25" if p["life"] < 0.5 else ""
                        )
                    except:
                        pass
    
    def clear(self):
        self.particles.clear()