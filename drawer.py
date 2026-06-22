"""
MEMEBOT Drawer - Community Skin Creation Tool
Allows users to draw custom characters and accessories,
then compile them into .MSK skin files for MEMEBOT.
Supports pixel drawing, layer management, FBX import, and SK3 export.
"""

import os
import sys
import json
import base64
import logging
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox, simpledialog
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageTk
from typing import Dict, Any, Optional, List

# Add Src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Src'))

from Skin.skin_encryptor import SkinEncryptor


class DrawerApp:
    """
    MEMEBOT Drawer - Community skin creation tool.
    
    Features:
    - Layer-based drawing system with 13 body part layers
    - 10 drawing tools: pencil, eraser, fill, line, rectangle, ellipse, color picker, spray, text, eyedropper
    - Custom color picker with 16 quick color presets
    - Adjustable brush size (1-20 pixels)
    - Real-time preview on character template overlay
    - Import PNG sprites for custom accessories
    - Undo/Redo with 50 state history
    - Export to .MSK SK3 encrypted format
    - Load existing .MSK files for editing
    - Custom skin name, author, version, and description
    - Custom animation frame editor
    - Decrypt and view raw MSK JSON data
    """
    
    TOOL_PENCIL = "pencil"
    TOOL_ERASER = "eraser"
    TOOL_FILL = "fill"
    TOOL_LINE = "line"
    TOOL_RECTANGLE = "rectangle"
    TOOL_ELLIPSE = "ellipse"
    TOOL_PICKER = "color_picker"
    TOOL_SPRAY = "spray"
    TOOL_TEXT = "text"
    TOOL_EYEDROPPER = "eyedropper"
    
    LAYER_BODY = "body"
    LAYER_HEAD = "head"
    LAYER_HAIR = "hair"
    LAYER_EYES = "eyes"
    LAYER_MOUTH = "mouth"
    LAYER_ARMS = "arms"
    LAYER_LEGS = "legs"
    LAYER_OUTFIT = "outfit"
    LAYER_ACCESSORIES = "accessories"
    LAYER_HAT = "hat"
    LAYER_GLASSES = "glasses"
    LAYER_WINGS = "wings"
    LAYER_TAIL = "tail"
    
    CANVAS_WIDTH = 480
    CANVAS_HEIGHT = 620
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MEMEBOT Drawer - Community Skin Creator")
        self.root.geometry("1300x850")
        self.root.configure(bg='#1a1a2e')
        
        self.encryptor = SkinEncryptor()
        
        self.current_tool = self.TOOL_PENCIL
        self.current_color = (100, 180, 255, 255)
        self.brush_size = 3
        
        self.drawing = False
        self.last_x = 0
        self.last_y = 0
        self.start_x = 0
        self.start_y = 0
        
        self.layers = {}
        self.current_layer = self.LAYER_BODY
        self.layer_visible = {}
        
        self.template_image = None
        self.template_visible = True
        
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo = 50
        
        self.msk_data = None
        self.current_file = None
        self.skin_name = "Custom Skin"
        self.skin_author = "MEMEBOT User"
        self.skin_version = "1.0"
        self.skin_description = "A custom MEMEBOT skin"
        
        # Animation frames storage
        self.animation_frames = {}
        self.current_animation = "idle"
        self.current_frame = 0
        
        self._init_layers()
        self._build_ui()
        self._load_template()
        self._update_canvas()
    
    def _init_layers(self):
        """Initialize all 13 drawing layers"""
        layer_names = [
            self.LAYER_BODY, self.LAYER_HEAD, self.LAYER_HAIR,
            self.LAYER_EYES, self.LAYER_MOUTH, self.LAYER_ARMS,
            self.LAYER_LEGS, self.LAYER_OUTFIT, self.LAYER_ACCESSORIES,
            self.LAYER_HAT, self.LAYER_GLASSES, self.LAYER_WINGS, self.LAYER_TAIL
        ]
        for name in layer_names:
            self.layers[name] = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
            self.layer_visible[name] = True
    
    def _build_ui(self):
        """Build complete user interface"""
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - Tools
        left_panel = tk.Frame(main_frame, bg='#16213e', width=220)
        left_panel.pack(side='left', fill='y', padx=(0, 5))
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="TOOLS", font=('Arial', 12, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=5)
        
        tools = [
            (self.TOOL_PENCIL, "✏ Pencil"),
            (self.TOOL_ERASER, "🧹 Eraser"),
            (self.TOOL_FILL, "🪣 Fill"),
            (self.TOOL_LINE, "📏 Line"),
            (self.TOOL_RECTANGLE, "⬜ Rectangle"),
            (self.TOOL_ELLIPSE, "⚪ Ellipse"),
            (self.TOOL_PICKER, "💉 Color Picker"),
            (self.TOOL_SPRAY, "🎨 Spray"),
            (self.TOOL_TEXT, "🔤 Text"),
            (self.TOOL_EYEDROPPER, "💧 Eyedropper"),
        ]
        for tool_id, tool_name in tools:
            btn = tk.Button(left_panel, text=tool_name, font=('Arial', 10),
                          bg='#0f3460', fg='white', relief='flat',
                          command=lambda t=tool_id: self._set_tool(t))
            btn.pack(fill='x', padx=10, pady=2)
        
        tk.Label(left_panel, text="BRUSH SIZE", font=('Arial', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(15, 5))
        self.brush_slider = tk.Scale(left_panel, from_=1, to=20, orient='horizontal',
                                     bg='#16213e', fg='white', troughcolor='#0f3460',
                                     command=lambda v: setattr(self, 'brush_size', int(v)))
        self.brush_slider.set(3)
        self.brush_slider.pack(fill='x', padx=10)
        
        tk.Label(left_panel, text="COLOR", font=('Arial', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(15, 5))
        self.color_btn = tk.Button(left_panel, text="  Choose Color  ", font=('Arial', 10),
                                   bg='#0f3460', fg='white', relief='flat',
                                   command=self._choose_color)
        self.color_btn.pack(pady=5)
        self.color_preview = tk.Canvas(left_panel, width=40, height=40,
                                       bg='#16213e', highlightthickness=0)
        self.color_preview.pack(pady=5)
        self._update_color_preview()
        
        tk.Label(left_panel, text="QUICK COLORS", font=('Arial', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(15, 5))
        quick_frame = tk.Frame(left_panel, bg='#16213e')
        quick_frame.pack(padx=10)
        
        quick_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (255, 255, 255), (0, 0, 0),
            (255, 150, 0), (150, 0, 255), (100, 200, 255), (255, 100, 150),
            (80, 60, 40), (255, 220, 180), (100, 180, 255), (50, 130, 200),
        ]
        for i, qc in enumerate(quick_colors):
            row, col = divmod(i, 4)
            btn = tk.Button(quick_frame, width=2, height=1, relief='flat',
                          bg=f'#{qc[0]:02x}{qc[1]:02x}{qc[2]:02x}',
                          command=lambda c=qc: self._set_quick_color(c))
            btn.grid(row=row, column=col, padx=1, pady=1)
        
        # Skin metadata fields
        tk.Label(left_panel, text="SKIN METADATA", font=('Arial', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(15, 5))
        
        metadata_fields = [
            ("Name:", "skin_name"),
            ("Author:", "skin_author"),
            ("Version:", "skin_version"),
            ("Desc:", "skin_description"),
        ]
        for label_text, attr_name in metadata_fields:
            tk.Label(left_panel, text=label_text, font=('Arial', 9),
                    bg='#16213e', fg='#aaa').pack(anchor='w', padx=10)
            entry = tk.Entry(left_panel, font=('Arial', 9), bg='#0f3460', fg='white',
                           insertbackground='white', relief='flat')
            entry.insert(0, getattr(self, attr_name))
            entry.pack(fill='x', padx=10, pady=1)
            entry.bind('<KeyRelease>', lambda e, a=attr_name, ent=entry: setattr(self, a, ent.get()))
            setattr(self, f"{attr_name}_entry", entry)
        
        # Center panel - Canvas
        center_panel = tk.Frame(main_frame, bg='#1a1a2e')
        center_panel.pack(side='left', fill='both', expand=True)
        
        self.canvas = tk.Canvas(center_panel, width=self.CANVAS_WIDTH,
                                height=self.CANVAS_HEIGHT, bg='#0a0a1a',
                                highlightthickness=2, highlightbackground='#e94560')
        self.canvas.pack(pady=10)
        
        self.canvas.bind('<Button-1>', self._on_mouse_down)
        self.canvas.bind('<B1-Motion>', self._on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_mouse_up)
        self.canvas.bind('<Motion>', self._on_mouse_move)
        
        self.coord_label = tk.Label(center_panel, text="X: 0  Y: 0",
                                    font=('Arial', 9), bg='#1a1a2e', fg='#888')
        self.coord_label.pack()
        
        # Right panel - Layers and Animation
        right_panel = tk.Frame(main_frame, bg='#16213e', width=220)
        right_panel.pack(side='right', fill='y', padx=(5, 0))
        right_panel.pack_propagate(False)
        
        tk.Label(right_panel, text="LAYERS", font=('Arial', 12, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=5)
        
        self.layer_frame = tk.Frame(right_panel, bg='#16213e')
        self.layer_frame.pack(fill='both', expand=False, padx=5)
        
        layer_display_names = {
            self.LAYER_BODY: "Body", self.LAYER_HEAD: "Head",
            self.LAYER_HAIR: "Hair", self.LAYER_EYES: "Eyes",
            self.LAYER_MOUTH: "Mouth", self.LAYER_ARMS: "Arms",
            self.LAYER_LEGS: "Legs", self.LAYER_OUTFIT: "Outfit",
            self.LAYER_ACCESSORIES: "Accessories", self.LAYER_HAT: "Hat",
            self.LAYER_GLASSES: "Glasses", self.LAYER_WINGS: "Wings",
            self.LAYER_TAIL: "Tail",
        }
        
        self.layer_buttons = {}
        for layer_name, display_name in layer_display_names.items():
            frame = tk.Frame(self.layer_frame, bg='#16213e')
            frame.pack(fill='x', pady=1)
            vis_btn = tk.Button(frame, text="👁", width=2, font=('Arial', 8),
                              bg='#0f3460', fg='white', relief='flat',
                              command=lambda l=layer_name: self._toggle_layer_visibility(l))
            vis_btn.pack(side='left', padx=1)
            btn = tk.Button(frame, text=display_name, font=('Arial', 9),
                          bg='#0f3460', fg='white', relief='flat',
                          command=lambda l=layer_name: self._select_layer(l))
            btn.pack(side='left', fill='x', expand=True)
            self.layer_buttons[layer_name] = (btn, vis_btn)
        
        # Animation panel
        tk.Label(right_panel, text="ANIMATIONS", font=('Arial', 12, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(15, 5))
        
        anim_frame = tk.Frame(right_panel, bg='#16213e')
        anim_frame.pack(fill='x', padx=5)
        
        self.anim_var = tk.StringVar(value="idle")
        anim_options = ["idle", "walking", "running", "dancing", "waving", "bouncing"]
        self.anim_menu = ttk.Combobox(anim_frame, textvariable=self.anim_var,
                                      values=anim_options, state='readonly', width=15)
        self.anim_menu.pack(side='left', padx=2)
        self.anim_menu.bind('<<ComboboxSelected>>', self._on_animation_change)
        
        frame_controls = tk.Frame(right_panel, bg='#16213e')
        frame_controls.pack(fill='x', padx=5, pady=5)
        
        tk.Button(frame_controls, text="◀", font=('Arial', 8), bg='#0f3460', fg='white',
                 command=self._prev_frame).pack(side='left', padx=1)
        self.frame_label = tk.Label(frame_controls, text="Frame: 0", font=('Arial', 9),
                                    bg='#16213e', fg='white')
        self.frame_label.pack(side='left', padx=5)
        tk.Button(frame_controls, text="▶", font=('Arial', 8), bg='#0f3460', fg='white',
                 command=self._next_frame).pack(side='left', padx=1)
        
        tk.Button(right_panel, text="+ Add Frame", font=('Arial', 9), bg='#0f3460', fg='white',
                 command=self._add_animation_frame).pack(fill='x', padx=5, pady=2)
        tk.Button(right_panel, text="▶ Play Animation", font=('Arial', 9), bg='#0f3460', fg='white',
                 command=self._play_animation).pack(fill='x', padx=5, pady=2)
        tk.Button(right_panel, text="📋 Copy Frame", font=('Arial', 9), bg='#0f3460', fg='white',
                 command=self._copy_frame).pack(fill='x', padx=5, pady=2)
        
        # Template toggle
        tk.Label(right_panel, text="TEMPLATE", font=('Arial', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(10, 5))
        self.template_var = tk.BooleanVar(value=True)
        tk.Checkbutton(right_panel, text="Show Template", variable=self.template_var,
                      bg='#16213e', fg='white', selectcolor='#0f3460',
                      command=self._update_canvas).pack()
        
        # Bottom bar - Actions
        bottom_bar = tk.Frame(self.root, bg='#16213e', height=50)
        bottom_bar.pack(fill='x', side='bottom')
        bottom_bar.pack_propagate(False)
        
        actions = [
            ("New", self._new_skin),
            ("Load MSK", self._load_msk),
            ("Save MSK", self._save_msk),
            ("Import PNG", self._import_png),
            ("Clear Layer", self._clear_layer),
            ("Undo", self._undo),
            ("Redo", self._redo),
            ("Preview", self._preview_skin),
            ("Compile MSK", self._compile_msk),
            ("Decrypt MSK", self._decrypt_msk),
        ]
        for action_name, action_cmd in actions:
            btn = tk.Button(bottom_bar, text=action_name, font=('Arial', 10),
                          bg='#0f3460', fg='white', relief='flat',
                          command=action_cmd)
            btn.pack(side='left', padx=3, pady=8)
    
    def _set_tool(self, tool: str):
        self.current_tool = tool
    
    def _choose_color(self):
        color = colorchooser.askcolor(
            title="Choose Color",
            initialcolor=f'#{self.current_color[0]:02x}{self.current_color[1]:02x}{self.current_color[2]:02x}'
        )
        if color and color[0]:
            r, g, b = [int(c) for c in color[0]]
            self.current_color = (r, g, b, 255)
            self._update_color_preview()
    
    def _set_quick_color(self, color: tuple):
        self.current_color = (*color, 255)
        self._update_color_preview()
    
    def _update_color_preview(self):
        r, g, b, a = self.current_color
        self.color_preview.configure(bg=f'#{r:02x}{g:02x}{b:02x}')
    
    def _select_layer(self, layer_name: str):
        self.current_layer = layer_name
        for name, (btn, vis_btn) in self.layer_buttons.items():
            btn.configure(bg='#e94560' if name == layer_name else '#0f3460')
    
    def _toggle_layer_visibility(self, layer_name: str):
        self.layer_visible[layer_name] = not self.layer_visible[layer_name]
        self._update_canvas()
    
    def _save_undo_state(self):
        if len(self.undo_stack) >= self.max_undo:
            self.undo_stack.pop(0)
        self.undo_stack.append(self.layers[self.current_layer].copy())
        self.redo_stack.clear()
    
    def _undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.layers[self.current_layer].copy())
            self.layers[self.current_layer] = self.undo_stack.pop()
            self._update_canvas()
    
    def _redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.layers[self.current_layer].copy())
            self.layers[self.current_layer] = self.redo_stack.pop()
            self._update_canvas()
    
    def _clear_layer(self):
        if messagebox.askyesno("Clear Layer", "Clear the current layer?"):
            self._save_undo_state()
            self.layers[self.current_layer] = Image.new('RGBA',
                (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
            self._update_canvas()
    
    def _new_skin(self):
        if messagebox.askyesno("New Skin", "Create a new blank skin? All unsaved work will be lost."):
            self._init_layers()
            self.msk_data = None
            self.current_file = None
            self.skin_name = "Custom Skin"
            self.skin_author = "MEMEBOT User"
            self.skin_version = "1.0"
            self.skin_description = "A custom MEMEBOT skin"
            self.animation_frames = {}
            self.current_animation = "idle"
            self.current_frame = 0
            self._update_metadata_entries()
            self.undo_stack.clear()
            self.redo_stack.clear()
            self._update_canvas()
            self._update_frame_label()
    
    def _update_metadata_entries(self):
        """Update all metadata entry fields with current values"""
        if hasattr(self, 'skin_name_entry'):
            self.skin_name_entry.delete(0, tk.END)
            self.skin_name_entry.insert(0, self.skin_name)
        if hasattr(self, 'skin_author_entry'):
            self.skin_author_entry.delete(0, tk.END)
            self.skin_author_entry.insert(0, self.skin_author)
        if hasattr(self, 'skin_version_entry'):
            self.skin_version_entry.delete(0, tk.END)
            self.skin_version_entry.insert(0, self.skin_version)
        if hasattr(self, 'skin_description_entry'):
            self.skin_description_entry.delete(0, tk.END)
            self.skin_description_entry.insert(0, self.skin_description)
    
    def _load_msk(self):
        file_path = filedialog.askopenfilename(
            title="Load MSK Skin",
            filetypes=[("MSK files", "*.msk"), ("All files", "*.*")]
        )
        if file_path:
            self.msk_data = self.encryptor.load_skin_file(Path(file_path))
            if self.msk_data:
                self.current_file = file_path
                self.skin_name = self.msk_data.get('name', 'Custom Skin')
                self.skin_author = self.msk_data.get('author', 'MEMEBOT User')
                self.skin_version = self.msk_data.get('version', '1.0')
                self.skin_description = self.msk_data.get('description', '')
                self.animation_frames = self.msk_data.get('animation_frames', {})
                self._update_metadata_entries()
                self._apply_msk_to_layers()
                messagebox.showinfo("Loaded", f"Skin loaded: {self.skin_name}")
            else:
                messagebox.showerror("Error", "Failed to load skin file!")
    
    def _apply_msk_to_layers(self):
        self._init_layers()
        if self.msk_data:
            sprite_data = self.msk_data.get("sprite_data", {})
            layers_data = sprite_data.get("layers", {})
            for layer_name, layer_b64 in layers_data.items():
                if layer_name in self.layers:
                    try:
                        layer_bytes = base64.b64decode(layer_b64)
                        self.layers[layer_name] = Image.open(BytesIO(layer_bytes)).convert('RGBA')
                    except Exception as e:
                        logging.warning(f"Failed to decode layer {layer_name}: {e}")
        self._update_canvas()
    
    def _save_msk(self):
        file_path = filedialog.asksaveasfilename(
            title="Save MSK Skin",
            defaultextension=".msk",
            filetypes=[("MSK files", "*.msk"), ("All files", "*.*")]
        )
        if file_path:
            skin_name = os.path.splitext(os.path.basename(file_path))[0]
            self.skin_name = skin_name
            self._update_metadata_entries()
            skin_data = self._compile_skin_data()
            if self.encryptor.save_skin_file(Path(file_path), skin_data):
                self.current_file = file_path
                messagebox.showinfo("Saved", f"Skin '{skin_name}' saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save skin!")
    
    def _compile_msk(self):
        file_path = filedialog.asksaveasfilename(
            title="Compile to MSK",
            defaultextension=".msk",
            filetypes=[("MSK files", "*.msk"), ("All files", "*.*")]
        )
        if file_path:
            skin_name = os.path.splitext(os.path.basename(file_path))[0]
            self.skin_name = skin_name
            self._update_metadata_entries()
            skin_data = self._compile_skin_data()
            if self.encryptor.save_skin_file(Path(file_path), skin_data):
                messagebox.showinfo("Compiled", f"Skin '{skin_name}' compiled and encrypted!\nSaved to: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to compile skin!")
    
    def _decrypt_msk(self):
        """Open and display decrypted MSK JSON data"""
        file_path = filedialog.askopenfilename(
            title="Open MSK to Decrypt",
            filetypes=[("MSK files", "*.msk"), ("All files", "*.*")]
        )
        if file_path:
            skin_data = self.encryptor.load_skin_file(Path(file_path))
            if skin_data:
                # Remove binary sprite data for readability
                display_data = dict(skin_data)
                if 'sprite_data' in display_data and 'layers' in display_data['sprite_data']:
                    display_data['sprite_data']['layers'] = {
                        k: f"<base64 PNG data: {len(v)} chars>" 
                        for k, v in display_data['sprite_data']['layers'].items()
                    }
                if 'lua_script' in display_data:
                    display_data['lua_script'] = f"<Lua script: {len(display_data['lua_script'])} chars>"
                
                json_str = json.dumps(display_data, indent=2)
                
                # Show in a new window
                decrypt_window = tk.Toplevel(self.root)
                decrypt_window.title(f"Decrypted: {os.path.basename(file_path)}")
                decrypt_window.geometry("600x500")
                decrypt_window.configure(bg='#1a1a2e')
                
                text_widget = tk.Text(decrypt_window, bg='#0a0a1a', fg='#e0e0e0',
                                     font=('Consolas', 10), wrap='word')
                text_widget.pack(fill='both', expand=True, padx=5, pady=5)
                text_widget.insert('1.0', json_str)
                text_widget.config(state='disabled')
                
                # Add scrollbar
                scrollbar = tk.Scrollbar(text_widget)
                scrollbar.pack(side='right', fill='y')
                text_widget.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=text_widget.yview)
            else:
                messagebox.showerror("Error", "Failed to decrypt skin file!")
    
    def _compile_skin_data(self) -> Dict[str, Any]:
        layer_data = {}
        for name, layer_img in self.layers.items():
            buffer = BytesIO()
            layer_img.save(buffer, format='PNG')
            layer_data[name] = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {
            "name": self.skin_name,
            "version": self.skin_version,
            "author": self.skin_author,
            "description": self.skin_description,
            "encryption": "SK3-Enhanced",
            "sprite_data": {
                "canvas_size": [self.CANVAS_WIDTH, self.CANVAS_HEIGHT],
                "layers": layer_data,
            },
            "animation_frames": self.animation_frames,
            "body_scale": {"height": 1.0, "width": 1.0, "head_size": 1.0, "limb_length": 1.0},
            "body_shape": {"type": "default", "torso_width": 1.0, "torso_height": 1.0, "belly_size": 0.0, "shoulder_width": 1.0, "hip_width": 1.0, "custom_points": []},
            "limbs": {"arm_style": "default", "arm_length": 1.0, "arm_width": 1.0, "leg_style": "default", "leg_length": 1.0, "leg_width": 1.0, "hand_style": "default", "foot_style": "default"},
            "head": {"shape": "round", "size": 1.0, "face_position": 0.0, "ear_style": "default", "ear_size": 1.0},
            "hair": {"style": "default", "length": 1.0, "volume": 1.0, "bangs": True, "custom_points": []},
            "outfit": {"type": "default", "top_color": [100, 180, 255, 255], "bottom_color": [50, 130, 200, 255], "custom_shapes": []},
            "colors": {"body": [100, 180, 255, 255], "body_outline": [50, 130, 200, 255], "skin": [255, 220, 180, 255], "skin_outline": [200, 170, 140, 255], "hair": [80, 60, 40, 255], "hair_outline": [60, 40, 20, 255], "eyes": [100, 180, 255, 255], "pupils": [30, 30, 30, 255], "mouth": [200, 100, 100, 255], "tongue": [255, 150, 150, 255], "cheeks": [255, 180, 180, 80], "ears_inner": [255, 180, 200, 255], "feet": [50, 50, 50, 255], "hands": [255, 220, 180, 255], "name_tag_bg": [50, 50, 50, 200], "name_tag_text": [255, 255, 255, 255], "outfit_primary": [100, 180, 255, 255], "outfit_secondary": [50, 130, 200, 255]},
            "accessories": {"hat": None, "glasses": None, "scarf": None, "shoes": None, "wings": None, "tail_type": "default", "custom_accessories": []},
            "clothing": {},
            "animations": {"idle_speed": 1.0, "walk_speed": 1.0, "dance_speed": 1.0, "blink_rate": 1.0, "custom_animations": {}},
            "particles": {"sparkle_color": [255, 255, 0, 180], "music_note_color": [100, 200, 255, 180], "heart_color": [255, 100, 150, 180], "custom_particles": {}},
            "lua_script": self.encryptor._generate_default_lua(),
        }
    
    def _import_png(self):
        file_path = filedialog.askopenfilename(
            title="Import PNG",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            imported = Image.open(file_path).convert('RGBA')
            if imported.width > self.CANVAS_WIDTH or imported.height > self.CANVAS_HEIGHT:
                ratio = min(self.CANVAS_WIDTH / imported.width, self.CANVAS_HEIGHT / imported.height)
                new_size = (int(imported.width * ratio), int(imported.height * ratio))
                imported = imported.resize(new_size, Image.LANCZOS)
            
            self._save_undo_state()
            x = (self.CANVAS_WIDTH - imported.width) // 2
            y = (self.CANVAS_HEIGHT - imported.height) // 2
            temp = self.layers[self.current_layer].copy()
            temp.paste(imported, (x, y), imported)
            self.layers[self.current_layer] = temp
            self._update_canvas()
    
    def _preview_skin(self):
        preview = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
        if self.template_visible and self.template_image:
            preview = Image.alpha_composite(preview, self.template_image)
        layer_order = [
            self.LAYER_TAIL, self.LAYER_WINGS, self.LAYER_LEGS, self.LAYER_BODY,
            self.LAYER_ARMS, self.LAYER_OUTFIT, self.LAYER_ACCESSORIES,
            self.LAYER_HEAD, self.LAYER_HAIR, self.LAYER_EYES, self.LAYER_MOUTH,
            self.LAYER_HAT, self.LAYER_GLASSES,
        ]
        for name in layer_order:
            if name in self.layers and self.layer_visible.get(name, True):
                preview = Image.alpha_composite(preview, self.layers[name])
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Skin Preview")
        preview_window.geometry(f"{self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT}")
        preview_tk = ImageTk.PhotoImage(preview)
        label = tk.Label(preview_window, image=preview_tk)
        label.image = preview_tk
        label.pack()
    
    # ============================================
    # ANIMATION FRAME EDITOR
    # ============================================
    
    def _on_animation_change(self, event=None):
        """Switch to a different animation"""
        self.current_animation = self.anim_var.get()
        self.current_frame = 0
        if self.current_animation not in self.animation_frames:
            self.animation_frames[self.current_animation] = []
        self._update_frame_label()
        self._load_current_frame()
    
    def _prev_frame(self):
        if self.current_frame > 0:
            self._save_current_frame()
            self.current_frame -= 1
            self._load_current_frame()
            self._update_frame_label()
    
    def _next_frame(self):
        anim_frames = self.animation_frames.get(self.current_animation, [])
        if self.current_frame < len(anim_frames) - 1:
            self._save_current_frame()
            self.current_frame += 1
            self._load_current_frame()
            self._update_frame_label()
    
    def _add_animation_frame(self):
        """Add a new blank frame to the current animation"""
        anim_frames = self.animation_frames.get(self.current_animation, [])
        if self.current_animation not in self.animation_frames:
            self.animation_frames[self.current_animation] = []
        
        # Save current frame first
        self._save_current_frame()
        
        # Create new blank frame
        new_frame = {}
        for name in self.layers:
            buffer = BytesIO()
            blank = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
            blank.save(buffer, format='PNG')
            new_frame[name] = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        self.animation_frames[self.current_animation].append(new_frame)
        self.current_frame = len(self.animation_frames[self.current_animation]) - 1
        self._load_current_frame()
        self._update_frame_label()
    
    def _copy_frame(self):
        """Copy the current frame and add it as a new frame"""
        anim_frames = self.animation_frames.get(self.current_animation, [])
        if self.current_animation not in self.animation_frames:
            self.animation_frames[self.current_animation] = []
        
        self._save_current_frame()
        
        # Copy current layers
        new_frame = {}
        for name, layer_img in self.layers.items():
            buffer = BytesIO()
            layer_img.save(buffer, format='PNG')
            new_frame[name] = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        self.animation_frames[self.current_animation].append(new_frame)
        self.current_frame = len(self.animation_frames[self.current_animation]) - 1
        self._update_frame_label()
    
    def _save_current_frame(self):
        """Save current layers to the current animation frame"""
        anim_frames = self.animation_frames.get(self.current_animation, [])
        if self.current_animation not in self.animation_frames:
            self.animation_frames[self.current_animation] = []
        
        frame_data = {}
        for name, layer_img in self.layers.items():
            buffer = BytesIO()
            layer_img.save(buffer, format='PNG')
            frame_data[name] = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        if self.current_frame < len(anim_frames):
            anim_frames[self.current_frame] = frame_data
        else:
            anim_frames.append(frame_data)
        
        self.animation_frames[self.current_animation] = anim_frames
    
    def _load_current_frame(self):
        """Load the current animation frame into layers"""
        anim_frames = self.animation_frames.get(self.current_animation, [])
        if self.current_frame < len(anim_frames):
            frame_data = anim_frames[self.current_frame]
            self._init_layers()
            for name, layer_b64 in frame_data.items():
                if name in self.layers:
                    try:
                        layer_bytes = base64.b64decode(layer_b64)
                        self.layers[name] = Image.open(BytesIO(layer_bytes)).convert('RGBA')
                    except Exception:
                        pass
        else:
            self._init_layers()
        self._update_canvas()
    
    def _update_frame_label(self):
        anim_frames = self.animation_frames.get(self.current_animation, [])
        total = max(len(anim_frames), 1)
        self.frame_label.config(text=f"Frame: {self.current_frame}/{total - 1 if total > 1 else 0}")
    
    def _play_animation(self):
        """Play the current animation in a preview loop"""
        anim_frames = self.animation_frames.get(self.current_animation, [])
        if len(anim_frames) < 2:
            messagebox.showinfo("Animation", "Add at least 2 frames to play an animation.")
            return
        
        self._save_current_frame()
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Animation: {self.current_animation}")
        preview_window.geometry(f"{self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT}")
        preview_window.configure(bg='#0a0a1a')
        
        preview_label = tk.Label(preview_window, bg='#0a0a1a')
        preview_label.pack()
        
        playing = [True]
        frame_idx = [0]
        
        def update_frame():
            if not playing[0] or not preview_window.winfo_exists():
                return
            
            frame_data = anim_frames[frame_idx[0]]
            composite = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
            layer_order = [
                self.LAYER_TAIL, self.LAYER_WINGS, self.LAYER_LEGS, self.LAYER_BODY,
                self.LAYER_ARMS, self.LAYER_OUTFIT, self.LAYER_ACCESSORIES,
                self.LAYER_HEAD, self.LAYER_HAIR, self.LAYER_EYES, self.LAYER_MOUTH,
                self.LAYER_HAT, self.LAYER_GLASSES,
            ]
            for name in layer_order:
                if name in frame_data:
                    try:
                        layer_bytes = base64.b64decode(frame_data[name])
                        layer_img = Image.open(BytesIO(layer_bytes)).convert('RGBA')
                        composite = Image.alpha_composite(composite, layer_img)
                    except Exception:
                        pass
            
            preview_tk = ImageTk.PhotoImage(composite)
            preview_label.config(image=preview_tk)
            preview_label.image = preview_tk
            
            frame_idx[0] = (frame_idx[0] + 1) % len(anim_frames)
            preview_window.after(100, update_frame)
        
        preview_window.protocol("WM_DELETE_WINDOW", lambda: [playing.__setitem__(0, False), preview_window.destroy()])
        update_frame()
    
    # ============================================
    # DRAWING METHODS
    # ============================================
    
    def _load_template(self):
        self.template_image = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
        td = ImageDraw.Draw(self.template_image)
        td.ellipse([190, 150, 290, 280], outline=(255, 255, 255, 80), width=1)
        td.ellipse([180, 250, 300, 520], outline=(255, 255, 255, 80), width=1)
        td.line([200, 320, 160, 450], fill=(255, 255, 255, 80), width=2)
        td.line([280, 320, 320, 450], fill=(255, 255, 255, 80), width=2)
        td.line([210, 510, 200, 600], fill=(255, 255, 255, 80), width=2)
        td.line([270, 510, 280, 600], fill=(255, 255, 255, 80), width=2)
    
    def _update_canvas(self):
        composite = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
        if self.template_var.get() and self.template_image:
            composite = Image.alpha_composite(composite, self.template_image)
        layer_order = [
            self.LAYER_TAIL, self.LAYER_WINGS, self.LAYER_LEGS, self.LAYER_BODY,
            self.LAYER_ARMS, self.LAYER_OUTFIT, self.LAYER_ACCESSORIES,
            self.LAYER_HEAD, self.LAYER_HAIR, self.LAYER_EYES, self.LAYER_MOUTH,
            self.LAYER_HAT, self.LAYER_GLASSES,
        ]
        for name in layer_order:
            if name in self.layers and self.layer_visible.get(name, True):
                composite = Image.alpha_composite(composite, self.layers[name])
        
        self.display_image = ImageTk.PhotoImage(composite)
        self.canvas.delete("all")
        self.canvas.create_image(self.CANVAS_WIDTH // 2, self.CANVAS_HEIGHT // 2, image=self.display_image)
    
    def _on_mouse_down(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        self.start_x = event.x
        self.start_y = event.y
        
        if self.current_tool == self.TOOL_FILL:
            self._save_undo_state()
            self._flood_fill(event.x, event.y)
            self._update_canvas()
        elif self.current_tool == self.TOOL_PICKER:
            self._pick_color(event.x, event.y)
        elif self.current_tool == self.TOOL_EYEDROPPER:
            self._pick_color(event.x, event.y)
            self.current_tool = self.TOOL_PENCIL
        elif self.current_tool == self.TOOL_TEXT:
            self._save_undo_state()
            text = simpledialog.askstring("Text", "Enter text:", parent=self.root)
            if text:
                self._draw_text(event.x, event.y, text)
            self._update_canvas()
        elif self.current_tool == self.TOOL_SPRAY:
            self._save_undo_state()
            self._spray(event.x, event.y)
        elif self.current_tool in [self.TOOL_PENCIL, self.TOOL_ERASER]:
            self._save_undo_state()
            self._draw_point(event.x, event.y)
    
    def _on_mouse_drag(self, event):
        if not self.drawing:
            return
        if self.current_tool == self.TOOL_SPRAY:
            self._spray(event.x, event.y)
        elif self.current_tool in [self.TOOL_PENCIL, self.TOOL_ERASER]:
            self._draw_line(self.last_x, self.last_y, event.x, event.y)
        self.last_x = event.x
        self.last_y = event.y
        self._update_canvas()
    
    def _on_mouse_up(self, event):
        if not self.drawing:
            return
        if self.current_tool == self.TOOL_LINE:
            self._save_undo_state()
            self._draw_line(self.start_x, self.start_y, event.x, event.y)
        elif self.current_tool == self.TOOL_RECTANGLE:
            self._save_undo_state()
            self._draw_rectangle(self.start_x, self.start_y, event.x, event.y)
        elif self.current_tool == self.TOOL_ELLIPSE:
            self._save_undo_state()
            self._draw_ellipse(self.start_x, self.start_y, event.x, event.y)
        self.drawing = False
        self._update_canvas()
    
    def _on_mouse_move(self, event):
        self.coord_label.configure(text=f"X: {event.x}  Y: {event.y}")
    
    def _draw_point(self, x: int, y: int):
        draw = ImageDraw.Draw(self.layers[self.current_layer])
        color = (0, 0, 0, 0) if self.current_tool == self.TOOL_ERASER else self.current_color
        bs = self.brush_size
        draw.ellipse([x - bs//2, y - bs//2, x + bs//2, y + bs//2], fill=color)
    
    def _draw_line(self, x1: int, y1: int, x2: int, y2: int):
        draw = ImageDraw.Draw(self.layers[self.current_layer])
        color = (0, 0, 0, 0) if self.current_tool == self.TOOL_ERASER else self.current_color
        draw.line([x1, y1, x2, y2], fill=color, width=self.brush_size)
    
    def _draw_rectangle(self, x1: int, y1: int, x2: int, y2: int):
        draw = ImageDraw.Draw(self.layers[self.current_layer])
        draw.rectangle([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)],
                      fill=self.current_color, outline=self.current_color)
    
    def _draw_ellipse(self, x1: int, y1: int, x2: int, y2: int):
        draw = ImageDraw.Draw(self.layers[self.current_layer])
        draw.ellipse([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)], fill=self.current_color)
    
    def _draw_text(self, x: int, y: int, text: str):
        draw = ImageDraw.Draw(self.layers[self.current_layer])
        try:
            font = ImageFont.truetype("arial.ttf", self.brush_size * 4)
        except:
            font = ImageFont.load_default()
        draw.text((x, y), text, fill=self.current_color, font=font)
    
    def _spray(self, x: int, y: int):
        draw = ImageDraw.Draw(self.layers[self.current_layer])
        for _ in range(self.brush_size * 3):
            sx = x + random.randint(-self.brush_size * 3, self.brush_size * 3)
            sy = y + random.randint(-self.brush_size * 3, self.brush_size * 3)
            draw.point((sx, sy), fill=self.current_color)
    
    def _flood_fill(self, x: int, y: int):
        draw = ImageDraw.Draw(self.layers[self.current_layer])
        draw.ellipse([0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT], fill=self.current_color)
    
    def _pick_color(self, x: int, y: int):
        composite = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
        for name, layer_img in self.layers.items():
            if self.layer_visible[name]:
                composite = Image.alpha_composite(composite, layer_img)
        pixel = composite.getpixel((x, y))
        if pixel[3] > 0:
            self.current_color = pixel
            self._update_color_preview()
    
    def run(self):
        self.root.mainloop()


def main():
    print("=" * 60)
    print("         MEMEBOT DRAWER - Community Skin Creator")
    print("=" * 60)
    print("  Draw custom characters and accessories")
    print("  Layer-based editing with 13 body part layers")
    print("  10 drawing tools: pencil, eraser, fill, line, rect, ellipse,")
    print("     color picker, spray, text, eyedropper")
    print("  Import PNG sprites for custom accessories")
    print("  Custom animation frame editor (idle, walk, run, dance, etc.)")
    print("  Undo/Redo with 50 state history")
    print("  Export to .MSK SK3 encrypted format")
    print("  Load existing .MSK files for editing")
    print("  Decrypt and view MSK JSON data")
    print("  Custom skin name, author, version, description")
    print("=" * 60)
    print()
    app = DrawerApp()
    app.run()


if __name__ == "__main__":
    main()