"""
MEMEEngine Enemy Type Definitions
Enemy behaviors and properties for game enemies
"""

ENEMY_TYPES = {
    "slime": {
        "name": "Slime",
        "description": "A bouncy slime that patrols back and forth",
        "health": 50,
        "speed": 2,
        "damage": 10,
        "patrol_distance": 100,
        "width": 36,
        "height": 36,
        "color": "#32CD32",
        "outline": "#228B22",
        "is_boss": False,
        "behavior": "patrol",
        "score_value": 100
    },
    "skeleton": {
        "name": "Skeleton",
        "description": "A spooky skeleton warrior",
        "health": 75,
        "speed": 3,
        "damage": 15,
        "patrol_distance": 120,
        "width": 36,
        "height": 44,
        "color": "#F5F5DC",
        "outline": "#D2B48C",
        "is_boss": False,
        "behavior": "patrol",
        "score_value": 150
    },
    "ghost": {
        "name": "Ghost",
        "description": "An ethereal ghost that floats through walls",
        "health": 40,
        "speed": 2,
        "damage": 10,
        "patrol_distance": 150,
        "width": 36,
        "height": 40,
        "color": "#DDA0DD",
        "outline": "#BA55D3",
        "is_boss": False,
        "behavior": "patrol",
        "score_value": 125
    },
    "robot_enemy": {
        "name": "Robot Enemy",
        "description": "A mechanical enemy with laser eyes",
        "health": 60,
        "speed": 3,
        "damage": 12,
        "patrol_distance": 120,
        "width": 36,
        "height": 40,
        "color": "#808080",
        "outline": "#606060",
        "is_boss": False,
        "behavior": "patrol",
        "score_value": 175
    },
    "meme_troll": {
        "name": "Meme Troll",
        "description": "A mischievous troll that taunts the player",
        "health": 45,
        "speed": 2,
        "damage": 8,
        "patrol_distance": 100,
        "width": 36,
        "height": 36,
        "color": "#FF6347",
        "outline": "#FF4500",
        "is_boss": False,
        "behavior": "patrol",
        "score_value": 130
    },
    "boss_slime": {
        "name": "Boss Slime",
        "description": "A massive slime boss with multiple phases",
        "health": 200,
        "speed": 3,
        "damage": 20,
        "patrol_distance": 0,
        "width": 60,
        "height": 60,
        "color": "#8B0000",
        "outline": "#FF0000",
        "is_boss": True,
        "behavior": "boss",
        "score_value": 1000,
        "phases": [
            {"health_threshold": 1.0, "speed": 3, "attack_cooldown": 60},
            {"health_threshold": 0.5, "speed": 5, "attack_cooldown": 30},
        ]
    }
}