"""
MEMEBOT 2D Character Renderer - Accessories Module
Handles all accessories, clothing items, hats, glasses, masks, etc.
Part 3 of 3 - Accessories & Clothing
"""

import math
from PIL import ImageFont


def draw_speech_bubble(renderer, draw, cx, y):
    """Draw speech bubble with shadow and gradient"""
    bubble_x = cx + 30
    text_w = len(renderer.speech_text) * 8 + 20
    bubble_w = max(60, min(text_w, 200))
    bubble_h = 30
    
    # Shadow
    draw.ellipse([bubble_x - bubble_w//2 + 3, y - bubble_h//2 + 3, 
                  bubble_x + bubble_w//2 + 3, y + bubble_h//2 + 3],
                fill=(0, 0, 0, 60))
    
    # Main bubble with subtle gradient
    for i in range(3):
        offset = i * 2
        alpha = 230 - i * 15
        draw.ellipse([bubble_x - bubble_w//2 + offset, y - bubble_h//2 + offset, 
                     bubble_x + bubble_w//2 - offset, y + bubble_h//2 - offset],
                    fill=(255, 255, 255, alpha), outline=(180, 180, 190, 255), width=1)
    
    # Shine highlight
    draw.ellipse([bubble_x - bubble_w//2 + 8, y - bubble_h//2 + 4, 
                  bubble_x - bubble_w//2 + 20, y - bubble_h//2 + 12],
                fill=(255, 255, 255, 100))
    
    # Tail shadow
    draw.polygon([(bubble_x - 13, y + bubble_h//2 + 3), (bubble_x - 23, y + bubble_h//2 + 18), 
                  (bubble_x - 3, y + bubble_h//2 + 3)],
                fill=(0, 0, 0, 40))
    
    # Tail
    draw.polygon([(bubble_x - 15, y + bubble_h//2), (bubble_x - 25, y + bubble_h//2 + 15), 
                  (bubble_x - 5, y + bubble_h//2)],
                fill=(255, 255, 255, 230), outline=(180, 180, 190, 255), width=1)
    
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    # Text shadow
    draw.text((bubble_x - bubble_w//2 + 6, y - 7), renderer.speech_text[:30], fill=(0, 0, 0, 80), font=font)
    # Text
    draw.text((bubble_x - bubble_w//2 + 5, y - 8), renderer.speech_text[:30], fill=(20, 20, 30, 255), font=font)


# ============================================
# TAIL DRAWING
# ============================================

def draw_tail(renderer, draw, c, cx, hip_y, ground_y, tail_type):
    """Draw tail accessory with fur texture and shading"""
    colors = {
        "cat": (200, 150, 100, 255),
        "dog": (180, 140, 100, 255),
        "demon": (180, 30, 30, 255),
        "dragon": (30, 120, 30, 255),
        "fox": (255, 150, 50, 255),
        "rabbit": (255, 255, 255, 255),
        "mouse": (200, 180, 180, 255),
        "lizard": (50, 180, 50, 255),
        "devil": (200, 20, 20, 255),
        "robot": (150, 150, 160, 255),
    }
    color = colors.get(tail_type, (200, 150, 100, 255))
    dark_color = tuple(max(0, c - 40) for c in color[:3]) + (color[3],)
    light_color = tuple(min(255, c + 30) for c in color[:3]) + (color[3],)
    
    if tail_type == "cat":
        tail_sway = math.sin(renderer.dance_timer * 0.2) * 15
        # Main tail with outline
        for i in range(3):
            offset = i * 1.5
            draw.line([cx, hip_y, cx + 30 + tail_sway + offset, hip_y - 20], fill=dark_color, width=8 - i)
        draw.line([cx, hip_y, cx + 30 + tail_sway, hip_y - 20], fill=color, width=6)
        draw.line([cx + 30 + tail_sway, hip_y - 20, cx + 50 + tail_sway, hip_y - 40], fill=color, width=4)
        draw.line([cx + 50 + tail_sway, hip_y - 40, cx + 55 + tail_sway, hip_y - 55], fill=light_color, width=2)
        # Tail tip highlight
        draw.ellipse([cx + 53 + tail_sway, hip_y - 58, cx + 57 + tail_sway, hip_y - 52], fill=(255, 255, 255, 100))
    elif tail_type == "dog":
        tail_wag = math.sin(renderer.dance_timer * 0.4) * 20
        # Shadow
        draw.line([cx + 2, hip_y + 1, cx + 27 + tail_wag, hip_y - 29], fill=(0, 0, 0, 40), width=9)
        draw.line([cx, hip_y, cx + 25 + tail_wag, hip_y - 30], fill=color, width=7)
        # Highlight
        draw.line([cx + 25 + tail_wag, hip_y - 30, cx + 28 + tail_wag, hip_y - 33], fill=light_color, width=3)
    elif tail_type == "demon":
        tail_sway = math.sin(renderer.dance_timer * 0.25) * 10
        for i in range(4):
            tx = cx + i * 12 + tail_sway * (i * 0.3)
            ty = hip_y - i * 10
            # Spike shadow
            draw.polygon([(tx-5, ty-3), (tx+1, ty+7), (tx+5, ty-3)], fill=(0, 0, 0, 60))
            # Spike
            draw.polygon([(tx-4, ty-4), (tx, ty+6), (tx+4, ty-4)], fill=color, outline=(120, 15, 15, 255))
            # Spike highlight
            draw.polygon([(tx-2, ty-2), (tx, ty+3), (tx+2, ty-2)], fill=(255, 80, 80, 100))
        draw.line([cx + 48 + tail_sway * 1.2, hip_y - 40, cx + 55 + tail_sway * 1.3, hip_y - 55], fill=color, width=2)
        # Arrow tip
        draw.polygon([(cx + 52 + tail_sway, hip_y - 58), (cx + 55 + tail_sway, hip_y - 62), 
                      (cx + 58 + tail_sway, hip_y - 58)], fill=(200, 20, 20, 255), outline=(150, 10, 10, 255))
    elif tail_type == "fox":
        tail_sway = math.sin(renderer.dance_timer * 0.2) * 12
        # Bushy tail base
        draw.line([cx, hip_y, cx + 35 + tail_sway, hip_y - 30], fill=color, width=10)
        # White tip
        draw.ellipse([cx + 25 + tail_sway, hip_y - 45, cx + 55 + tail_sway, hip_y - 15], fill=(255, 255, 255, 220))
        # Fluffy texture lines
        for i in range(5):
            fx = cx + 10 + i * 6 + tail_sway * (i * 0.2)
            fy = hip_y - 8 - i * 6
            draw.arc([fx-4, fy-2, fx+4, fy+2], 0, 180, fill=light_color, width=1)
    elif tail_type == "rabbit":
        # Fluffy ball shadow
        draw.ellipse([cx + 12, hip_y - 8, cx + 27, hip_y + 7], fill=(0, 0, 0, 30))
        draw.ellipse([cx + 10, hip_y - 10, cx + 25, hip_y + 5], fill=color, outline=(200, 200, 200, 255), width=1)
        # Fluff detail
        for i in range(4):
            fx = cx + 13 + i * 3
            fy = hip_y - 5 + math.sin(i) * 3
            draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=(255, 255, 255, 150))
    elif tail_type == "devil":
        tail_sway = math.sin(renderer.dance_timer * 0.3) * 10
        # Shadow
        draw.line([cx + 1, hip_y + 1, cx + 41 + tail_sway, hip_y - 34], fill=(0, 0, 0, 50), width=7)
        draw.line([cx, hip_y, cx + 40 + tail_sway, hip_y - 35], fill=color, width=5)
        # Forked tip
        draw.polygon([(cx + 40 + tail_sway, hip_y - 35), (cx + 28 + tail_sway, hip_y - 52), 
                     (cx + 36 + tail_sway, hip_y - 48)], fill=(200, 20, 20, 255), outline=(150, 10, 10, 255))
        draw.polygon([(cx + 40 + tail_sway, hip_y - 35), (cx + 48 + tail_sway, hip_y - 52), 
                     (cx + 42 + tail_sway, hip_y - 48)], fill=(200, 20, 20, 255), outline=(150, 10, 10, 255))
# ============================================
# CAPE DRAWING
# ============================================

def draw_cape(renderer, draw, c, cx, shoulder_y, hip_y, cape_type):
    """Draw cape accessory with fabric folds and shading"""
    colors = {
        "Red": (200, 30, 30, 200),
        "Blue": (30, 30, 200, 200),
        "Black": (30, 30, 30, 200),
        "Purple": (120, 30, 180, 200),
        "Green": (30, 150, 30, 200),
    }
    color = colors.get(cape_type, (200, 30, 30, 200))
    dark_color = tuple(max(0, c - 50) for c in color[:3]) + (color[3],)
    light_color = tuple(min(255, c + 40) for c in color[:3]) + (color[3],)
    cape_sway = math.sin(renderer.dance_timer * 0.15) * 8
    
    # Cape shadow
    draw.polygon([(cx - 30, shoulder_y + 3), (cx + 30, shoulder_y + 3),
                 (cx + 42 + cape_sway, hip_y + 23), (cx - 38 - cape_sway, hip_y + 23)],
                fill=(0, 0, 0, 50))
    
    # Main cape
    draw.polygon([(cx - 32, shoulder_y), (cx + 32, shoulder_y),
                 (cx + 40 + cape_sway, hip_y + 20), (cx - 40 - cape_sway, hip_y + 20)],
                fill=color, outline=(0, 0, 0, 100), width=1)
    
    # Fabric fold lines
    for i in range(5):
        fold_x = cx - 20 + i * 10 + cape_sway * (i * 0.1)
        draw.line([(fold_x, shoulder_y + 5), (fold_x - 5 + cape_sway, hip_y + 10)], 
                 fill=dark_color, width=1)
    
    # Hem highlight
    draw.line([(cx - 38 - cape_sway, hip_y + 18), (cx + 38 + cape_sway, hip_y + 18)], 
             fill=light_color, width=2)
    
    # Cape clasp with metallic effect
    draw.ellipse([cx-7, shoulder_y-5, cx+7, shoulder_y+7], fill=(255, 215, 0, 255), outline=(200, 160, 0, 255), width=2)
    draw.ellipse([cx-4, shoulder_y-2, cx+4, shoulder_y+4], fill=(255, 235, 100, 200))
    # Clasp shine
    draw.ellipse([cx-3, shoulder_y-3, cx, shoulder_y], fill=(255, 255, 200, 150))


# ============================================
# WINGS DRAWING
# ============================================

def draw_wings(draw, c, cx, chest_y, shoulder_y, wings_type):
    """Draw wings accessory with feather detail and gradients"""
    wing_colors = {
        "Angel": (255,255,255,200), "Demon": (180,30,30,200), "Dragon": (30,120,30,200),
        "Fairy": (255,200,255,180), "Bat": (40,40,50,200), "Butterfly": (100,255,200,180),
        "Phoenix": (255,100,50,200), "Crow": (20,20,30,220), "Pegasus": (255,255,255,220),
        "Harpy": (150,120,100,200), "Mechanical": (150,150,160,220), "Ice": (200,230,255,200),
        "Shadow": (20,20,40,220), "Leaf": (50,200,50,180), "Crystal": (200,150,255,200),
    }
    color = wing_colors.get(wings_type, (200,200,200,200))
    dark_color = tuple(max(0, c - 40) for c in color[:3]) + (color[3],)
    
    for side in [-1,1]:
        wx = cx-40*side
        wy = chest_y-20
        if wings_type == "Fairy":
            # Outer wing with gradient
            for i in range(4):
                offset = i * 2
                alpha = 100 - i * 20
                draw.ellipse([wx-25+offset,wy-40+offset,wx+5-offset,wy+20-offset], 
                           fill=(255, 200, 255, alpha), outline=(200, 150, 200, 100), width=1)
            draw.ellipse([wx-25,wy-40,wx+5,wy+20], fill=color, outline=(200,150,200,100), width=1)
            # Wing vein patterns
            for i in range(4):
                vx = wx - 15 + i * 5
                vy = wy - 25 + i * 8
                draw.arc([vx-3, vy-5, vx+3, vy+5], 180, 360, fill=(255, 255, 255, 100), width=1)
            draw.ellipse([wx-15,wy-30,wx-5,wy+10], fill=(255,255,255,100), outline=None)
            # Sparkle dots
            for i in range(6):
                sx = wx - 20 + i * 5
                sy = wy - 30 + i * 4
                draw.ellipse([sx-1, sy-1, sx+1, sy+1], fill=(255, 255, 255, 200))
        elif wings_type == "Bat":
            # Membrane shadow
            draw.polygon([(wx-3,wy-18),(wx-33,wy-38),(wx-23,wy-8),(wx-38,wy-8),
                         (wx-18,wy+7),(wx-33,wy+22),(wx-8,wy+7)], 
                        fill=(0, 0, 0, 60))
            draw.polygon([(wx-5,wy-20),(wx-35,wy-40),(wx-25,wy-10),(wx-40,wy-10),
                         (wx-20,wy+5),(wx-35,wy+20),(wx-10,wy+5)], 
                        fill=color, outline=(20,20,30,255), width=1)
            # Wing bone structure
            for bone in [(wx-5,wy-20,wx-30,wy-35), (wx-10,wy-10,wx-35,wy-5), (wx-8,wy+2,wx-28,wy+18)]:
                draw.line([bone[0], bone[1], bone[2], bone[3]], fill=dark_color, width=2)
        elif wings_type == "Mechanical":
            # Gear joints
            for i in range(3):
                wy2 = wy-20+i*15
                draw.rectangle([wx-32,wy2-5,wx+7,wy2+5], fill=(0, 0, 0, 40))
                draw.rectangle([wx-30,wy2-3,wx+5,wy2+3], fill=color, outline=(100,100,110,255), width=1)
                # Rivet details
                for rx in [wx-25, wx-15, wx-5]:
                    draw.ellipse([rx-2, wy2-2, rx+2, wy2+2], fill=(200, 200, 210, 255))
            # Central gear
            draw.ellipse([wx-8,wy-13,wx+8,wy+13], fill=(180, 180, 190, 255), outline=(100,100,110,255), width=2)
            for j in range(6):
                gear_angle = j * (math.pi/3)
                gear_x = wx + int(8 * math.cos(gear_angle))
                gear_y = wy + int(8 * math.sin(gear_angle))
                draw.rectangle([gear_x-2, gear_y-5, gear_x+2, gear_y+5], fill=(200, 200, 210, 255))
        else:
            # Main wing with layered feathers
            for i in range(3):
                offset = i * 3
                alpha = color[3] - i * 30
                layer_color = tuple(list(color[:3]) + [max(0, alpha)])
                draw.ellipse([wx-35+offset,wy-50+offset,wx+15-offset,wy+30-offset], 
                           fill=layer_color, outline=(0,0,0,100), width=2)
            # Feather lines
            for i in range(8):
                fx = wx - 25 + i * 4
                fy = wy - 30 + i * 5
                draw.arc([fx-3, fy-8, fx+3, fy+8], 180, 360, fill=(255, 255, 255, 50), width=1)
            # Inner highlight
            draw.ellipse([wx-25,wy-40,wx+5,wy+20], 
                        fill=(255,255,255,100) if wings_type=="Angel" else (0,0,0,50), outline=None)


# ============================================
# SCARF DRAWING
# ============================================

def draw_scarf(draw, c, cx, neck_y, shoulder_y, scarf_type):
    """Draw scarf accessory with knitted texture and shadows"""
    colors = {
        "Red": (220,40,40,255), "Blue": (40,40,220,255), "Green": (40,180,40,255),
        "Striped": (220,40,40,255), "Winter": (255,255,255,255), "Yellow": (220,220,40,255),
        "Purple": (160,40,200,255), "Pink": (255,100,150,255), "Orange": (255,150,40,255),
        "Black": (40,40,40,255), "Rainbow": (255,50,50,255), "Checkered": (50,50,50,255),
        "Polka Dot": (40,40,220,255), "Camo": (80,120,60,255), "Gradient": (200,50,50,255),
    }
    color = colors.get(scarf_type, (200,200,200,255))
    dark_color = tuple(max(0, c - 50) for c in color[:3]) + (color[3],)
    
    # Scarf shadow
    draw.ellipse([cx-18, neck_y-3, cx+22, neck_y+17], fill=(0, 0, 0, 40))
    
    # Main scarf wrap with folds
    for i in range(3):
        offset = i * 1.5
        draw.ellipse([cx-20+offset, neck_y-5+offset, cx+20-offset, neck_y+15-offset], 
                    fill=color if i == 1 else dark_color, outline=(0,0,0,100), width=1)
    
    # Scarf tail shadow
    draw.line([cx+17, neck_y+7, cx+27, shoulder_y+12], fill=(0, 0, 0, 50), width=8)
    draw.line([cx+15, neck_y+5, cx+25, shoulder_y+10], fill=color, width=6)
    
    # Knitted texture (horizontal lines)
    for i in range(5):
        ky = neck_y - 2 + i * 3.5
        draw.arc([cx-16, ky-1, cx+16, ky+1], 0, 180, fill=dark_color, width=1)
    
    # Scarf fringe at end
    for i in range(4):
        fx = cx + 22 + i * 2
        draw.line([fx, shoulder_y + 8, fx + 1, shoulder_y + 18], fill=color, width=2)
    
    if scarf_type == "Striped":
        for i in range(4):
            sy = neck_y + i * 4.5
            draw.line([cx-18, sy, cx+18, sy], fill=(255, 255, 255, 200), width=3)
            draw.line([cx-18, sy+1.5, cx+18, sy+1.5], fill=(0, 0, 0, 30), width=1)
    elif scarf_type == "Checkered":
        for i in range(4):
            sy = neck_y + i * 4.5
            for j in range(6):
                sx = cx-17 + j * 6
                if (i+j) % 2 == 0:
                    draw.rectangle([sx, sy-2, sx+6, sy+4], fill=(255, 255, 255, 200))
                    draw.rectangle([sx, sy-2, sx+6, sy+4], outline=(0, 0, 0, 30), width=1)
    elif scarf_type == "Rainbow":
        for i in range(4):
            sy = neck_y + i * 4.5
            colors_seq = [(255,0,0,200),(255,165,0,200),(255,255,0,200),(0,255,0,200),(0,0,255,200),(75,0,130,200)]
            for j in range(6):
                sx = cx-16 + j * 6
                draw.line([sx, sy, sx+5, sy], fill=colors_seq[j], width=3)


# ============================================
# OUTFIT DETAILS
# ============================================

def draw_outfit_details(draw, c, cx, shoulder_y, chest_y, hip_y, neck_y, outfit_type, body_color, body_outline_color):
    """Draw outfit-specific details with enhanced textures and shadows"""
    if outfit_type == "suit" or outfit_type == "tuxedo":
        # Tie shadow
        draw.polygon([(cx-3, neck_y+7), (cx+5, neck_y+7), (cx+7, chest_y+7), (cx-5, chest_y+7)], 
                    fill=(0, 0, 0, 50))
        # Tie with silk gradient
        tie_top = neck_y + 5
        tie_bottom = chest_y + 5
        draw.polygon([(cx-4, tie_top), (cx+4, tie_top), (cx+6, tie_bottom), (cx-6, tie_bottom)], 
                    fill=(180, 30, 30, 255), outline=(140, 20, 20, 255), width=1)
        # Tie highlight
        draw.polygon([(cx-2, tie_top+2), (cx+2, tie_top+2), (cx+3, tie_bottom-2), (cx-3, tie_bottom-2)], 
                    fill=(220, 60, 60, 150))
        # Collar with lapel detail
        draw.polygon([(cx-15, neck_y), (cx, neck_y+15), (cx+15, neck_y)], 
                    fill=(255, 255, 255, 200), outline=body_outline_color, width=1)
        # Lapel stitching
        draw.line([(cx-14, neck_y+2), (cx-1, neck_y+13)], fill=(200, 200, 200, 100), width=1)
        draw.line([(cx+14, neck_y+2), (cx+1, neck_y+13)], fill=(200, 200, 200, 100), width=1)
        # Buttons with 3D effect
        for i in range(3):
            by = chest_y - 10 + i * 15
            draw.ellipse([cx-4, by-3, cx+4, by+3], fill=(0, 0, 0, 50))
            draw.ellipse([cx-3, by-2, cx+3, by+2], fill=(80, 80, 80, 255))
            draw.ellipse([cx-2, by-1, cx+2, by+1], fill=(200, 200, 200, 255))
            # Button shine
            draw.ellipse([cx-1, by-1, cx+1, by], fill=(255, 255, 255, 150))
    elif outfit_type == "armor":
        # Armor plate shadows
        for i in range(3):
            py = chest_y - 15 + i * 18
            draw.ellipse([cx-18, py-3, cx+22, py+12], fill=(0, 0, 0, 50))
            draw.ellipse([cx-20, py-5, cx+20, py+10], fill=(200, 200, 220, 100), outline=body_outline_color, width=2)
            # Plate rivet
            draw.ellipse([cx-15, py, cx-11, py+4], fill=(180, 180, 200, 255))
            draw.ellipse([cx+11, py, cx+15, py+4], fill=(180, 180, 200, 255))
        # Shoulder pads with metallic sheen
        for side in [-1, 1]:
            draw.ellipse([cx-36*side, shoulder_y-3, cx-20*side, shoulder_y+17], 
                        fill=(0, 0, 0, 50))
            draw.ellipse([cx-38*side, shoulder_y-5, cx-22*side, shoulder_y+15], 
                        fill=(180, 180, 200, 255), outline=body_outline_color, width=2)
            # Shoulder highlight
            draw.arc([cx-34*side, shoulder_y-2, cx-26*side, shoulder_y+8], 180, 360, 
                    fill=(220, 220, 240, 150), width=3)
        # Belt with buckle
        draw.rectangle([cx-28, hip_y-8, cx+28, hip_y+2], fill=(100, 80, 40, 255), outline=body_outline_color, width=1)
        # Belt stitching
        draw.line([cx-26, hip_y-6, cx+26, hip_y-6], fill=(150, 130, 80, 100), width=1)
        # Buckle
        draw.rectangle([cx-7, hip_y-12, cx+7, hip_y+6], fill=(0, 0, 0, 50))
        draw.rectangle([cx-5, hip_y-10, cx+5, hip_y+4], fill=(200, 180, 40, 255), outline=(150, 130, 30, 255), width=2)
        draw.rectangle([cx-3, hip_y-8, cx+3, hip_y+2], fill=(255, 220, 80, 200))
    elif outfit_type == "military":
        # Pockets with flaps
        for side in [-1, 1]:
            draw.rectangle([cx-20*side, chest_y-6, cx-8*side, chest_y+10], 
                          fill=(0, 0, 0, 50))
            draw.rectangle([cx-22*side, chest_y-8, cx-10*side, chest_y+8], 
                          fill=(70, 90, 50, 255), outline=body_outline_color, width=1)
            # Pocket flap
            draw.polygon([(cx-22*side, chest_y-4), (cx-10*side, chest_y-4), 
                         (cx-12*side, chest_y), (cx-20*side, chest_y)], 
                        fill=(80, 100, 60, 255), outline=body_outline_color, width=1)
            # Button on pocket
            draw.ellipse([cx-17*side, chest_y+2, cx-15*side, chest_y+6], fill=(150, 150, 50, 255))
        # Belt
        draw.rectangle([cx-28, hip_y-8, cx+28, hip_y+2], fill=(80, 60, 30, 255), outline=body_outline_color, width=1)
        draw.rectangle([cx-7, hip_y-12, cx+7, hip_y+6], fill=(0, 0, 0, 40))
        draw.rectangle([cx-5, hip_y-10, cx+5, hip_y+4], fill=(150, 150, 50, 255), outline=(120, 120, 30, 255), width=2)
        # Medals with ribbon
        for i in range(2):
            mx = cx - 5 + i * 15
            draw.rectangle([mx-4, chest_y-6, mx+4, chest_y-2], fill=(200, 50, 50, 255), outline=(150, 30, 30, 255))
            draw.rectangle([mx-3, chest_y-4, mx+3, chest_y+8], fill=(200, 50, 50, 255), outline=(150, 30, 30, 255))
            # Medal shine
            draw.ellipse([mx-2, chest_y-3, mx+2, chest_y+1], fill=(255, 200, 200, 100))
    elif outfit_type == "cyberpunk":
        # Circuit traces
        for i in range(4):
            ly = chest_y - 12 + i * 15
            draw.line([cx-16, ly, cx+16, ly], fill=(0, 0, 0, 60), width=3)
            draw.line([cx-18, ly, cx+18, ly], fill=(0, 255, 200, 150), width=2)
            # Glow effect
            draw.line([cx-18, ly, cx+18, ly], fill=(0, 255, 200, 50), width=6)
            # Node points
            for nx in [cx-16, cx, cx+16]:
                draw.ellipse([nx-3, ly-3, nx+3, ly+3], fill=(0, 255, 200, 200))
                draw.ellipse([nx-1, ly-1, nx+1, ly+1], fill=(255, 255, 255, 200))
        # Chip modules
        draw.rectangle([cx-14, chest_y-7, cx-6, chest_y+7], fill=(0, 0, 0, 50))
        draw.rectangle([cx-12, chest_y-5, cx-6, chest_y+5], fill=(0, 255, 200, 100), outline=(0, 255, 200, 200), width=1)
        draw.rectangle([cx+6, chest_y-7, cx+14, chest_y+7], fill=(0, 0, 0, 50))
        draw.rectangle([cx+6, chest_y-5, cx+12, chest_y+5], fill=(0, 255, 200, 100), outline=(0, 255, 200, 200), width=1)
        # Data lines
        for i in range(3):
            dx = cx - 8 + i * 8
            draw.line([dx, chest_y-4, dx+2, chest_y+4], fill=(0, 255, 200, 80), width=1)


# ============================================
# HAT DRAWING
# ============================================

def draw_hat(renderer, draw, c, cx, head_y, head_shift, hat_type):
    """Draw hat accessory with 3D shading and texture"""
    hat_y = head_y - 15 + head_shift
    if hat_type == "Top Hat":
        # Shadow
        draw.rectangle([cx-16, hat_y-33, cx+20, hat_y+7], fill=(0, 0, 0, 60))
        # Brim
        draw.rectangle([cx-24, hat_y-3, cx+24, hat_y+8], fill=(30,30,30,255), outline=(10,10,10,255), width=2)
        draw.rectangle([cx-22, hat_y-1, cx+22, hat_y+6], fill=(50, 50, 50, 200))
        # Crown
        draw.rectangle([cx-18, hat_y-35, cx+18, hat_y+5], fill=(30,30,30,255), outline=(10,10,10,255), width=2)
        # Crown highlight
        draw.rectangle([cx-16, hat_y-33, cx-8, hat_y+3], fill=(60, 60, 60, 100))
        # Hat band
        draw.rectangle([cx-16, hat_y-20, cx+16, hat_y-10], fill=(180,30,30,255), outline=(140,20,20,255), width=1)
        # Band buckle
        draw.rectangle([cx-6, hat_y-22, cx+6, hat_y-8], fill=(200, 180, 40, 255), outline=(150, 130, 30, 255))
        draw.rectangle([cx-3, hat_y-20, cx+3, hat_y-10], fill=(255, 220, 80, 200))
    elif hat_type == "Cap":
        # Shadow
        draw.arc([cx-23, hat_y-28, cx+27, hat_y+7], 180, 0, fill=(0, 0, 0, 60), width=22)
        # Dome
        draw.arc([cx-25, hat_y-30, cx+25, hat_y+5], 180, 0, fill=(50,50,150,255), width=20)
        # Highlight
        draw.arc([cx-20, hat_y-25, cx+20, hat_y+2], 180, 0, fill=(80, 80, 200, 150), width=10)
        # Brim with stitching
        draw.rectangle([cx-28, hat_y-3, cx+28, hat_y+5], fill=(50,50,150,255), outline=(30,30,100,255))
        draw.line([cx-26, hat_y, cx+26, hat_y], fill=(80, 80, 180, 100), width=1)
        # Ventilation holes
        for vx in [cx-10, cx-5, cx, cx+5, cx+10]:
            draw.ellipse([vx-1, hat_y-15, vx+1, hat_y-13], fill=(30, 30, 80, 255))
    elif hat_type == "Crown":
        pts = [(cx-20,hat_y+5),(cx-25,hat_y-20),(cx-15,hat_y-10),(cx-5,hat_y-25),(cx,hat_y-8),(cx+5,hat_y-25),(cx+15,hat_y-10),(cx+25,hat_y-20),(cx+20,hat_y+5)]
        # Shadow
        shadow_pts = [(x+2, y+2) for x, y in pts]
        draw.polygon(shadow_pts, fill=(0, 0, 0, 60))
        # Main crown
        draw.polygon(pts, fill=(255,215,0,255), outline=(200,160,0,255), width=2)
        # Gold texture gradient
        draw.polygon(pts, fill=(255, 235, 100, 80))
        # Jewels on points
        for px in [cx-25,cx-5,cx+5,cx+25]:
            draw.ellipse([px-4,hat_y-24,px+4,hat_y-16], fill=(0, 0, 0, 50))
            draw.ellipse([px-3,hat_y-23,px+3,hat_y-17], fill=(255,50,50,255), outline=(200,30,30,255), width=1)
            # Jewel shine
            draw.ellipse([px-1,hat_y-22,px+1,hat_y-20], fill=(255, 200, 200, 200))
        # Velvet interior
        draw.ellipse([cx-16, hat_y-2, cx+16, hat_y+6], fill=(120, 20, 20, 200), outline=(200,160,0,255))
    elif hat_type == "Helmet":
        # Shadow
        draw.ellipse([cx-22, hat_y-23, cx+26, hat_y+12], fill=(0, 0, 0, 60))
        # Outer shell
        draw.ellipse([cx-24, hat_y-25, cx+24, hat_y+10], fill=(100,100,100,255), outline=(60,60,60,255), width=3)
        # Metallic reflection
        draw.ellipse([cx-20, hat_y-20, cx-8, hat_y+5], fill=(150, 150, 160, 150))
        # Top ridge
        draw.arc([cx-12, hat_y-30, cx+12, hat_y-10], 180, 0, fill=(200, 200, 210, 100), width=4)
        # Face guard bars
        draw.rectangle([cx-3, hat_y-5, cx+3, hat_y+15], fill=(60, 60, 60, 255))
        for by in range(hat_y-3, hat_y+16, 5):
            draw.line([cx-6, by, cx+6, by], fill=(100, 100, 100, 255), width=2)
    elif hat_type == "Santa":
        # Shadow
        draw.polygon([(cx-10, hat_y+7), (cx+14, hat_y+7), (cx+2, hat_y-28)], fill=(0, 0, 0, 50))
        # Hat body
        draw.polygon([(cx-12, hat_y+5), (cx+12, hat_y+5), (cx, hat_y-30)], fill=(200, 30, 30, 255), outline=(150, 20, 20, 255), width=2)
        # Fur trim
        draw.rectangle([cx-16, hat_y, cx+16, hat_y+5], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=1)
        # Fur texture dots
        for i in range(8):
            fx = cx - 12 + i * 3
            draw.ellipse([fx-1, hat_y+1, fx+1, hat_y+3], fill=(240, 240, 240, 150))
        # Pom pom
        draw.ellipse([cx-7, hat_y-34, cx+7, hat_y-20], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=1)
        draw.ellipse([cx-4, hat_y-30, cx+4, hat_y-24], fill=(240, 240, 240, 150))
    elif hat_type == "Propeller":
        # Shadow
        draw.ellipse([cx-16, hat_y-13, cx+20, hat_y+7], fill=(0, 0, 0, 50))
        # Cap body
        draw.ellipse([cx-18, hat_y-15, cx+18, hat_y+5], fill=(50, 50, 150, 255), outline=(30, 30, 100, 255), width=2)
        # Cap highlight
        draw.ellipse([cx-14, hat_y-12, cx-4, hat_y+2], fill=(80, 80, 200, 150))
        # Stem
        draw.line([cx, hat_y-15, cx, hat_y-30], fill=(100, 100, 100, 255), width=2)
        # Stem highlight
        draw.line([cx-1, hat_y-16, cx-1, hat_y-28], fill=(150, 150, 150, 150), width=1)
        # Propeller blades with motion blur
        angle = renderer.dance_timer * 0.3
        prop_len = 18
        for blade in range(2):
            blade_angle = angle + blade * math.pi
            dx = int(prop_len * math.cos(blade_angle))
            dy = int(prop_len * math.sin(blade_angle))
            # Blade shadow
            draw.line([cx-dx+1, hat_y-30-dy+1, cx+dx+1, hat_y-30+dy+1], fill=(0, 0, 0, 50), width=6)
            # Main blade
            draw.line([cx-dx, hat_y-30-dy, cx+dx, hat_y-30+dy], fill=(255, 50, 50, 255), width=4)
            # Blade highlight
            draw.line([cx-dx//2, hat_y-30-dy//2, cx+dx//2, hat_y-30+dy//2], fill=(255, 150, 150, 150), width=2)
        # Hub
        draw.ellipse([cx-4, hat_y-34, cx+4, hat_y-26], fill=(0, 0, 0, 50))
        draw.ellipse([cx-3, hat_y-33, cx+3, hat_y-27], fill=(200, 200, 200, 255), outline=(150, 150, 150, 255))
    elif hat_type == "Viking":
        # Shadow
        draw.ellipse([cx-18, hat_y-13, cx+22, hat_y+7], fill=(0, 0, 0, 50))
        # Helmet body
        draw.ellipse([cx-20, hat_y-15, cx+20, hat_y+5], fill=(100, 100, 100, 255), outline=(60, 60, 60, 255), width=3)
        # Metallic highlight
        draw.ellipse([cx-16, hat_y-12, cx-4, hat_y+2], fill=(150, 150, 160, 150))
        # Horns with shading
        for hx in [cx-10, cx, cx+10]:
            draw.line([hx+1, hat_y-14, hx+1, hat_y-34], fill=(0, 0, 0, 50), width=5)
            draw.line([hx, hat_y-15, hx, hat_y-35], fill=(200, 180, 140, 255), width=4)
            draw.line([hx-1, hat_y-16, hx-1, hat_y-30], fill=(220, 200, 160, 150), width=2)
    elif hat_type == "Pirate":
        # Shadow
        draw.arc([cx-23, hat_y-6, cx+27, hat_y+17], 180, 0, fill=(0, 0, 0, 60), width=20)
        # Tricorn body
        draw.arc([cx-25, hat_y-8, cx+25, hat_y+15], 180, 0, fill=(30, 30, 30, 255), width=18)
        # Highlight
        draw.arc([cx-20, hat_y-5, cx+20, hat_y+10], 180, 0, fill=(60, 60, 60, 150), width=10)
        # Skull emblem
        draw.ellipse([cx-9, hat_y-16, cx+9, hat_y-2], fill=(255, 255, 255, 200), outline=(200, 200, 200, 255), width=1)
        for ex in [cx-4, cx+4]:
            draw.ellipse([ex-2, hat_y-12, ex+2, hat_y-8], fill=(30, 30, 30, 255))
        draw.arc([cx-3, hat_y-7, cx+3, hat_y-3], 0, 180, fill=(30, 30, 30, 255), width=1)


# ============================================
# MASK DRAWING
# ============================================

def draw_mask(draw, c, cx, head_y, head_shift, mask_type):
    """Draw mask accessory with detailed textures"""
    mask_y = head_y + 10
    if mask_type == "Batman":
        # Shadow
        draw.ellipse([cx-23, mask_y-3, cx+27, mask_y+27], fill=(0, 0, 0, 60))
        # Main mask
        draw.ellipse([cx-25, mask_y-5, cx+25, mask_y+25], fill=(20,20,40,220), outline=(10,10,20,255), width=2)
        # Ear points
        draw.polygon([(cx-20, mask_y-3), (cx-22, mask_y-20), (cx-15, mask_y)], fill=(20,20,40,220), outline=(10,10,20,255))
        draw.polygon([(cx+20, mask_y-3), (cx+22, mask_y-20), (cx+15, mask_y)], fill=(20,20,40,220), outline=(10,10,20,255))
        # Eye holes with glow
        for ex in [cx-12, cx+12]:
            draw.ellipse([ex-12, mask_y, ex+12, mask_y+14], fill=(255, 255, 255, 255))
            draw.ellipse([ex-8, mask_y+3, ex+8, mask_y+11], fill=(255, 255, 200, 200))
        # Nose guard
        draw.polygon([(cx-3, mask_y+25), (cx+3, mask_y+25), (cx+5, mask_y+35), (cx-5, mask_y+35)], 
                    fill=(20,20,40,220), outline=(10,10,20,255), width=1)
    elif mask_type == "Skull":
        # Shadow
        draw.ellipse([cx-18, mask_y+2, cx+22, mask_y+27], fill=(0, 0, 0, 60))
        # Bone mask
        draw.ellipse([cx-20, mask_y, cx+20, mask_y+25], fill=(230,230,220,220), outline=(180,180,170,255), width=2)
        # Bone texture lines
        for i in range(5):
            draw.arc([cx-15, mask_y+5+i*3, cx+15, mask_y+8+i*3], 180, 360, fill=(200, 200, 190, 50), width=1)
        # Eye sockets
        for ex in [cx-10, cx+10]:
            draw.ellipse([ex-9, mask_y+5, ex+9, mask_y+15], fill=(0, 0, 0, 255))
            draw.ellipse([ex-7, mask_y+7, ex+7, mask_y+13], fill=(20, 20, 20, 255))
        # Nasal cavity
        draw.polygon([(cx-5, mask_y+16), (cx+5, mask_y+16), (cx+3, mask_y+22), (cx-3, mask_y+22)], fill=(0, 0, 0, 200))
        # Cheek bone shadows
        draw.ellipse([cx-15, mask_y+12, cx-7, mask_y+20], fill=(180, 180, 170, 100))
        draw.ellipse([cx+7, mask_y+12, cx+15, mask_y+20], fill=(180, 180, 170, 100))
    elif mask_type == "Cyberpunk":
        # Shadow
        draw.ellipse([cx-20, mask_y+2, cx+24, mask_y+30], fill=(0, 0, 0, 60))
        # Main mask
        draw.ellipse([cx-22, mask_y, cx+22, mask_y+28], fill=(30,30,50,240), outline=(0,255,200,255), width=2)
        # Neon glow effect
        draw.ellipse([cx-22, mask_y, cx+22, mask_y+28], fill=(0, 255, 200, 30), outline=None)
        # Eye displays
        for ex in [cx-10, cx+10]:
            draw.ellipse([ex-8, mask_y+7, ex+8, mask_y+15], fill=(255, 0, 100, 200), outline=(255, 100, 150, 255))
            # Display glare
            draw.ellipse([ex-4, mask_y+8, ex, mask_y+12], fill=(255, 255, 255, 100))
        # Circuit traces
        for i in range(4):
            ly = mask_y + 5 + i * 6
            draw.line([cx-15, ly, cx+15, ly], fill=(0, 255, 200, 150), width=1)
            draw.line([cx-15, ly, cx+15, ly], fill=(0, 255, 200, 50), width=3)
        # Data port
        draw.rectangle([cx-4, mask_y+20, cx+4, mask_y+26], fill=(0, 255, 200, 200), outline=(0, 200, 150, 255))
    elif mask_type == "Dragon":
        # Shadow
        draw.ellipse([cx-20, mask_y+2, cx+24, mask_y+30], fill=(0, 0, 0, 60))
        # Scale mask
        draw.ellipse([cx-22, mask_y, cx+22, mask_y+28], fill=(30,120,30,240), outline=(15,80,15,255), width=2)
        # Scale texture
        for i in range(5):
            for j in range(4):
                sx = cx - 16 + j * 8 + (i % 2) * 4
                sy = mask_y + 3 + i * 5
                draw.arc([sx-3, sy-2, sx+3, sy+2], 0, 180, fill=(50, 150, 50, 150), width=1)
        # Glowing eyes
        for ex in [cx-10, cx+10]:
            draw.ellipse([ex-8, mask_y+7, ex+8, mask_y+15], fill=(255, 200, 50, 200), outline=(200, 150, 20, 255))
            draw.ellipse([ex-4, mask_y+8, ex, mask_y+12], fill=(255, 255, 200, 150))
        # Horns
        for hx in [cx-18, cx+18]:
            draw.line([hx+1, mask_y-4, hx+1, mask_y-24], fill=(0, 0, 0, 60), width=6)
            draw.line([hx, mask_y-5, hx, mask_y-25], fill=(30,120,30,240), width=5)
            draw.line([hx-1, mask_y-6, hx-1, mask_y-22], fill=(60, 180, 60, 150), width=2)


# ============================================
# GLASSES DRAWING
# ============================================

def draw_glasses(draw, c, cx, head_y, head_shift, glasses_type):
    """Draw glasses accessory with lens reflections and 3D frames"""
    gl_y = head_y + 20
    if glasses_type == "Sunglasses":
        # Frame shadow
        for ex in [cx-12, cx+12]:
            draw.ellipse([ex-10, gl_y, ex+14, gl_y+14], fill=(0, 0, 0, 60))
            # Frame
            draw.ellipse([ex-12, gl_y-2, ex+12, gl_y+12], fill=(20,20,20,200), outline=(0,0,0,255), width=2)
            # Lens gradient
            draw.ellipse([ex-10, gl_y, ex+10, gl_y+10], fill=(40, 40, 40, 200))
            # Reflection
            draw.ellipse([ex-6, gl_y, ex-2, gl_y+4], fill=(255, 255, 255, 80))
            draw.ellipse([ex-8, gl_y+6, ex-4, gl_y+8], fill=(255, 255, 255, 40))
        # Bridge
        draw.line([cx-2, gl_y+4, cx+2, gl_y+4], fill=(0,0,0,255), width=2)
        draw.line([cx-1, gl_y+3, cx+1, gl_y+3], fill=(100, 100, 100, 100), width=1)
    elif glasses_type == "Nerd":
        for ex in [cx-12, cx+12]:
            draw.ellipse([ex-10, gl_y, ex+14, gl_y+14], fill=(0, 0, 0, 40))
            draw.ellipse([ex-12, gl_y-2, ex+12, gl_y+12], fill=(255,255,255,100), outline=(0,0,0,255), width=2)
            # Lens shine
            draw.ellipse([ex-6, gl_y, ex-2, gl_y+4], fill=(255, 255, 255, 120))
            draw.ellipse([ex-8, gl_y+6, ex-4, gl_y+8], fill=(200, 200, 255, 60))
        draw.line([cx-2, gl_y+4, cx+2, gl_y+4], fill=(0,0,0,255), width=2)
        # Tape on bridge
        draw.rectangle([cx-3, gl_y+2, cx+3, gl_y+6], fill=(255, 255, 255, 200), outline=(200, 200, 200, 255))
    elif glasses_type == "Monocle":
        # Chain
        draw.line([cx+17, gl_y+5, cx+22, gl_y+18], fill=(255,215,0,255), width=1)
        for ci in range(4):
            chain_y = gl_y + 7 + ci * 3
            draw.ellipse([cx+18, chain_y-1, cx+20, chain_y+1], fill=(255, 215, 0, 255))
        # Lens shadow
        draw.ellipse([cx+6, gl_y, cx+19, gl_y+14], fill=(0, 0, 0, 40))
        # Frame
        draw.ellipse([cx+5, gl_y-2, cx+17, gl_y+12], fill=(255,255,255,100), outline=(255,215,0,255), width=2)
        # Lens reflection
        draw.ellipse([cx+7, gl_y, cx+11, gl_y+4], fill=(255, 255, 255, 100))
    elif glasses_type == "Goggles":
        # Strap
        draw.line([cx-24, gl_y+2, cx-30, gl_y-5], fill=(50,50,50,255), width=4)
        draw.line([cx+24, gl_y+2, cx+30, gl_y-5], fill=(50,50,50,255), width=4)
        # Lens shadow
        draw.ellipse([cx-16, gl_y-6, cx+20, gl_y+12], fill=(0, 0, 0, 50))
        # Frame
        draw.ellipse([cx-18, gl_y-8, cx+18, gl_y+10], fill=(150,200,255,150), outline=(50,100,150,255), width=3)
        # Inner lens
        draw.ellipse([cx-14, gl_y-5, cx+14, gl_y+8], fill=(200,230,255,100))
        # Lens reflections
        draw.ellipse([cx-10, gl_y-4, cx-2, gl_y+2], fill=(255, 255, 255, 80))
        draw.ellipse([cx+2, gl_y+2, cx+10, gl_y+6], fill=(255, 255, 255, 60))
        # Ventilation holes
        for vx in [cx-16, cx-12, cx+12, cx+16]:
            draw.ellipse([vx-1, gl_y-1, vx+1, gl_y+1], fill=(50, 100, 150, 255))
    elif glasses_type == "Cyclops":
        # Visor shadow
        draw.ellipse([cx-14, gl_y, cx+18, gl_y+14], fill=(0, 0, 0, 50))
        # Visor frame
        draw.ellipse([cx-16, gl_y-2, cx+16, gl_y+12], fill=(255,50,50,150), outline=(200,30,30,255), width=3)
        # Visor lens
        draw.ellipse([cx-10, gl_y+2, cx+10, gl_y+10], fill=(255, 200, 200, 200))
        # Tech lines
        for i in range(3):
            ly = gl_y + 4 + i * 3
            draw.arc([cx-8, ly-1, cx+8, ly+1], 0, 180, fill=(200, 50, 50, 100), width=1)


# ============================================
# SHIRT DRAWING
# ============================================

def draw_shirt(draw, c, cx, hip_y, chest_y, shoulder_y, shirt_type):
    """Draw shirt clothing with fabric textures and wrinkles"""
    colors = {
        "T-Shirt": (255,255,255,200), "Jacket": (80,50,30,220), "Hoodie": (100,100,120,220),
        "Armor": (180,180,200,220), "Suit": (30,30,50,220), "Vest": (60,40,20,220),
        "Sweater": (200,50,50,220), "Tank Top": (255,255,255,180), "Flannel": (200,50,50,220),
        "Turtleneck": (50,50,50,220), "Hawaiian": (50,200,150,220), "Leather": (40,30,30,240),
        "Chainmail": (180,180,200,200), "Lab Coat": (255,255,255,220), "Poncho": (200,150,100,220),
    }
    outline_colors = {
        "T-Shirt": (200,200,200,255), "Jacket": (50,30,15,255), "Hoodie": (70,70,90,255),
        "Armor": (140,140,160,255), "Suit": (15,15,30,255), "Vest": (40,25,10,255),
        "Sweater": (150,30,30,255), "Tank Top": (200,200,200,255), "Flannel": (150,30,30,255),
        "Turtleneck": (30,30,30,255), "Hawaiian": (30,150,100,255), "Leather": (20,15,15,255),
        "Chainmail": (140,140,160,255), "Lab Coat": (200,200,200,255), "Poncho": (150,100,60,255),
    }
    color = colors.get(shirt_type, (200,200,200,200))
    outline = outline_colors.get(shirt_type, (150,150,150,255))
    dark_color = tuple(max(0, c - 40) for c in color[:3]) + (color[3],)
    light_color = tuple(min(255, c + 30) for c in color[:3]) + (color[3],)
    
    if shirt_type == "Suit":
        # Jacket shadow
        draw.rectangle([cx-30, shoulder_y+7, cx+34, hip_y-3], fill=(0, 0, 0, 50))
        draw.rectangle([cx-32, shoulder_y+5, cx+32, hip_y-5], fill=color, outline=outline, width=2)
        # Jacket opening
        draw.line([cx, shoulder_y+5, cx, hip_y-5], fill=(15,15,30,255), width=1)
        # Lapel highlights
        draw.line([cx-15, shoulder_y+8, cx-3, chest_y-5], fill=(40, 40, 60, 150), width=2)
        draw.line([cx+15, shoulder_y+8, cx+3, chest_y-5], fill=(40, 40, 60, 150), width=2)
        # Pocket square
        draw.polygon([(cx-8, chest_y-8), (cx-4, chest_y-14), (cx, chest_y-8)], fill=(255, 255, 255, 200))
        # Shirt underneath
        draw.ellipse([cx-4, chest_y-10, cx+4, chest_y-2], fill=(255,255,255,200), outline=(200,200,200,255))
    elif shirt_type == "Hoodie":
        draw.rectangle([cx-32, shoulder_y+12, cx+36, hip_y-3], fill=(0, 0, 0, 50))
        draw.rectangle([cx-34, shoulder_y+10, cx+34, hip_y-5], fill=color, outline=outline, width=2)
        # Hood
        draw.ellipse([cx-30, shoulder_y, cx+30, shoulder_y+25], fill=dark_color, outline=outline, width=1)
        # Hood opening
        draw.ellipse([cx-15, shoulder_y+3, cx+15, shoulder_y+18], fill=light_color)
        # Kangaroo pocket
        draw.rectangle([cx-20, chest_y+5, cx+20, hip_y-10], fill=dark_color, outline=outline, width=1)
        # Drawstring
        for ds in [-3, 3]:
            draw.line([cx+ds, shoulder_y+12, cx+ds+5, chest_y+2], fill=(255, 255, 255, 200), width=1.5)
    elif shirt_type == "Flannel":
        draw.rectangle([cx-28, shoulder_y+7, cx+32, hip_y-3], fill=(0, 0, 0, 50))
        draw.rectangle([cx-30, shoulder_y+5, cx+30, hip_y-5], fill=color, outline=outline, width=2)
        # Plaid pattern
        for i in range(5):
            ly = shoulder_y + 8 + i * 15
            draw.line([cx-28, ly, cx+28, ly], fill=(255,255,255,80), width=1)
        for i in range(4):
            lx = cx-20 + i * 13
            draw.line([lx, shoulder_y+5, lx, hip_y-5], fill=(255,255,255,80), width=1)
        # Plaid intersections
        for i in range(4):
            for j in range(4):
                ix = cx - 18 + i * 12
                iy = shoulder_y + 10 + j * 12
                if iy < hip_y - 5:
                    draw.ellipse([ix-2, iy-2, ix+2, iy+2], fill=(0, 0, 0, 100))
    elif shirt_type == "Hawaiian":
        draw.rectangle([cx-28, shoulder_y+7, cx+32, hip_y-3], fill=(0, 0, 0, 50))
        draw.rectangle([cx-30, shoulder_y+5, cx+30, hip_y-5], fill=color, outline=outline, width=2)
        # Flower pattern
        for i in range(6):
            fx = cx - 22 + i * 8
            fy = chest_y - 8 + i * 5
            # Petals
            for j in range(5):
                petal_angle = j * (2*math.pi/5)
                px = fx + int(4 * math.cos(petal_angle))
                py = fy + int(4 * math.sin(petal_angle))
                draw.ellipse([px-3, py-3, px+3, py+3], fill=(255, 50, 150, 150))
            # Center
            draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=(255, 255, 50, 255))
    elif shirt_type == "Chainmail":
        draw.rectangle([cx-28, shoulder_y+7, cx+32, hip_y-3], fill=(0, 0, 0, 50))
        draw.rectangle([cx-30, shoulder_y+5, cx+30, hip_y-5], fill=color, outline=outline, width=2)
        # Ring pattern
        for i in range(8):
            for j in range(6):
                rx = cx - 25 + j * 8 + (i % 2) * 4
                ry = shoulder_y + 8 + i * 8
                if ry < hip_y - 5:
                    draw.ellipse([rx-3, ry-3, rx+3, ry+3], outline=(200, 200, 220, 200), width=1)
                    draw.ellipse([rx-2, ry-4, rx+2, ry], fill=(220, 220, 240, 80))
    else:
        draw.rectangle([cx-28, shoulder_y+7, cx+32, hip_y-3], fill=(0, 0, 0, 50))
        draw.rectangle([cx-30, shoulder_y+5, cx+30, hip_y-5], fill=color, outline=outline, width=2)
        # Fabric wrinkle lines
        for i in range(3):
            wy = chest_y - 5 + i * 15
            draw.arc([cx-15, wy-2, cx+15, wy+2], 180, 360, fill=dark_color, width=1)


# ============================================
# PANTS DRAWING
# ============================================

def draw_pants(draw, c, cx, hip_y, ground_y, leg_swing, pants_type):
    """Draw pants clothing with fabric folds and seams"""
    colors = {
        "Jeans": (50,80,150,220), "Shorts": (150,150,100,220), "Skirt": (200,100,150,220),
        "Cargo": (100,130,80,220), "Sweatpants": (100,100,100,220), "Leather Pants": (30,30,30,240),
        "Plaid Pants": (150,50,50,220), "Khakis": (180,170,140,220), "Joggers": (50,50,60,220),
        "Ripped Jeans": (60,90,170,220), "Bell Bottoms": (50,100,200,220), "Tights": (30,30,30,220),
        "Overalls Pants": (80,100,200,220), "Culottes": (180,150,120,220), "Bloomers": (255,255,255,220),
    }
    outline_colors = {
        "Jeans": (30,50,100,255), "Shorts": (100,100,70,255), "Skirt": (150,70,100,255),
        "Cargo": (70,100,50,255), "Sweatpants": (70,70,70,255), "Leather Pants": (15,15,15,255),
        "Plaid Pants": (100,30,30,255), "Khakis": (140,130,100,255), "Joggers": (30,30,40,255),
        "Ripped Jeans": (40,60,120,255), "Bell Bottoms": (30,70,150,255), "Tights": (15,15,15,255),
        "Overalls Pants": (50,70,150,255), "Culottes": (140,110,80,255), "Bloomers": (200,200,200,255),
    }
    color = colors.get(pants_type, (100,100,100,200))
    outline = outline_colors.get(pants_type, (70,70,70,255))
    dark_color = tuple(max(0, c - 30) for c in color[:3]) + (color[3],)
    light_color = tuple(min(255, c + 20) for c in color[:3]) + (color[3],)
    
    if pants_type == "Skirt":
        # Shadow
        draw.polygon([(cx-18, hip_y-3), (cx+22, hip_y-3), (cx+30, hip_y+37), (cx-26, hip_y+37)], fill=(0, 0, 0, 50))
        draw.polygon([(cx-20, hip_y-5), (cx+20, hip_y-5), (cx+28, hip_y+35), (cx-28, hip_y+35)], 
                    fill=color, outline=outline, width=2)
        # Pleats
        for i in range(6):
            px = cx - 15 + i * 6
            draw.line([px, hip_y, px - 2 + (i % 2) * 4, hip_y + 30], fill=dark_color, width=1)
        # Hem line
        draw.line([(cx-26, hip_y+33), (cx+26, hip_y+33)], fill=light_color, width=2)
    elif pants_type == "Jeans":
        for side, hx in [(-1,cx-20),(1,cx+20)]:
            draw.rectangle([hx-8, hip_y-3, hx+12, ground_y-68], fill=(0, 0, 0, 40))
            draw.rectangle([hx-10, hip_y-5, hx+10, ground_y-70], fill=color, outline=outline, width=2)
            # Seam lines
            draw.line([hx-8, hip_y, hx-8, ground_y-68], fill=(30, 60, 130, 100), width=1)
            draw.line([hx+8, hip_y, hx+8, ground_y-68], fill=(30, 60, 130, 100), width=1)
            # Knee wrinkles
            for i in range(3):
                ky = hip_y + 20 + i * 12
                draw.arc([hx-7, ky-1, hx+7, ky+1], 0, 180, fill=dark_color, width=1)
        # Pocket stitching
        for side in [-1, 1]:
            draw.arc([cx-10*side, hip_y-2, cx-20*side, hip_y+15], 0, 180, fill=(200, 180, 50, 100), width=1)
    elif pants_type == "Ripped Jeans":
        for side, hx in [(-1,cx-20),(1,cx+20)]:
            draw.rectangle([hx-8, hip_y-3, hx+12, ground_y-68], fill=(0, 0, 0, 40))
            draw.rectangle([hx-10, hip_y-5, hx+10, ground_y-70], fill=color, outline=outline, width=2)
            # Rips with torn edges
            for r in range(3):
                ry = hip_y + 10 + r * 20
                draw.ellipse([hx-6, ry-4, hx+6, ry+4], fill=(255, 200, 150, 150), outline=None)
                # Torn threads
                for tx in [hx-4, hx-2, hx+2, hx+4]:
                    draw.line([tx, ry-2, tx + random.choice([-1, 1]), ry+2], fill=(220, 200, 180, 200), width=1)
    else:
        for side, hx in [(-1,cx-20),(1,cx+20)]:
            leg_bottom = hip_y+30 if pants_type == "Shorts" else ground_y-70
            draw.rectangle([hx-8, hip_y-3, hx+12, leg_bottom+2], fill=(0, 0, 0, 40))
            draw.rectangle([hx-10, hip_y-5, hx+10, leg_bottom], fill=color, outline=outline, width=2)
            # Highlight
            draw.rectangle([hx-6, hip_y-3, hx-2, leg_bottom-2], fill=light_color)
            # Cuff (for pants)
            if pants_type != "Shorts":
                draw.line([hx-9, leg_bottom-5, hx+9, leg_bottom-5], fill=dark_color, width=2)


# ============================================
# SHOES DRAWING
# ============================================

def draw_shoes(draw, c, cx, ground_y, leg_swing, shoes_type):
    """Draw shoes clothing with detailed soles, laces, and textures"""
    colors = {
        "Sneakers": (255,255,255,255), "Boots": (80,50,30,255), "Sandals": (200,150,100,255),
        "Heels": (255,100,150,255), "Cowboy Boots": (100,60,30,255), "Slippers": (255,200,200,255),
        "Flip Flops": (50,50,255,255), "Hiking Boots": (80,70,50,255), "Ballet Flats": (255,150,200,255),
        "Clogs": (180,140,100,255), "Snow Boots": (255,255,255,255), "Rain Boots": (255,255,0,255),
        "Loafers": (100,60,30,255), "High Tops": (255,50,50,255), "Cleats": (30,30,30,255),
    }
    outline_colors = {
        "Sneakers": (200,200,200,255), "Boots": (50,30,15,255), "Sandals": (150,100,70,255),
        "Heels": (200,70,100,255), "Cowboy Boots": (70,40,15,255), "Slippers": (200,150,150,255),
        "Flip Flops": (30,30,200,255), "Hiking Boots": (50,40,30,255), "Ballet Flats": (200,100,150,255),
        "Clogs": (140,100,60,255), "Snow Boots": (200,200,200,255), "Rain Boots": (200,200,0,255),
        "Loafers": (70,40,15,255), "High Tops": (200,30,30,255), "Cleats": (15,15,15,255),
    }
    color = colors.get(shoes_type, (100,100,100,255))
    outline = outline_colors.get(shoes_type, (70,70,70,255))
    dark_color = tuple(max(0, c - 30) for c in color[:3]) + (color[3],)
    light_color = tuple(min(255, c + 30) for c in color[:3]) + (color[3],)
    
    for fx in [cx-14+leg_swing, cx+14-leg_swing]:
        if shoes_type == "Sneakers":
            # Sole shadow
            draw.ellipse([fx-18, ground_y-46, fx+24, ground_y-44], fill=(0, 0, 0, 60))
            # Sole
            draw.rectangle([fx-22, ground_y-52, fx+24, ground_y-46], fill=(240, 240, 240, 255), outline=(200, 200, 200, 255))
            # Sole tread lines
            for i in range(6):
                tx = fx - 18 + i * 7
                draw.line([tx, ground_y-50, tx+3, ground_y-47], fill=(200, 200, 200, 255), width=2)
            # Upper
            draw.ellipse([fx-20, ground_y-78, fx+22, ground_y-48], fill=color, outline=outline, width=2)
            # Toe cap
            draw.arc([fx-18, ground_y-75, fx+5, ground_y-60], 180, 0, fill=light_color, width=4)
            # Laces
            for i in range(4):
                lx = fx - 5 + i * 3
                ly = ground_y - 70 + i * 4
                draw.line([lx-3, ly, lx+3, ly], fill=(200, 200, 200, 255), width=1)
            # Swoosh/Side stripe
            draw.arc([fx-15, ground_y-70, fx+10, ground_y-50], 200, 340, fill=(200, 50, 50, 200), width=3)
        elif shoes_type == "Boots":
            # Sole
            draw.ellipse([fx-18, ground_y-48, fx+22, ground_y-44], fill=(0, 0, 0, 60))
            draw.rectangle([fx-20, ground_y-52, fx+22, ground_y-46], fill=(30, 20, 10, 255), outline=(15, 10, 5, 255))
            # Heel
            draw.rectangle([fx+10, ground_y-58, fx+22, ground_y-46], fill=(30, 20, 10, 255), outline=(15, 10, 5, 255))
            # Upper
            draw.rectangle([fx-18, ground_y-85, fx+20, ground_y-50], fill=color, outline=outline, width=2)
            # Leather highlight
            draw.rectangle([fx-14, ground_y-80, fx-6, ground_y-55], fill=light_color)
            # Stitching
            for sy in range(ground_y-75, ground_y-52, 8):
                draw.arc([fx-16, sy-1, fx+18, sy+1], 0, 180, fill=(150, 120, 80, 150), width=1)
        elif shoes_type == "Heels":
            # Thin heel
            draw.rectangle([fx-3, ground_y-65, fx+5, ground_y-44], fill=(0, 0, 0, 60))
            draw.rectangle([fx-4, ground_y-65, fx+4, ground_y-55], fill=color, outline=outline)
            # Heel tip
            draw.ellipse([fx-4, ground_y-47, fx+4, ground_y-44], fill=(30, 30, 30, 255))
            # Upper
            draw.ellipse([fx-12, ground_y-85, fx+12, ground_y-65], fill=color, outline=outline)
            # Shine
            draw.ellipse([fx-8, ground_y-80, fx-2, ground_y-70], fill=light_color)
        else:
            draw.ellipse([fx-18, ground_y-46, fx+24, ground_y-44], fill=(0, 0, 0, 50))
            draw.ellipse([fx-20, ground_y-78, fx+22, ground_y-48], fill=color, outline=outline, width=2)
            # Highlight
            draw.ellipse([fx-14, ground_y-72, fx-6, ground_y-55], fill=light_color)


# ============================================
# HAIR STYLE DRAWING
# ============================================

def draw_hair_style(renderer, draw, c, hair_cfg, cx, adj_head_y, head_shift, head_size_mult, width_mult):
    """Draw hair with style, strands, and highlights"""
    hair_style = hair_cfg.get("style", "default")
    hair_len = hair_cfg.get("length", 1.0)
    hair_vol = hair_cfg.get("volume", 1.0)
    hair_bangs = hair_cfg.get("bangs", True)
    hair_color = c["hair"]
    hair_dark = tuple(max(0, c - 30) for c in hair_color[:3]) + (hair_color[3],)
    hair_light = tuple(min(255, c + 40) for c in hair_color[:3]) + (hair_color[3],)
    
    if hair_style == "bald":
        return
    elif hair_style == "spiky":
        for i in range(7):
            sx = cx - int(30 * hair_vol) + i * int(10 * hair_vol)
            sy = adj_head_y - 15 - int(abs(i - 3) * 8 * hair_len)
            # Shadow
            draw.polygon([(sx-3, adj_head_y-3), (sx+5, adj_head_y-3), (sx+1, sy+2)], fill=(0, 0, 0, 60))
            # Main spike
            draw.polygon([(sx-4, adj_head_y-5), (sx+4, adj_head_y-5), (sx, sy)], fill=hair_color, outline=c["hair_outline"])
            # Highlight
            draw.polygon([(sx-2, adj_head_y-4), (sx+1, adj_head_y-4), (sx, sy-4)], fill=hair_light)
        if hair_bangs:
            draw.ellipse([cx - int(44 * hair_vol) + head_shift - 1, adj_head_y - 5, 
                         cx + int(44 * hair_vol) + head_shift + 1, adj_head_y + int(15 * hair_len) + 1], 
                        fill=(0, 0, 0, 40))
            draw.ellipse([cx - int(44 * hair_vol) + head_shift, adj_head_y - 6, 
                         cx + int(44 * hair_vol) + head_shift, adj_head_y + int(15 * hair_len)], 
                        fill=hair_color, outline=c["hair_outline"], width=1)
            # Bang highlight
            draw.ellipse([cx - int(30 * hair_vol) + head_shift, adj_head_y - 3, 
                         cx + int(10 * hair_vol) + head_shift, adj_head_y + int(8 * hair_len)], 
                        fill=hair_light)
    elif hair_style == "long":
        # Main hair mass
        draw.ellipse([cx - int(46 * hair_vol) + head_shift - 1, adj_head_y - 9, 
                     cx + int(46 * hair_vol) + head_shift + 1, adj_head_y + int(50 * hair_len) + 1], 
                    fill=(0, 0, 0, 50))
        draw.ellipse([cx - int(46 * hair_vol) + head_shift, adj_head_y - 10, 
                     cx + int(46 * hair_vol) + head_shift, adj_head_y + int(50 * hair_len)], 
                    fill=hair_color, outline=c["hair_outline"], width=1)
        # Long back
        draw.rectangle([cx - int(28 * hair_vol) + head_shift, adj_head_y + int(30 * hair_len) - 1,
                       cx + int(28 * hair_vol) + head_shift + 1, adj_head_y + int(90 * hair_len) + 1], 
                      fill=(0, 0, 0, 40))
        draw.rectangle([cx - int(30 * hair_vol) + head_shift, adj_head_y + int(30 * hair_len), 
                       cx + int(30 * hair_vol) + head_shift, adj_head_y + int(90 * hair_len)], 
                      fill=hair_color, outline=c["hair_outline"])
        # Hair strands
        for i in range(8):
            strand_x = cx - int(20 * hair_vol) + i * int(5 * hair_vol) + head_shift
            draw.line([strand_x, adj_head_y + int(20 * hair_len), strand_x + 2, adj_head_y + int(80 * hair_len)], 
                     fill=hair_dark, width=1)
        # Shine
        draw.rectangle([cx - int(15 * hair_vol) + head_shift, adj_head_y + int(35 * hair_len),
                       cx - int(5 * hair_vol) + head_shift, adj_head_y + int(75 * hair_len)], 
                      fill=hair_light)
    elif hair_style == "mohawk":
        # Main strip shadow
        draw.rectangle([cx - int(7 * hair_vol) + head_shift + 1, adj_head_y - int(49 * hair_len) + 1,
                       cx + int(7 * hair_vol) + head_shift + 1, adj_head_y + 1], 
                      fill=(0, 0, 0, 50))
        draw.rectangle([cx - int(8 * hair_vol) + head_shift, adj_head_y - int(50 * hair_len), 
                       cx + int(8 * hair_vol) + head_shift, adj_head_y], 
                      fill=hair_color, outline=c["hair_outline"])
        # Spikes on top
        for i in range(6):
            spike_x = cx - int(5 * hair_vol) + i * int(2 * hair_vol) + head_shift
            spike_h = int(15 * hair_len) + (i % 3) * int(10 * hair_len)
            draw.line([spike_x, adj_head_y - int(40 * hair_len), spike_x, adj_head_y - int(40 * hair_len) - spike_h], 
                     fill=hair_color, width=3)
        # Shaved sides texture
        for i in range(5):
            sx = cx - int(15 * hair_vol) + i * int(8 * hair_vol) + head_shift
            draw.arc([sx-2, adj_head_y-2, sx+2, adj_head_y+2], 0, 180, fill=hair_dark, width=1)
    elif hair_style == "afro":
        # Massive volume
        for i in range(3):
            offset = i * 2
            alpha = 255 - i * 30
            layer_color = tuple(list(hair_color[:3]) + [alpha])
            draw.ellipse([cx - int(55 * hair_vol) + head_shift - offset, adj_head_y - int(30 * hair_len) - offset,
                         cx + int(55 * hair_vol) + head_shift + offset, adj_head_y + int(25 * hair_len) + offset], 
                        fill=layer_color, outline=c["hair_outline"], width=2)
        # Texture curls
        for i in range(20):
            curl_x = cx - int(45 * hair_vol) + random.randint(0, int(90 * hair_vol)) + head_shift
            curl_y = adj_head_y - int(25 * hair_len) + random.randint(0, int(50 * hair_len))
            draw.arc([curl_x-4, curl_y-4, curl_x+4, curl_y+4], 0, random.randint(180, 360), fill=hair_dark, width=2)
    elif hair_style == "ponytail":
        draw.ellipse([cx - int(42 * hair_vol) + head_shift, adj_head_y - 6, cx + int(42 * hair_vol) + head_shift, adj_head_y + int(20 * hair_len)], 
                    fill=hair_color, outline=c["hair_outline"], width=1)
        # Ponytail base
        draw.line([cx + int(20 * hair_vol) + head_shift, adj_head_y + int(10 * hair_len), 
                  cx + int(25 * hair_vol) + head_shift, adj_head_y + int(60 * hair_len)], 
                 fill=hair_color, width=int(12 * hair_vol))
        # Ponytail highlight
        draw.line([cx + int(18 * hair_vol) + head_shift, adj_head_y + int(12 * hair_len), 
                  cx + int(20 * hair_vol) + head_shift, adj_head_y + int(55 * hair_len)], 
                 fill=hair_light, width=int(4 * hair_vol))
        # Hair tie
        draw.ellipse([cx + int(17 * hair_vol) + head_shift, adj_head_y + int(8 * hair_len),
                     cx + int(23 * hair_vol) + head_shift, adj_head_y + int(14 * hair_len)], 
                    fill=(255, 100, 150, 255), outline=(200, 70, 100, 255))
        # Ponytail end
        draw.ellipse([cx + int(18 * hair_vol) + head_shift, adj_head_y + int(55 * hair_len), 
                     cx + int(32 * hair_vol) + head_shift, adj_head_y + int(70 * hair_len)], 
                    fill=hair_color, outline=c["hair_outline"])
    elif hair_style == "buzzcut":
        # Very short uniform length
        draw.ellipse([cx - int(40 * hair_vol) + head_shift, adj_head_y - 4, 
                     cx + int(40 * hair_vol) + head_shift, adj_head_y + int(5 * hair_len)], 
                    fill=hair_color, outline=c["hair_outline"], width=1)
        # Tiny hair dots
        for i in range(15):
            dx = cx - int(35 * hair_vol) + random.randint(0, int(70 * hair_vol)) + head_shift
            dy = adj_head_y - 2 + random.randint(0, int(5 * hair_len))
            draw.ellipse([dx-1, dy-1, dx+1, dy+1], fill=hair_dark)
    elif hair_style == "custom" and hair_cfg.get("custom_points"):
        pts = [(cx + p[0] + head_shift, adj_head_y + p[1]) for p in hair_cfg["custom_points"]]
        if len(pts) >= 3:
            # Shadow
            shadow_pts = [(x+2, y+2) for x, y in pts]
            draw.polygon(shadow_pts, fill=(0, 0, 0, 60))
            draw.polygon(pts, fill=hair_color, outline=c["hair_outline"], width=1)
            # Highlight
            draw.polygon(pts, fill=hair_light)
    else:
        draw.ellipse([cx - int(44 * hair_vol) + head_shift - 1, adj_head_y - 5, 
                     cx + int(44 * hair_vol) + head_shift + 1, adj_head_y + int(30 * hair_len) + 1], 
                    fill=(0, 0, 0, 40))
        draw.ellipse([cx - int(44 * hair_vol) + head_shift, adj_head_y - 6, 
                     cx + int(44 * hair_vol) + head_shift, adj_head_y + int(30 * hair_len)], 
                    fill=hair_color, outline=c["hair_outline"], width=1)
        # Top highlight
        draw.ellipse([cx - int(25 * hair_vol) + head_shift, adj_head_y - 3, 
                     cx + int(10 * hair_vol) + head_shift, adj_head_y + int(15 * hair_len)], 
                    fill=hair_light)


# ============================================
# EAR STYLE DRAWING
# ============================================

def draw_ear_style(renderer, draw, c, body_color, body_outline_color, ear_style, ear_size, cx, ear_y, head_shift):
    """Draw ear style with detailed inner shading"""
    ear_dark = tuple(max(0, c - 30) for c in body_color[:3]) + (body_color[3],)
    ear_light = tuple(min(255, c + 30) for c in body_color[:3]) + (body_color[3],)
    
    if ear_style == "pointy":
        for es in [-1, 1]:
            tip_x = cx - int(18 * ear_size) * es + head_shift
            tip_y = ear_y - int(60 * ear_size)
            # Shadow
            draw.line([cx - int(24 * ear_size) * es + head_shift + 1, ear_y + 1, tip_x + 1, tip_y + 1], 
                     fill=(0, 0, 0, 40), width=int(16 * ear_size))
            # Main ear
            draw.line([cx - int(24 * ear_size) * es + head_shift, ear_y, tip_x, tip_y], 
                     fill=body_outline_color, width=int(14 * ear_size))
            draw.line([cx - int(24 * ear_size) * es + head_shift, ear_y, tip_x, tip_y], 
                     fill=body_color, width=int(9 * ear_size))
            # Highlight
            draw.line([cx - int(22 * ear_size) * es + head_shift, ear_y-2, tip_x-2, tip_y-2], 
                     fill=ear_light, width=int(4 * ear_size))
            # Tip point
            draw.polygon([(tip_x-3, tip_y), (tip_x+3, tip_y), (tip_x, tip_y-10)], fill=body_color, outline=body_outline_color)
    elif ear_style == "cat":
        for es in [-1, 1]:
            tip_x = cx - int(18 * ear_size) * es + head_shift
            tip_y = ear_y - int(55 * ear_size)
            # Outer ear shadow
            draw.polygon([(cx - int(28 * ear_size) * es + head_shift + 1, ear_y + 1), 
                         (tip_x + 1, tip_y + 1), 
                         (cx - int(10 * ear_size) * es + head_shift + 1, ear_y + 1)], 
                        fill=(0, 0, 0, 40))
            # Outer ear
            draw.polygon([(cx - int(28 * ear_size) * es + head_shift, ear_y), 
                         (tip_x, tip_y), 
                         (cx - int(10 * ear_size) * es + head_shift, ear_y)], 
                        fill=body_color, outline=body_outline_color, width=2)
            # Inner ear
            draw.polygon([(cx - int(24 * ear_size) * es + head_shift, ear_y - 3), 
                         (tip_x, tip_y + 10), 
                         (cx - int(14 * ear_size) * es + head_shift, ear_y - 3)], 
                        fill=c["ears_inner"], outline=None)
            # Inner ear highlight
            draw.polygon([(cx - int(22 * ear_size) * es + head_shift, ear_y - 1), 
                         (tip_x-2, tip_y + 6), 
                         (cx - int(16 * ear_size) * es + head_shift, ear_y - 1)], 
                        fill=(255, 200, 220, 150))
    elif ear_style == "elf":
        for es in [-1, 1]:
            tip_x = cx - int(15 * ear_size) * es + head_shift
            tip_y = ear_y - int(70 * ear_size)
            # Long elegant ear
            draw.line([cx - int(22 * ear_size) * es + head_shift, ear_y, tip_x, tip_y], 
                     fill=c["skin_outline"], width=int(12 * ear_size))
            draw.line([cx - int(22 * ear_size) * es + head_shift, ear_y, tip_x, tip_y], 
                     fill=c["skin"], width=int(7 * ear_size))
            # Ear ridge highlight
            draw.line([cx - int(21 * ear_size) * es + head_shift, ear_y-1, tip_x-1, tip_y-1], 
                     fill=(255, 240, 210, 150), width=int(2 * ear_size))
            # Pointed tip
            draw.ellipse([tip_x-5, tip_y-3, tip_x+5, tip_y+3], fill=c["skin"], outline=c["skin_outline"])
            draw.ellipse([tip_x-2, tip_y-1, tip_x+2, tip_y+1], fill=(255, 255, 255, 150))
    elif ear_style == "demon":
        for es in [-1, 1]:
            tip_x = cx - int(15 * ear_size) * es + head_shift
            tip_y = ear_y - int(65 * ear_size)
            # Spiky demon ear
            draw.polygon([(cx - int(22 * ear_size) * es + head_shift, ear_y), 
                         (tip_x, tip_y), 
                         (cx - int(8 * ear_size) * es + head_shift, ear_y + 5)], 
                        fill=(180, 30, 30, 255), outline=(120, 15, 15, 255), width=2)
            # Inner glow
            draw.polygon([(cx - int(20 * ear_size) * es + head_shift, ear_y), 
                         (tip_x-1, tip_y + 5), 
                         (cx - int(10 * ear_size) * es + head_shift, ear_y + 3)], 
                        fill=(255, 60, 60, 100))
    elif ear_style == "mouse":
        for es in [-1, 1]:
            # Large round mouse ear
            draw.ellipse([cx - int(37 * ear_size) * es + head_shift - 1, ear_y - int(52 * ear_size) - 1,
                         cx - int(8 * ear_size) * es + head_shift + 1, ear_y + int(7 * ear_size) + 1], 
                        fill=(0, 0, 0, 40))
            draw.ellipse([cx - int(35 * ear_size) * es + head_shift, ear_y - int(50 * ear_size), 
                         cx - int(10 * ear_size) * es + head_shift, ear_y + int(5 * ear_size)], 
                        fill=c["skin"], outline=c["skin_outline"], width=2)
            # Inner ear pink
            draw.ellipse([cx - int(30 * ear_size) * es + head_shift, ear_y - int(42 * ear_size), 
                         cx - int(15 * ear_size) * es + head_shift, ear_y - int(2 * ear_size)], 
                        fill=c["ears_inner"], outline=None)
            # Vein lines
            for v in range(3):
                vx = cx - int(28 * ear_size) * es + head_shift + v * int(4 * ear_size)
                vy = ear_y - int(38 * ear_size) + v * int(8 * ear_size)
                draw.arc([vx-1, vy-2, vx+1, vy+2], 0, 180, fill=(255, 200, 220, 100), width=1)
    else:
        for es in [-1, 1]:
            tip_x = cx - int(18 * ear_size) * es + head_shift
            tip_y = ear_y - int(50 * ear_size)
            # Default round ear
            draw.line([cx - int(24 * ear_size) * es + head_shift + 1, ear_y + 1, tip_x + 1, tip_y + 1], 
                     fill=(0, 0, 0, 30), width=int(16 * ear_size))
            draw.line([cx - int(24 * ear_size) * es + head_shift, ear_y, tip_x, tip_y], 
                     fill=body_outline_color, width=int(14 * ear_size))
            draw.line([cx - int(24 * ear_size) * es + head_shift, ear_y, tip_x, tip_y], 
                     fill=body_color, width=int(9 * ear_size))
            # Ear lobe
            draw.ellipse([tip_x - 7, tip_y - 5, tip_x + 7, tip_y + 5], fill=body_color, outline=body_outline_color)
            # Lobe highlight
            draw.ellipse([tip_x - 4, tip_y - 3, tip_x + 2, tip_y + 3], fill=ear_light)