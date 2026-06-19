"""
MEMEBOT Dance Engine
Handles all dance move animations and choreography
"""

import math
import random

class DanceEngine:
    """Calculates dance animation parameters for all dance styles"""
    
    # Dance duration in frames (30fps)
    DURATIONS = {
        "worm": 180,
        "moonwalk": 200,
        "thriller": 180,
        "robot": 180,
        "disco": 180,
        "dancing": 120,
        "meme": 150,
        "waving": 90,
        "bouncing": 60,
        "video_dancing": 120,
    }
    
    @staticmethod
    def get_params(character):
        """
        Calculate dance parameters based on current state
        
        Args:
            character: CharacterRenderer instance
        
        Returns:
            Tuple of (leg_swing, arm_swing, body_bob, extra_spin, arm_raise, head_bob, body_squash, laying_down)
        """
        state = character.state
        timer = character.dance_timer
        
        # Auto-end dance when duration expires
        if character.dance_override and timer >= DanceEngine.DURATIONS.get(state, 120):
            character.state = character.DANCE_IDLE
            character.dance_override = False
            character.y = character.dance_start_y
        
        # Route to appropriate dance handler
        if state == character.DANCE_WORM:
            return DanceEngine._worm(character, timer)
        elif state == character.DANCE_MOONWALK:
            return DanceEngine._moonwalk(character, timer)
        elif state == character.DANCE_THRILLER:
            return DanceEngine._thriller(character, timer)
        elif state == character.DANCE_ROBOT:
            return DanceEngine._robot(character, timer)
        elif state == character.DANCE_DISCO:
            return DanceEngine._disco(character, timer)
        elif state == character.DANCE_DANCING:
            return DanceEngine._default_dance(character, timer)
        elif state == character.DANCE_MEME:
            return DanceEngine._meme_dance(character, timer)
        elif state == character.DANCE_VIDEO:
            return DanceEngine._video_dance(character, timer)
        elif state in [character.DANCE_WALKING, character.DANCE_RUNNING]:
            return DanceEngine._walking(character, timer)
        elif state == character.DANCE_WAVING:
            return DanceEngine._waving(character, timer)
        elif state == character.DANCE_BOUNCING:
            return DanceEngine._bouncing(character, timer)
        else:
            return DanceEngine._idle(character, timer)
    
    @staticmethod
    def _worm(character, timer):
        """Worm dance - character lays down and undulates"""
        t = timer * 0.06
        cycle = t % (2 * math.pi)
        duration = DanceEngine.DURATIONS["worm"]
        third = duration / 3
        
        if timer < third:
            # Going down
            p = timer / third
            character.y = character.dance_start_y + int(p * 100)
            body_squash = 1.0 - p * 0.5
            body_bob = -int(p * 35)
            leg_swing = int(p * 25)
            arm_swing = -int(p * 15)
            head_bob = -int(p * 45)
            laying_down = False
        elif timer < third * 2:
            # On ground undulating
            laying_down = True
            wp = (timer - third) / third
            character.y = character.dance_start_y + 100
            body_squash = 0.5 + math.sin(wp * 8) * 0.2
            body_bob = int(math.sin(wp * 5) * 20)
            leg_swing = int(math.cos(wp * 4) * 30)
            arm_swing = int(math.sin(wp * 4 + 1) * 25)
            head_bob = int(math.sin(wp * 5) * 15)
        else:
            # Getting up
            p = (timer - third * 2) / third
            character.y = character.dance_start_y + 100 - int(p * 100)
            body_squash = 0.5 + p * 0.5
            body_bob = -35 + int(p * 35)
            leg_swing = 25 - int(p * 25)
            arm_swing = -15 + int(p * 15)
            head_bob = -45 + int(p * 45)
            laying_down = False
        
        if timer % 6 == 0:
            character.add_particle(240, int(350 + (character.y - character.dance_start_y)), "sparkle", 3)
        
        return (leg_swing, arm_swing, body_bob, 0, 0, head_bob, body_squash, laying_down)
    
    @staticmethod
    def _moonwalk(character, timer):
        """Moonwalk - smooth backward glide"""
        t = timer * 0.05
        character.x = character.dance_start_x - (t * 2.5)
        
        phase = t * 1.5
        leg_swing = int(math.sin(phase) * 28)
        arm_swing = int(math.cos(phase) * 22)
        extra_spin = int(math.sin(phase * 0.5) * 4)
        
        if timer % 10 == 0:
            character.add_particle(240, 520, "sparkle", 2)
        
        return (leg_swing, arm_swing, 0, extra_spin, 0, 0, 1.0, False)
    
    @staticmethod
    def _thriller(character, timer):
        """Thriller - stomping and claw hands"""
        beat = (timer // 10) % 8
        
        moves = {
            0: (25, 45, 20, -15, 0),
            1: (-25, -10, -20, 15, 0),
            2: (0, 30, 35, -5, 15),
            3: (0, 30, -35, 5, -15),
            4: (20, 40, 15, -10, 5),
            5: (-20, -5, -15, 10, -5),
            6: (0, 35, 30, -5, 12),
            7: (0, 35, -30, 5, -12),
        }
        
        ls, ar, aw, bb, es = moves.get(beat, (0, 0, 0, 0, 0))
        head_bob = int(math.sin(timer * 0.3) * 8)
        
        if timer % 5 == 0:
            character.add_particle(240, 300, "star", 4)
        
        return (ls, aw, bb, es, ar, head_bob, 1.0, False)
    
    @staticmethod
    def _robot(character, timer):
        """Robot - mechanical popping"""
        beat = (timer // 12) % 12
        
        robot_moves = {
            0: (0, 20, 0, -15, 0),
            1: (0, 0, 0, 15, 0),
            2: (0, 40, 15, 0, 0),
            3: (0, 40, -15, 0, 0),
            4: (0, 20, 0, 0, 20),
            5: (0, 20, 0, 0, -20),
            6: (0, 25, 30, 0, 0),
            7: (0, 25, -30, 0, 0),
            8: (20, 0, 0, -10, 0),
            9: (-20, 0, 0, 10, 0),
            10: (0, 35, 0, 0, 0),
            11: (0, 0, 0, 0, 0),
        }
        
        ls, ar, aw, bb, es = robot_moves.get(beat, (0, 0, 0, 0, 0))
        
        if timer % 15 == 0:
            character.add_particle(240, 350, "sparkle", 1)
        
        return (ls, aw, bb, es, ar, 0, 1.0, False)
    
    @staticmethod
    def _disco(character, timer):
        """Disco - Saturday Night Fever style"""
        beat = (timer // 10) % 8
        
        disco_moves = {
            0: (15, 50, 40, 8, 10),
            1: (-15, 50, -40, 8, -10),
            2: (10, 0, 35, 8, 20),
            3: (-10, 0, -35, 8, -20),
            4: (15, 45, 30, 8, 8),
            5: (-15, 45, -30, 8, -8),
            6: (10, 0, 40, 8, 25),
            7: (-10, 0, -40, 8, -25),
        }
        
        ls, ar, aw, bb, es = disco_moves.get(beat, (0, 0, 0, 0, 0))
        head_bob = int(math.sin(timer * 0.25) * 6)
        
        if beat in [2, 3, 6, 7]:
            character.x += (2 if beat in [2, 6] else -2)
        
        if timer % 6 == 0:
            character.add_particle(240, 300, "music", 3)
        
        return (ls, aw, bb, es, ar, head_bob, 1.0, False)
    
    @staticmethod
    def _default_dance(character, timer):
        """Default meme dance"""
        t = timer * 0.12
        leg_swing = int(math.sin(t * 2.5) * 18)
        arm_swing = int(math.sin(t * 2) * 35)
        body_bob = int(abs(math.sin(t * 3)) * 12)
        arm_raise = int(math.sin(t * 0.8) * 15)
        extra_spin = int(math.sin(t * 1.5) * 6)
        
        if timer % 10 == 0:
            character.add_particle(240, 320, "sparkle", 2)
        
        return (leg_swing, arm_swing, body_bob, extra_spin, arm_raise, 0, 1.0, False)
    
    @staticmethod
    def _meme_dance(character, timer):
        """Extra wild meme dance"""
        t = timer * 0.2
        leg_swing = int(math.sin(t * 3) * 22)
        arm_swing = int(math.sin(t * 3.5) * 38)
        body_bob = int(abs(math.sin(t * 2.5)) * 20)
        arm_raise = int(math.cos(t * 2.5) * 28)
        extra_spin = int(math.sin(t * 5) * 14)
        
        if timer % 4 == 0:
            character.add_particle(240, 300, "star", 5)
        
        return (leg_swing, arm_swing, body_bob, extra_spin, arm_raise, 0, 1.0, False)
    
    @staticmethod
    def _video_dance(character, timer):
        """Video watching dance"""
        t = timer * 0.1
        leg_swing = int(math.sin(t * 2) * 14)
        arm_swing = int(math.sin(t * 1.8) * 28)
        body_bob = int(abs(math.sin(t * 2)) * 9)
        extra_spin = int(math.sin(t * 0.5) * 5)
        
        return (leg_swing, arm_swing, body_bob, extra_spin, 0, 0, 1.0, False)
    
    @staticmethod
    def _walking(character, timer):
        """Walking/running animation"""
        character.dance_override = False
        speed = 0.14 if character.state == character.DANCE_WALKING else 0.32
        mult = 20 if character.state == character.DANCE_WALKING else 28
        arm_mult = 14 if character.state == character.DANCE_WALKING else 24
        bob_mult = 5 if character.state == character.DANCE_WALKING else 10
        
        character.walk_cycle = (character.walk_cycle + speed) % (2 * math.pi)
        phase = character.walk_cycle
        
        leg_swing = int(math.sin(phase) * mult)
        arm_swing = int(math.sin(phase + math.pi) * arm_mult)
        body_bob = int(abs(math.sin(phase * 2)) * bob_mult)
        
        return (leg_swing, arm_swing, body_bob, 0, 0, 0, 1.0, False)
    
    @staticmethod
    def _waving(character, timer):
        """Waving animation"""
        character.dance_override = True
        t = timer * 0.12
        arm_swing = int(math.sin(t * 2.5) * 55)
        arm_raise = 15
        body_bob = int(math.sin(t) * 4)
        
        return (0, arm_swing, body_bob, 0, arm_raise, 0, 1.0, False)
    
    @staticmethod
    def _bouncing(character, timer):
        """Bouncing animation"""
        character.dance_override = True
        body_bob = int(math.sin(character.frame * 0.5) * 25)
        
        return (0, 0, body_bob, 0, 0, 0, 1.0, False)
    
    @staticmethod
    def _idle(character, timer):
        """Idle animation"""
        character.dance_override = False
        return (0, 0, 0, 0, 0, 0, 1.0, False)