#!/usr/bin/env python3
"""
Reusable Slide Templates Engine for Finance Reel Factory.
Provides 6 standardized viral reel layouts:
1. Hook Layout (Meme/Host + Punchy text)
2. Comparison Layout (Option A vs Option B)
3. Stat / Metric Layout (Big numbers + calculation)
4. Alert / Warning Layout (Drawdown / Tax trap)
5. Tier List Layout (Capital brackets / category maps)
6. Outro / CTA Layout (Follow badge + disclaimer)
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Brand Colors
BG_COLOR = (244, 235, 221)       # #F4EBDD Warm Cream
TEXT_DARK = (26, 26, 26)         # #1A1A1A Deep Charcoal
TEXT_MUTED = (110, 110, 110)     # Gray
GREEN_ACCENT = (22, 163, 74)     # Bullish / SIP Green
RED_ACCENT = (220, 38, 38)       # Risk / Alert Red
BLUE_ACCENT = (37, 99, 235)      # FD / DICGC Blue
PURPLE_ACCENT = (147, 51, 234)   # HNI Purple
CARD_BG = (255, 255, 255)        # Pure White

try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_FILTER = getattr(Image, 'LANCZOS', getattr(Image, 'ANTIALIAS', 1))

def get_font(size, bold=False):
    font_candidates = [
        f"{BASE_DIR}/fonts/NotoSans-Bold.ttf" if bold else f"{BASE_DIR}/fonts/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/system/fonts/Roboto-Bold.ttf" if bold else "/system/fonts/Roboto-Regular.ttf"
    ]
    for p in font_candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

def create_base_canvas():
    return Image.new("RGB", (1080, 1920), BG_COLOR)

def draw_header(draw, title, category="FINANCE REALITY CHECK"):
    # Pill
    pill_w, pill_h = 700, 70
    pill_x = (1080 - pill_w) // 2
    draw.rounded_rectangle([pill_x, 90, pill_x + pill_w, 160], radius=35, fill=TEXT_DARK)
    draw.text((540, 125), category, fill=(255, 255, 255), anchor="mm", font=get_font(26, bold=True))
    
    # Title
    lines = title.split("\n")
    y = 200
    for line in lines:
        draw.text((540, y), line, fill=TEXT_DARK, anchor="mm", font=get_font(46, bold=True))
        y += 60

def paste_centered_image(img, image_path, center_y, max_w=500, max_h=500):
    if not image_path or not os.path.exists(image_path):
        return
    try:
        with Image.open(image_path) as overlay:
            overlay = overlay.convert("RGBA")
            overlay.thumbnail((max_w, max_h), RESAMPLE_FILTER)
            w, h = overlay.size
            img.paste(overlay, ((1080 - w) // 2, center_y - (h // 2)), overlay)
    except Exception as e:
        print(f"Notice: Overlay note: {e}")

# ==============================================================================
# 6 REUSABLE SLIDE TEMPLATES
# ==============================================================================

def template_hook(tag, title, body_text, image_path=None):
    """Template 1: High engagement Hook layout"""
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, title, tag)
    
    img_path = image_path or f"{BASE_DIR}/BRAND/main_cat.png"
    paste_centered_image(img, img_path, center_y=750, max_w=520, max_h=520)
    
    d.rounded_rectangle([90, 1150, 990, 1650], radius=30, fill=CARD_BG, outline=TEXT_DARK, width=4)
    y = 1260
    for line in body_text.split("\n"):
        d.text((540, y), line, fill=TEXT_DARK, anchor="mm", font=get_font(34, bold=True))
        y += 60
    return img

def template_comparison(tag, title, opt_a_name, opt_a_rows, opt_b_name, opt_b_rows):
    """Template 2: Split comparison (e.g. SIP vs Lump Sum, FD vs Debt MFs)"""
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, title, tag)
    
    # Card A (e.g. Option A - Green)
    d.rounded_rectangle([90, 420, 990, 980], radius=25, fill=CARD_BG, outline=GREEN_ACCENT, width=4)
    d.text((140, 480), opt_a_name, fill=GREEN_ACCENT, font=get_font(36, bold=True))
    y = 560
    for label, val in opt_a_rows:
        d.text((140, y), f"• {label}: ", fill=TEXT_MUTED, font=get_font(26, bold=False))
        d.text((450, y), val, fill=TEXT_DARK, font=get_font(28, bold=True))
        y += 65
        
    # Card B (e.g. Option B - Blue/Red)
    d.rounded_rectangle([90, 1060, 990, 1680], radius=25, fill=CARD_BG, outline=BLUE_ACCENT, width=4)
    d.text((140, 1120), opt_b_name, fill=BLUE_ACCENT, font=get_font(36, bold=True))
    y = 1200
    for label, val in opt_b_rows:
        d.text((140, y), f"• {label}: ", fill=TEXT_MUTED, font=get_font(26, bold=False))
        d.text((450, y), val, fill=TEXT_DARK, font=get_font(28, bold=True))
        y += 65
    return img

def template_stat(tag, title, main_stat, subtitle, rows, accent_color=GREEN_ACCENT):
    """Template 3: Metric & Math Breakdown (e.g. 14% CAGR or Negative Real Return)"""
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, title, tag)
    
    d.rounded_rectangle([90, 420, 990, 1680], radius=30, fill=CARD_BG, outline=accent_color, width=4)
    d.text((540, 520), main_stat, fill=accent_color, anchor="mm", font=get_font(64, bold=True))
    d.text((540, 600), subtitle, fill=TEXT_MUTED, anchor="mm", font=get_font(26, bold=False))
    
    # Divider
    d.line([(140, 660), (940, 660)], fill=(220, 220, 220), width=2)
    
    y = 730
    for lbl, val in rows:
        d.text((150, y), lbl, fill=TEXT_MUTED, font=get_font(28, bold=False))
        y += 45
        d.text((150, y), val, fill=TEXT_DARK, font=get_font(38, bold=True))
        y += 90
    return img

def template_alert(tag, title, alert_headline, alert_body, reaction_image=None):
    """Template 4: Critical Risk / Reality Check Alert"""
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, title, tag)
    
    img_path = reaction_image or f"{BASE_DIR}/PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/shocked_cat.png"
    paste_centered_image(img, img_path, center_y=720, max_w=480, max_h=480)
    
    d.rounded_rectangle([90, 1100, 990, 1680], radius=30, fill=CARD_BG, outline=RED_ACCENT, width=5)
    d.text((540, 1180), alert_headline, fill=RED_ACCENT, anchor="mm", font=get_font(38, bold=True))
    
    y = 1280
    for line in alert_body.split("\n"):
        d.text((540, y), line, fill=TEXT_DARK, anchor="mm", font=get_font(30, bold=True))
        y += 55
    return img

def template_tier_list(tag, title, tier_name, tier_color, items):
    """Template 5: Multi-item Capital Map / Ranking list"""
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, title, tag)
    
    d.rounded_rectangle([80, 420, 1000, 1720], radius=30, fill=CARD_BG, outline=tier_color, width=4)
    d.text((540, 490), tier_name, fill=tier_color, anchor="mm", font=get_font(34, bold=True))
    
    y = 570
    for name, capital, note in items:
        d.text((120, y), f"{name}  ➔  {capital}", fill=TEXT_DARK, font=get_font(28, bold=True))
        y += 40
        d.text((150, y), f"({note})", fill=TEXT_MUTED, font=get_font(20, bold=False))
        y += 75
    return img

def template_outro(tag, title, cta_headline, upcoming_list, disclaimer):
    """Template 6: Follow CTA and Next Reel teasers"""
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, title, tag)
    
    paste_centered_image(img, f"{BASE_DIR}/BRAND/main_cat.png", center_y=600, max_w=420, max_h=420)
    
    # CTA button
    btn_box = [190, 880, 890, 1000]
    d.rounded_rectangle(btn_box, radius=35, fill=RED_ACCENT)
    d.text((540, 940), cta_headline, fill=(255, 255, 255), anchor="mm", font=get_font(42, bold=True))
    
    # Upcoming box
    d.rounded_rectangle([100, 1080, 980, 1500], radius=25, fill=CARD_BG, outline=TEXT_DARK, width=3)
    d.text((140, 1130), "NEXT IN SERIES:", fill=GREEN_ACCENT, font=get_font(24, bold=True))
    y = 1190
    for up in upcoming_list:
        d.text((140, y), f"• {up}", fill=TEXT_DARK, font=get_font(26, bold=True))
        y += 65
        
    y_disc = 1580
    for line in disclaimer.split("\n"):
        d.text((540, y_disc), line, fill=TEXT_MUTED, anchor="mm", font=get_font(22, bold=False))
        y_disc += 40
    return img
