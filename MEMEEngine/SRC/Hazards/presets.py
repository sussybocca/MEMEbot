"""
MEMEEngine Hazard Type Definitions
Environmental hazards and obstacle behaviors
"""

HAZARD_TYPES = {
    "meteor": {
        "name": "Meteor",
        "description": "A falling meteor from the sky",
        "damage": 25,
        "width": 40,
        "height": 40,
        "color": "#FF4500",
        "outline": "#FF0000",
        "behavior": "falling",
        "fall_speed": 5,
        "respawn": True,
        "respawn_min_y": -200,
        "respawn_max_y": -50
    },
    "lava": {
        "name": "Lava Pit",
        "description": "A pool of molten lava that damages on contact",
        "damage": 50,
        "width": 2000,
        "height": 60,
        "color": "#FF4500",
        "outline": "#FF0000",
        "behavior": "static",
        "respawn": False,
        "surface_anim": True
    },
    "spike": {
        "name": "Spike Trap",
        "description": "Sharp spikes that damage the player",
        "damage": 30,
        "width": 40,
        "height": 40,
        "color": "#C0C0C0",
        "outline": "#808080",
        "behavior": "static",
        "respawn": False
    },
    "laser": {
        "name": "Laser Beam",
        "description": "A deadly laser beam that activates periodically",
        "damage": 40,
        "width": 20,
        "height": 100,
        "color": "#FF0000",
        "outline": "#FF4444",
        "behavior": "timed",
        "active_duration": 30,
        "inactive_duration": 60,
        "respawn": False
    }
}