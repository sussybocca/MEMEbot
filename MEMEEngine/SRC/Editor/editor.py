"""
MEMEEngine Editor - Modern UI Redesign
Professional game creation interface with animations and effects
"""

import os
import json
import math
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Dict, Any, List, Optional

from SRC.Engine.game_engine import MEMEEngine
from SRC.Characters.presets import PRESET_CHARACTERS
from SRC.Maps.presets import PRESET_MAPS
from SRC.Core.templates import GAME_TEMPLATES


class ModernColors:
    """Professional color scheme"""
    BG_DARK = "#0F1119"
    BG_MEDIUM = "#1A1D2E"
    BG_LIGHT = "#242838"
    BG_CARD = "#2A2F45"
    BG_HOVER = "#323852"
    ACCENT = "#6C5CE7"
    ACCENT_HOVER = "#7E6FF0"
    ACCENT_LIGHT = "#A29BFE"
    SUCCESS = "#00D68F"
    DANGER = "#FF6B6B"
    WARNING = "#FFD93D"
    INFO = "#54A0FF"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B0B5CC"
    TEXT_MUTED = "#6E7491"
    BORDER = "#3D4260"
    BORDER_LIGHT = "#4A5075"
    GRADIENT_1 = "#6C5CE7"
    GRADIENT_2 = "#00D68F"
    SHADOW = "#00000040"
    GLOW_ACCENT = "#6C5CE740"
    GLOW_SUCCESS = "#00D68F40"
    GLOW_DANGER = "#FF6B6B40"


class AnimatedButton(tk.Canvas):
    """Custom animated button with hover effects"""
    
    def __init__(self, parent, text, command=None, width=120, height=40, 
                 color=ModernColors.ACCENT, hover_color=None, icon="", 
                 font_size=10, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=ModernColors.BG_DARK, highlightthickness=0, bd=0, **kwargs)
        
        self.text = text
        self.command = command
        self.color = color
        self.hover_color = hover_color or self._lighten_color(color)
        self.icon = icon
        self.font_size = font_size
        self.width = width
        self.height = height
        self.is_hovered = False
        self.anim_progress = 0.0
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        self._draw()
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color by 15%"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
        r = min(255, int(r * 1.15))
        g = min(255, int(g * 1.15))
        b = min(255, int(b * 1.15))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _draw(self):
        self.delete("all")
        
        current_color = self._interpolate_color(self.color, self.hover_color, self.anim_progress)
        radius = 10
        
        if self.is_hovered:
            for i in range(3, 0, -1):
                alpha = int(40 * (1 - i * 0.3) * self.anim_progress)
                glow_color = self._hex_to_rgb(current_color) + (alpha,)
                self._create_rounded_rect(0 - i, 0 - i, self.width + i, self.height + i,
                                         radius + i, fill="", outline=self._rgb_to_hex(glow_color[:3]),
                                         width=2)
        
        self._create_rounded_rect(0, 0, self.width, self.height, radius, 
                                 fill=current_color, outline=current_color)
        
        display_text = f"{self.icon} {self.text}".strip()
        text_color = ModernColors.TEXT_PRIMARY
        self.create_text(self.width // 2, self.height // 2, text=display_text,
                        fill=text_color, font=("Segoe UI", self.font_size, "bold"))
    
    def _create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        """Create a rounded rectangle"""
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def _interpolate_color(self, color1, color2, t):
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return self._rgb_to_hex((r, g, b))
    
    def _on_enter(self, event):
        self.is_hovered = True
        self._animate_hover(0.0)
    
    def _on_leave(self, event):
        self.is_hovered = False
        self._animate_hover(1.0)
    
    def _animate_hover(self, start):
        target = 1.0 if self.is_hovered else 0.0
        step = 0.15
        
        def update():
            nonlocal start
            if self.is_hovered:
                start = min(1.0, start + step)
            else:
                start = max(0.0, start - step)
            
            self.anim_progress = start
            self._draw()
            
            if (self.is_hovered and start < 1.0) or (not self.is_hovered and start > 0.0):
                self.after(16, update)
        
        update()
    
    def _on_click(self, event):
        self.anim_progress = 0.5
        self._draw()
    
    def _on_release(self, event):
        self.anim_progress = 1.0 if self.is_hovered else 0.0
        self._draw()
        if self.command:
            self.after(50, self.command)


class GlowCard(tk.Frame):
    """Card widget with subtle glow effect"""
    
    def __init__(self, parent, glow_color=ModernColors.ACCENT, **kwargs):
        super().__init__(parent, bg=ModernColors.BG_CARD, **kwargs)
        self.glow_color = glow_color
        self.glow_intensity = 0.0
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        self._animate_glow(0.0, 1.0)
    
    def _on_leave(self, event):
        self._animate_glow(self.glow_intensity, 0.0)
    
    def _animate_glow(self, start, target):
        step = 0.1
        current = start
        
        def update():
            nonlocal current
            if target > start:
                current = min(target, current + step)
            else:
                current = max(target, current - step)
            
            self.glow_intensity = current
            r, g, b = self._hex_to_rgb(self.glow_color)
            self.configure(bg=self._rgb_to_hex((r, g, b)) if current > 0.5 else ModernColors.BG_CARD)
            
            if abs(current - target) > 0.01:
                self.after(16, update)
        
        update()
    
    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


class ParticleCanvas(tk.Canvas):
    """Canvas with animated particles"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=ModernColors.BG_DARK, highlightthickness=0, **kwargs)
        self.particles = []
        self._spawn_particles()
        self._animate()
    
    def _spawn_particles(self):
        for _ in range(20):
            self.particles.append({
                'x': 0,
                'y': 0,
                'vx': 0,
                'vy': 0,
                'size': 0,
                'alpha': 0,
                'life': 0,
                'max_life': 0
            })
        self._reset_particles()
    
    def _reset_particles(self):
        w = self.winfo_width() or 800
        h = self.winfo_height() or 600
        for p in self.particles:
            p['x'] = random.randint(0, w)
            p['y'] = random.randint(0, h)
            p['vx'] = random.uniform(-0.5, 0.5)
            p['vy'] = random.uniform(-0.5, 0.5)
            p['size'] = random.randint(1, 3)
            p['alpha'] = random.uniform(0.1, 0.4)
            p['life'] = random.uniform(0, 300)
            p['max_life'] = random.uniform(200, 500)
    
    def _animate(self):
        self.delete("particle")
        w = self.winfo_width() or 800
        h = self.winfo_height() or 600
        
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] += 1
            
            if p['life'] > p['max_life']:
                p['x'] = random.randint(0, w)
                p['y'] = random.randint(0, h)
                p['life'] = 0
                p['max_life'] = random.uniform(200, 500)
            
            if p['x'] < 0: p['x'] = w
            if p['x'] > w: p['x'] = 0
            if p['y'] < 0: p['y'] = h
            if p['y'] > h: p['y'] = 0
            
            alpha = int(255 * p['alpha'] * (1 - abs(p['life'] / p['max_life'] - 0.5) * 2))
            color = ModernColors.ACCENT_LIGHT
            try:
                self.create_oval(p['x'], p['y'], p['x'] + p['size'], p['y'] + p['size'],
                               fill=color, outline="", tags="particle",
                               stipple="gray50" if p['alpha'] < 0.2 else "")
            except:
                pass
        
        self.after(50, self._animate)


class MEMEEngineEditor:
    """Modern professional editor for MEMEEngine game creation"""
    
    def __init__(self, parent, config, memebot_app):
        self.parent = parent
        self.config = config
        self.memebot_app = memebot_app
        self.engine = MEMEEngine(config)
        
        self.window = None
        self.edit_canvas = None
        self.property_panel_frame = None
        self.game_window = None
        self.game_canvas = None
        
        self.grid_enabled = True
        self.snap_enabled = True
        self.grid_size = 50
        self.selected_asset = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False
        self.game_loop_running = False
        
        self.sidebar_anim_progress = 0.0
        self.cards_anim_offset = 0
        self.status_message_timer = 0
        
        # Initialize all UI variables to None (created during _build_modern_ui)
        self.game_name_entry = None
        self.diff_var = None
        self.win_var = None
        self.lives_spinbox = None
        self.selected_label = None
        self.status_var = None
        self.status_label = None
        self.pos_var = None
        self.grid_btn = None
        self.snap_btn = None
        self.drag_asset_type = None
        self.drag_asset_id = None
        self.sidebar = None
    
    def show(self):
        """Show or create the editor window"""
        if self.window and self.window.winfo_exists():
            self.window.deiconify()
            self.window.lift()
            return
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("MEMEEngine - Professional Game Creator")
        self.window.geometry("1400x850")
        self.window.configure(bg=ModernColors.BG_DARK)
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
        
        self.window.update_idletasks()
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - 1400) // 2
        y = (screen_h - 850) // 2
        self.window.geometry(f"1400x850+{x}+{y}")
        
        self._build_modern_ui()
        self._refresh_canvas()
        self._set_status("Ready to create! Drag assets or start a new game.", "info")
    
    def _build_modern_ui(self):
        """Build the modern professional interface"""
        
        # ===== TOP HEADER BAR =====
        header = tk.Frame(self.window, bg=ModernColors.BG_MEDIUM, height=50)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        logo_frame = tk.Frame(header, bg=ModernColors.BG_MEDIUM)
        logo_frame.pack(side="left", padx=15, pady=8)
        
        tk.Label(logo_frame, text="🎮", bg=ModernColors.BG_MEDIUM, fg=ModernColors.TEXT_PRIMARY,
                font=("Segoe UI", 16)).pack(side="left")
        tk.Label(logo_frame, text="MEMEEngine", bg=ModernColors.BG_MEDIUM, 
                fg=ModernColors.ACCENT_LIGHT, font=("Segoe UI", 14, "bold")).pack(side="left", padx=(8, 0))
        tk.Label(logo_frame, text="PRO", bg=ModernColors.BG_MEDIUM, 
                fg=ModernColors.SUCCESS, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(4, 0))
        
        actions_frame = tk.Frame(header, bg=ModernColors.BG_MEDIUM)
        actions_frame.pack(side="right", padx=15, pady=8)
        
        btn_new = AnimatedButton(actions_frame, "New", command=self._new_game_dialog,
                                width=80, height=32, color=ModernColors.ACCENT, 
                                icon="📄", font_size=9)
        btn_new.pack(side="left", padx=3)
        
        btn_load = AnimatedButton(actions_frame, "Load", command=self._load_game_dialog,
                                 width=80, height=32, color=ModernColors.BG_LIGHT,
                                 icon="📂", font_size=9)
        btn_load.pack(side="left", padx=3)
        
        btn_save = AnimatedButton(actions_frame, "Save", command=self._save_game,
                                 width=80, height=32, color=ModernColors.SUCCESS,
                                 icon="💾", font_size=9)
        btn_save.pack(side="left", padx=3)
        
        tk.Frame(header, bg=ModernColors.BORDER, width=1, height=24).pack(side="right", padx=10)
        
        btn_play = AnimatedButton(actions_frame, "PLAY", command=self._play_game,
                                 width=100, height=32, color="#FF6B6B",
                                 icon="▶", font_size=9)
        btn_play.pack(side="right", padx=3)
        
        btn_stop = AnimatedButton(actions_frame, "Stop", command=self._stop_game,
                                 width=70, height=32, color=ModernColors.BG_LIGHT,
                                 icon="⏹", font_size=9)
        btn_stop.pack(side="right", padx=3)
        
        # ===== MAIN CONTENT AREA =====
        main_frame = tk.Frame(self.window, bg=ModernColors.BG_DARK)
        main_frame.pack(fill="both", expand=True)
        
        # ===== LEFT SIDEBAR - ASSET PALETTE =====
        self.sidebar = tk.Frame(main_frame, bg=ModernColors.BG_MEDIUM, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self._build_modern_sidebar()
        
        # ===== CENTER - CANVAS AREA =====
        canvas_container = tk.Frame(main_frame, bg=ModernColors.BG_DARK)
        canvas_container.pack(side="left", fill="both", expand=True)
        
        canvas_header = tk.Frame(canvas_container, bg=ModernColors.BG_MEDIUM, height=36)
        canvas_header.pack(fill="x")
        canvas_header.pack_propagate(False)
        
        tk.Label(canvas_header, text="  Game World", bg=ModernColors.BG_MEDIUM, 
                fg=ModernColors.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(side="left", padx=10, pady=8)
        
        grid_frame = tk.Frame(canvas_header, bg=ModernColors.BG_MEDIUM)
        grid_frame.pack(side="right", padx=10)
        
        self.grid_btn = tk.Label(grid_frame, text="⊞ Grid", bg=ModernColors.BG_MEDIUM, 
                                 fg=ModernColors.SUCCESS, font=("Segoe UI", 9, "bold"),
                                 cursor="hand2")
        self.grid_btn.pack(side="left", padx=5)
        self.grid_btn.bind("<Button-1>", lambda e: self._toggle_grid())
        
        self.snap_btn = tk.Label(grid_frame, text="⊙ Snap", bg=ModernColors.BG_MEDIUM, 
                                 fg=ModernColors.SUCCESS, font=("Segoe UI", 9, "bold"),
                                 cursor="hand2")
        self.snap_btn.pack(side="left", padx=5)
        self.snap_btn.bind("<Button-1>", lambda e: self._toggle_snap())
        
        # Canvas frame to hold the edit canvas
        canvas_frame = tk.Frame(canvas_container, bg=ModernColors.BG_DARK)
        canvas_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Particle background
        canvas_bg = ParticleCanvas(canvas_frame)
        canvas_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Edit canvas
        self.edit_canvas = tk.Canvas(canvas_frame, bg=ModernColors.BG_DARK, 
                                     highlightthickness=0, bd=0)
        self.edit_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        h_scroll = tk.Scrollbar(canvas_container, orient="horizontal", 
                               command=self.edit_canvas.xview,
                               bg=ModernColors.BG_MEDIUM, troughcolor=ModernColors.BG_DARK)
        h_scroll.pack(side="bottom", fill="x")
        v_scroll = tk.Scrollbar(canvas_container, orient="vertical",
                               command=self.edit_canvas.yview,
                               bg=ModernColors.BG_MEDIUM, troughcolor=ModernColors.BG_DARK)
        v_scroll.pack(side="right", fill="y")
        
        self.edit_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        self._setup_canvas_events()
        
        # ===== RIGHT SIDEBAR - PROPERTIES =====
        self._build_modern_properties(main_frame)
        
        # ===== BOTTOM STATUS BAR =====
        status_bar = tk.Frame(self.window, bg=ModernColors.BG_MEDIUM, height=32)
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(status_bar, textvariable=self.status_var, 
                                     bg=ModernColors.BG_MEDIUM, fg=ModernColors.TEXT_MUTED,
                                     font=("Segoe UI", 9), anchor="w")
        self.status_label.pack(side="left", fill="x", padx=15, pady=6)
        
        self.pos_var = tk.StringVar(value="X: 0  Y: 0")
        tk.Label(status_bar, textvariable=self.pos_var, bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.TEXT_MUTED, font=("Segoe UI", 9)).pack(side="right", padx=15, pady=6)
    
    def _build_modern_sidebar(self):
        """Build the modern asset palette sidebar"""
        
        sidebar_header = tk.Frame(self.sidebar, bg=ModernColors.BG_LIGHT, height=45)
        sidebar_header.pack(fill="x")
        sidebar_header.pack_propagate(False)
        
        tk.Label(sidebar_header, text="ASSETS", bg=ModernColors.BG_LIGHT, 
                fg=ModernColors.ACCENT_LIGHT, font=("Segoe UI", 11, "bold")).pack(side="left", padx=15, pady=12)
        
        search_frame = tk.Frame(self.sidebar, bg=ModernColors.BG_MEDIUM, height=35)
        search_frame.pack(fill="x", padx=8, pady=(8, 4))
        search_frame.pack_propagate(False)
        
        search_entry = tk.Entry(search_frame, bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_PRIMARY,
                               insertbackground=ModernColors.TEXT_PRIMARY, bd=0,
                               font=("Segoe UI", 10))
        search_entry.pack(fill="both", expand=True, ipady=6, padx=2, pady=2)
        search_entry.insert(0, "🔍  Search assets...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, "end") if search_entry.get() == "🔍  Search assets..." else None)
        search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, "🔍  Search assets...") if not search_entry.get() else None)
        
        asset_canvas = tk.Canvas(self.sidebar, bg=ModernColors.BG_MEDIUM, 
                                highlightthickness=0, width=230)
        asset_scroll = tk.Scrollbar(self.sidebar, orient="vertical", command=asset_canvas.yview)
        asset_inner = tk.Frame(asset_canvas, bg=ModernColors.BG_MEDIUM)
        
        asset_inner.bind("<Configure>", lambda e: asset_canvas.configure(
            scrollregion=asset_canvas.bbox("all")))
        win_id = asset_canvas.create_window((0, 0), window=asset_inner, anchor="nw", width=225)
        asset_canvas.configure(yscrollcommand=asset_scroll.set)
        
        asset_canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
        asset_scroll.pack(side="right", fill="y", padx=(0, 3))
        
        def on_mousewheel(event):
            asset_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        asset_canvas.bind("<Enter>", lambda e: asset_canvas.bind_all("<MouseWheel>", on_mousewheel))
        asset_canvas.bind("<Leave>", lambda e: asset_canvas.unbind_all("<MouseWheel>"))
        
        self._add_modern_category(asset_inner, "CHARACTERS", "👥", ModernColors.INFO)
        for char_id, char_data in PRESET_CHARACTERS.items():
            self._add_modern_asset_item(asset_inner, char_data["name"], "character", char_id,
                                       f"HP: {char_data['health']}  SPD: {char_data['speed']}",
                                       ModernColors.INFO)
        
        self._add_modern_category(asset_inner, "MAPS", "🗺", ModernColors.SUCCESS)
        for map_id, map_data in PRESET_MAPS.items():
            self._add_modern_asset_item(asset_inner, map_data["name"], "map", map_id,
                                       f"{map_data['theme'].title()}  •  {map_data['default_size'][0]}×{map_data['default_size'][1]}",
                                       ModernColors.SUCCESS)
        
        self._add_modern_category(asset_inner, "COLLECTIBLES", "💎", ModernColors.WARNING)
        points_map = {"coin": 10, "gem": 25, "star": 50, "meme_coin": 30}
        for item in ["coin", "gem", "star", "meme_coin"]:
            self._add_modern_asset_item(asset_inner, item.replace("_", " ").title(), 
                                       "collectible", item,
                                       f"+{points_map.get(item, 10)} points",
                                       ModernColors.WARNING)
        
        self._add_modern_category(asset_inner, "ENEMIES", "👾", ModernColors.DANGER)
        for enemy in ["slime", "skeleton", "ghost", "robot_enemy", "meme_troll", "boss_slime"]:
            self._add_modern_asset_item(asset_inner, enemy.replace("_", " ").title(),
                                       "enemy", enemy, "", ModernColors.DANGER)
        
        self._add_modern_category(asset_inner, "HAZARDS", "⚠", "#FF9800")
        self._add_modern_asset_item(asset_inner, "Meteor", "hazard", "meteor", 
                                   "Falling hazard", "#FF9800")
        self._add_modern_asset_item(asset_inner, "Lava Pit", "hazard", "lava",
                                   "Floor hazard", "#FF9800")
    
    def _add_modern_category(self, parent, title, icon, color):
        """Add a modern category header"""
        frame = tk.Frame(parent, bg=ModernColors.BG_MEDIUM, height=32)
        frame.pack(fill="x", pady=(14, 4), padx=8)
        frame.pack_propagate(False)
        
        tk.Label(frame, text=f"{icon}  {title}", bg=ModernColors.BG_MEDIUM, fg=color,
                font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x", padx=6, pady=6)
        
        tk.Frame(frame, bg=color, height=2, width=30).place(x=6, y=29)
    
    def _add_modern_asset_item(self, parent, name, asset_type, asset_id, tooltip, color):
        """Add a modern draggable asset item"""
        container = tk.Frame(parent, bg=ModernColors.BG_MEDIUM)
        container.pack(fill="x", padx=8, pady=1)
        
        card = tk.Frame(container, bg=ModernColors.BG_CARD, height=38, cursor="hand2")
        card.pack(fill="x")
        card.pack_propagate(False)
        
        tk.Frame(card, bg=color, width=3).pack(side="left", fill="y")
        
        content = tk.Frame(card, bg=ModernColors.BG_CARD)
        content.pack(side="left", fill="both", expand=True, padx=8)
        
        tk.Label(content, text=name, bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_PRIMARY,
                font=("Segoe UI", 9, "bold"), anchor="w").pack(anchor="w")
        
        if tooltip:
            tk.Label(content, text=tooltip, bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_MUTED,
                    font=("Segoe UI", 7), anchor="w").pack(anchor="w")
        
        def on_enter(e):
            card.configure(bg=ModernColors.BG_HOVER)
            content.configure(bg=ModernColors.BG_HOVER)
            for child in content.winfo_children():
                child.configure(bg=ModernColors.BG_HOVER)
        
        def on_leave(e):
            card.configure(bg=ModernColors.BG_CARD)
            content.configure(bg=ModernColors.BG_CARD)
            for child in content.winfo_children():
                child.configure(bg=ModernColors.BG_CARD)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        content.bind("<Enter>", on_enter)
        content.bind("<Leave>", on_leave)
        
        all_widgets = [card, content] + list(content.winfo_children())
        for widget in all_widgets:
            widget.bind("<Button-1>", lambda e, t=asset_type, i=asset_id: self._start_palette_drag(e, t, i))
            widget.bind("<B1-Motion>", self._on_palette_drag)
            widget.bind("<ButtonRelease-1>", self._on_palette_drop)
    
    def _build_modern_properties(self, parent):
        """Build modern properties panel"""
        prop_frame = tk.Frame(parent, bg=ModernColors.BG_MEDIUM, width=260)
        prop_frame.pack(side="right", fill="y")
        prop_frame.pack_propagate(False)
        
        prop_header = tk.Frame(prop_frame, bg=ModernColors.BG_LIGHT, height=45)
        prop_header.pack(fill="x")
        prop_header.pack_propagate(False)
        
        tk.Label(prop_header, text="PROPERTIES", bg=ModernColors.BG_LIGHT,
                fg=ModernColors.ACCENT_LIGHT, font=("Segoe UI", 11, "bold")).pack(side="left", padx=15, pady=12)
        
        prop_canvas = tk.Canvas(prop_frame, bg=ModernColors.BG_MEDIUM, highlightthickness=0)
        prop_scroll = tk.Scrollbar(prop_frame, orient="vertical", command=prop_canvas.yview)
        prop_inner = tk.Frame(prop_canvas, bg=ModernColors.BG_MEDIUM)
        
        prop_inner.bind("<Configure>", lambda e: prop_canvas.configure(
            scrollregion=prop_canvas.bbox("all")))
        prop_canvas.create_window((0, 0), window=prop_inner, anchor="nw", width=250)
        prop_canvas.configure(yscrollcommand=prop_scroll.set)
        
        prop_canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
        prop_scroll.pack(side="right", fill="y")
        
        def on_mousewheel(event):
            prop_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        prop_canvas.bind("<Enter>", lambda e: prop_canvas.bind_all("<MouseWheel>", on_mousewheel))
        prop_canvas.bind("<Leave>", lambda e: prop_canvas.unbind_all("<MouseWheel>"))
        
        self._add_property_section(prop_inner, "GAME SETTINGS", ModernColors.INFO)
        
        settings_frame = tk.Frame(prop_inner, bg=ModernColors.BG_MEDIUM)
        settings_frame.pack(fill="x", padx=12, pady=4)
        
        tk.Label(settings_frame, text="Name", bg=ModernColors.BG_MEDIUM, 
                fg=ModernColors.TEXT_SECONDARY, font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
        self.game_name_entry = tk.Entry(settings_frame, bg=ModernColors.BG_CARD, 
                                       fg=ModernColors.TEXT_PRIMARY, bd=0,
                                       insertbackground=ModernColors.TEXT_PRIMARY,
                                       font=("Segoe UI", 10))
        self.game_name_entry.pack(fill="x", ipady=8, pady=(0, 8))
        
        tk.Label(settings_frame, text="Difficulty", bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.TEXT_SECONDARY, font=("Segoe UI", 9)).pack(anchor="w", pady=2)
        self.diff_var = tk.StringVar(value="normal")
        diff_menu = tk.OptionMenu(settings_frame, self.diff_var, "easy", "normal", "hard", "memetic")
        diff_menu.configure(bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_PRIMARY, bd=0,
                           font=("Segoe UI", 9), highlightthickness=0, activebackground=ModernColors.BG_HOVER)
        diff_menu["menu"].configure(bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_PRIMARY, bd=0)
        diff_menu.pack(fill="x", ipady=4, pady=(0, 8))
        
        tk.Label(settings_frame, text="Win Condition", bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.TEXT_SECONDARY, font=("Segoe UI", 9)).pack(anchor="w", pady=2)
        self.win_var = tk.StringVar(value="reach_end")
        win_menu = tk.OptionMenu(settings_frame, self.win_var, "reach_end", "target_score", 
                                "high_score", "survival_time", "defeat_boss")
        win_menu.configure(bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_PRIMARY, bd=0,
                          font=("Segoe UI", 9), highlightthickness=0, activebackground=ModernColors.BG_HOVER)
        win_menu["menu"].configure(bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_PRIMARY, bd=0)
        win_menu.pack(fill="x", ipady=4, pady=(0, 8))
        
        tk.Label(settings_frame, text="Lives", bg=ModernColors.BG_MEDIUM,
                fg=ModernColors.TEXT_SECONDARY, font=("Segoe UI", 9)).pack(anchor="w", pady=2)
        self.lives_spinbox = tk.Spinbox(settings_frame, from_=1, to=99, bg=ModernColors.BG_CARD,
                                       fg=ModernColors.TEXT_PRIMARY, bd=0, font=("Segoe UI", 10),
                                       buttonbackground=ModernColors.BG_LIGHT)
        self.lives_spinbox.pack(fill="x", ipady=6, pady=(0, 12))
        self.lives_spinbox.delete(0, "end")
        self.lives_spinbox.insert(0, "3")
        
        self._add_property_section(prop_inner, "SELECTED ASSET", ModernColors.ACCENT)
        
        self.selected_label = tk.Label(prop_inner, text="No asset selected", 
                                       bg=ModernColors.BG_MEDIUM, fg=ModernColors.TEXT_MUTED,
                                       font=("Segoe UI", 9))
        self.selected_label.pack(pady=10, padx=12)
        
        save_frame = tk.Frame(prop_inner, bg=ModernColors.BG_MEDIUM)
        save_frame.pack(fill="x", padx=12, pady=(20, 10))
        
        btn_save_large = AnimatedButton(save_frame, "Save Game", command=self._save_game,
                                       width=220, height=45, color=ModernColors.SUCCESS,
                                       icon="💾", font_size=11)
        btn_save_large.pack()
    
    def _add_property_section(self, parent, title, color):
        """Add a property section header"""
        frame = tk.Frame(parent, bg=ModernColors.BG_MEDIUM)
        frame.pack(fill="x", padx=12, pady=(16, 4))
        
        tk.Label(frame, text=title, bg=ModernColors.BG_MEDIUM, fg=color,
                font=("Segoe UI", 8, "bold")).pack(anchor="w")
        
        tk.Frame(frame, bg=color, height=1).pack(fill="x", pady=(4, 0))
    
    def _set_status(self, message, status_type="info"):
        """Set status with color coding"""
        if not self.status_var or not self.status_label:
            return
        colors = {
            "info": ModernColors.INFO,
            "success": ModernColors.SUCCESS,
            "warning": ModernColors.WARNING,
            "danger": ModernColors.DANGER,
        }
        color = colors.get(status_type, ModernColors.TEXT_MUTED)
        self.status_var.set(message)
        self.status_label.configure(fg=color)
    
    def _setup_canvas_events(self):
        """Setup canvas mouse events"""
        if not self.edit_canvas:
            return
        self.edit_canvas.bind("<Button-1>", self._canvas_click)
        self.edit_canvas.bind("<B1-Motion>", self._canvas_drag)
        self.edit_canvas.bind("<ButtonRelease-1>", self._canvas_release)
        self.edit_canvas.bind("<Button-3>", self._canvas_right_click)
        self.edit_canvas.bind("<Motion>", self._canvas_motion)
        self.edit_canvas.bind("<MouseWheel>", self._canvas_scroll)
        self.edit_canvas.bind("<Control-g>", lambda e: self._toggle_grid())
    
    def _canvas_click(self, event):
        x = self.edit_canvas.canvasx(event.x)
        y = self.edit_canvas.canvasy(event.y)
        
        items = self.edit_canvas.find_overlapping(x-5, y-5, x+5, y+5)
        if items:
            for item in items:
                tags = self.edit_canvas.gettags(item)
                for tag in tags:
                    if tag.startswith("asset_"):
                        self._select_asset(tag)
                        self.drag_start_x = x
                        self.drag_start_y = y
                        self.is_dragging = True
                        return
        
        self._deselect_asset()
        self.drag_start_x = x
        self.drag_start_y = y
        self.is_dragging = False
    
    def _canvas_drag(self, event):
        x = self.edit_canvas.canvasx(event.x)
        y = self.edit_canvas.canvasy(event.y)
        
        if self.is_dragging and self.selected_asset:
            dx = x - self.drag_start_x
            dy = y - self.drag_start_y
            
            if self.snap_enabled:
                dx = round(dx / self.grid_size) * self.grid_size
                dy = round(dy / self.grid_size) * self.grid_size
            
            if dx != 0 or dy != 0:
                self.edit_canvas.move(f"asset_{self.selected_asset}", dx, dy)
                self.edit_canvas.move(f"label_{self.selected_asset}", dx, dy)
                self.drag_start_x = x
                self.drag_start_y = y
                self._update_asset_position(self.selected_asset, dx, dy)
    
    def _canvas_release(self, event):
        self.is_dragging = False
    
    def _canvas_right_click(self, event):
        x = self.edit_canvas.canvasx(event.x)
        y = self.edit_canvas.canvasy(event.y)
        
        items = self.edit_canvas.find_overlapping(x-5, y-5, x+5, y+5)
        if items:
            for item in items:
                tags = self.edit_canvas.gettags(item)
                for tag in tags:
                    if tag.startswith("asset_"):
                        self._select_asset(tag)
                        break
        
        menu = tk.Menu(self.window, tearoff=0, bg=ModernColors.BG_CARD, 
                      fg=ModernColors.TEXT_PRIMARY, bd=1, relief="flat")
        if self.selected_asset:
            menu.add_command(label="📋  Duplicate", command=self._duplicate_selected,
                           font=("Segoe UI", 10))
            menu.add_separator()
            menu.add_command(label="🗑  Delete", command=self._delete_selected,
                           foreground=ModernColors.DANGER, font=("Segoe UI", 10))
            menu.add_separator()
        menu.add_command(label="➕  Add Platform", command=lambda: self._add_platform_at(x, y),
                        font=("Segoe UI", 10))
        menu.add_command(label="🪙  Add Coin", command=lambda: self._add_collectible_at(x, y, "coin"),
                        font=("Segoe UI", 10))
        menu.add_command(label="👾  Add Enemy", command=lambda: self._add_enemy_at(x, y),
                        font=("Segoe UI", 10))
        menu.post(event.x_root, event.y_root)
    
    def _canvas_motion(self, event):
        if not self.pos_var:
            return
        x = int(self.edit_canvas.canvasx(event.x))
        y = int(self.edit_canvas.canvasy(event.y))
        self.pos_var.set(f"X: {x}  Y: {y}")
    
    def _canvas_scroll(self, event):
        self.edit_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _start_palette_drag(self, event, asset_type, asset_id):
        self.drag_asset_type = asset_type
        self.drag_asset_id = asset_id
        self._set_status(f"Placing {asset_id}... Drop on canvas", "info")
    
    def _on_palette_drag(self, event):
        pass
    
    def _on_palette_drop(self, event):
        if hasattr(self, 'drag_asset_type') and hasattr(self, 'drag_asset_id') and self.drag_asset_type:
            canvas_x = self.edit_canvas.winfo_rootx()
            canvas_y = self.edit_canvas.winfo_rooty()
            x = event.x_root - canvas_x + self.edit_canvas.canvasx(0)
            y = event.y_root - canvas_y + self.edit_canvas.canvasy(0)
            
            if self.snap_enabled:
                x = round(x / self.grid_size) * self.grid_size
                y = round(y / self.grid_size) * self.grid_size
            
            self._place_asset(self.drag_asset_type, self.drag_asset_id, int(x), int(y))
            self._set_status(f"✓ Placed {self.drag_asset_id} at ({int(x)}, {int(y)})", "success")
            
            self.drag_asset_type = None
            self.drag_asset_id = None
    
    def _place_asset(self, asset_type, asset_id, x, y):
        if not self.engine.current_game:
            self._set_status("Create a game first!", "warning")
            return
        
        colors = {
            "character": ModernColors.INFO,
            "map": ModernColors.SUCCESS,
            "collectible": ModernColors.WARNING,
            "enemy": ModernColors.DANGER,
            "hazard": "#FF9800",
        }
        color = colors.get(asset_type, "#FFFFFF")
        
        asset_list_key = asset_type + "s"
        if asset_list_key not in self.engine.current_game:
            self.engine.current_game[asset_list_key] = []
        
        count = len(self.engine.current_game[asset_list_key])
        asset_key = f"{asset_type}_{asset_id}_{count}"
        tag = f"asset_{asset_key}"
        label_tag = f"label_{asset_key}"
        
        if asset_type == "character":
            char_data = PRESET_CHARACTERS.get(asset_id, {})
            w = char_data.get("width", 40)
            h = char_data.get("height", 50)
            self.edit_canvas.create_oval(x, y, x + w, y + h, fill=color, outline="white", 
                                        width=2, tags=(tag, "asset", "character"))
            self.edit_canvas.create_text(x + w//2, y - 10, text=char_data.get("name", asset_id),
                                        fill="white", font=("Segoe UI", 8), tags=(label_tag, "label", tag))
            self.engine.current_game[asset_list_key].append({
                "id": asset_id, "x": x, "y": y, "type": asset_id
            })
            
        elif asset_type == "collectible":
            self.edit_canvas.create_oval(x, y, x + 24, y + 24, fill=color, outline="white",
                                        width=2, tags=(tag, "asset", "collectible"))
            self.edit_canvas.create_text(x + 12, y + 12, text=asset_id[0].upper(),
                                        fill="white", font=("Segoe UI", 10, "bold"), 
                                        tags=(label_tag, "label", tag))
            self.engine.current_game[asset_list_key].append({
                "x": x, "y": y, "type": asset_id
            })
            
        elif asset_type == "enemy":
            self.edit_canvas.create_rectangle(x, y, x + 36, y + 36, fill=color, outline="white",
                                             width=2, tags=(tag, "asset", "enemy"))
            self.edit_canvas.create_text(x + 18, y + 18, text="E", fill="white",
                                        font=("Segoe UI", 12, "bold"), tags=(label_tag, "label", tag))
            self.engine.current_game[asset_list_key].append({
                "x": x, "y": y, "type": asset_id, "patrol": 100, "speed": 2, "damage": 10
            })
            
        elif asset_type == "map":
            self.engine.current_game["map"] = asset_id
            self._refresh_canvas()
            self._set_status(f"✓ Map changed to {asset_id}", "success")
            
        elif asset_type == "hazard":
            self.edit_canvas.create_polygon(x, y, x + 40, y, x + 20, y + 40,
                                           fill=color, outline="white", width=2, 
                                           tags=(tag, "asset", "hazard"))
            self.edit_canvas.create_text(x + 20, y + 15, text="⚠", fill="white",
                                        font=("Segoe UI", 14, "bold"), tags=(label_tag, "label", tag))
            self.engine.current_game[asset_list_key].append({
                "x": x, "y": y, "width": 40, "height": 40, "type": asset_id,
                "fall_speed": 5 if asset_id == "meteor" else 0
            })
    
    def _select_asset(self, tag):
        self._deselect_asset()
        self.selected_asset = tag.replace("asset_", "")
        for item in self.edit_canvas.find_withtag(tag):
            try:
                self.edit_canvas.itemconfig(item, outline=ModernColors.ACCENT_LIGHT, width=3)
            except tk.TclError:
                pass
        if self.selected_label:
            self.selected_label.config(text=f"Selected:\n{self.selected_asset[:25]}", 
                                       fg=ModernColors.ACCENT_LIGHT)
        self._set_status(f"Selected {self.selected_asset[:30]}", "info")
    
    def _deselect_asset(self):
        if self.selected_asset:
            tag = f"asset_{self.selected_asset}"
            for item in self.edit_canvas.find_withtag(tag):
                try:
                    self.edit_canvas.itemconfig(item, outline="white", width=2)
                except tk.TclError:
                    pass
            self.selected_asset = None
            if self.selected_label:
                self.selected_label.config(text="No asset selected", fg=ModernColors.TEXT_MUTED)
    
    def _delete_selected(self):
        if not self.selected_asset:
            return
        
        tag = f"asset_{self.selected_asset}"
        label_tag = f"label_{self.selected_asset}"
        self.edit_canvas.delete(tag)
        self.edit_canvas.delete(label_tag)
        
        parts = self.selected_asset.split("_")
        if len(parts) >= 2:
            asset_type = parts[0]
            if asset_type == "character" and "characters" in self.engine.current_game:
                idx = int(parts[2]) if len(parts) > 2 else -1
                if 0 <= idx < len(self.engine.current_game["characters"]):
                    del self.engine.current_game["characters"][idx]
            elif asset_type == "collectible" and "collectibles" in self.engine.current_game:
                idx = int(parts[2]) if len(parts) > 2 else -1
                if 0 <= idx < len(self.engine.current_game["collectibles"]):
                    del self.engine.current_game["collectibles"][idx]
            elif asset_type == "enemy" and "enemies" in self.engine.current_game:
                idx = int(parts[2]) if len(parts) > 2 else -1
                if 0 <= idx < len(self.engine.current_game["enemies"]):
                    del self.engine.current_game["enemies"][idx]
            elif asset_type == "hazard" and "hazards" in self.engine.current_game:
                idx = int(parts[2]) if len(parts) > 2 else -1
                if 0 <= idx < len(self.engine.current_game["hazards"]):
                    del self.engine.current_game["hazards"][idx]
        
        self._deselect_asset()
        self._set_status("✓ Asset deleted", "warning")
    
    def _duplicate_selected(self):
        if not self.selected_asset:
            return
        
        parts = self.selected_asset.split("_", 2)
        if len(parts) >= 3:
            asset_type = parts[0]
            asset_id = parts[1]
            
            tag = f"asset_{self.selected_asset}"
            coords = self.edit_canvas.coords(tag)
            if coords:
                new_x = coords[0] + 60
                new_y = coords[1] + 60
                self._place_asset(asset_type, asset_id, int(new_x), int(new_y))
                self._set_status("✓ Asset duplicated", "success")
    
    def _add_platform_at(self, x, y):
        if not self.engine.current_game:
            return
        tag = f"asset_platform_{int(x)}_{int(y)}"
        self.edit_canvas.create_rectangle(x, y, x + 200, y + 20, fill="#8B4513", outline="#654321",
                                         width=2, tags=(tag, "asset", "platform"))
        if "platforms" not in self.engine.current_game:
            self.engine.current_game["platforms"] = []
        self.engine.current_game["platforms"].append({
            "x": x, "y": y, "width": 200, "height": 20, "type": "static"
        })
        self._set_status("✓ Platform added", "success")
    
    def _add_collectible_at(self, x, y, coll_type):
        self._place_asset("collectible", coll_type, x, y)
    
    def _add_enemy_at(self, x, y):
        self._place_asset("enemy", "slime", x, y)
    
    def _update_asset_position(self, asset_key, dx, dy):
        parts = asset_key.split("_")
        if len(parts) < 3:
            return
        
        asset_type = parts[0]
        try:
            idx = int(parts[2])
        except ValueError:
            return
        
        if asset_type == "character" and "characters" in self.engine.current_game:
            if 0 <= idx < len(self.engine.current_game["characters"]):
                self.engine.current_game["characters"][idx]["x"] += dx
                self.engine.current_game["characters"][idx]["y"] += dy
        elif asset_type == "collectible" and "collectibles" in self.engine.current_game:
            if 0 <= idx < len(self.engine.current_game["collectibles"]):
                self.engine.current_game["collectibles"][idx]["x"] += dx
                self.engine.current_game["collectibles"][idx]["y"] += dy
        elif asset_type == "enemy" and "enemies" in self.engine.current_game:
            if 0 <= idx < len(self.engine.current_game["enemies"]):
                self.engine.current_game["enemies"][idx]["x"] += dx
                self.engine.current_game["enemies"][idx]["y"] += dy
    
    def _refresh_canvas(self):
        if not self.edit_canvas:
            return
        
        self.edit_canvas.delete("all")
        
        if self.grid_enabled:
            canvas_width = 2400
            canvas_height = 1200
            for x in range(0, canvas_width, self.grid_size):
                self.edit_canvas.create_line(x, 0, x, canvas_height, 
                                            fill=ModernColors.BORDER, dash=(2, 4))
            for y in range(0, canvas_height, self.grid_size):
                self.edit_canvas.create_line(0, y, canvas_width, y, 
                                            fill=ModernColors.BORDER, dash=(2, 4))
        
        self.edit_canvas.create_line(0, 500, 2400, 500, 
                                     fill=ModernColors.SUCCESS, width=2, dash=(10, 5))
        
        if not self.engine.current_game:
            self.edit_canvas.create_text(400, 280, text="🎮  No Game Loaded", 
                                        fill=ModernColors.TEXT_MUTED, font=("Segoe UI", 20))
            self.edit_canvas.create_text(400, 320, text="Create a new game or load an existing one",
                                        fill=ModernColors.TEXT_MUTED, font=("Segoe UI", 11))
            self.edit_canvas.create_text(400, 350, text="Then drag assets from the palette to build your world",
                                        fill=ModernColors.TEXT_MUTED, font=("Segoe UI", 9))
            return
        
        game = self.engine.current_game
        map_id = game.get("map", "grassy_hills")
        map_data = PRESET_MAPS.get(map_id, PRESET_MAPS["grassy_hills"])
        
        platforms = game.get("platforms", [])
        if not platforms:
            platforms = map_data.get("platforms", [])
        for plat in platforms:
            x, y = plat["x"], plat["y"]
            w, h = plat.get("width", 200), plat.get("height", 20)
            plat_type = plat.get("type", "static")
            colors = {
                "static": ("#8B4513", "#654321"),
                "moving": ("#4169E1", "#1E90FF"),
                "crumbling": ("#A0522D", "#8B4513"),
                "sinking": ("#DAA520", "#B8860B"),
                "bouncy": ("#FF69B4", "#FF1493"),
            }
            color1, color2 = colors.get(plat_type, ("#808080", "#606060"))
            self.edit_canvas.create_rectangle(x, y, x + w, y + h,
                                             fill=color1, outline=color2, width=2)
        
        for haz in map_data.get("hazards", []):
            hx, hy = haz["x"], haz["y"]
            hw, hh = haz.get("width", 40), haz.get("height", 40)
            if haz.get("type") == "lava":
                self.edit_canvas.create_rectangle(hx, hy, hx + hw, hy + hh,
                                                 fill="#FF4500", outline="#FF0000", width=2)
            elif haz.get("type") == "meteor":
                self.edit_canvas.create_oval(hx, hy, hx + hw, hy + hh,
                                            fill="#FF4500", outline="#FF0000", width=2)
        
        for haz in game.get("hazards", []):
            hx, hy = haz["x"], haz["y"]
            hw, hh = haz.get("width", 40), haz.get("height", 40)
            if haz.get("type") == "lava":
                self.edit_canvas.create_rectangle(hx, hy, hx + hw, hy + hh,
                                                 fill="#FF4500", outline="#FF0000", width=2)
            elif haz.get("type") == "meteor":
                self.edit_canvas.create_oval(hx, hy, hx + hw, hy + hh,
                                            fill="#FF4500", outline="#FF0000", width=2)
        
        spawn = map_data.get("spawn_point", (100, 420))
        self.edit_canvas.create_oval(spawn[0]-6, spawn[1]-6, spawn[0]+6, spawn[1]+6,
                                    fill=ModernColors.SUCCESS, outline="")
        self.edit_canvas.create_text(spawn[0], spawn[1]-18, text="SPAWN", 
                                    fill=ModernColors.SUCCESS, font=("Segoe UI", 7, "bold"))
        
        end = map_data.get("end_point", (2200, 420))
        self.edit_canvas.create_rectangle(end[0]-15, end[1]-35, end[0]+15, end[1],
                                         fill="", outline=ModernColors.WARNING, width=2)
        self.edit_canvas.create_text(end[0], end[1]-45, text="END", 
                                    fill=ModernColors.WARNING, font=("Segoe UI", 7, "bold"))
        
        self._draw_user_assets_batched(game, map_data, 0)
    
    def _draw_user_assets_batched(self, game, map_data, start_index):
        characters = game.get("characters", [])
        if start_index < len(characters):
            char = characters[start_index]
            self._place_asset_quiet("character", char.get("type", "memebot"), char["x"], char["y"])
            self.window.after(1, lambda: self._draw_user_assets_batched(game, map_data, start_index + 1))
            return
        
        collectibles = game.get("collectibles", [])
        if not collectibles:
            collectibles = map_data.get("collectibles", [])
        coll_start = start_index - len(characters)
        if coll_start < len(collectibles):
            coll = collectibles[coll_start]
            self._place_asset_quiet("collectible", coll.get("type", "coin"), coll["x"], coll["y"])
            self.window.after(1, lambda: self._draw_user_assets_batched(game, map_data, start_index + 1))
            return
        
        enemies = game.get("enemies", [])
        if not enemies:
            enemies = map_data.get("enemies", [])
        enemy_start = start_index - len(characters) - len(collectibles)
        if enemy_start < len(enemies):
            enemy = enemies[enemy_start]
            self._place_asset_quiet("enemy", enemy.get("type", "slime"), enemy["x"], enemy["y"])
            self.window.after(1, lambda: self._draw_user_assets_batched(game, map_data, start_index + 1))
            return
    
    def _place_asset_quiet(self, asset_type, asset_id, x, y):
        colors = {
            "character": ModernColors.INFO,
            "map": ModernColors.SUCCESS,
            "collectible": ModernColors.WARNING,
            "enemy": ModernColors.DANGER,
            "hazard": "#FF9800",
        }
        color = colors.get(asset_type, "#FFFFFF")
        
        if asset_type == "character":
            char_data = PRESET_CHARACTERS.get(asset_id, {})
            w = char_data.get("width", 40)
            h = char_data.get("height", 50)
            self.edit_canvas.create_oval(x, y, x + w, y + h, fill=color, outline="white", width=2)
            self.edit_canvas.create_text(x + w//2, y - 10, text=char_data.get("name", asset_id),
                                        fill="white", font=("Segoe UI", 8))
        elif asset_type == "collectible":
            self.edit_canvas.create_oval(x, y, x + 24, y + 24, fill=color, outline="white", width=2)
            self.edit_canvas.create_text(x + 12, y + 12, text=asset_id[0].upper(),
                                        fill="white", font=("Segoe UI", 10, "bold"))
        elif asset_type == "enemy":
            self.edit_canvas.create_rectangle(x, y, x + 36, y + 36, fill=color, outline="white", width=2)
            self.edit_canvas.create_text(x + 18, y + 18, text="E", fill="white",
                                        font=("Segoe UI", 12, "bold"))
    
    def _toggle_grid(self):
        self.grid_enabled = not self.grid_enabled
        if self.grid_btn:
            self.grid_btn.configure(fg=ModernColors.SUCCESS if self.grid_enabled else ModernColors.TEXT_MUTED)
        self._refresh_canvas()
        self._set_status(f"Grid: {'ON' if self.grid_enabled else 'OFF'}", "info")
    
    def _toggle_snap(self):
        self.snap_enabled = not self.snap_enabled
        if self.snap_btn:
            self.snap_btn.configure(fg=ModernColors.SUCCESS if self.snap_enabled else ModernColors.TEXT_MUTED)
        self._set_status(f"Snap: {'ON' if self.snap_enabled else 'OFF'}", "info")
    
    def _play_game(self):
        if not self.engine.current_game:
            messagebox.showwarning("No Game", "Create or load a game first!")
            return
        
        self._save_game()
        
        self.game_window = tk.Toplevel(self.window)
        self.game_window.title(f"MEMEEngine - {self.engine.current_game.get('name', 'Game')}")
        self.game_window.geometry("800x600")
        self.game_window.configure(bg="black")
        self.game_window.protocol("WM_DELETE_WINDOW", self._stop_game)
        
        self.game_canvas = tk.Canvas(self.game_window, bg="black", width=800, height=600,
                                     highlightthickness=0)
        self.game_canvas.pack(fill="both", expand=True)
        
        self.engine.load_game_runtime()
        
        self.game_window.bind("<KeyPress>", lambda e: self.engine.handle_input(e.keysym, True))
        self.game_window.bind("<KeyRelease>", lambda e: self.engine.handle_input(e.keysym, False))
        self.game_window.bind("<r>", lambda e: self.engine.restart())
        self.game_window.bind("<R>", lambda e: self.engine.restart())
        self.game_window.bind("<Escape>", lambda e: self._stop_game())
        self.game_window.bind("<p>", lambda e: self._pause_game())
        self.game_window.bind("<P>", lambda e: self._pause_game())
        
        self.game_canvas.focus_set()
        self.game_window.update()
        
        self.game_loop_running = True
        self._run_game_loop()
        
        self._set_status("▶ Game running! Arrow Keys to move, Space to jump, ESC to stop", "success")
    
    def _run_game_loop(self):
        if not self.game_loop_running or not self.game_window:
            return
        
        try:
            if not self.game_window.winfo_exists():
                self._stop_game()
                return
            
            if self.engine.is_playing and not self.engine.is_paused:
                self.engine.update()
                self.engine.render(self.game_canvas)
            
            self.game_window.after(self.engine.frame_delay, self._run_game_loop)
            
        except tk.TclError:
            self._stop_game()
    
    def _pause_game(self):
        if self.engine.is_playing:
            self.engine.is_paused = not self.engine.is_paused
            self._set_status("⏸ Game paused" if self.engine.is_paused else "▶ Game resumed", "warning")
    
    def _stop_game(self):
        self.game_loop_running = False
        self.engine.is_playing = False
        self.engine.is_paused = False
        
        if self.game_window:
            try:
                self.game_window.destroy()
            except tk.TclError:
                pass
            self.game_window = None
            self.game_canvas = None
        
        self._set_status("⏹ Game stopped", "info")
    
    def _new_game_dialog(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("New Game")
        dialog.geometry("520x620")
        dialog.configure(bg=ModernColors.BG_DARK)
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.focus_force()
        
        dialog.update_idletasks()
        x = dialog.winfo_screenwidth() // 2 - 260
        y = dialog.winfo_screenheight() // 2 - 310
        dialog.geometry(f"520x620+{x}+{y}")
        
        header = tk.Frame(dialog, bg=ModernColors.BG_MEDIUM, height=55)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🎮  Create New Game", bg=ModernColors.BG_MEDIUM, 
                fg=ModernColors.TEXT_PRIMARY, font=("Segoe UI", 16, "bold")).pack(pady=12)
        
        tk.Label(dialog, text="Choose a template to get started:", bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY, font=("Segoe UI", 10)).pack(pady=(15, 5))
        
        list_frame = tk.Frame(dialog, bg=ModernColors.BG_DARK)
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        list_canvas = tk.Canvas(list_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        list_scroll = tk.Scrollbar(list_frame, orient="vertical", command=list_canvas.yview)
        list_inner = tk.Frame(list_canvas, bg=ModernColors.BG_DARK)
        
        list_inner.bind("<Configure>", lambda e: list_canvas.configure(
            scrollregion=list_canvas.bbox("all")))
        list_canvas.create_window((0, 0), window=list_inner, anchor="nw", width=480)
        list_canvas.configure(yscrollcommand=list_scroll.set)
        
        list_canvas.pack(side="left", fill="both", expand=True)
        list_scroll.pack(side="right", fill="y")
        
        def select_template(template_id):
            self.engine.create_new_game(template_id)
            dialog.destroy()
            self._refresh_canvas()
            
            if self.engine.current_game:
                if self.game_name_entry:
                    self.game_name_entry.delete(0, "end")
                    self.game_name_entry.insert(0, self.engine.current_game.get("name", ""))
                if self.win_var:
                    self.win_var.set(self.engine.current_game.get("win_condition", "reach_end"))
            
            self._set_status(f"✓ Created: {self.engine.current_game.get('name', 'Untitled')}", "success")
        
        for template_id, template in GAME_TEMPLATES.items():
            card = tk.Frame(list_inner, bg=ModernColors.BG_CARD, bd=0, cursor="hand2")
            card.pack(fill="x", padx=5, pady=4)
            
            tk.Label(card, text=f"🎮  {template['name']}", bg=ModernColors.BG_CARD,
                    fg=ModernColors.ACCENT_LIGHT, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(8, 2))
            tk.Label(card, text=template["description"], bg=ModernColors.BG_CARD,
                    fg=ModernColors.TEXT_SECONDARY, wraplength=440, font=("Segoe UI", 9)).pack(anchor="w", padx=12)
            
            info = f"Win: {template['win_condition']}  |  Controls: {', '.join(template['default_controls'].keys())}"
            tk.Label(card, text=info, bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_MUTED,
                    font=("Segoe UI", 8)).pack(anchor="w", padx=12, pady=(2, 8))
            
            def on_enter(e, c=card):
                c.configure(bg=ModernColors.BG_HOVER)
                for child in c.winfo_children():
                    child.configure(bg=ModernColors.BG_HOVER)
            
            def on_leave(e, c=card):
                c.configure(bg=ModernColors.BG_CARD)
                for child in c.winfo_children():
                    child.configure(bg=ModernColors.BG_CARD)
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            card.bind("<Button-1>", lambda e, t=template_id: select_template(t))
            for child in card.winfo_children():
                child.bind("<Enter>", on_enter)
                child.bind("<Leave>", on_leave)
                child.bind("<Button-1>", lambda e, t=template_id: select_template(t))
        
        bottom_frame = tk.Frame(dialog, bg=ModernColors.BG_DARK, height=55)
        bottom_frame.pack(fill="x", side="bottom", pady=12)
        bottom_frame.pack_propagate(False)
        
        btn_blank = AnimatedButton(bottom_frame, "Start from Scratch", 
                                  command=lambda: select_template(None),
                                  width=200, height=38, color=ModernColors.BG_LIGHT,
                                  icon="📄", font_size=10)
        btn_blank.pack()
    
    def _load_game_dialog(self):
        games = self.engine.get_available_games()
        
        if not games:
            messagebox.showinfo("No Games", "No saved games found! Create one first.")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Load Game")
        dialog.geometry("550x480")
        dialog.configure(bg=ModernColors.BG_DARK)
        dialog.transient(self.window)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = dialog.winfo_screenwidth() // 2 - 275
        y = dialog.winfo_screenheight() // 2 - 240
        dialog.geometry(f"550x480+{x}+{y}")
        
        header = tk.Frame(dialog, bg=ModernColors.BG_MEDIUM, height=55)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📂  Load Game", bg=ModernColors.BG_MEDIUM, 
                fg=ModernColors.TEXT_PRIMARY, font=("Segoe UI", 16, "bold")).pack(pady=12)
        
        for game in games:
            card = tk.Frame(dialog, bg=ModernColors.BG_CARD, bd=0, cursor="hand2")
            card.pack(fill="x", padx=20, pady=4)
            
            tk.Label(card, text=game["name"], bg=ModernColors.BG_CARD,
                    fg=ModernColors.ACCENT_LIGHT, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(8, 2))
            
            info = f"Template: {game['template']}  •  Author: {game['author']}"
            tk.Label(card, text=info, bg=ModernColors.BG_CARD, fg=ModernColors.TEXT_MUTED,
                    font=("Segoe UI", 8)).pack(anchor="w", padx=12, pady=(2, 8))
            
            def on_enter(e, c=card):
                c.configure(bg=ModernColors.BG_HOVER)
                for child in c.winfo_children():
                    child.configure(bg=ModernColors.BG_HOVER)
            
            def on_leave(e, c=card):
                c.configure(bg=ModernColors.BG_CARD)
                for child in c.winfo_children():
                    child.configure(bg=ModernColors.BG_CARD)
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            card.bind("<Button-1>", lambda e, p=game["path"]: self._load_selected_game(p, dialog))
            for child in card.winfo_children():
                child.bind("<Enter>", on_enter)
                child.bind("<Leave>", on_leave)
                child.bind("<Button-1>", lambda e, p=game["path"]: self._load_selected_game(p, dialog))
    
    def _load_selected_game(self, path, dialog):
        game = self.engine.load_game(Path(path))
        dialog.destroy()
        
        if game:
            if self.game_name_entry:
                self.game_name_entry.delete(0, "end")
                self.game_name_entry.insert(0, game.get("name", ""))
            if self.win_var:
                self.win_var.set(game.get("win_condition", "reach_end"))
            self._set_status(f"✓ Loaded: {game.get('name', 'Game')}", "success")
        
        self.window.after(100, self._refresh_canvas)
    
    def _save_game(self):
        if not self.engine.current_game:
            messagebox.showwarning("No Game", "Nothing to save!")
            return
        
        if self.game_name_entry:
            self.engine.current_game["name"] = self.game_name_entry.get()
        if self.diff_var:
            self.engine.current_game["difficulty"] = self.diff_var.get()
        if self.win_var:
            self.engine.current_game["win_condition"] = self.win_var.get()
        if self.lives_spinbox:
            try:
                self.engine.current_game["lives"] = int(self.lives_spinbox.get())
            except:
                pass
        
        if self.engine.save_game():
            self._set_status(f"✓ Saved: {self.engine.current_game.get('name', '')}", "success")
        else:
            messagebox.showerror("Error", "Failed to save game!")
    
    def _save_game_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("MEME Game", "*.json")],
            initialdir=self.engine.games_path
        )
        if file_path:
            if self.game_name_entry:
                self.engine.current_game["name"] = self.game_name_entry.get()
            if self.diff_var:
                self.engine.current_game["difficulty"] = self.diff_var.get()
            if self.win_var:
                self.engine.current_game["win_condition"] = self.win_var.get()
            
            if self.engine.save_game(Path(file_path)):
                self._set_status(f"✓ Saved as: {Path(file_path).name}", "success")
    
    def hide(self):
        if self.game_loop_running:
            self._stop_game()
        if self.window:
            self.window.withdraw()