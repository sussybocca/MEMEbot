"""
MEMEBOT Circular Mod Menu v2.0
A radial menu for skin creation, clothing, accessories, Lua scripting, and mod management
"""

import os
import math
import json
import logging
import tkinter as tk
from tkinter import colorchooser, simpledialog, messagebox
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageTk

class ModMenu:
    """Circular radial menu for MEMEBOT mods and skins"""
    
    def __init__(self, root, config, skin_loader, app):
        self.root = root
        self.config = config
        self.skin_loader = skin_loader
        self.app = app
        
        self.menu_window = None
        self.menu_canvas = None
        self.is_visible = False
        
        self.center_x = 0
        self.center_y = 0
        self.radius = 150
        self.item_radius = 30
        self.items = []
        self.selected_index = -1
        self.hovered_index = -1
        self.rotation = 0
        self.target_rotation = 0
        
        self.current_page = "main"
        self.pages = {
            "main": ["Skins", "Create Skin", "Body Customize", "Clothing", "Accessories", "Lua Scripts", "Dance Moves", "Settings", "Exit"],
            "skins": [],
            "create_skin": ["Body Color", "Hair Color", "Eye Color", "Skin Color", "Mouth Color", "Outfit Color", "Write Lua", "Save Skin", "Preview", "Back"],
            "body_customize": ["Body Shape", "Body Scale", "Arm Style", "Leg Style", "Head Shape", "Hair Style", "Ear Style", "Hand Style", "Foot Style", "Outfit Type", "Tail Style", "Back"],
            "body_shape": ["Default", "Round", "Square", "Triangle", "Pear", "Athletic", "Slime", "Barrel", "Wasp", "Ghost", "Custom", "Back"],
            "body_scale": ["Height +", "Height -", "Width +", "Width -", "Head Size +", "Head Size -", "Limb Length +", "Limb Length -", "Torso Width +", "Torso Width -", "Back"],
            "arm_style": ["Default", "Muscular", "Robot", "Tentacle", "Thin", "Wing Arms", "Stretchy", "Blade", "Crystal", "Gooey", "Back"],
            "leg_style": ["Default", "Animal", "Robot", "Thick", "Thin", "Spring", "Pillar", "Peg", "Digitigrade", "Tentacle Legs", "Back"],
            "head_shape": ["Round", "Oval", "Square", "Triangle", "Heart", "Hexagon", "Diamond", "Star", "Moon", "Alien", "Robot Head", "Back"],
            "hair_style": ["Default", "Spiky", "Long", "Mohawk", "Afro", "Ponytail", "Pigtails", "Dreadlocks", "Bob", "Buzzcut", "Mullet", "Curly", "Bald", "Back"],
            "ear_style": ["Default", "Pointy", "Round", "Floppy", "Elf", "Mouse", "Cat", "Demon", "Wing Ears", "Tentacle Ears", "None", "Back"],
            "hand_style": ["Default", "Mitten", "Claw", "Hook", "Paws", "Tentacle Hands", "Robot Hands", "Gloves", "Spikes", "Suction Cups", "Energy", "Back"],
            "foot_style": ["Default", "Boot", "Bare", "Hoof", "Sneaker", "Sandals", "Heels", "Rollerskates", "Flippers", "Clown Shoes", "Ice Skates", "Back"],
            "outfit_type": ["Default", "None", "Armor", "Suit", "Robe", "Space Suit", "Ninja", "Swimwear", "Overalls", "Tuxedo", "Raincoat", "Kimono", "Military", "Pirate", "Cyberpunk", "Steampunk", "Custom", "Back"],
            "tail_style": ["None", "Cat", "Dog", "Demon", "Dragon", "Fox", "Rabbit", "Mouse", "Lizard", "Devil", "Robot", "Back"],
            "clothing": ["Hats", "Shirts", "Pants", "Shoes", "Cape", "Back"],
            "hats": ["None", "Top Hat", "Cap", "Cowboy", "Crown", "Wizard", "Beanie", "Fedora", "Helmet", "Sombrero", "Beret", "Bucket Hat", "Santa", "Viking", "Pirate Hat", "Chef", "Flower Crown", "Ushanka", "Propeller", "Back"],
            "shirts": ["None", "T-Shirt", "Jacket", "Hoodie", "Armor", "Suit", "Vest", "Sweater", "Tank Top", "Flannel", "Turtleneck", "Hawaiian", "Leather", "Chainmail", "Lab Coat", "Poncho", "Back"],
            "pants": ["None", "Jeans", "Shorts", "Skirt", "Cargo", "Sweatpants", "Leather Pants", "Plaid Pants", "Khakis", "Joggers", "Ripped Jeans", "Bell Bottoms", "Tights", "Overalls Pants", "Culottes", "Bloomers", "Back"],
            "shoes": ["None", "Sneakers", "Boots", "Sandals", "Heels", "Cowboy Boots", "Slippers", "Flip Flops", "Hiking Boots", "Ballet Flats", "Clogs", "Snow Boots", "Rain Boots", "Loafers", "High Tops", "Cleats", "Back"],
            "cape": ["None", "Red", "Blue", "Black", "Purple", "Green", "Back"],
            "accessories": ["Masks", "Glasses", "Wings", "Scarfs", "Back"],
            "masks": ["None", "Batman", "Spiderman", "Iron Man", "Deadpool", "Skull", "Gas Mask", "Ninja", "Hockey", "Bane", "Plague Doctor", "Cyberpunk", "Oni", "Jester", "Dragon", "Back"],
            "glasses": ["None", "Sunglasses", "Nerd", "Monocle", "Goggles", "3D", "Cyclops", "Heart", "Star", "Round Retro", "Visor", "Cat Eye", "Steampunk", "Futuristic", "Shutter Shades", "Welding", "Back"],
            "wings": ["None", "Angel", "Demon", "Dragon", "Fairy", "Bat", "Butterfly", "Phoenix", "Crow", "Pegasus", "Harpy", "Mechanical", "Ice", "Shadow", "Leaf", "Crystal", "Back"],
            "scarfs": ["None", "Red", "Blue", "Green", "Striped", "Winter", "Yellow", "Purple", "Pink", "Orange", "Black", "Rainbow", "Checkered", "Polka Dot", "Camo", "Gradient", "Back"],
            "dances": ["Worm", "Moonwalk", "Thriller", "Robot", "Disco", "Back"],
            "settings": ["Volume Up", "Volume Down", "Auto-Play Toggle", "Back"],
        }
        
        self.animation_id = None
        
        self.lua_scripts = []
        self.lua_available = False
        self._check_lua()
        self._scan_lua_scripts()
        
        self.editing_skin = None
        self.skin_preview_window = None
        self.skin_preview_canvas = None
        
        self._ensure_default_skin()
    
    def _ensure_default_skin(self):
        """Ensure default.msk exists"""
        default_path = self.config.SKINS_PATH / "Default.msk"
        if not default_path.exists():
            default_skin = self.skin_loader.encryptor.create_default_skin("Default")
            self.skin_loader.encryptor.save_skin_file(default_path, default_skin)
            logging.info("Created default.msk skin file")
    
    def _check_lua(self):
        """Check if Lua interpreter is available"""
        try:
            import lupa
            self.lua = lupa.LuaRuntime(unpack_returned_tuples=True)
            self.lua_available = True
        except ImportError:
            self.lua = None
            self.lua_available = False
    
    def _scan_lua_scripts(self):
        """Scan for Lua scripts in mods directory"""
        self.lua_scripts = []
        mods_path = self.config.MODS_PATH
        if mods_path.exists():
            for file in mods_path.glob("*.lua"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.lua_scripts.append({
                        "name": file.stem,
                        "path": str(file),
                        "size": len(content),
                        "valid": content.strip().startswith("--[["),
                        "content": content
                    })
                except:
                    pass
    
    def toggle(self):
        """Toggle menu visibility"""
        if self.is_visible:
            self.hide()
        else:
            self.show()
    
    def show(self):
        """Show the circular menu"""
        if self.is_visible:
            return
        
        self.hide()
        
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("MEMEBOT Mod Menu")
        self.menu_window.attributes('-topmost', True)
        self.menu_window.overrideredirect(True)
        self.menu_window.configure(bg='black')
        self.menu_window.attributes('-transparentcolor', 'black')
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.center_x = screen_w // 2
        self.center_y = screen_h // 2
        
        menu_size = self.radius * 2 + 100
        self.menu_window.geometry(f"{menu_size}x{menu_size}+{self.center_x - menu_size//2}+{self.center_y - menu_size//2}")
        
        self.menu_canvas = tk.Canvas(
            self.menu_window, bg='black', highlightthickness=0,
            width=menu_size, height=menu_size
        )
        self.menu_canvas.pack(fill='both', expand=True)
        
        self.menu_canvas.bind('<Motion>', self._on_mouse_move)
        self.menu_canvas.bind('<Button-1>', self._on_click)
        self.menu_canvas.bind('<MouseWheel>', self._on_scroll)
        self.menu_window.bind('<Escape>', lambda e: self.hide())
        
        self.is_visible = True
        self._update_items()
        self._animate()
    
    def hide(self):
        """Hide the menu"""
        self.is_visible = False
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        if self.menu_window:
            try:
                self.menu_window.destroy()
            except:
                pass
            self.menu_window = None
            self.menu_canvas = None
        if self.skin_preview_window:
            try:
                self.skin_preview_window.destroy()
            except:
                pass
            self.skin_preview_window = None
    
    def _update_items(self):
        """Update menu items based on current page"""
        page_items = self.pages.get(self.current_page, self.pages["main"])
        
        if self.current_page == "skins":
            skins = self.skin_loader.get_available_skins()
            self.items = [s["name"] for s in skins] + ["Back"]
        elif self.current_page == "lua":
            self.items = [s["name"] + (" ✓" if s["valid"] else " ✗") for s in self.lua_scripts] + ["New Script", "Back"]
        else:
            self.items = page_items
    
    def _get_item_position(self, index: int) -> tuple:
        """Get x,y position for menu item"""
        total = len(self.items)
        if total == 0:
            return (self.radius + 50, self.radius + 50)
        
        angle = (2 * math.pi / total) * index + self.rotation
        x = self.radius + 50 + math.cos(angle) * self.radius
        y = self.radius + 50 + math.sin(angle) * self.radius
        return (x, y)
    
    def _draw_menu(self):
        """Draw the circular menu"""
        if not self.menu_canvas:
            return
        
        self.menu_canvas.delete("all")
        
        cx = self.radius + 50
        cy = self.radius + 50
        
        self.menu_canvas.create_oval(
            cx - self.radius - 10, cy - self.radius - 10,
            cx + self.radius + 10, cy + self.radius + 10,
            outline='#555555', width=3, fill='#1a1a1a'
        )
        
        self.menu_canvas.create_oval(
            cx - self.radius + 20, cy - self.radius + 20,
            cx + self.radius - 20, cy + self.radius - 20,
            outline='#333333', width=1
        )
        
        self.menu_canvas.create_oval(
            cx - 45, cy - 45, cx + 45, cy + 45,
            fill='#2a2a2a', outline='#666666', width=3
        )
        
        title = self.current_page.upper() if self.current_page != "main" else "MEMEBOT"
        self.menu_canvas.create_text(cx, cy - 5, text=title, fill='white', font=('Arial', 12, 'bold'))
        self.menu_canvas.create_text(cx, cy + 15, text="MOD MENU", fill='#888888', font=('Arial', 7))
        
        if self.current_page == "main":
            lua_status = "Lua: ON" if self.lua_available else "Lua: OFF"
            lua_color = '#00ff00' if self.lua_available else '#ff0000'
            self.menu_canvas.create_text(cx, cy + 30, text=lua_status, fill=lua_color, font=('Arial', 6))
        
        for i, item in enumerate(self.items):
            x, y = self._get_item_position(i)
            
            if i == self.hovered_index:
                fill_color = '#4a90d9'
                outline_color = '#6ab0f9'
                text_color = 'white'
            else:
                fill_color = '#333333'
                outline_color = '#555555'
                text_color = '#cccccc'
            
            r = self.item_radius
            self.menu_canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=fill_color, outline=outline_color, width=2
            )
            
            display_text = item[:10] + ".." if len(item) > 12 else item
            self.menu_canvas.create_text(
                x, y, text=display_text,
                fill=text_color, font=('Arial', 7, 'bold')
            )
    
    def _animate(self):
        """Animate menu rotation"""
        if not self.is_visible:
            return
        
        self.rotation += (self.target_rotation - self.rotation) * 0.1
        self._draw_menu()
        self.animation_id = self.root.after(33, self._animate)
    
    def _on_mouse_move(self, event):
        """Handle mouse movement"""
        if not self.is_visible:
            return
        
        self.hovered_index = -1
        for i in range(len(self.items)):
            x, y = self._get_item_position(i)
            dx = event.x - x
            dy = event.y - y
            if math.sqrt(dx * dx + dy * dy) < self.item_radius + 10:
                self.hovered_index = i
                break
    
    def _on_click(self, event):
        """Handle click on menu item"""
        if not self.is_visible or self.hovered_index < 0:
            return
        
        item = self.items[self.hovered_index].replace(" ✓", "").replace(" ✗", "")
        self._execute_action(item)
    
    def _on_scroll(self, event):
        """Handle mouse wheel"""
        if not self.is_visible:
            return
        
        if event.delta > 0:
            self.target_rotation += 0.3
        else:
            self.target_rotation -= 0.3
    
    def _execute_action(self, item: str):
        """Execute menu action"""
        logging.info(f"Menu: {item} ({self.current_page})")
        
        # Navigation actions
        nav_pages = {
            "main": {
                "Skins": "skins", "Create Skin": "create_skin_start",
                "Body Customize": "body_customize",
                "Clothing": "clothing", "Accessories": "accessories",
                "Lua Scripts": "lua", "Dance Moves": "dances",
                "Settings": "settings", "Exit": "hide"
            },
            "body_customize": {
                "Body Shape": "body_shape", "Body Scale": "body_scale",
                "Arm Style": "arm_style", "Leg Style": "leg_style",
                "Head Shape": "head_shape", "Hair Style": "hair_style",
                "Ear Style": "ear_style", "Hand Style": "hand_style",
                "Foot Style": "foot_style", "Outfit Type": "outfit_type",
                "Tail Style": "tail_style",
                "Back": "main"
            },
            "clothing": {"Hats": "hats", "Shirts": "shirts", "Pants": "pants", "Shoes": "shoes", "Cape": "cape", "Back": "main"},
            "accessories": {"Masks": "masks", "Glasses": "glasses", "Wings": "wings", "Scarfs": "scarfs", "Back": "main"},
        }
        
        # Handle navigation
        if self.current_page in nav_pages and item in nav_pages[self.current_page]:
            target = nav_pages[self.current_page][item]
            if target == "hide":
                self.hide()
            elif target == "create_skin_start":
                self._start_skin_creation()
            elif target == "main":
                self.current_page = "main"
                self._update_items()
            else:
                self.current_page = target
                self._update_items()
            return
        
        # Back button
        if item == "Back":
            back_map = {
                "skins": "main", "lua": "main", "dances": "main", "settings": "main",
                "hats": "clothing", "shirts": "clothing", "pants": "clothing", "shoes": "clothing", "cape": "clothing",
                "masks": "accessories", "glasses": "accessories", "wings": "accessories", "scarfs": "accessories",
                "body_shape": "body_customize", "body_scale": "body_customize",
                "arm_style": "body_customize", "leg_style": "body_customize",
                "head_shape": "body_customize", "hair_style": "body_customize",
                "ear_style": "body_customize", "hand_style": "body_customize",
                "foot_style": "body_customize", "outfit_type": "body_customize",
                "tail_style": "body_customize",
            }
            if self.current_page == "create_skin":
                self.current_page = "main"
                if self.skin_preview_window:
                    self.skin_preview_window.destroy()
                    self.skin_preview_window = None
                self.editing_skin = None
            elif self.current_page in back_map:
                self.current_page = back_map[self.current_page]
            self._update_items()
            return
        
        # Body customization actions
        body_actions = {
            "body_shape": ["Default", "Round", "Square", "Triangle", "Pear", "Athletic", "Slime", "Barrel", "Wasp", "Ghost", "Custom"],
            "body_scale": ["Height +", "Height -", "Width +", "Width -", "Head Size +", "Head Size -", "Limb Length +", "Limb Length -", "Torso Width +", "Torso Width -"],
            "arm_style": ["Default", "Muscular", "Robot", "Tentacle", "Thin", "Wing Arms", "Stretchy", "Blade", "Crystal", "Gooey"],
            "leg_style": ["Default", "Animal", "Robot", "Thick", "Thin", "Spring", "Pillar", "Peg", "Digitigrade", "Tentacle Legs"],
            "head_shape": ["Round", "Oval", "Square", "Triangle", "Heart", "Hexagon", "Diamond", "Star", "Moon", "Alien", "Robot Head"],
            "hair_style": ["Default", "Spiky", "Long", "Mohawk", "Afro", "Ponytail", "Pigtails", "Dreadlocks", "Bob", "Buzzcut", "Mullet", "Curly", "Bald"],
            "ear_style": ["Default", "Pointy", "Round", "Floppy", "Elf", "Mouse", "Cat", "Demon", "Wing Ears", "Tentacle Ears", "None"],
            "hand_style": ["Default", "Mitten", "Claw", "Hook", "Paws", "Tentacle Hands", "Robot Hands", "Gloves", "Spikes", "Suction Cups", "Energy"],
            "foot_style": ["Default", "Boot", "Bare", "Hoof", "Sneaker", "Sandals", "Heels", "Rollerskates", "Flippers", "Clown Shoes", "Ice Skates"],
            "outfit_type": ["Default", "None", "Armor", "Suit", "Robe", "Space Suit", "Ninja", "Swimwear", "Overalls", "Tuxedo", "Raincoat", "Kimono", "Military", "Pirate", "Cyberpunk", "Steampunk", "Custom"],
            "tail_style": ["None", "Cat", "Dog", "Demon", "Dragon", "Fox", "Rabbit", "Mouse", "Lizard", "Devil", "Robot"],
        }
        
        if self.current_page in body_actions:
            self._apply_body_customization(self.current_page, item)
            return
        
        # Clothing & Accessory items
        clothing_items = {
            "hats": ["None", "Top Hat", "Cap", "Cowboy", "Crown", "Wizard", "Beanie", "Fedora", "Helmet", "Sombrero", "Beret", "Bucket Hat", "Santa", "Viking", "Pirate Hat", "Chef", "Flower Crown", "Ushanka", "Propeller"],
            "shirts": ["None", "T-Shirt", "Jacket", "Hoodie", "Armor", "Suit", "Vest", "Sweater", "Tank Top", "Flannel", "Turtleneck", "Hawaiian", "Leather", "Chainmail", "Lab Coat", "Poncho"],
            "pants": ["None", "Jeans", "Shorts", "Skirt", "Cargo", "Sweatpants", "Leather Pants", "Plaid Pants", "Khakis", "Joggers", "Ripped Jeans", "Bell Bottoms", "Tights", "Overalls Pants", "Culottes", "Bloomers"],
            "shoes": ["None", "Sneakers", "Boots", "Sandals", "Heels", "Cowboy Boots", "Slippers", "Flip Flops", "Hiking Boots", "Ballet Flats", "Clogs", "Snow Boots", "Rain Boots", "Loafers", "High Tops", "Cleats"],
            "cape": ["None", "Red", "Blue", "Black", "Purple", "Green"],
            "masks": ["None", "Batman", "Spiderman", "Iron Man", "Deadpool", "Skull", "Gas Mask", "Ninja", "Hockey", "Bane", "Plague Doctor", "Cyberpunk", "Oni", "Jester", "Dragon"],
            "glasses": ["None", "Sunglasses", "Nerd", "Monocle", "Goggles", "3D", "Cyclops", "Heart", "Star", "Round Retro", "Visor", "Cat Eye", "Steampunk", "Futuristic", "Shutter Shades", "Welding"],
            "wings": ["None", "Angel", "Demon", "Dragon", "Fairy", "Bat", "Butterfly", "Phoenix", "Crow", "Pegasus", "Harpy", "Mechanical", "Ice", "Shadow", "Leaf", "Crystal"],
            "scarfs": ["None", "Red", "Blue", "Green", "Striped", "Winter", "Yellow", "Purple", "Pink", "Orange", "Black", "Rainbow", "Checkered", "Polka Dot", "Camo", "Gradient"],
        }
        
        if self.current_page in clothing_items:
            self._apply_clothing(self.current_page, item)
            return
        
        # Skins page
        if self.current_page == "skins":
            skins = self.skin_loader.get_available_skins()
            for skin in skins:
                if skin["name"] == item:
                    loaded = self.skin_loader.load_skin(skin["path"])
                    if loaded and loaded.get("lua_script") and self.lua_available:
                        self._execute_lua_string(loaded["lua_script"])
                    self.app.character.say(f"Skin: {item}")
                    self.hide()
                    break
            return
        
        # Lua scripts
        if self.current_page == "lua":
            if item == "New Script":
                self.hide()
                self._create_new_lua_script()
                self.show()
            else:
                for script in self.lua_scripts:
                    if script["name"] == item:
                        self._execute_lua_file(script["path"])
                        self.app.character.say(f"Lua: {item}")
                        break
            return
        
        # Dances
        if self.current_page == "dances":
            dance_map = {
                "Worm": "worm", "Moonwalk": "moonwalk",
                "Thriller": "thriller", "Robot": "robot", "Disco": "disco"
            }
            dance = dance_map.get(item)
            if dance:
                self.app.character.set_dance(dance)
                self.app.character.say(f"{item}!")
                self.hide()
            return
        
        # Settings
        if self.current_page == "settings":
            if item == "Volume Up":
                vol = min(1.0, self.config.get("volume", 0.8) + 0.1)
                self.config.set("volume", vol)
                self.app.audio_player.set_volume(vol)
                self.app.character.say(f"Vol: {int(vol*100)}%")
            elif item == "Volume Down":
                vol = max(0.0, self.config.get("volume", 0.8) - 0.1)
                self.config.set("volume", vol)
                self.app.audio_player.set_volume(vol)
                self.app.character.say(f"Vol: {int(vol*100)}%")
            elif item == "Auto-Play Toggle":
                self.app.toggle_auto_play()
            return
        
        # Create skin editor
        if self.current_page == "create_skin":
            self._handle_skin_editor(item)
    
    def _apply_body_customization(self, category: str, item: str):
        """Apply body customization to current skin"""
        skin = self.skin_loader.get_current_skin()
        
        # Map categories to skin data paths
        config_map = {
            "body_shape": ("body_shape", "type"),
            "arm_style": ("limbs", "arm_style"),
            "leg_style": ("limbs", "leg_style"),
            "head_shape": ("head", "shape"),
            "hair_style": ("hair", "style"),
            "ear_style": ("head", "ear_style"),
            "hand_style": ("limbs", "hand_style"),
            "foot_style": ("limbs", "foot_style"),
            "outfit_type": ("outfit", "type"),
            "tail_style": ("accessories", "tail_type"),
        }
        
        if category in config_map:
            section, key = config_map[category]
            if section not in skin:
                skin[section] = {}
            skin[section][key] = item.lower().replace(" ", "_")
        
        # Handle scale adjustments
        if category == "body_scale":
            if "body_scale" not in skin:
                skin["body_scale"] = {"height": 1.0, "width": 1.0, "head_size": 1.0, "limb_length": 1.0}
            scale = skin["body_scale"]
            if item == "Height +":
                scale["height"] = min(3.0, scale.get("height", 1.0) + 0.1)
            elif item == "Height -":
                scale["height"] = max(0.3, scale.get("height", 1.0) - 0.1)
            elif item == "Width +":
                scale["width"] = min(3.0, scale.get("width", 1.0) + 0.1)
            elif item == "Width -":
                scale["width"] = max(0.3, scale.get("width", 1.0) - 0.1)
            elif item == "Head Size +":
                scale["head_size"] = min(3.0, scale.get("head_size", 1.0) + 0.1)
            elif item == "Head Size -":
                scale["head_size"] = max(0.3, scale.get("head_size", 1.0) - 0.1)
            elif item == "Limb Length +":
                scale["limb_length"] = min(3.0, scale.get("limb_length", 1.0) + 0.1)
            elif item == "Limb Length -":
                scale["limb_length"] = max(0.3, scale.get("limb_length", 1.0) - 0.1)
            elif item == "Torso Width +":
                skin.setdefault("body_shape", {})["torso_width"] = min(3.0, skin.get("body_shape", {}).get("torso_width", 1.0) + 0.1)
            elif item == "Torso Width -":
                skin.setdefault("body_shape", {})["torso_width"] = max(0.3, skin.get("body_shape", {}).get("torso_width", 1.0) - 0.1)
        
        # Save and reload
        temp_path = self.config.SKINS_PATH / "_current.msk"
        self.skin_loader.encryptor.save_skin_file(temp_path, skin)
        self.skin_loader.load_skin(str(temp_path))
        self.app.character.say(f"{category}: {item}")
    
    def _apply_clothing(self, category: str, item: str):
        """Apply clothing/accessory item to character"""
        skin = self.skin_loader.get_current_skin()
        if "clothing" not in skin:
            skin["clothing"] = {}
        
        skin["clothing"][category] = item
        
        temp_path = self.config.SKINS_PATH / "_current.msk"
        self.skin_loader.encryptor.save_skin_file(temp_path, skin)
        self.skin_loader.load_skin(str(temp_path))
        self.app.character.say(f"{category}: {item}")
    
    def _start_skin_creation(self):
        """Start the skin creation process"""
        self.editing_skin = self.skin_loader.encryptor.create_default_skin("New Skin")
        self.current_page = "create_skin"
        self._update_items()
        self._show_skin_preview()
    
    def _show_skin_preview(self):
        """Show skin preview window"""
        if self.skin_preview_window:
            try:
                self.skin_preview_window.destroy()
            except:
                pass
        
        self.skin_preview_window = tk.Toplevel(self.root)
        self.skin_preview_window.title("Skin Preview")
        self.skin_preview_window.geometry("350x520+150+100")
        self.skin_preview_window.attributes('-topmost', True)
        self.skin_preview_window.configure(bg='#2a2a2a')
        
        tk.Label(self.skin_preview_window, text="SKIN PREVIEW", bg='#2a2a2a', fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        self.skin_preview_canvas = tk.Canvas(self.skin_preview_window, width=320, height=380, bg='#1a1a1a')
        self.skin_preview_canvas.pack(pady=5)
        
        self._draw_skin_preview()
        
        if self.editing_skin:
            colors = self.editing_skin.get("colors", {})
            info_frame = tk.Frame(self.skin_preview_window, bg='#2a2a2a')
            info_frame.pack(fill='x', padx=10)
            
            color_keys = ["body", "hair", "eyes", "skin", "mouth", "body_outline"]
            for i, key in enumerate(color_keys):
                if key in colors:
                    color = colors[key]
                    hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
                    tk.Label(info_frame, text=f"{key}:", bg='#2a2a2a', fg='white', 
                            font=('Arial', 8)).grid(row=i, column=0, sticky='w', pady=1)
                    color_label = tk.Label(info_frame, text=f"  {hex_color}  ", bg=hex_color, 
                                          fg='white' if sum(color[:3]) < 400 else 'black', 
                                          font=('Arial', 8))
                    color_label.grid(row=i, column=1, padx=5, pady=1)
    
    def _draw_skin_preview(self):
        """Draw the character preview with current skin colors"""
        if not self.skin_preview_canvas or not self.editing_skin:
            return
        
        try:
            self.skin_preview_canvas.delete("all")
        except:
            return
        
        colors = self.editing_skin.get("colors", {})
        outfit = self.editing_skin.get("outfit", {})
        outfit_type = outfit.get("type", "default")
        
        # Determine body colors based on outfit type
        if outfit_type == "none":
            body_color = tuple(colors.get("skin", [255, 220, 180, 255]))
            body_outline_color = tuple(colors.get("skin_outline", [200, 170, 140, 255]))
        elif outfit_type == "armor":
            body_color = (180, 180, 200, 255)
            body_outline_color = (140, 140, 160, 255)
        elif outfit_type == "suit":
            body_color = (30, 30, 50, 255)
            body_outline_color = (15, 15, 30, 255)
        elif outfit_type == "tuxedo":
            body_color = (20, 20, 30, 255)
            body_outline_color = (10, 10, 20, 255)
        elif outfit_type == "robe":
            body_color = (120, 60, 140, 255)
            body_outline_color = (80, 30, 100, 255)
        elif outfit_type == "space_suit":
            body_color = (200, 200, 220, 255)
            body_outline_color = (150, 150, 170, 255)
        elif outfit_type == "ninja":
            body_color = (20, 20, 30, 255)
            body_outline_color = (10, 10, 15, 255)
        elif outfit_type == "military":
            body_color = (60, 80, 40, 255)
            body_outline_color = (40, 50, 25, 255)
        elif outfit_type == "pirate":
            body_color = (80, 20, 30, 255)
            body_outline_color = (50, 10, 15, 255)
        elif outfit_type == "cyberpunk":
            body_color = (40, 40, 80, 255)
            body_outline_color = (0, 255, 200, 255)
        elif outfit_type == "steampunk":
            body_color = (100, 70, 40, 255)
            body_outline_color = (180, 140, 40, 255)
        elif outfit_type == "raincoat":
            body_color = (255, 255, 100, 255)
            body_outline_color = (200, 200, 60, 255)
        elif outfit_type == "kimono":
            body_color = (200, 50, 80, 255)
            body_outline_color = (150, 30, 50, 255)
        elif outfit_type == "overalls":
            body_color = (80, 120, 200, 255)
            body_outline_color = (50, 80, 150, 255)
        elif outfit_type == "custom":
            body_color = tuple(outfit.get("top_color", [100, 180, 255, 255]))
            body_outline_color = tuple(outfit.get("bottom_color", [50, 130, 200, 255]))
        else:
            body_color = tuple(colors.get("body", [100, 180, 255, 255]))
            body_outline_color = tuple(colors.get("body_outline", [50, 130, 200, 255]))
        
        c = {
            "body": body_color,
            "body_outline": body_outline_color,
            "skin": tuple(colors.get("skin", [255, 220, 180, 255])),
            "skin_outline": tuple(colors.get("skin_outline", [200, 170, 140, 255])),
            "hair": tuple(colors.get("hair", [80, 60, 40, 255])),
            "hair_outline": tuple(colors.get("hair_outline", [60, 40, 20, 255])),
            "eyes": tuple(colors.get("eyes", [100, 180, 255, 255])),
            "pupils": tuple(colors.get("pupils", [30, 30, 30, 255])),
            "mouth": tuple(colors.get("mouth", [200, 100, 100, 255])),
            "feet": tuple(colors.get("feet", [50, 50, 50, 255])),
        }
        
        def hx(color_tuple):
            return f'#{color_tuple[0]:02x}{color_tuple[1]:02x}{color_tuple[2]:02x}'
        
        canvas = self.skin_preview_canvas
        cx, cy = 160, 200
        ground_y = 360
        
        canvas.create_oval(cx-50, ground_y-5, cx+50, ground_y+10, fill='#000000', outline='')
        
        for side, lx, fx in [(-1, cx-22, cx-14), (1, cx+22, cx+14)]:
            canvas.create_line(cx-26*side, cy+10, cx-30*side, cy-35, fill=hx(c["body_outline"]), width=18)
            canvas.create_line(cx-26*side, cy+10, cx-30*side, cy-35, fill=hx(c["body"]), width=12)
            canvas.create_line(cx-30*side, cy-35, lx, ground_y-70, fill=hx(c["body_outline"]), width=14)
            canvas.create_line(cx-30*side, cy-35, lx, ground_y-70, fill=hx(c["body"]), width=9)
            canvas.create_oval(fx-18, ground_y-78, fx+20, ground_y-48, fill=hx(c["feet"]), outline=hx(c["body_outline"]))
        
        canvas.create_polygon(cx-28, cy+10, cx+28, cy+10, cx+34, cy-50, cx-34, cy-50, 
                             fill=hx(c["body"]), outline=hx(c["body_outline"]), width=2)
        
        # Draw outfit details in preview
        if outfit_type == "suit" or outfit_type == "tuxedo":
            canvas.create_polygon(cx-4, cy-43, cx+4, cy-43, cx+6, cy-20, cx-6, cy-20, fill='#b41e1e', outline='#8c1414', width=1)
            canvas.create_polygon(cx-15, cy-50, cx, cy-35, cx+15, cy-50, fill='#ffffff', outline=hx(c["body_outline"]), width=1)
        elif outfit_type == "armor":
            for i in range(2):
                py = cy - 35 + i * 15
                canvas.create_oval(cx-18, py-4, cx+18, py+8, fill='#c8c8dc', outline=hx(c["body_outline"]), width=1)
            for side in [-1, 1]:
                canvas.create_oval(cx-38*side, cy-53, cx-22*side, cy-40, fill='#b4b4c8', outline=hx(c["body_outline"]), width=2)
            canvas.create_rectangle(cx-26, cy+2, cx+26, cy+12, fill='#645028', outline=hx(c["body_outline"]), width=1)
            canvas.create_rectangle(cx-4, cy, cx+4, cy+14, fill='#c8b428', outline='#968214')
        elif outfit_type == "ninja":
            canvas.create_rectangle(cx-24, cy, cx+24, cy+10, fill='#32323c', outline='#1e1e23', width=1)
        
        for side in [-1, 1]:
            canvas.create_line(cx-34*side, cy-50, cx-48*side, cy-40, fill=hx(c["body_outline"]), width=14)
            canvas.create_line(cx-34*side, cy-50, cx-48*side, cy-40, fill=hx(c["body"]), width=9)
            canvas.create_line(cx-48*side, cy-40, cx-36*side, cy-20, fill=hx(c["body_outline"]), width=11)
            canvas.create_line(cx-48*side, cy-40, cx-36*side, cy-20, fill=hx(c["body"]), width=7)
            canvas.create_oval(cx-36*side-12, cy-28, cx-36*side+12, cy-8, fill=hx(c["skin"]), outline=hx(c["skin_outline"]))
        
        head_y = cy - 115
        canvas.create_oval(cx-40, head_y-5, cx+40, head_y+65, fill=hx(c["skin"]), outline=hx(c["skin_outline"]), width=2)
        canvas.create_oval(cx-42, head_y-3, cx+42, head_y+28, fill=hx(c["hair"]), outline=hx(c["hair_outline"]), width=1)
        
        eye_y = head_y + 22
        for es in [-1, 1]:
            ex = cx - 18 * es
            canvas.create_oval(ex-14, eye_y, ex+14, eye_y+16, fill='white', outline=hx(c["skin_outline"]), width=1)
            canvas.create_oval(ex-9, eye_y+4, ex+9, eye_y+12, fill=hx(c["eyes"]))
            canvas.create_oval(ex-5, eye_y+6, ex+5, eye_y+10, fill=hx(c["pupils"]))
        
        mouth_y = head_y + 42
        canvas.create_arc(cx-10, mouth_y, cx+10, mouth_y+14, start=0, extent=180, 
                         style='arc', outline=hx(c["mouth"]), width=2)
        
        ear_y = head_y - 2
        for es in [-1, 1]:
            canvas.create_line(cx-22*es, ear_y, cx-16*es, ear_y-45, fill=hx(c["body_outline"]), width=12)
            canvas.create_line(cx-22*es, ear_y, cx-16*es, ear_y-45, fill=hx(c["body"]), width=7)
        
        tag_y = cy - 35
        canvas.create_rectangle(cx-35, tag_y-8, cx+35, tag_y+8, fill='#333333', outline='white', width=1)
        for i in range(6):
            canvas.create_oval(cx-22+i*8-2, tag_y-2, cx-22+i*8+2, tag_y+2, fill='white')
        
        canvas.create_text(cx, ground_y+20, text=self.editing_skin.get("name", "New Skin"), 
                          fill='white', font=('Arial', 10))
    
    def _handle_skin_editor(self, item: str):
        """Handle skin editor actions"""
        if item == "Back":
            self.current_page = "main"
            self._update_items()
            if self.skin_preview_window:
                self.skin_preview_window.destroy()
                self.skin_preview_window = None
            self.editing_skin = None
        elif item == "Body Color":
            if self.menu_window: self.menu_window.withdraw()
            self._pick_skin_color("body")
            if self.menu_window: self.menu_window.deiconify()
        elif item == "Hair Color":
            if self.menu_window: self.menu_window.withdraw()
            self._pick_skin_color("hair")
            if self.menu_window: self.menu_window.deiconify()
        elif item == "Eye Color":
            if self.menu_window: self.menu_window.withdraw()
            self._pick_skin_color("eyes")
            if self.menu_window: self.menu_window.deiconify()
        elif item == "Skin Color":
            if self.menu_window: self.menu_window.withdraw()
            self._pick_skin_color("skin")
            if self.menu_window: self.menu_window.deiconify()
        elif item == "Mouth Color":
            if self.menu_window: self.menu_window.withdraw()
            self._pick_skin_color("mouth")
            if self.menu_window: self.menu_window.deiconify()
        elif item == "Outfit Color":
            if self.menu_window: self.menu_window.withdraw()
            self._pick_skin_color("outfit_primary")
            if self.menu_window: self.menu_window.deiconify()
        elif item == "Preview":
            self._apply_skin_preview()
        elif item == "Write Lua":
            self._edit_lua_script()
        elif item == "Save Skin":
            if self.menu_window: self.menu_window.withdraw()
            self._save_current_skin()
            if self.menu_window: self.menu_window.deiconify()
    
    def _pick_skin_color(self, color_key: str):
        """Pick a color for a specific skin part"""
        if not self.editing_skin:
            return
        
        colors = self.editing_skin.get("colors", {})
        current = tuple(colors.get(color_key, [255, 255, 255, 255])[:3])
        
        color = colorchooser.askcolor(
            title=f"Choose {color_key} color",
            initialcolor=current
        )
        if color and color[0]:
            colors[color_key] = list(int(c) for c in color[0]) + [255]
            self._draw_skin_preview()
            self.app.character.say(f"{color_key} updated!")
    
    def _apply_skin_preview(self):
        """Apply the editing skin to the character temporarily"""
        if not self.editing_skin:
            return
        
        temp_path = self.config.SKINS_PATH / "_preview.msk"
        self.skin_loader.encryptor.save_skin_file(temp_path, self.editing_skin)
        self.skin_loader.load_skin(str(temp_path))
        self.app.character.say("Preview applied!")
    
    def _edit_lua_script(self):
        """Edit the Lua script"""
        if not self.editing_skin:
            return
        
        editor = tk.Toplevel(self.root)
        editor.title("Lua Script Editor")
        editor.geometry("600x400")
        editor.attributes('-topmost', True)
        
        text_widget = tk.Text(editor, font=('Courier', 10), bg='#1e1e1e', fg='#d4d4d4', insertbackground='white')
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', self.editing_skin.get("lua_script", ""))
        
        def save_script():
            self.editing_skin["lua_script"] = text_widget.get('1.0', 'end-1c')
            editor.destroy()
            self.app.character.say("Lua script saved!")
        
        btn_frame = tk.Frame(editor, bg='#2d2d2d')
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="Save", command=save_script, bg='#4a90d9', fg='white').pack(side='left', padx=5, pady=5)
        tk.Button(btn_frame, text="Cancel", command=editor.destroy, bg='#555555', fg='white').pack(side='left', padx=5, pady=5)
    
    def _save_current_skin(self):
        """Save the current skin"""
        if not self.editing_skin:
            return
        
        name = simpledialog.askstring("Skin Name", "Enter skin name:", 
                                       initialvalue=self.editing_skin.get("name", "Custom"))
        if name:
            self.editing_skin["name"] = name
            if self.skin_loader.save_skin(name, self.editing_skin):
                self.app.character.say(f"Skin '{name}' saved!")
                skin_path = self.config.SKINS_PATH / f"{name}.msk"
                self.skin_loader.load_skin(str(skin_path))
                self.current_page = "skins"
                self._update_items()
            else:
                self.app.character.say("Failed to save skin!")
    
    def _create_new_lua_script(self):
        """Create a new Lua script"""
        name = simpledialog.askstring("Script Name", "Enter script name:")
        if name:
            default_lua = self.skin_loader.encryptor._generate_default_lua()
            script_path = self.config.MODS_PATH / f"{name}.lua"
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(default_lua)
            self._scan_lua_scripts()
            self._update_items()
            self.app.character.say(f"Script '{name}' created!")
    
    def _execute_lua_file(self, script_path: str):
        """Execute a Lua script file"""
        if not self.lua_available:
            self.app.character.say("Lua not installed! pip install lupa")
            return
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script = f.read()
            
            lua_globals = self.lua.globals()
            lua_globals['memebot'] = {
                'log': lambda msg: logging.info(f"[Lua] {msg}"),
                'setEmotion': lambda e: setattr(self.app.character, 'emotion', e),
                'resetToDefault': lambda: self.skin_loader.load_skin(None),
            }
            
            self.lua.execute(script)
            
            on_load = lua_globals.get('onSkinLoad')
            if on_load is not None and callable(on_load):
                try:
                    on_load()
                except:
                    pass
            
            self.app.character.say("Lua executed!")
        except Exception as e:
            self.app.character.say(f"Lua error: {str(e)[:30]}")
    
    def _execute_lua_string(self, lua_code: str):
        """Execute Lua code from string"""
        if not self.lua_available:
            return
        
        try:
            lua_globals = self.lua.globals()
            lua_globals['memebot'] = {
                'log': lambda msg: logging.info(f"[Lua] {msg}"),
                'setEmotion': lambda e: setattr(self.app.character, 'emotion', e),
                'resetToDefault': lambda: self.skin_loader.load_skin(None),
            }
            
            self.lua.execute(lua_code)
            
            on_load = lua_globals.get('onSkinLoad')
            if on_load is not None and callable(on_load):
                try:
                    on_load()
                except:
                    pass
        except:
            pass