#!/usr/bin/env python3
"""
Native Slide Renderer for Raw Termux & PC (Zero LibreOffice dependency).
Renders crisp 1080x1920 vertical slide images directly using Pillow.
100% compatible with Android Termux (ARM64) and Linux (x86_64).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Visual Colors (from brand guide)
BG_COLOR = (244, 235, 221)       # #F4EBDD Warm Cream
TEXT_DARK = (26, 26, 26)         # #1A1A1A Charcoal
TEXT_MUTED = (110, 110, 110)     # Gray
GREEN_ACCENT = (22, 163, 74)     # #16A34A Bullish Green
RED_ACCENT = (220, 38, 38)       # #DC2626 Risk Red
BLUE_ACCENT = (37, 99, 235)      # #2563EB Security Blue
PURPLE_ACCENT = (147, 51, 234)   # HNI Purple
CARD_BG = (255, 255, 255)        # Pure White
CARD_BORDER = (210, 200, 185)    # Border

def get_font(size, bold=False):
    """Find available fonts across Linux and Termux."""
    font_candidates = [
        # Linux host noto fonts
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoSans-Bold.ttf" if bold else "/usr/share/fonts/opentype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        # Android / Termux system fonts
        "/system/fonts/Roboto-Bold.ttf" if bold else "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/NotoSansDevanagari-Bold.ttf" if bold else "/system/fonts/NotoSansDevanagari-Regular.ttf",
        f"{BASE_DIR}/fonts/NotoSans-Bold.ttf" if bold else f"{BASE_DIR}/fonts/NotoSans-Regular.ttf"
    ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_header(draw, title, category="FINANCE REALITY CHECK"):
    # Header tag pill
    pill_w, pill_h = 700, 70
    pill_x = (1080 - pill_w) // 2
    pill_y = 90
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=35, fill=TEXT_DARK)
    
    font_pill = get_font(26, bold=True)
    draw.text((540, pill_y + 35), category, fill=(255, 255, 255), anchor="mm", font=font_pill)
    
    # Title text
    font_title = get_font(46, bold=True)
    lines = title.split("\n")
    y_start = 200
    for line in lines:
        draw.text((540, y_start), line, fill=TEXT_DARK, anchor="mm", font=font_title)
        y_start += 60

def paste_centered_image(img, image_path, center_y, max_width=500, max_height=500):
    if not os.path.exists(image_path):
        return
    try:
        with Image.open(image_path) as overlay:
            overlay = overlay.convert("RGBA")
            overlay.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            w, h = overlay.size
            pos = ((1080 - w) // 2, center_y - (h // 2))
            img.paste(overlay, pos, overlay)
    except Exception as e:
        print(f"Notice: Image overlay note: {e}")

def create_base_canvas():
    return Image.new("RGB", (1080, 1920), BG_COLOR)

def render_slide_1(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "SIP ya FD?\n95-Sec Reality Check!", "🚨 CRITICAL MONEY DECISION")
    
    paste_centered_image(img, f"{BASE_DIR}/BRAND/main_cat.png", center_y=750, max_width=550, max_height=550)
    
    # Bottom Card
    card_box = [90, 1150, 990, 1650]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=TEXT_DARK, width=4)
    font_card = get_font(34, bold=True)
    text = "Agar aap SIP ya FD kar rahe ho,\ntoh yeh 95 seconds\naapke hazaron bacha sakte hain!"
    y = 1280
    for line in text.split("\n"):
        d.text((540, y), line, fill=TEXT_DARK, anchor="mm", font=font_card)
        y += 60
    img.save(out_path)

def render_slide_2(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "Bank me paisa safe hai?\nYa sirf illusion?", "THE BIG QUESTION")
    
    paste_centered_image(img, f"{BASE_DIR}/PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/smug_cat.png", center_y=750, max_width=500, max_height=500)
    
    card_box = [90, 1150, 990, 1650]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=TEXT_DARK, width=4)
    font_card = get_font(32, bold=True)
    text = "Sab kehte hain FD 100% safe hai...\n\nLekin kya aapne Inflation aur\nTax calculate kiya hai?"
    y = 1280
    for line in text.split("\n"):
        d.text((540, y), line, fill=TEXT_DARK, anchor="mm", font=font_card)
        y += 60
    img.save(out_path)

def render_slide_3(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "SIP: Systematic Wealth Machine", "GROWTH ENGINE")
    
    card_box = [90, 420, 990, 1680]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=GREEN_ACCENT, width=5)
    
    items = [
        ("Monthly Investment", "₹1,000 / month"),
        ("Underlying Asset", "Top 500 Indian Companies"),
        ("Historical CAGR (10-15 Yrs)", "11% – 14%"),
        ("Secret Power", "Rupee Cost Averaging + Compounding")
    ]
    y = 520
    font_label = get_font(26, bold=False)
    font_val = get_font(36, bold=True)
    for title, val in items:
        d.text((140, y), title, fill=TEXT_MUTED, font=font_label)
        y += 45
        d.text((140, y), val, fill=GREEN_ACCENT, font=font_val)
        y += 100
    img.save(out_path)

def render_slide_4(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "SIP Risk: Market Crash Reality!", "REALITY CHECK #1")
    
    paste_centered_image(img, f"{BASE_DIR}/PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/shocked_cat.png", center_y=750, max_width=500, max_height=500)
    
    card_box = [90, 1150, 990, 1680]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=RED_ACCENT, width=5)
    font_card = get_font(30, bold=True)
    text = "SIP koi magic nahi hai!\nShort term me portfolio -20% se -30%\ntak RED ho sakta hai!\n\nRule: 5 saal se kam time ho\ntoh equity SIP mat karo!"
    y = 1250
    for line in text.split("\n"):
        d.text((540, y), line, fill=RED_ACCENT, anchor="mm", font=font_card)
        y += 55
    img.save(out_path)

def render_slide_5(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "Fixed Deposit (FD): Guaranteed?", "SECURITY ANALYSIS")
    
    card_box = [90, 420, 990, 1680]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=BLUE_ACCENT, width=5)
    
    items = [
        ("Nominal Bank Rate", "6.5% – 7.2% p.a."),
        ("Security Level", "High (Scheduled Commercial Banks)"),
        ("Liquidity", "Instant (Subject to 1% penalty)"),
        ("TDS Section", "Section 194A (Above ₹40k interest)")
    ]
    y = 520
    font_label = get_font(26, bold=False)
    font_val = get_font(36, bold=True)
    for title, val in items:
        d.text((140, y), title, fill=TEXT_MUTED, font=font_label)
        y += 45
        d.text((140, y), val, fill=BLUE_ACCENT, font=font_val)
        y += 100
    img.save(out_path)

def render_slide_6(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "The Real Return Trap\nFD Math Revealed", "SHOCKING TRUTH")
    
    card_box = [90, 420, 990, 1680]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=RED_ACCENT, width=5)
    
    calcs = [
        ("Bank FD Rate", "+ 7.0%", TEXT_DARK),
        ("30% Tax Slab", "- 2.1%", RED_ACCENT),
        ("Post-Tax In-Hand", "= 4.9%", TEXT_DARK),
        ("CPI Inflation", "- 5.5% to 6.0%", RED_ACCENT),
        ("YOUR REAL RETURN", "NEGATIVE (-0.6% to -1.1%)", RED_ACCENT)
    ]
    y = 500
    font_label = get_font(26, bold=False)
    font_val = get_font(38, bold=True)
    for lbl, val, color in calcs:
        d.text((140, y), lbl, fill=TEXT_MUTED, font=font_label)
        y += 45
        d.text((140, y), val, fill=color, font=font_val)
        y += 85
    img.save(out_path)

def render_slide_7(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "DICGC Insurance Limit:\nOnly ₹5 Lakh Covered!", "REGULATORY RULE")
    
    card_box = [90, 420, 990, 1680]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=BLUE_ACCENT, width=5)
    
    d.text((540, 520), "RBI Subsidiary: DICGC", fill=BLUE_ACCENT, anchor="mm", font=get_font(28, bold=True))
    d.text((540, 640), "MAXIMUM COVER:\n₹5,00,000", fill=RED_ACCENT, anchor="mm", font=get_font(48, bold=True))
    
    text = "Key Takeaway:\n\nChahe aapke bank account me\n₹50 Lakh pade hon...\n\nBank default hone par kanoon ke mutabik\nsirf ₹5 Lakh (Principal + Byaj) protected hain.\n\nIsliye paisa multiple scheduled banks me\ndiversify karein!"
    y = 860
    font_body = get_font(28, bold=True)
    for line in text.split("\n"):
        d.text((540, y), line, fill=TEXT_DARK, anchor="mm", font=font_body)
        y += 45
    img.save(out_path)

def render_slide_8(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "Capital Map: Tier 1\nEntry: ₹100 – ₹5,000", "INVESTMENT BLUEPRINT")
    
    card_box = [80, 420, 1000, 1720]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=GREEN_ACCENT, width=4)
    
    tier1 = [
        ("1. Mutual Funds", "₹100 – ₹500", "Micro SIPs on broad index"),
        ("2. ETFs", "~₹20 – ₹500", "1 unit NiftyBeES, GoldBeES"),
        ("3. Direct Stocks", "₹10 – ₹5,000+", "Single share on NSE/BSE"),
        ("4. PPF / EPF / SSY", "₹250 – ₹500/yr", "Guaranteed Sovereign backing"),
        ("5. NPS", "₹500 – ₹1,000", "Tier 1 retirement account"),
        ("6. Bank FDs / RDs", "₹100 – ₹1,000", "Short-term parking")
    ]
    y = 480
    font_name = get_font(28, bold=True)
    font_note = get_font(20, bold=False)
    for name, cap, note in tier1:
        d.text((120, y), f"{name}  ➔  {cap}", fill=TEXT_DARK, font=font_name)
        y += 40
        d.text((150, y), f"({note})", fill=TEXT_MUTED, font=font_note)
        y += 70
    img.save(out_path)

def render_slide_9(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "Capital Map: Tier 2\nEntry: ₹10,000 – ₹5 Lakh", "INVESTMENT BLUEPRINT")
    
    card_box = [80, 420, 1000, 1720]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=BLUE_ACCENT, width=4)
    
    tier2 = [
        ("7. Government Securities", "₹10,000", "RBI Retail Direct (T-bills & G-Sec)"),
        ("8. REITs / InvITs", "₹100 – ₹400/unit", "Commercial real estate yield"),
        ("9. Sovereign Gold Bonds", "~₹7,500 – ₹8,500+", "1g Gold issue + 2.5% annual payout"),
        ("10. Corporate Bonds / NCDs", "₹10,000 – ₹1,00,000", "Listed debentures on debt portals"),
        ("11. P2P / Invoice Investing", "₹5,000 – ₹50,000", "High yield alt debt (Higher risk)")
    ]
    y = 500
    font_name = get_font(28, bold=True)
    font_note = get_font(20, bold=False)
    for name, cap, note in tier2:
        d.text((120, y), f"{name}  ➔  {cap}", fill=TEXT_DARK, font=font_name)
        y += 40
        d.text((150, y), f"({note})", fill=TEXT_MUTED, font=font_note)
        y += 85
    img.save(out_path)

def render_slide_10(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "Capital Map: Tier 3\nEntry: ₹20 Lakh – ₹1 Crore+", "HNI / SPECIALIZED")
    
    card_box = [80, 420, 1000, 1720]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=PURPLE_ACCENT, width=4)
    
    tier3 = [
        ("12. Real Estate (Physical)", "₹20 Lakh – ₹1 Crore+", "Land / Residential / Commercial property"),
        ("13. PMS (Portfolio Mgmt)", "₹50 Lakh", "SEBI Statutory Minimum per individual"),
        ("14. AIF (Alternative Inv)", "₹1 Crore", "SEBI Statutory Minimum (PE/VC/Hedge)")
    ]
    y = 560
    font_name = get_font(30, bold=True)
    font_note = get_font(22, bold=False)
    for name, cap, note in tier3:
        d.text((120, y), f"{name}  ➔  {cap}", fill=TEXT_DARK, font=font_name)
        y += 45
        d.text((150, y), f"({note})", fill=TEXT_MUTED, font=font_note)
        y += 120
    img.save(out_path)

def render_slide_11(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "Coming Up in Next Reels!", "UPCOMING CONTENT")
    
    card_box = [80, 420, 1000, 1720]
    d.rounded_rectangle(card_box, radius=30, fill=CARD_BG, outline=TEXT_DARK, width=4)
    
    teasers = [
        ("Reel 02", "SIP vs Lump Sum: Which Wins in 2026?"),
        ("Reel 03", "FD vs Debt Mutual Funds: Tax Showdown"),
        ("Reel 04", "How Inflation Secretly Destroys Savings"),
        ("Reel 05", "Where to Invest Your First ₹1,000")
    ]
    y = 520
    for ep, title in teasers:
        d.text((130, y), ep, fill=GREEN_ACCENT, font=get_font(24, bold=True))
        y += 35
        d.text((130, y), title, fill=TEXT_DARK, font=get_font(32, bold=True))
        y += 110
    img.save(out_path)

def render_slide_12(out_path):
    img = create_base_canvas()
    d = ImageDraw.Draw(img)
    draw_header(d, "Become a Financially\nSmart Investor!", "JOIN THE COMMUNITY")
    
    paste_centered_image(img, f"{BASE_DIR}/BRAND/main_cat.png", center_y=750, max_width=500, max_height=500)
    
    # CTA button
    btn_box = [190, 1150, 890, 1300]
    d.rounded_rectangle(btn_box, radius=40, fill=RED_ACCENT)
    d.text((540, 1225), "👉 TAP FOLLOW", fill=(255, 255, 255), anchor="mm", font=get_font(44, bold=True))
    
    # Disclaimer
    disclaimer = "Disclaimer: For educational purposes only.\nSecurities investments are subject to market risks.\nNot SEBI registered investment advice."
    y = 1450
    for line in disclaimer.split("\n"):
        d.text((540, y), line, fill=TEXT_MUTED, anchor="mm", font=get_font(22, bold=False))
        y += 40
    img.save(out_path)

def render_all_slides(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    renderers = [
        render_slide_1, render_slide_2, render_slide_3, render_slide_4,
        render_slide_5, render_slide_6, render_slide_7, render_slide_8,
        render_slide_9, render_slide_10, render_slide_11, render_slide_12
    ]
    for idx, func in enumerate(renderers, 1):
        out_f = os.path.join(output_dir, f"slide-{idx:02d}.png")
        func(out_f)
        print(f"Rendered native slide {idx:02d} -> {out_f}")

if __name__ == "__main__":
    out_dir = os.path.join(BASE_DIR, "PROJECTS", "REEL_001_SIP_FD_REALITY_CHECK", "05_SLIDES")
    render_all_slides(out_dir)
