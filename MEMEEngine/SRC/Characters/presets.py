"""
MEMEEngine Character Presets
Pre-built playable characters with stats and animations
"""

PRESET_CHARACTERS = {
    "memebot": {
        "name": "MEMEBOT",
        "description": "The classic MEMEBOT character",
        "animations": ["idle", "walk", "run", "jump", "attack", "hit", "die"],
        "default_colors": {"body": "#64B4FF", "outline": "#3282C8", "eyes": "#FFFFFF"},
        "width": 40,
        "height": 50,
        "speed": 5,
        "jump_power": -14,
        "health": 100,
        "attack_power": 15
    },
    "pixel_knight": {
        "name": "Pixel Knight",
        "description": "A brave pixel knight with sword and shield",
        "animations": ["idle", "walk", "run", "jump", "slash", "block", "die"],
        "default_colors": {"armor": "#C0C0C0", "cape": "#FF0000", "sword": "#FFD700"},
        "width": 42,
        "height": 52,
        "speed": 4,
        "jump_power": -13,
        "health": 150,
        "attack_power": 25
    },
    "ninja_cat": {
        "name": "Ninja Cat",
        "description": "A stealthy feline warrior",
        "animations": ["idle", "walk", "run", "jump", "throw", "vanish", "die"],
        "default_colors": {"fur": "#FF8C00", "mask": "#000000", "eyes": "#00FF00"},
        "width": 38,
        "height": 44,
        "speed": 7,
        "jump_power": -16,
        "health": 80,
        "attack_power": 12
    },
    "space_blob": {
        "name": "Space Blob",
        "description": "An alien blob from outer space",
        "animations": ["idle", "bounce", "stretch", "squash", "absorb", "die"],
        "default_colors": {"body": "#00FF00", "eyes": "#000000", "spots": "#00CC00"},
        "width": 44,
        "height": 44,
        "speed": 4,
        "jump_power": -12,
        "health": 120,
        "attack_power": 18
    },
    "robot_dude": {
        "name": "Robot Dude",
        "description": "A funky robot with lasers and moves",
        "animations": ["idle", "walk", "run", "jump", "dance", "shoot", "die"],
        "default_colors": {"metal": "#808080", "lights": "#00FFFF", "joints": "#404040"},
        "width": 40,
        "height": 50,
        "speed": 5,
        "jump_power": -13,
        "health": 130,
        "attack_power": 20
    }
}