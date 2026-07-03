"""
MEMEEngine Game Templates Library
Pre-built game templates for quick creation
"""

GAME_TEMPLATES = {
    "platformer": {
        "name": "Platformer",
        "description": "Jump and run through levels collecting items",
        "default_controls": {
            "Left": "move_left",
            "Right": "move_right",
            "Up": "jump",
            "Space": "action"
        },
        "mechanics": ["gravity", "jumping", "collecting", "enemies", "platforms"],
        "win_condition": "reach_end",
        "target_score": 0,
        "default_map": "grassy_hills"
    },
    "endless_runner": {
        "name": "Endless Runner",
        "description": "Run forever avoiding obstacles",
        "default_controls": {
            "Up": "jump",
            "Down": "slide",
            "Space": "boost"
        },
        "mechanics": ["auto_scroll", "obstacles", "power_ups", "gravity"],
        "win_condition": "high_score",
        "target_score": 0,
        "default_map": "meme_city"
    },
    "meme_collector": {
        "name": "Meme Collector",
        "description": "Collect falling memes before they hit the ground",
        "default_controls": {
            "Left": "move_left",
            "Right": "move_right"
        },
        "mechanics": ["falling_objects", "scoring", "combo_system"],
        "win_condition": "target_score",
        "target_score": 100,
        "default_map": "beach_party"
    },
    "dodge_meteor": {
        "name": "Dodge the Meteor",
        "description": "Avoid falling meteors and survive as long as possible",
        "default_controls": {
            "Left": "move_left",
            "Right": "move_right",
            "Up": "jump",
            "Down": "duck"
        },
        "mechanics": ["falling_hazards", "power_ups", "survival_timer"],
        "win_condition": "survival_time",
        "target_score": 0,
        "default_map": "space_station"
    },
    "boss_battle": {
        "name": "Boss Battle",
        "description": "Defeat the boss by dodging attacks and striking back",
        "default_controls": {
            "Left": "move_left",
            "Right": "move_right",
            "Up": "jump",
            "Space": "attack"
        },
        "mechanics": ["boss_ai", "health_bars", "phase_changes", "gravity"],
        "win_condition": "defeat_boss",
        "target_score": 0,
        "default_map": "spooky_cave"
    },
    "rhythm_game": {
        "name": "Rhythm Game",
        "description": "Hit notes in time with the music",
        "default_controls": {
            "Left": "hit_left",
            "Up": "hit_up",
            "Right": "hit_right",
            "Down": "hit_down"
        },
        "mechanics": ["scrolling_notes", "timing", "combo_multiplier"],
        "win_condition": "song_complete",
        "target_score": 0,
        "default_map": "meme_city"
    }
}