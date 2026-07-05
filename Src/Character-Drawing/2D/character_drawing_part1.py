"""
MEMEBOT 2D Character Renderer - Drawing Module Part 1
Torso, Legs, Feet drawing with all style variations
Part 1 of 2
"""

import math


def draw_torso(draw, shape, body_color, body_outline_color, cx, hip_y, chest_y, shoulder_y, 
               shoulder_w, hip_w, width_mult, body_radius, idle_bonus):
    """Draw torso with shape customization"""
    torso_type = shape.get("type", "default")
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


def draw_legs(renderer, draw, c, limbs, body_color, body_outline_color, 
              cx, hip_y, ground_y, leg_swing, arm_swing, hip_w, leg_w, leg_len, idle_bonus):
    """Draw legs with all style variations"""
    leg_style = limbs.get("leg_style", "default")
    leg_specific = idle_bonus.get('leg_specific', 0)
    
    for side, hx, kx, ax, fx in [
        (-1, cx - int(26 * hip_w), cx - int(30 * leg_w) + leg_swing * 0.3,
         cx - int(22 * leg_w) + leg_swing * 0.55, cx - int(14 * leg_w) + leg_swing),
        (1, cx + int(26 * hip_w), cx + int(30 * leg_w) - leg_swing * 0.3,
         cx + int(22 * leg_w) - leg_swing * 0.55, cx + int(14 * leg_w) - leg_swing)
    ]:
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