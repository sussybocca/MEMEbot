"""
MEMEBOT 2D Character Renderer - Drawing Module
Handles standing and laying character drawing with body parts
Part 2 of 3 - Body Drawing
"""

import math

def draw_standing_character(renderer, draw, c, cfg, cx, ground_y, leg_swing, arm_swing, 
                           body_bob, extra_spin, arm_raise, head_bob, idle_bonus):
    """Draw standing character with FULL body customization from MSK file"""
    
    from character_accessories import (draw_tail, draw_cape, draw_wings, draw_scarf,
                                       draw_hat, draw_mask, draw_glasses, draw_shirt,
                                       draw_pants, draw_shoes, draw_outfit_details)
    
    shape = cfg["shape"]
    limbs = cfg["limbs"]
    head_cfg = cfg["head_cfg"]
    hair_cfg = cfg["hair_cfg"]
    outfit_cfg = cfg["outfit_cfg"]
    scale = cfg["scale"]
    clothing = cfg["clothing"]
    
    height_mult = scale.get("height", 1.0)
    width_mult = scale.get("width", 1.0)
    head_size_mult = scale.get("head_size", 1.0)
    limb_len_mult = scale.get("limb_length", 1.0)
    
    torso_w = shape.get("torso_width", 1.0) * width_mult
    torso_h = shape.get("torso_height", 1.0) * height_mult
    shoulder_w = shape.get("shoulder_width", 1.0) * width_mult
    hip_w = shape.get("hip_width", 1.0) * width_mult
    belly_s = shape.get("belly_size", 0.0)
    
    arm_len = limbs.get("arm_length", 1.0) * limb_len_mult
    arm_w = limbs.get("arm_width", 1.0)
    leg_len = limbs.get("leg_length", 1.0) * limb_len_mult
    leg_w = limbs.get("leg_width", 1.0)
    
    body_radius = int(55 * width_mult)
    hip_y = ground_y - int(155 * height_mult) + body_bob
    chest_y = hip_y - int(70 * torso_h)
    shoulder_y = chest_y - int(35 * torso_h)
    neck_y = shoulder_y - 8
    head_y = shoulder_y - int(73 * head_size_mult) + head_bob
    
    # Apply idle bonus to positions
    hip_y += idle_bonus.get('extra_bounce', 0) * 0.5
    shoulder_y += idle_bonus.get('extra_bounce', 0) * 0.3
    
    outfit_type = outfit_cfg.get("type", "default")
    
    # Get outfit colors
    outfit_primary = c.get("outfit_primary", c["body"])
    outfit_secondary = c.get("outfit_secondary", c["body_outline"])
    
    if outfit_type == "none":
        body_color = c["skin"]
        body_outline_color = c["skin_outline"]
    elif outfit_type == "armor":
        body_color = (180, 180, 200, 255)
        body_outline_color = (140, 140, 160, 255)
    elif outfit_type == "suit":
        body_color = (30, 30, 50, 255)
        body_outline_color = (15, 15, 30, 255)
    elif outfit_type == "robe":
        body_color = (120, 60, 140, 255)
        body_outline_color = (80, 30, 100, 255)
    elif outfit_type == "space_suit":
        body_color = (200, 200, 220, 255)
        body_outline_color = (150, 150, 170, 255)
    elif outfit_type == "ninja":
        body_color = (20, 20, 30, 255)
        body_outline_color = (10, 10, 15, 255)
    elif outfit_type == "swimwear":
        body_color = c["skin"]
        body_outline_color = c["skin_outline"]
    elif outfit_type == "overalls":
        body_color = (80, 120, 200, 255)
        body_outline_color = (50, 80, 150, 255)
    elif outfit_type == "tuxedo":
        body_color = (20, 20, 30, 255)
        body_outline_color = (10, 10, 20, 255)
    elif outfit_type == "raincoat":
        body_color = (255, 255, 100, 255)
        body_outline_color = (200, 200, 60, 255)
    elif outfit_type == "kimono":
        body_color = (200, 50, 80, 255)
        body_outline_color = (150, 30, 50, 255)
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
    elif outfit_type == "custom":
        body_color = tuple(outfit_cfg.get("top_color", [100, 180, 255, 255]))
        body_outline_color = tuple(outfit_cfg.get("bottom_color", [50, 130, 200, 255]))
    else:
        body_color = outfit_primary
        body_outline_color = outfit_secondary
    
    # ============================================
    # DRAW LEGS with customization
    # ============================================
    draw_legs(renderer, draw, c, limbs, body_color, body_outline_color, 
              cx, hip_y, ground_y, leg_swing, arm_swing, hip_w, leg_w, leg_len, idle_bonus)
    
    # ============================================
    # DRAW PANTS (clothing overlay)
    # ============================================
    pants = clothing.get("pants", "None")
    if pants and pants != "None":
        draw_pants(draw, c, cx, hip_y, ground_y, leg_swing, pants)
    
    # ============================================
    # DRAW TAIL (accessory)
    # ============================================
    tail_type = cfg.get("accessories", {}).get("tail_type", "default")
    if tail_type and tail_type != "default":
        draw_tail(renderer, draw, c, cx, hip_y, ground_y, tail_type)
    
    # ============================================
    # DRAW TORSO with body shape
    # ============================================
    draw_torso(draw, shape, body_color, body_outline_color, cx, hip_y, chest_y, shoulder_y, 
               shoulder_w, hip_w, width_mult, body_radius, idle_bonus)
    
    # Draw outfit-specific details
    draw_outfit_details(draw, c, cx, shoulder_y, chest_y, hip_y, neck_y, outfit_type, body_color, body_outline_color)
    
    # ============================================
    # DRAW BELLY
    # ============================================
    if belly_s > 0:
        belly_r = int(body_radius * 0.5 * belly_s)
        draw.ellipse([cx - belly_r, chest_y - belly_r//2, cx + belly_r, chest_y + belly_r], fill=(180, 220, 255, 150), outline=None)
    else:
        belly = [(cx - int(15 * width_mult), hip_y + 4), (cx + int(15 * width_mult), hip_y + 4),
                 (cx + int(20 * width_mult), chest_y + 8), (cx - int(20 * width_mult), chest_y + 8)]
        draw.polygon(belly, fill=(150, 210, 255, 255))
    
    # ============================================
    # DRAW SHIRT (clothing overlay)
    # ============================================
    shirt = clothing.get("shirts", "None")
    if shirt and shirt != "None":
        draw_shirt(draw, c, cx, hip_y, chest_y, shoulder_y, shirt)
    
    # ============================================
    # DRAW SCARF (clothing overlay)
    # ============================================
    scarf = clothing.get("scarfs", "None")
    if scarf and scarf != "None":
        draw_scarf(draw, c, cx, neck_y, shoulder_y, scarf)
    
    # ============================================
    # DRAW ARMS with customization
    # ============================================
    draw_arms(renderer, draw, c, limbs, body_color, body_outline_color, 
              cx, shoulder_y, chest_y, hip_y, shoulder_w, arm_w, arm_len, 
              arm_swing, arm_raise, idle_bonus)
    
    # ============================================
    # DRAW WINGS (accessory)
    # ============================================
    wings = clothing.get("wings", "None")
    if wings and wings != "None":
        draw_wings(draw, c, cx, chest_y, shoulder_y, wings)
    
    # ============================================
    # DRAW CAPE (accessory/clothing)
    # ============================================
    cape = clothing.get("cape", "None")
    if cape and cape != "None":
        draw_cape(renderer, draw, c, cx, shoulder_y, hip_y, cape)
    
    # ============================================
    # DRAW HEAD with shape customization
    # ============================================
    draw_head(renderer, draw, c, head_cfg, hair_cfg, clothing, 
              cx, head_y, head_size_mult, width_mult, height_mult, extra_spin, idle_bonus)
    
    # ============================================
    # DRAW EYES
    # ============================================
    draw_eyes(renderer, draw, c, head_cfg, cx, head_y, head_size_mult, width_mult, extra_spin)
    
    # ============================================
    # DRAW NOSE
    # ============================================
    draw_nose(renderer, draw, c, head_cfg, cx, head_y, head_size_mult, width_mult)
    
    # ============================================
    # DRAW MOUTH
    # ============================================
    draw_mouth(renderer, draw, c, head_cfg, cx, head_y, head_size_mult, extra_spin)
    
    # ============================================
    # DRAW EARS with style customization
    # ============================================
    draw_ears(renderer, draw, c, body_color, body_outline_color, head_cfg, cx, head_y, head_size_mult, extra_spin)
    
    # ============================================
    # DRAW SHOES (clothing)
    # ============================================
    shoes = clothing.get("shoes", "None")
    if shoes and shoes != "None":
        draw_shoes(draw, c, cx, ground_y, leg_swing, shoes)
    
    # ============================================
    # DRAW NAME TAG
    # ============================================
    tag_y = hip_y - body_radius - 30
    draw.rectangle([cx - 40, tag_y - 9, cx + 40, tag_y + 9], fill=c["tag_bg"], outline=c["tag_text"], width=1)
    for i in range(7):
        dx = cx - 25 + i * 8
        draw.ellipse([dx - 2, tag_y - 2, dx + 2, tag_y + 2], fill=c["tag_text"])


def draw_laying_character(renderer, draw, c, cfg, cx, ground_y, body_bob):
    """Draw laying down character"""
    lay_y = ground_y - 20
    body_x = cx + body_bob * 0.5
    body_length = 120
    body_radius = 55
    
    # Body
    draw.ellipse([body_x - body_length//2, lay_y - body_radius, body_x + body_length//2, lay_y + body_radius],
                fill=c["body"], outline=c["body_outline"], width=3)
    
    # Head
    head_x = body_x + body_length//2 + 20
    head_r = 28
    draw.ellipse([head_x - head_r, lay_y - head_r - 10, head_x + head_r, lay_y + head_r + 10],
                fill=c["skin"], outline=c["skin_outline"], width=2)
    draw.ellipse([head_x - head_r - 2, lay_y - head_r - 15, head_x + head_r + 2, lay_y + head_r//2 - 5],
                fill=c["hair"], outline=c["hair_outline"], width=1)
    
    # Eyes
    eye_y = lay_y - 5
    for es in [-1, 1]:
        ex = head_x - 8 * es
        if renderer.is_dead:
            # Cross eyes
            draw.line([ex - 6, eye_y - 6, ex + 6, eye_y + 6], fill=(255, 0, 0, 255), width=2)
            draw.line([ex + 6, eye_y - 6, ex - 6, eye_y + 6], fill=(255, 0, 0, 255), width=2)
        else:
            draw.ellipse([ex - 6, eye_y - 6, ex + 6, eye_y + 6], fill=(255, 255, 255, 255), outline=c["skin_outline"], width=1)
            draw.ellipse([ex - 3, eye_y - 3, ex + 3, eye_y + 3], fill=c["pupils"])
    
    # Arms
    for side in [-1, 1]:
        arm_x = body_x - 30 * side
        arm_y = lay_y + math.sin(renderer.dance_timer * 0.3 + side) * 20
        draw.line([arm_x, lay_y, arm_x - 20 * side, arm_y - 15], fill=c["body_outline"], width=10)
        draw.line([arm_x, lay_y, arm_x - 20 * side, arm_y - 15], fill=c["body"], width=6)
        
        # Legs
        leg_x = body_x + 30 * side
        leg_y = lay_y + math.cos(renderer.dance_timer * 0.3 + side) * 20
        draw.line([leg_x, lay_y, leg_x + 15 * side, leg_y - 10], fill=c["body_outline"], width=12)
        draw.line([leg_x, lay_y, leg_x + 15 * side, leg_y - 10], fill=c["body"], width=8)


def draw_legs(renderer, draw, c, limbs, body_color, body_outline_color, 
              cx, hip_y, ground_y, leg_swing, arm_swing, hip_w, leg_w, leg_len, idle_bonus):
    """Draw legs with all style variations"""
    leg_style = limbs.get("leg_style", "default")
    foot_style = limbs.get("foot_style", "default")
    
    leg_specific = idle_bonus.get('leg_specific', 0)
    
    for side, hx, kx, ax, fx in [
        (-1, cx - int(26 * hip_w), cx - int(30 * leg_w) + leg_swing * 0.3,
         cx - int(22 * leg_w) + leg_swing * 0.55, cx - int(14 * leg_w) + leg_swing),
        (1, cx + int(26 * hip_w), cx + int(30 * leg_w) - leg_swing * 0.3,
         cx + int(22 * leg_w) - leg_swing * 0.55, cx + int(14 * leg_w) - leg_swing)
    ]:
        # Apply leg specific animation
        kx += leg_specific * side
        ax += leg_specific * side * 0.5
        
        if leg_style == "animal":
            knee_y = hip_y - int(25 * leg_len)
            draw.line([hx, hip_y, kx, knee_y], fill=body_outline_color, width=int(18 * leg_w))
            draw.line([hx, hip_y, kx, knee_y], fill=body_color, width=int(12 * leg_w))
            draw.line([kx, knee_y, ax, ground_y - 70], fill=body_outline_color, width=int(14 * leg_w))
            draw.line([kx, knee_y, ax, ground_y - 70], fill=body_color, width=int(9 * leg_w))
        elif leg_style == "robot":
            mid_y = hip_y - int(40 * leg_len)
            draw.line([hx, hip_y, kx, mid_y], fill=(150, 150, 160, 255), width=int(14 * leg_w))
            draw.ellipse([kx-6, mid_y-6, kx+6, mid_y+6], fill=(200, 200, 210, 255))
            draw.line([kx, mid_y, ax, ground_y - 70], fill=(150, 150, 160, 255), width=int(12 * leg_w))
            draw.ellipse([ax-5, ground_y-75, ax+5, ground_y-65], fill=(200, 200, 210, 255))
        elif leg_style == "thick":
            draw.line([hx, hip_y, kx, hip_y - 45], fill=body_outline_color, width=int(24 * leg_w))
            draw.line([hx, hip_y, kx, hip_y - 45], fill=body_color, width=int(18 * leg_w))
            draw.line([kx, hip_y - 40, ax, ground_y - 70], fill=body_outline_color, width=int(20 * leg_w))
            draw.line([kx, hip_y - 40, ax, ground_y - 70], fill=body_color, width=int(14 * leg_w))
        elif leg_style == "thin":
            draw.line([hx, hip_y, kx, hip_y - 45], fill=body_outline_color, width=int(10 * leg_w))
            draw.line([hx, hip_y, kx, hip_y - 45], fill=body_color, width=int(6 * leg_w))
            draw.line([kx, hip_y - 40, ax, ground_y - 70], fill=body_outline_color, width=int(8 * leg_w))
            draw.line([kx, hip_y - 40, ax, ground_y - 70], fill=body_color, width=int(5 * leg_w))
        elif leg_style == "spring":
            for i in range(4):
                sy = hip_y - 10 - i * 12
                draw.ellipse([hx-8, sy-4, hx+8, sy+4], fill=body_color, outline=body_outline_color)
            draw.line([hx, hip_y - 50, ax, ground_y - 70], fill=body_color, width=int(10 * leg_w))
        elif leg_style == "pillar":
            draw.rectangle([hx-12, hip_y, hx+12, ground_y-70], fill=body_color, outline=body_outline_color, width=2)
        elif leg_style == "peg":
            draw.line([hx, hip_y, ax, ground_y-70], fill=body_outline_color, width=int(16 * leg_w))
            draw.line([hx, hip_y, ax, ground_y-70], fill=body_color, width=int(8 * leg_w))
        elif leg_style == "digitigrade":
            knee_y = hip_y - int(30 * leg_len)
            ankle_y = knee_y - int(15 * leg_len)
            draw.line([hx, hip_y, kx, knee_y], fill=body_outline_color, width=int(16 * leg_w))
            draw.line([hx, hip_y, kx, knee_y], fill=body_color, width=int(11 * leg_w))
            draw.line([kx, knee_y, ax, ankle_y], fill=body_outline_color, width=int(12 * leg_w))
            draw.line([kx, knee_y, ax, ankle_y], fill=body_color, width=int(8 * leg_w))
            draw.line([ax, ankle_y, fx, ground_y-70], fill=body_outline_color, width=int(8 * leg_w))
            draw.line([ax, ankle_y, fx, ground_y-70], fill=body_color, width=int(5 * leg_w))
        elif leg_style == "tentacle_legs":
            for i in range(4):
                seg_y = hip_y - i * 12
                seg_x = hx + math.sin(renderer.dance_timer * 0.3 + i + side) * 5
                draw.ellipse([seg_x-6, seg_y-4, seg_x+6, seg_y+4], fill=body_color, outline=body_outline_color)
            draw.line([hx, hip_y - 48, ax, ground_y - 70], fill=body_color, width=int(6 * leg_w))
        else:
            draw.line([hx, hip_y, kx, hip_y - 45], fill=body_outline_color, width=int(18 * leg_w))
            draw.line([hx, hip_y, kx, hip_y - 45], fill=body_color, width=int(12 * leg_w))
            draw.line([kx, hip_y - 40, ax, ground_y - 70], fill=body_outline_color, width=int(14 * leg_w))
            draw.line([kx, hip_y - 40, ax, ground_y - 70], fill=body_color, width=int(9 * leg_w))
        
        # Draw foot
        draw_foot(draw, c, limbs, body_color, body_outline_color, fx, ground_y, leg_w)


def draw_foot(draw, c, limbs, body_color, body_outline_color, fx, ground_y, leg_w):
    """Draw foot with style"""
    foot_style = limbs.get("foot_style", "default")
    
    if foot_style == "boot":
        draw.rectangle([fx-18, ground_y-85, fx+20, ground_y-50], fill=(80, 50, 30, 255), outline=(50, 30, 15, 255), width=2)
    elif foot_style == "bare":
        draw.ellipse([fx-16, ground_y-75, fx+18, ground_y-50], fill=c["skin"], outline=c["skin_outline"], width=2)
    elif foot_style == "hoof":
        draw.rectangle([fx-14, ground_y-78, fx+16, ground_y-52], fill=(60, 60, 60, 255), outline=(30, 30, 30, 255), width=2)
    elif foot_style == "sneaker":
        draw.ellipse([fx-20, ground_y-78, fx+22, ground_y-48], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)
    elif foot_style == "sandals":
        draw.ellipse([fx-15, ground_y-72, fx+17, ground_y-48], fill=c["skin"], outline=c["skin_outline"], width=2)
        draw.arc([fx-12, ground_y-58, fx+12, ground_y-48], 180, 0, fill=(150, 100, 50, 255), width=3)
    elif foot_style == "heels":
        draw.ellipse([fx-12, ground_y-85, fx+14, ground_y-65], fill=(255, 100, 150, 255), outline=(200, 70, 100, 255), width=2)
        draw.rectangle([fx-3, ground_y-70, fx+3, ground_y-55], fill=(255, 100, 150, 255), outline=(200, 70, 100, 255))
    elif foot_style == "rollerskates":
        draw.rectangle([fx-18, ground_y-80, fx+20, ground_y-55], fill=(255, 50, 150, 255), outline=(200, 30, 100, 255), width=2)
        for wx in [fx-12, fx-4, fx+4, fx+12]:
            draw.ellipse([wx-4, ground_y-55, wx+4, ground_y-47], fill=(200, 200, 200, 255), outline=(150, 150, 150, 255))
    elif foot_style == "flippers":
        draw.ellipse([fx-25, ground_y-70, fx+27, ground_y-48], fill=(50, 200, 150, 255), outline=(30, 150, 100, 255), width=2)
    elif foot_style == "clown_shoes":
        draw.ellipse([fx-28, ground_y-75, fx+30, ground_y-48], fill=(255, 100, 50, 255), outline=(200, 70, 30, 255), width=2)
        draw.ellipse([fx-15, ground_y-70, fx+17, ground_y-50], fill=(255, 200, 50, 255))
    elif foot_style == "ice_skates":
        draw.rectangle([fx-16, ground_y-75, fx+18, ground_y-48], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)
        draw.line([fx-8, ground_y-48, fx+8, ground_y-48], fill=(180, 180, 190, 255), width=3)
    else:
        draw.ellipse([fx-20, ground_y-78, fx+22, ground_y-48], fill=c["feet"], outline=body_outline_color)


def draw_torso(draw, shape, body_color, body_outline_color, cx, hip_y, chest_y, shoulder_y, 
               shoulder_w, hip_w, width_mult, body_radius, idle_bonus):
    """Draw torso with shape customization"""
    torso_type = shape.get("type", "default")
    
    # Apply idle twist
    twist = idle_bonus.get('extra_twist', 0) * 0.5
    
    if torso_type == "custom" and shape.get("custom_points"):
        pts = [(cx + p[0], hip_y + p[1]) for p in shape["custom_points"]]
        draw.polygon(pts, fill=body_color, outline=body_outline_color)
    elif torso_type == "round":
        torso_r = int(body_radius * 1.5 * width_mult)
        draw.ellipse([cx - torso_r + twist, shoulder_y - 10, cx + torso_r - twist, hip_y + 10], 
                    fill=body_color, outline=body_outline_color, width=3)
    elif torso_type == "square":
        draw.rectangle([cx - int(40 * shoulder_w), shoulder_y, cx + int(40 * shoulder_w), hip_y], 
                      fill=body_color, outline=body_outline_color, width=2)
    elif torso_type == "triangle":
        draw.polygon([(cx, shoulder_y - 20), (cx - int(45 * hip_w), hip_y), (cx + int(45 * hip_w), hip_y)], 
                    fill=body_color, outline=body_outline_color, width=2)
    elif torso_type == "pear":
        draw.polygon([(cx - int(25 * shoulder_w), shoulder_y), (cx + int(25 * shoulder_w), shoulder_y),
                     (cx + int(45 * hip_w), hip_y), (cx - int(45 * hip_w), hip_y)], 
                    fill=body_color, outline=body_outline_color, width=2)
    elif torso_type == "athletic":
        draw.polygon([(cx - int(38 * shoulder_w), shoulder_y), (cx + int(38 * shoulder_w), shoulder_y),
                     (cx + int(30 * hip_w), hip_y), (cx - int(30 * hip_w), hip_y)], 
                    fill=body_color, outline=body_outline_color, width=2)
    elif torso_type == "slime":
        draw.ellipse([cx - int(35 * width_mult), shoulder_y - 10, cx + int(35 * width_mult), hip_y + 20], 
                    fill=body_color, outline=body_outline_color, width=2)
    elif torso_type == "barrel":
        draw.ellipse([cx - int(42 * width_mult), shoulder_y - 5, cx + int(42 * width_mult), hip_y + 5], 
                    fill=body_color, outline=body_outline_color, width=2)
    elif torso_type == "wasp":
        mid_y = (shoulder_y + hip_y) // 2
        draw.polygon([(cx - int(35 * shoulder_w), shoulder_y), (cx + int(35 * shoulder_w), shoulder_y),
                     (cx + int(18 * width_mult), mid_y), (cx - int(18 * width_mult), mid_y),
                     (cx + int(32 * hip_w), hip_y), (cx - int(32 * hip_w), hip_y)],
                    fill=body_color, outline=body_outline_color, width=2)
    elif torso_type == "ghost":
        draw.ellipse([cx - int(32 * width_mult), shoulder_y - 20, cx + int(32 * width_mult), hip_y + 30], 
                    fill=body_color, outline=body_outline_color, width=2)
        for i in range(4):
            wave_x = cx - 25 + i * 16
            draw.arc([wave_x, hip_y + 15, wave_x + 20, hip_y + 45], 180, 0, fill=body_color, width=2)
    else:
        torso = [(cx - int(30 * hip_w), hip_y), (cx + int(30 * hip_w), hip_y),
                 (cx + int(36 * shoulder_w), shoulder_y), (cx - int(36 * shoulder_w), shoulder_y)]
        draw.polygon(torso, fill=body_color, outline=body_outline_color)


def draw_arms(renderer, draw, c, limbs, body_color, body_outline_color, 
              cx, shoulder_y, chest_y, hip_y, shoulder_w, arm_w, arm_len, 
              arm_swing, arm_raise, idle_bonus):
    """Draw arms with all style variations"""
    arm_style = limbs.get("arm_style", "default")
    hand_style = limbs.get("hand_style", "default")
    
    arm_specific = idle_bonus.get('arm_specific', 0)
    extra_flail = idle_bonus.get('extra_flail', 0)
    
    for side in [-1, 1]:
        shx = cx - int(36 * shoulder_w) * side
        elx = cx - int(50 * arm_len) * side + arm_swing * 0.3 * side
        wrx = cx - int(38 * arm_len) * side + arm_swing * side
        elx += arm_raise * side * 0.5
        wrx += arm_raise * side
        
        # Apply idle bonuses
        elx += arm_specific * side * 0.3
        wrx += arm_specific * side * 0.5
        wrx += extra_flail * side
        
        el_y = chest_y + 8 - arm_raise * 0.6
        wr_y = hip_y - 25 - arm_raise * 0.8
        el_y -= arm_specific * 0.2
        
        if arm_style == "muscular":
            draw.line([shx, shoulder_y, elx, el_y], fill=body_outline_color, width=int(18 * arm_w))
            draw.line([shx, shoulder_y, elx, el_y], fill=body_color, width=int(12 * arm_w))
            draw.ellipse([elx-8, el_y-8, elx+8, el_y+8], fill=body_color, outline=body_outline_color)
            draw.line([elx, el_y, wrx, wr_y], fill=body_outline_color, width=int(14 * arm_w))
            draw.line([elx, el_y, wrx, wr_y], fill=body_color, width=int(9 * arm_w))
        elif arm_style == "robot":
            draw.line([shx, shoulder_y, elx, el_y], fill=(150, 150, 160, 255), width=int(12 * arm_w))
            draw.ellipse([elx-5, el_y-5, elx+5, el_y+5], fill=(200, 200, 210, 255))
            draw.line([elx, el_y, wrx, wr_y], fill=(150, 150, 160, 255), width=int(10 * arm_w))
        elif arm_style == "tentacle":
            for i in range(3):
                seg_y = el_y + i * 10
                draw.ellipse([elx-6, seg_y-4, elx+6, seg_y+4], fill=body_color, outline=body_outline_color)
            draw.line([elx, el_y, wrx, wr_y], fill=body_color, width=int(8 * arm_w))
        elif arm_style == "thin":
            draw.line([shx, shoulder_y, elx, el_y], fill=body_outline_color, width=int(8 * arm_w))
            draw.line([shx, shoulder_y, elx, el_y], fill=body_color, width=int(5 * arm_w))
            draw.line([elx, el_y, wrx, wr_y], fill=body_outline_color, width=int(6 * arm_w))
            draw.line([elx, el_y, wrx, wr_y], fill=body_color, width=int(4 * arm_w))
        elif arm_style == "wing_arms":
            draw.arc([shx-20, shoulder_y-40, shx+50, shoulder_y+30], 200, 340, fill=body_color, width=int(8 * arm_w))
        elif arm_style == "stretchy":
            for i in range(5):
                seg_x = shx + (elx - shx) * (i/4) + math.sin(renderer.dance_timer * 0.2 + i + side) * 4
                seg_y = shoulder_y + (el_y - shoulder_y) * (i/4)
                draw.ellipse([seg_x-5, seg_y-3, seg_x+5, seg_y+3], fill=body_color, outline=body_outline_color)
            draw.line([elx, el_y, wrx, wr_y], fill=body_color, width=int(7 * arm_w))
        elif arm_style == "blade":
            draw.line([shx, shoulder_y, wrx, wr_y], fill=body_outline_color, width=int(14 * arm_w))
            draw.line([shx, shoulder_y, wrx, wr_y], fill=body_color, width=int(8 * arm_w))
            draw.polygon([(wrx-10, wr_y-15), (wrx, wr_y-5), (wrx+10, wr_y-15)], fill=(200, 200, 220, 255), outline=(150, 150, 170, 255))
        elif arm_style == "crystal":
            for i in range(3):
                seg_y = shoulder_y + (el_y - shoulder_y) * ((i+1)/3)
                seg_x = shx + (elx - shx) * ((i+1)/3)
                crystal_size = 6 - i
                draw.polygon([(seg_x, seg_y-crystal_size*2), (seg_x+crystal_size, seg_y), 
                             (seg_x, seg_y+crystal_size*2), (seg_x-crystal_size, seg_y)],
                            fill=(200, 100, 255, 200 - i*40), outline=(150, 50, 200, 255))
        elif arm_style == "gooey":
            for i in range(4):
                seg_y = shoulder_y + (wr_y - shoulder_y) * ((i+1)/4)
                seg_x = shx + (wrx - shx) * ((i+1)/4) + math.sin(renderer.dance_timer * 0.25 + i + side) * 5
                draw.ellipse([seg_x-7, seg_y-5, seg_x+7, seg_y+5], fill=body_color, outline=body_outline_color)
        else:
            draw.line([shx, shoulder_y, elx, el_y], fill=body_outline_color, width=int(14 * arm_w))
            draw.line([shx, shoulder_y, elx, el_y], fill=body_color, width=int(9 * arm_w))
            draw.line([elx, el_y, wrx, wr_y], fill=body_outline_color, width=int(11 * arm_w))
            draw.line([elx, el_y, wrx, wr_y], fill=body_color, width=int(7 * arm_w))
        
        # Draw hand
        draw_hand(draw, c, hand_style, wrx, wr_y, renderer)


def draw_hand(draw, c, hand_style, wrx, wr_y, renderer):
    """Draw hand with style"""
    if hand_style == "mitten":
        draw.ellipse([wrx-15, wr_y-12, wrx+15, wr_y+8], fill=c["hands"], outline=c["skin_outline"], width=2)
    elif hand_style == "claw":
        for fi in range(3):
            fx2 = wrx - 8 + fi * 8
            draw.line([fx2, wr_y-5, fx2-3, wr_y-18], fill=c["skin_outline"], width=3)
        draw.ellipse([wrx-12, wr_y-8, wrx+12, wr_y+6], fill=c["hands"], outline=c["skin_outline"])
    elif hand_style == "hook":
        draw.arc([wrx-10, wr_y-20, wrx+10, wr_y+5], 0, 270, fill=(100, 100, 110, 255), width=6)
    elif hand_style == "paws":
        draw.ellipse([wrx-14, wr_y-10, wrx+14, wr_y+10], fill=c["hands"], outline=c["skin_outline"], width=2)
        for pi in range(3):
            px = wrx - 6 + pi * 6
            draw.ellipse([px-3, wr_y-5, px+3, wr_y+2], fill=c["skin_outline"])
    elif hand_style == "tentacle_hands":
        for i in range(5):
            fx2 = wrx - 12 + i * 6
            fy = wr_y - 8 + math.sin(i + renderer.dance_timer * 0.3) * 5
            draw.line([wrx, wr_y+2, fx2, fy], fill=c["hands"], width=3)
    elif hand_style == "robot_hands":
        draw.rectangle([wrx-14, wr_y-12, wrx+14, wr_y+8], fill=(180, 180, 190, 255), outline=(140, 140, 150, 255), width=2)
        for fi in range(3):
            fx2 = wrx - 8 + fi * 8
            draw.rectangle([fx2-2, wr_y-10, fx2+2, wr_y-5], fill=(200, 200, 210, 255))
    elif hand_style == "gloves":
        draw.ellipse([wrx-15, wr_y-12, wrx+15, wr_y+8], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)
        draw.arc([wrx-8, wr_y-8, wrx+8, wr_y-2], 180, 0, fill=(200, 200, 200, 255), width=1)
    elif hand_style == "spikes":
        for fi in range(4):
            spike_angle = fi * (math.pi/3) - math.pi/2
            sx = wrx + math.cos(spike_angle) * 10
            sy = wr_y + math.sin(spike_angle) * 10
            draw.line([wrx, wr_y, sx, sy], fill=c["skin_outline"], width=3)
        draw.ellipse([wrx-10, wr_y-8, wrx+10, wr_y+6], fill=c["hands"], outline=c["skin_outline"])
    elif hand_style == "suction_cups":
        draw.ellipse([wrx-14, wr_y-10, wrx+14, wr_y+10], fill=c["hands"], outline=c["skin_outline"], width=2)
        for ci in range(3):
            cx_cup = wrx - 6 + ci * 6
            draw.ellipse([cx_cup-3, wr_y-3, cx_cup+3, wr_y+3], fill=c["skin_outline"], outline=c["skin"])
    elif hand_style == "energy":
        for i in range(3):
            er = 10 - i * 3
            draw.ellipse([wrx-er, wr_y-er, wrx+er, wr_y+er], 
                        fill=(100, 200, 255, 80 - i*20), outline=(100, 200, 255, 150 - i*30), width=1)
    else:
        draw.ellipse([wrx-13, wr_y-10, wrx+13, wr_y+10], fill=c["hands"], outline=c["skin_outline"])


def draw_head(renderer, draw, c, head_cfg, hair_cfg, clothing, 
              cx, head_y, head_size_mult, width_mult, height_mult, extra_spin, idle_bonus):
    """Draw head with shape and hair customization"""
    head_shift = extra_spin
    head_size = head_cfg.get("size", 1.0) * head_size_mult
    head_shape = head_cfg.get("shape", "round")
    head_w = int(42 * head_size * width_mult)
    head_h = int(38 * head_size * height_mult)
    face_pos = head_cfg.get("face_position", 0.0)
    adj_head_y = head_y + int(face_pos * 15 * height_mult)
    
    # Apply head animation
    adj_head_y += idle_bonus.get('head_specific', 0)
    
    if head_shape == "oval":
        draw.ellipse([cx - head_w + head_shift, adj_head_y - head_h - 10, cx + head_w + head_shift, adj_head_y + head_h + 30], 
                    fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "square":
        draw.rectangle([cx - head_w + head_shift, adj_head_y - 8, cx + head_w + head_shift, adj_head_y + int(68 * head_size)], 
                      fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "triangle":
        draw.polygon([(cx + head_shift, adj_head_y - 30), (cx - head_w + head_shift, adj_head_y + 60), (cx + head_w + head_shift, adj_head_y + 60)], 
                    fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "heart":
        draw.ellipse([cx - head_w//2 + head_shift - 10, adj_head_y - 20, cx + head_shift + 10, adj_head_y + 10], fill=c["skin"], outline=c["skin_outline"], width=2)
        draw.ellipse([cx - head_w//2 + head_shift + 10, adj_head_y - 20, cx + head_shift + 30, adj_head_y + 10], fill=c["skin"], outline=c["skin_outline"], width=2)
        draw.polygon([(cx - head_w//2 + head_shift, adj_head_y), (cx + head_w//2 + head_shift, adj_head_y), (cx + head_shift, adj_head_y + 60)], 
                    fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "hexagon":
        points = []
        for i in range(6):
            angle = i * (math.pi / 3) - math.pi / 2
            px = cx + head_shift + int(head_w * math.cos(angle))
            py = adj_head_y + 30 + int(head_h * math.sin(angle))
            points.append((px, py))
        draw.polygon(points, fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "diamond":
        draw.polygon([(cx + head_shift, adj_head_y - 30), (cx - head_w + head_shift, adj_head_y + 30),
                     (cx + head_shift, adj_head_y + 70), (cx + head_w + head_shift, adj_head_y + 30)],
                    fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "star":
        points = []
        for i in range(10):
            angle = i * (math.pi / 5) - math.pi / 2
            r = head_w if i % 2 == 0 else head_w * 0.5
            px = cx + head_shift + int(r * math.cos(angle))
            py = adj_head_y + 30 + int(r * math.sin(angle))
            points.append((px, py))
        draw.polygon(points, fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "moon":
        draw.ellipse([cx - head_w + head_shift, adj_head_y - 8, cx + head_w + head_shift, adj_head_y + int(68 * head_size)], 
                    fill=c["skin"], outline=c["skin_outline"], width=2)
        draw.ellipse([cx - int(head_w * 0.7) + head_shift, adj_head_y - 5, cx + int(head_w * 0.7) + head_shift, adj_head_y + int(62 * head_size)], 
                    fill=(0, 0, 0, 200), outline=c["skin_outline"], width=2)
    elif head_shape == "alien":
        draw.ellipse([cx - int(head_w * 0.7) + head_shift, adj_head_y - 10, cx + int(head_w * 0.7) + head_shift, adj_head_y + int(50 * head_size)], 
                    fill=c["skin"], outline=c["skin_outline"], width=2)
        draw.ellipse([cx - int(head_w * 1.1) + head_shift, adj_head_y + int(20 * head_size), cx + int(head_w * 1.1) + head_shift, adj_head_y + int(75 * head_size)], 
                    fill=c["skin"], outline=c["skin_outline"], width=2)
    elif head_shape == "robot_head":
        draw.rectangle([cx - head_w + head_shift, adj_head_y - 10, cx + head_w + head_shift, adj_head_y + int(60 * head_size)], 
                      fill=c["skin"], outline=c["skin_outline"], width=2)
        for i in range(3):
            line_y = adj_head_y + int(15 * head_size) + i * int(15 * head_size)
            draw.line([cx - head_w + head_shift + 5, line_y, cx + head_w + head_shift - 5, line_y], fill=c["skin_outline"], width=1)
    else:
        draw.ellipse([cx - head_w + head_shift, adj_head_y - 8, cx + head_w + head_shift, adj_head_y + int(68 * head_size)], 
                    fill=c["skin"], outline=c["skin_outline"], width=2)
    
    # Draw hair
    draw_hair(renderer, draw, c, hair_cfg, cx, adj_head_y, head_shift, head_size_mult, width_mult)
    
    # Draw hat
    hat = clothing.get("hats", "None")
    if hat and hat != "None":
        from character_accessories import draw_hat
        draw_hat(draw, c, cx, adj_head_y, head_shift, hat)
    
    # Draw mask
    mask = clothing.get("masks", "None")
    if mask and mask != "None":
        from character_accessories import draw_mask
        draw_mask(draw, c, cx, adj_head_y, head_shift, mask)
    
    # Draw glasses
    glasses = clothing.get("glasses", "None")
    if glasses and glasses != "None":
        from character_accessories import draw_glasses
        draw_glasses(draw, c, cx, adj_head_y, head_shift, glasses)


def draw_hair(renderer, draw, c, hair_cfg, cx, adj_head_y, head_shift, head_size_mult, width_mult):
    """Draw hair with style"""
    from character_accessories import draw_hair_style
    draw_hair_style(renderer, draw, c, hair_cfg, cx, adj_head_y, head_shift, head_size_mult, width_mult)


def draw_eyes(renderer, draw, c, head_cfg, cx, head_y, head_size_mult, width_mult, extra_spin):
    """Draw eyes"""
    head_shift = extra_spin
    face_pos = head_cfg.get("face_position", 0.0)
    adj_head_y = head_y + int(face_pos * 15)
    eye_y = adj_head_y + int(22 * head_size_mult)
    
    for es in [-1, 1]:
        ex = cx - int(20 * width_mult) * es + head_shift
        
        if renderer.is_dead:
            # Cross eyes for death
            draw.line([ex - 8, eye_y, ex + 8, eye_y + 8], fill=(255, 0, 0, 255), width=3)
            draw.line([ex + 8, eye_y, ex - 8, eye_y + 8], fill=(255, 0, 0, 255), width=3)
        elif renderer.emotion == "happy":
            draw.arc([ex - 16, eye_y - 4, ex + 16, eye_y + 18], 0, 180, fill=c["skin_outline"], width=3)
        elif renderer.is_blinking:
            draw.ellipse([ex - 16, eye_y + 6, ex + 16, eye_y + 12], fill=c["skin_outline"])
        else:
            draw.ellipse([ex - 16, eye_y, ex + 16, eye_y + 18], fill=(255, 255, 255, 255), outline=c["skin_outline"], width=2)
            draw.ellipse([ex - 10, eye_y + 4, ex + 10, eye_y + 14], fill=c["eyes"])
            draw.ellipse([ex - 6, eye_y + 6, ex + 6, eye_y + 10], fill=c["pupils"])


def draw_nose(renderer, draw, c, head_cfg, cx, head_y, head_size_mult, width_mult):
    """Draw nose"""
    head_shift = 0
    face_pos = head_cfg.get("face_position", 0.0)
    adj_head_y = head_y + int(face_pos * 15)
    nose_y = adj_head_y + int(40 * head_size_mult)
    ns = int((5 + math.sin(renderer.nose_twitch) * 2) * width_mult)
    draw.ellipse([cx - ns + head_shift, nose_y - 3, cx + ns + head_shift, nose_y + 4], fill=c["mouth"], outline=c["skin_outline"])


def draw_mouth(renderer, draw, c, head_cfg, cx, head_y, head_size_mult, extra_spin):
    """Draw mouth"""
    head_shift = extra_spin
    face_pos = head_cfg.get("face_position", 0.0)
    adj_head_y = head_y + int(face_pos * 15)
    nose_y = adj_head_y + int(40 * head_size_mult)
    mouth_y = nose_y + 10
    
    if renderer.is_dead:
        draw.line([cx - 10 + head_shift, mouth_y + 5, cx + 10 + head_shift, mouth_y + 5], fill=(0, 0, 0, 255), width=2)
    elif renderer.is_talking:
        mf = (renderer.frame // 2) % 4
        if mf == 0:
            draw.ellipse([cx - 10 + head_shift, mouth_y, cx + 10 + head_shift, mouth_y + 16], fill=c["mouth"], outline=c["skin_outline"])
        else:
            draw.arc([cx - 8 + head_shift, mouth_y + 4, cx + 8 + head_shift, mouth_y + 12], 0, 180, fill=c["mouth"], width=2)
    else:
        draw.arc([cx - 8 + head_shift, mouth_y + 2, cx + 8 + head_shift, mouth_y + 12], 0, 180, fill=c["mouth"], width=2)


def draw_ears(renderer, draw, c, body_color, body_outline_color, head_cfg, cx, head_y, head_size_mult, extra_spin):
    """Draw ears with style"""
    head_shift = extra_spin
    ear_style = head_cfg.get("ear_style", "default")
    ear_size = head_cfg.get("ear_size", 1.0)
    face_pos = head_cfg.get("face_position", 0.0)
    adj_head_y = head_y + int(face_pos * 15)
    ear_y = adj_head_y - 5
    
    if ear_style == "none":
        return
    
    from character_accessories import draw_ear_style
    draw_ear_style(renderer, draw, c, body_color, body_outline_color, ear_style, ear_size, cx, ear_y, head_shift)