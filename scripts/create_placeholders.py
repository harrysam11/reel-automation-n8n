#!/usr/bin/env python3
"""Generate placeholder images for brand mascot and reaction assets."""
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(path, width, height, text, bg_color=(235, 230, 220), fg_color=(40, 40, 40)):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new("RGBA", (width, height), bg_color + (255,))
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([4, 4, width - 4, height - 4], outline=(180, 170, 150), width=4)
    
    # Text overlay
    bbox = draw.textbbox((0, 0), text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(((width - text_w) // 2, (height - text_h) // 2), text, fill=fg_color)
    
    img.save(path)
    print(f"Created: {path}")

if __name__ == "__main__":
    create_placeholder("BRAND/main_cat.png", 600, 600, "🕶️ [PLACEHOLDER]\nSUNGLASSES CAT\n(Drop original mascot here)")
    create_placeholder("BRAND/logo.png", 400, 150, "FINANCE REEL FACTORY\n[LOGO]")
    
    reactions = [
        ("PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/smug_cat.png", "😼 [SMUG CAT]"),
        ("PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/shocked_cat.png", "🙀 [SHOCKED CAT]"),
        ("PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/thinking_cat.png", "🐱 [THINKING CAT]"),
    ]
    for p, t in reactions:
        create_placeholder(p, 500, 500, t)
