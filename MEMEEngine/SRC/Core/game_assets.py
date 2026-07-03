"""
MEMEEngine Asset Data Classes
Base dataclasses for all game assets
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple


@dataclass
class GameAsset:
    """Base class for all MEMEEngine assets"""
    id: str = ""
    name: str = ""
    asset_type: str = ""
    file_path: str = ""
    x: int = 0
    y: int = 0
    width: int = 40
    height: int = 40
    scale: float = 1.0
    rotation: float = 0.0
    z_index: int = 0
    visible: bool = True
    tags: List[str] = field(default_factory=list)
    custom_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GameCharacter(GameAsset):
    """Character asset with animations"""
    animation_state: str = "idle"
    speed: int = 5
    jump_power: int = -15
    can_jump: bool = True
    is_jumping: bool = False
    health: int = 100
    max_health: int = 100
    attack_power: int = 10
    lives: int = 3
    invincible: bool = False
    invincible_timer: int = 0
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    on_ground: bool = False
    facing_right: bool = True
    animation_frame: int = 0
    animation_timer: int = 0
    is_player: bool = False
    score: int = 0
    coins: int = 0


@dataclass
class GameMap:
    """Map/level asset"""
    name: str = ""
    background_color: str = "#87CEEB"
    background_image: str = ""
    width: int = 2400
    height: int = 600
    gravity: float = 0.8
    ground_y: int = 500
    platforms: List[Dict] = field(default_factory=list)
    spawn_point: Tuple[int, int] = (100, 400)
    end_point: Tuple[int, int] = (2200, 400)
    parallax_layers: List[Dict] = field(default_factory=list)
    camera_x: int = 0
    camera_y: int = 0


@dataclass
class GameCollectible(GameAsset):
    """Collectible item asset"""
    points: int = 10
    sound_effect: str = ""
    respawn_time: int = 0
    collected: bool = False
    bob_offset: float = 0.0
    sparkle_timer: int = 0


@dataclass
class GameEnemy(GameAsset):
    """Enemy asset"""
    health: int = 50
    max_health: int = 50
    speed: int = 2
    damage: int = 10
    patrol_distance: int = 100
    patrol_start_x: int = 0
    moving_right: bool = True
    is_boss: bool = False
    boss_phase: int = 0
    attack_timer: int = 0
    attack_cooldown: int = 60
    death_timer: int = 0
    is_dead: bool = False


@dataclass
class GameSound:
    """Sound/music asset"""
    name: str
    file_path: str
    loop: bool = False
    volume: float = 1.0
    is_playing: bool = False


@dataclass
class GameMeme:
    """Meme video/GIF asset"""
    name: str
    file_path: str
    trigger_type: str = "collision"
    trigger_value: Any = None
    played: bool = False


@dataclass
class GameUIElement:
    """UI element for HUD"""
    element_type: str = "text"
    text: str = ""
    x: int = 10
    y: int = 10
    font_size: int = 20
    color: str = "#FFFFFF"
    visible: bool = True
    binding: str = ""