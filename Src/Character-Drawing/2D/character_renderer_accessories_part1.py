"""
MEMEBOT 2D Character Renderer - Accessories Module Part 1
Speech bubble, Tail, Cape, Wings, Scarf, Outfit Details, Hats
Part 1 of 2
"""

import math
from PIL import ImageFont


def draw_speech_bubble(renderer, draw, cx, y):
    """Draw speech bubble with shadow and gradient"""
    bubble_x = cx + 30
    text_w = len(renderer.speech_text) * 8 + 20
    bubble_w = max(60, min(text_w, 200))
    bubble_h = 30
    
    draw.ellipse([bubble_x - bubble_w//2 + 3, y - bubble_h//2 + 3, 
                  bubble_x + bubble_w//2 + 3, y + bubble_h//2 + 3], fill=(0, 0, 0, 60))
    for i in range(3):
        offset = i * 2; alpha = 230 - i * 15
        draw.ellipse([bubble_x - bubble_w//2 + offset, y - bubble_h//2 + offset, 
                     bubble_x + bubble_w//2 - offset, y + bubble_h//2 - offset],
                    fill=(255, 255, 255, alpha), outline=(180, 180, 190, 255), width=1)
    draw.ellipse([bubble_x - bubble_w//2 + 8, y - bubble_h//2 + 4, 
                  bubble_x - bubble_w//2 + 20, y - bubble_h//2 + 12], fill=(255, 255, 255, 100))
    draw.polygon([(bubble_x - 13, y + bubble_h//2 + 3), (bubble_x - 23, y + bubble_h//2 + 18), 
                  (bubble_x - 3, y + bubble_h//2 + 3)], fill=(0, 0, 0, 40))
    draw.polygon([(bubble_x - 15, y + bubble_h//2), (bubble_x - 25, y + bubble_h//2 + 15), 
                  (bubble_x - 5, y + bubble_h//2)], fill=(255, 255, 255, 230), outline=(180, 180, 190, 255), width=1)
    try: font = ImageFont.truetype("arial.ttf", 12)
    except: font = ImageFont.load_default()
    draw.text((bubble_x - bubble_w//2 + 6, y - 7), renderer.speech_text[:30], fill=(0, 0, 0, 80), font=font)
    draw.text((bubble_x - bubble_w//2 + 5, y - 8), renderer.speech_text[:30], fill=(20, 20, 30, 255), font=font)


def draw_tail(renderer, draw, c, cx, hip_y, ground_y, tail_type):
    """Draw tail accessory with fur texture and shading"""
    colors = {
        "cat": (200, 150, 100, 255), "dog": (180, 140, 100, 255), "demon": (180, 30, 30, 255),
        "dragon": (30, 120, 30, 255), "fox": (255, 150, 50, 255), "rabbit": (255, 255, 255, 255),
        "mouse": (200, 180, 180, 255), "lizard": (50, 180, 50, 255), "devil": (200, 20, 20, 255),
        "robot": (150, 150, 160, 255),
    }
    color = colors.get(tail_type, (200, 150, 100, 255))
    dark_color = tuple(max(0, c - 40) for c in color[:3]) + (color[3],)
    light_color = tuple(min(255, c + 30) for c in color[:3]) + (color[3],)
    
    if tail_type == "cat":
        tail_sway = math.sin(renderer.dance_timer * 0.2) * 15
        for i in range(3):
            offset = i * 1.5
            draw.line([cx, hip_y, cx + 30 + tail_sway + offset, hip_y - 20], fill=dark_color, width=8 - i)
        draw.line([cx, hip_y, cx + 30 + tail_sway, hip_y - 20], fill=color, width=6)
        draw.line([cx + 30 + tail_sway, hip_y - 20, cx + 50 + tail_sway, hip_y - 40], fill=color, width=4)
        draw.line([cx + 50 + tail_sway, hip_y - 40, cx + 55 + tail_sway, hip_y - 55], fill=light_color, width=2)
        draw.ellipse([cx + 53 + tail_sway, hip_y - 58, cx + 57 + tail_sway, hip_y - 52], fill=(255, 255, 255, 100))
    elif tail_type == "dog":
        tail_wag = math.sin(renderer.dance_timer * 0.4) * 20
        draw.line([cx + 2, hip_y + 1, cx + 27 + tail_wag, hip_y - 29], fill=(0, 0, 0, 40), width=9)
        draw.line([cx, hip_y, cx + 25 + tail_wag, hip_y - 30], fill=color, width=7)
        draw.line([cx + 25 + tail_wag, hip_y - 30, cx + 28 + tail_wag, hip_y - 33], fill=light_color, width=3)
    elif tail_type == "demon":
        tail_sway = math.sin(renderer.dance_timer * 0.25) * 10
        for i in range(4):
            tx = cx + i * 12 + tail_sway * (i * 0.3); ty = hip_y - i * 10
            draw.polygon([(tx-5, ty-3), (tx+1, ty+7), (tx+5, ty-3)], fill=(0, 0, 0, 60))
            draw.polygon([(tx-4, ty-4), (tx, ty+6), (tx+4, ty-4)], fill=color, outline=(120, 15, 15, 255))
            draw.polygon([(tx-2, ty-2), (tx, ty+3), (tx+2, ty-2)], fill=(255, 80, 80, 100))
        draw.line([cx + 48 + tail_sway * 1.2, hip_y - 40, cx + 55 + tail_sway * 1.3, hip_y - 55], fill=color, width=2)
        draw.polygon([(cx + 52 + tail_sway, hip_y - 58), (cx + 55 + tail_sway, hip_y - 62), 
                      (cx + 58 + tail_sway, hip_y - 58)], fill=(200, 20, 20, 255), outline=(150, 10, 10, 255))
    elif tail_type == "fox":
        tail_sway = math.sin(renderer.dance_timer * 0.2) * 12
        draw.line([cx, hip_y, cx + 35 + tail_sway, hip_y - 30], fill=color, width=10)
        draw.ellipse([cx + 25 + tail_sway, hip_y - 45, cx + 55 + tail_sway, hip_y - 15], fill=(255, 255, 255, 220))
        for i in range(5):
            fx = cx + 10 + i * 6 + tail_sway * (i * 0.2); fy = hip_y - 8 - i * 6
            draw.arc([fx-4, fy-2, fx+4, fy+2], 0, 180, fill=light_color, width=1)
    elif tail_type == "rabbit":
        draw.ellipse([cx + 12, hip_y - 8, cx + 27, hip_y + 7], fill=(0, 0, 0, 30))
        draw.ellipse([cx + 10, hip_y - 10, cx + 25, hip_y + 5], fill=color, outline=(200, 200, 200, 255), width=1)
        for i in range(4):
            fx = cx + 13 + i * 3; fy = hip_y - 5 + math.sin(i) * 3
            draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=(255, 255, 255, 150))
    elif tail_type == "devil":
        tail_sway = math.sin(renderer.dance_timer * 0.3) * 10
        draw.line([cx + 1, hip_y + 1, cx + 41 + tail_sway, hip_y - 34], fill=(0, 0, 0, 50), width=7)
        draw.line([cx, hip_y, cx + 40 + tail_sway, hip_y - 35], fill=color, width=5)
        draw.polygon([(cx + 40 + tail_sway, hip_y - 35), (cx + 28 + tail_sway, hip_y - 52), 
                     (cx + 36 + tail_sway, hip_y - 48)], fill=(200, 20, 20, 255), outline=(150, 10, 10, 255))
        draw.polygon([(cx + 40 + tail_sway, hip_y - 35), (cx + 48 + tail_sway, hip_y - 52), 
                     (cx + 42 + tail_sway, hip_y - 48)], fill=(200, 20, 20, 255), outline=(150, 10, 10, 255))
    elif tail_type == "mouse":
        tail_sway = math.sin(renderer.dance_timer * 0.3) * 12
        draw.line([cx + 1, hip_y + 1, cx + 45 + tail_sway, hip_y - 25], fill=(0, 0, 0, 40), width=5)
        draw.line([cx, hip_y, cx + 45 + tail_sway, hip_y - 26], fill=color, width=3)
        for i in range(10):
            tx = cx + i * 5 + tail_sway * (i * 0.1); ty = hip_y - i * 2.5
            draw.ellipse([tx-1, ty-1, tx+1, ty+1], fill=dark_color)
    elif tail_type == "lizard":
        tail_sway = math.sin(renderer.dance_timer * 0.2) * 8
        for i in range(6):
            tx = cx + i * 8 + tail_sway * (i * 0.15); ty = hip_y - i * 5
            draw.ellipse([tx-5, ty-5, tx+5, ty+5], fill=color, outline=dark_color, width=1)
            draw.ellipse([tx-2, ty-2, tx+2, ty+2], fill=light_color)
        draw.line([cx + 48 + tail_sway, hip_y - 30, cx + 60 + tail_sway, hip_y - 40], fill=color, width=2)
    elif tail_type == "dragon":
        tail_sway = math.sin(renderer.dance_timer * 0.15) * 6
        for i in range(8):
            tx = cx + i * 7 + tail_sway * (i * 0.1); ty = hip_y - i * 4
            spike_size = 6 - i * 0.5
            draw.polygon([(tx-4, ty-4), (tx+4, ty-4), (tx, ty-4-spike_size)], fill=color, outline=dark_color, width=1)
        draw.polygon([(cx + 56, hip_y - 36), (cx + 64, hip_y - 44), (cx + 56, hip_y - 40)], fill=(255, 50, 50, 255), outline=dark_color)
    else:
        tail_sway = math.sin(renderer.dance_timer * 0.2) * 10
        draw.line([cx + 1, hip_y + 1, cx + 35 + tail_sway, hip_y - 20], fill=(0, 0, 0, 40), width=7)
        draw.line([cx, hip_y, cx + 35 + tail_sway, hip_y - 21], fill=color, width=5)
        draw.ellipse([cx + 32 + tail_sway, hip_y - 26, cx + 40 + tail_sway, hip_y - 16], fill=light_color)


def draw_cape(renderer, draw, c, cx, shoulder_y, hip_y, cape_type):
    """Draw cape accessory with fabric folds and shading"""
    colors = {"Red": (200, 30, 30, 200), "Blue": (30, 30, 200, 200), "Black": (30, 30, 30, 200),
              "Purple": (120, 30, 180, 200), "Green": (30, 150, 30, 200)}
    color = colors.get(cape_type, (200, 30, 30, 200))
    dark_color = tuple(max(0, c - 50) for c in color[:3]) + (color[3],)
    light_color = tuple(min(255, c + 40) for c in color[:3]) + (color[3],)
    cape_sway = math.sin(renderer.dance_timer * 0.15) * 8
    
    draw.polygon([(cx - 30, shoulder_y + 3), (cx + 30, shoulder_y + 3),
                 (cx + 42 + cape_sway, hip_y + 23), (cx - 38 - cape_sway, hip_y + 23)], fill=(0, 0, 0, 50))
    draw.polygon([(cx - 32, shoulder_y), (cx + 32, shoulder_y),
                 (cx + 40 + cape_sway, hip_y + 20), (cx - 40 - cape_sway, hip_y + 20)],
                fill=color, outline=(0, 0, 0, 100), width=1)
    for i in range(5):
        fold_x = cx - 20 + i * 10 + cape_sway * (i * 0.1)
        draw.line([(fold_x, shoulder_y + 5), (fold_x - 5 + cape_sway, hip_y + 10)], fill=dark_color, width=1)
    draw.line([(cx - 38 - cape_sway, hip_y + 18), (cx + 38 + cape_sway, hip_y + 18)], fill=light_color, width=2)
    draw.ellipse([cx-7, shoulder_y-5, cx+7, shoulder_y+7], fill=(255, 215, 0, 255), outline=(200, 160, 0, 255), width=2)
    draw.ellipse([cx-4, shoulder_y-2, cx+4, shoulder_y+4], fill=(255, 235, 100, 200))
    draw.ellipse([cx-3, shoulder_y-3, cx, shoulder_y], fill=(255, 255, 200, 150))


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
        wx = cx-40*side; wy = chest_y-20
        if wings_type == "Fairy":
            for i in range(4):
                offset = i * 2; alpha = 100 - i * 20
                draw.ellipse([wx-25+offset,wy-40+offset,wx+5-offset,wy+20-offset], 
                           fill=(255, 200, 255, alpha), outline=(200, 150, 200, 100), width=1)
            draw.ellipse([wx-25,wy-40,wx+5,wy+20], fill=color, outline=(200,150,200,100), width=1)
            for i in range(4):
                vx = wx - 15 + i * 5; vy = wy - 25 + i * 8
                draw.arc([vx-3, vy-5, vx+3, vy+5], 180, 360, fill=(255, 255, 255, 100), width=1)
            draw.ellipse([wx-15,wy-30,wx-5,wy+10], fill=(255,255,255,100), outline=None)
            for i in range(6):
                sx = wx - 20 + i * 5; sy = wy - 30 + i * 4
                draw.ellipse([sx-1, sy-1, sx+1, sy+1], fill=(255, 255, 255, 200))
        elif wings_type == "Bat":
            draw.polygon([(wx-3,wy-18),(wx-33,wy-38),(wx-23,wy-8),(wx-38,wy-8),
                         (wx-18,wy+7),(wx-33,wy+22),(wx-8,wy+7)], fill=(0, 0, 0, 60))
            draw.polygon([(wx-5,wy-20),(wx-35,wy-40),(wx-25,wy-10),(wx-40,wy-10),
                         (wx-20,wy+5),(wx-35,wy+20),(wx-10,wy+5)], fill=color, outline=(20,20,30,255), width=1)
            for bone in [(wx-5,wy-20,wx-30,wy-35), (wx-10,wy-10,wx-35,wy-5), (wx-8,wy+2,wx-28,wy+18)]:
                draw.line([bone[0], bone[1], bone[2], bone[3]], fill=dark_color, width=2)
        elif wings_type == "Mechanical":
            for i in range(3):
                wy2 = wy-20+i*15
                draw.rectangle([wx-32,wy2-5,wx+7,wy2+5], fill=(0, 0, 0, 40))
                draw.rectangle([wx-30,wy2-3,wx+5,wy2+3], fill=color, outline=(100,100,110,255), width=1)
                for rx in [wx-25, wx-15, wx-5]:
                    draw.ellipse([rx-2, wy2-2, rx+2, wy2+2], fill=(200, 200, 210, 255))
            draw.ellipse([wx-8,wy-13,wx+8,wy+13], fill=(180, 180, 190, 255), outline=(100,100,110,255), width=2)
            for j in range(6):
                gear_angle = j * (math.pi/3)
                gear_x = wx + int(8 * math.cos(gear_angle)); gear_y = wy + int(8 * math.sin(gear_angle))
                draw.rectangle([gear_x-2, gear_y-5, gear_x+2, gear_y+5], fill=(200, 200, 210, 255))
        else:
            for i in range(3):
                offset = i * 3; alpha = color[3] - i * 30
                layer_color = tuple(list(color[:3]) + [max(0, alpha)])
                draw.ellipse([wx-35+offset,wy-50+offset,wx+15-offset,wy+30-offset], 
                           fill=layer_color, outline=(0,0,0,100), width=2)
            for i in range(8):
                fx = wx - 25 + i * 4; fy = wy - 30 + i * 5
                draw.arc([fx-3, fy-8, fx+3, fy+8], 180, 360, fill=(255, 255, 255, 50), width=1)
            draw.ellipse([wx-25,wy-40,wx+5,wy+20], 
                        fill=(255,255,255,100) if wings_type=="Angel" else (0,0,0,50), outline=None)


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
    
    draw.ellipse([cx-18, neck_y-3, cx+22, neck_y+17], fill=(0, 0, 0, 40))
    for i in range(3):
        offset = i * 1.5
        draw.ellipse([cx-20+offset, neck_y-5+offset, cx+20-offset, neck_y+15-offset], 
                    fill=color if i == 1 else dark_color, outline=(0,0,0,100), width=1)
    draw.line([cx+17, neck_y+7, cx+27, shoulder_y+12], fill=(0, 0, 0, 50), width=8)
    draw.line([cx+15, neck_y+5, cx+25, shoulder_y+10], fill=color, width=6)
    for i in range(5):
        ky = neck_y - 2 + i * 3.5
        draw.arc([cx-16, ky-1, cx+16, ky+1], 0, 180, fill=dark_color, width=1)
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


def draw_outfit_details(draw, c, cx, shoulder_y, chest_y, hip_y, neck_y, outfit_type, body_color, body_outline_color):
    """Draw outfit-specific details with enhanced textures and shadows"""
    if outfit_type == "suit" or outfit_type == "tuxedo":
        draw.polygon([(cx-3, neck_y+7), (cx+5, neck_y+7), (cx+7, chest_y+7), (cx-5, chest_y+7)], fill=(0, 0, 0, 50))
        tie_top = neck_y + 5; tie_bottom = chest_y + 5
        draw.polygon([(cx-4, tie_top), (cx+4, tie_top), (cx+6, tie_bottom), (cx-6, tie_bottom)], fill=(180, 30, 30, 255), outline=(140, 20, 20, 255), width=1)
        draw.polygon([(cx-2, tie_top+2), (cx+2, tie_top+2), (cx+3, tie_bottom-2), (cx-3, tie_bottom-2)], fill=(220, 60, 60, 150))
        draw.polygon([(cx-15, neck_y), (cx, neck_y+15), (cx+15, neck_y)], fill=(255, 255, 255, 200), outline=body_outline_color, width=1)
        draw.line([(cx-14, neck_y+2), (cx-1, neck_y+13)], fill=(200, 200, 200, 100), width=1)
        draw.line([(cx+14, neck_y+2), (cx+1, neck_y+13)], fill=(200, 200, 200, 100), width=1)
        for i in range(3):
            by = chest_y - 10 + i * 15
            draw.ellipse([cx-4, by-3, cx+4, by+3], fill=(0, 0, 0, 50))
            draw.ellipse([cx-3, by-2, cx+3, by+2], fill=(80, 80, 80, 255))
            draw.ellipse([cx-2, by-1, cx+2, by+1], fill=(200, 200, 200, 255))
            draw.ellipse([cx-1, by-1, cx+1, by], fill=(255, 255, 255, 150))
    elif outfit_type == "armor":
        for i in range(3):
            py = chest_y - 15 + i * 18
            draw.ellipse([cx-18, py-3, cx+22, py+12], fill=(0, 0, 0, 50))
            draw.ellipse([cx-20, py-5, cx+20, py+10], fill=(200, 200, 220, 100), outline=body_outline_color, width=2)
            draw.ellipse([cx-15, py, cx-11, py+4], fill=(180, 180, 200, 255))
            draw.ellipse([cx+11, py, cx+15, py+4], fill=(180, 180, 200, 255))
        for side in [-1, 1]:
            draw.ellipse([cx-36*side, shoulder_y-3, cx-20*side, shoulder_y+17], fill=(0, 0, 0, 50))
            draw.ellipse([cx-38*side, shoulder_y-5, cx-22*side, shoulder_y+15], fill=(180, 180, 200, 255), outline=body_outline_color, width=2)
            draw.arc([cx-34*side, shoulder_y-2, cx-26*side, shoulder_y+8], 180, 360, fill=(220, 220, 240, 150), width=3)
        draw.rectangle([cx-28, hip_y-8, cx+28, hip_y+2], fill=(100, 80, 40, 255), outline=body_outline_color, width=1)
        draw.line([cx-26, hip_y-6, cx+26, hip_y-6], fill=(150, 130, 80, 100), width=1)
        draw.rectangle([cx-7, hip_y-12, cx+7, hip_y+6], fill=(0, 0, 0, 50))
        draw.rectangle([cx-5, hip_y-10, cx+5, hip_y+4], fill=(200, 180, 40, 255), outline=(150, 130, 30, 255), width=2)
        draw.rectangle([cx-3, hip_y-8, cx+3, hip_y+2], fill=(255, 220, 80, 200))
    elif outfit_type == "military":
        for side in [-1, 1]:
            draw.rectangle([cx-20*side, chest_y-6, cx-8*side, chest_y+10], fill=(0, 0, 0, 50))
            draw.rectangle([cx-22*side, chest_y-8, cx-10*side, chest_y+8], fill=(70, 90, 50, 255), outline=body_outline_color, width=1)
            draw.polygon([(cx-22*side, chest_y-4), (cx-10*side, chest_y-4), (cx-12*side, chest_y), (cx-20*side, chest_y)], fill=(80, 100, 60, 255), outline=body_outline_color, width=1)
            draw.ellipse([cx-17*side, chest_y+2, cx-15*side, chest_y+6], fill=(150, 150, 50, 255))
        draw.rectangle([cx-28, hip_y-8, cx+28, hip_y+2], fill=(80, 60, 30, 255), outline=body_outline_color, width=1)
        draw.rectangle([cx-7, hip_y-12, cx+7, hip_y+6], fill=(0, 0, 0, 40))
        draw.rectangle([cx-5, hip_y-10, cx+5, hip_y+4], fill=(150, 150, 50, 255), outline=(120, 120, 30, 255), width=2)
        for i in range(2):
            mx = cx - 5 + i * 15
            draw.rectangle([mx-4, chest_y-6, mx+4, chest_y-2], fill=(200, 50, 50, 255), outline=(150, 30, 30, 255))
            draw.rectangle([mx-3, chest_y-4, mx+3, chest_y+8], fill=(200, 50, 50, 255), outline=(150, 30, 30, 255))
            draw.ellipse([mx-2, chest_y-3, mx+2, chest_y+1], fill=(255, 200, 200, 100))
    elif outfit_type == "cyberpunk":
        for i in range(4):
            ly = chest_y - 12 + i * 15
            draw.line([cx-16, ly, cx+16, ly], fill=(0, 0, 0, 60), width=3)
            draw.line([cx-18, ly, cx+18, ly], fill=(0, 255, 200, 150), width=2)
            draw.line([cx-18, ly, cx+18, ly], fill=(0, 255, 200, 50), width=6)
            for nx in [cx-16, cx, cx+16]:
                draw.ellipse([nx-3, ly-3, nx+3, ly+3], fill=(0, 255, 200, 200))
                draw.ellipse([nx-1, ly-1, nx+1, ly+1], fill=(255, 255, 255, 200))
        draw.rectangle([cx-14, chest_y-7, cx-6, chest_y+7], fill=(0, 0, 0, 50))
        draw.rectangle([cx-12, chest_y-5, cx-6, chest_y+5], fill=(0, 255, 200, 100), outline=(0, 255, 200, 200), width=1)
        draw.rectangle([cx+6, chest_y-7, cx+14, chest_y+7], fill=(0, 0, 0, 50))
        draw.rectangle([cx+6, chest_y-5, cx+12, chest_y+5], fill=(0, 255, 200, 100), outline=(0, 255, 200, 200), width=1)
        for i in range(3):
            dx = cx - 8 + i * 8
            draw.line([dx, chest_y-4, dx+2, chest_y+4], fill=(0, 255, 200, 80), width=1)