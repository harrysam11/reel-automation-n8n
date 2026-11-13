#!/usr/bin/env python3
"""
Generate editable PowerPoint slides for Reel 01: SIP & FD Reality Check.
Vertical 9:16 layout (1080 x 1920), Warm Beige #F4EBDD background,
14 preserved investment categories across 3 capital-map slides.
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_pptx_path):
    os.makedirs(os.path.dirname(output_pptx_path), exist_ok=True)
    
    prs = Presentation()
    # 9:16 vertical ratio (9 inches x 16 inches = exactly 1080 x 1920 ratio)
    prs.slide_width = Inches(9.0)
    prs.slide_height = Inches(16.0)
    blank_layout = prs.slide_layouts[6]
    
    BG_COLOR = RGBColor(244, 235, 221)      # #F4EBDD
    TEXT_DARK = RGBColor(26, 26, 26)        # #1A1A1A
    TEXT_MUTED = RGBColor(100, 100, 100)    # Subdued gray
    GREEN_ACCENT = RGBColor(22, 163, 74)    # #16A34A (Bullish / SIP)
    RED_ACCENT = RGBColor(220, 38, 38)      # #DC2626 (Risk / Tax trap)
    BLUE_ACCENT = RGBColor(37, 99, 235)     # #2563EB (FD / DICGC)
    CARD_BG = RGBColor(255, 255, 255)       # White card container
    
    mascot_img = "BRAND/main_cat.png"
    logo_img = "BRAND/logo.png"
    smug_img = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/smug_cat.png"
    shocked_img = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/shocked_cat.png"
    thinking_img = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/04_ASSETS/cat_reactions/thinking_cat.png"

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background() # No border
        return bg

    def add_header(slide, title_text, category_tag="FINANCE REALITY CHECK"):
        # Category pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(0.8), Inches(6.0), Inches(0.6))
        pill.fill.solid()
        pill.fill.fore_color.rgb = TEXT_DARK
        pill.line.fill.background()
        tf = pill.text_frame
        tf.text = category_tag
        tf.paragraphs[0].font.size = Pt(16)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        # Main Title Box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.4), Inches(2.0))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p = tf_title.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 1: Hook
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    add_header(s1, "SIP ya FD?\n95-Sec Reality Check!", "🚨 CRITICAL MONEY DECISION")
    if os.path.exists(mascot_img):
        s1.shapes.add_picture(mascot_img, Inches(2.0), Inches(4.2), width=Inches(5.0))
    
    hook_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(10.0), Inches(7.0), Inches(4.5))
    hook_card.fill.solid()
    hook_card.fill.fore_color.rgb = CARD_BG
    hook_card.line.color.rgb = TEXT_DARK
    hook_card.line.width = Pt(3)
    tf1 = hook_card.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Agar aap SIP ya FD kar rahe ho,\ntoh yeh 95 seconds aapke hazaron bacha sakte hain!"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_DARK
    p1.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 2: Question
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Bank me paisa sach me safe hai?\nYa illusion hai?", "THE BIG QUESTION")
    if os.path.exists(smug_img):
        s2.shapes.add_picture(smug_img, Inches(2.2), Inches(4.5), width=Inches(4.6))
    
    q_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(10.2), Inches(7.0), Inches(4.2))
    q_card.fill.solid()
    q_card.fill.fore_color.rgb = CARD_BG
    q_card.line.color.rgb = TEXT_DARK
    tf2 = q_card.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "Sab kehte hain FD safe hai...\nLekin kya aapne Inflation aur Tax calculate kiya hai?"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 3: SIP Explanation
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "SIP: Systematic Wealth Machine", "GROWTH ENGINE")
    
    sip_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.0), Inches(7.0), Inches(10.5))
    sip_card.fill.solid()
    sip_card.fill.fore_color.rgb = CARD_BG
    sip_card.line.color.rgb = GREEN_ACCENT
    sip_card.line.width = Pt(3)
    tf3 = sip_card.text_frame
    tf3.word_wrap = True
    
    items_s3 = [
        ("Monthly Investment", "₹1,000 / month"),
        ("Underlying Asset", "Top 50 / 500 Indian Companies"),
        ("Historical CAGR (10-15 Yrs)", "11% – 14%"),
        ("Magic Power", "Rupee Cost Averaging + Compounding")
    ]
    for idx, (title, val) in enumerate(items_s3):
        p_t = tf3.add_paragraph() if idx > 0 else tf3.paragraphs[0]
        p_t.text = f"{title}:"
        p_t.font.size = Pt(20)
        p_t.font.bold = False
        p_t.font.color.rgb = TEXT_MUTED
        
        p_v = tf3.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(28)
        p_v.font.bold = True
        p_v.font.color.rgb = GREEN_ACCENT
        p_v.space_after = Pt(20)

    # -------------------------------------------------------------
    # SLIDE 4: SIP Risk (Reality Check)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "SIP Risk: Market Crash Reality!", "REALITY CHECK #1")
    if os.path.exists(shocked_img):
        s4.shapes.add_picture(shocked_img, Inches(2.2), Inches(4.2), width=Inches(4.6))
        
    s4_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(10.0), Inches(7.0), Inches(4.5))
    s4_card.fill.solid()
    s4_card.fill.fore_color.rgb = CARD_BG
    s4_card.line.color.rgb = RED_ACCENT
    s4_card.line.width = Pt(3)
    tf4 = s4_card.text_frame
    tf4.word_wrap = True
    p4 = tf4.paragraphs[0]
    p4.text = "SIP koi magic nahi hai!\nShort term me portfolio -20% se -30% tak red ho sakta hai.\n\nRule: Agar 5 saal se pehle paisa chahiye, toh equity SIP mat karo!"
    p4.font.size = Pt(22)
    p4.font.bold = True
    p4.font.color.rgb = RED_ACCENT
    p4.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 5: FD Explanation
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Fixed Deposit (FD): Guaranteed?", "SECURITY ANALYSIS")
    
    fd_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.0), Inches(7.0), Inches(10.5))
    fd_card.fill.solid()
    fd_card.fill.fore_color.rgb = CARD_BG
    fd_card.line.color.rgb = BLUE_ACCENT
    fd_card.line.width = Pt(3)
    tf5 = fd_card.text_frame
    tf5.word_wrap = True
    
    items_s5 = [
        ("Nominal FD Rate", "6.5% – 7.2% p.a."),
        ("Security Level", "High (Scheduled Banks)"),
        ("Liquidity", "Instant (Subject to penalty)"),
        ("TDS Section", "Section 194A (Above ₹40k interest)")
    ]
    for idx, (title, val) in enumerate(items_s5):
        p_t = tf5.add_paragraph() if idx > 0 else tf5.paragraphs[0]
        p_t.text = f"{title}:"
        p_t.font.size = Pt(20)
        p_t.font.bold = False
        p_t.font.color.rgb = TEXT_MUTED
        
        p_v = tf5.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(28)
        p_v.font.bold = True
        p_v.font.color.rgb = BLUE_ACCENT
        p_v.space_after = Pt(20)

    # -------------------------------------------------------------
    # SLIDE 6: Inflation & Tax Trap
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "The Real Return Trap\nFD Math Revealed", "SHOCKING TRUTH")
    
    math_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.2), Inches(7.0), Inches(10.5))
    math_card.fill.solid()
    math_card.fill.fore_color.rgb = CARD_BG
    math_card.line.color.rgb = RED_ACCENT
    math_card.line.width = Pt(3)
    tf6 = math_card.text_frame
    tf6.word_wrap = True
    
    calcs = [
        ("Bank FD Rate", "+ 7.0%"),
        ("30% Tax Slab", "- 2.1%"),
        ("Post-Tax In-Hand", "= 4.9%"),
        ("CPI Inflation", "- 5.5% to 6.0%"),
        ("YOUR REAL RETURN", "NEGATIVE (-0.6% to -1.1%)")
    ]
    for idx, (lbl, val) in enumerate(calcs):
        p_l = tf6.add_paragraph() if idx > 0 else tf6.paragraphs[0]
        p_l.text = lbl
        p_l.font.size = Pt(20)
        p_l.font.color.rgb = TEXT_MUTED
        
        p_v = tf6.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(28)
        p_v.font.bold = True
        p_v.font.color.rgb = RED_ACCENT if "REAL RETURN" in lbl or "-" in val else TEXT_DARK
        p_v.space_after = Pt(15)

    # -------------------------------------------------------------
    # SLIDE 7: DICGC Fact Card
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "DICGC Insurance Limit:\nOnly ₹5 Lakh Covered!", "REGULATORY RULE")
    
    dicgc_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(7.0), Inches(9.5))
    dicgc_card.fill.solid()
    dicgc_card.fill.fore_color.rgb = CARD_BG
    dicgc_card.line.color.rgb = BLUE_ACCENT
    dicgc_card.line.width = Pt(3)
    tf7 = dicgc_card.text_frame
    tf7.word_wrap = True
    
    p7_1 = tf7.paragraphs[0]
    p7_1.text = "RBI Subsidiary: DICGC"
    p7_1.font.size = Pt(22)
    p7_1.font.bold = True
    p7_1.font.color.rgb = BLUE_ACCENT
    p7_1.space_after = Pt(15)
    
    p7_2 = tf7.add_paragraph()
    p7_2.text = "Maximum Insurance Cover:\n₹5,00,000"
    p7_2.font.size = Pt(32)
    p7_2.font.bold = True
    p7_2.font.color.rgb = RED_ACCENT
    p7_2.space_after = Pt(20)
    
    p7_3 = tf7.add_paragraph()
    p7_3.text = "Key Takeaway:\nChahe aapke account me ₹50 Lakh ho, bank default hone par kanoon ke mutabik sirf ₹5 Lakh (Principal + Interest) protected hain.\n\nIsliye apna paisa multiple scheduled banks me diversify karein!"
    p7_3.font.size = Pt(20)
    p7_3.font.bold = True
    p7_3.font.color.rgb = TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 8: Capital Map Tier 1 (₹100 - ₹5,000)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Capital Map: Tier 1\nEntry: ₹100 – ₹5,000", "INVESTMENT BLUEPRINT")
    
    t1_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(7.4), Inches(10.5))
    t1_card.fill.solid()
    t1_card.fill.fore_color.rgb = CARD_BG
    t1_card.line.color.rgb = GREEN_ACCENT
    t1_card.line.width = Pt(2)
    tf8 = t1_card.text_frame
    tf8.word_wrap = True
    
    tier1_items = [
        ("1. Mutual Funds", "₹100 – ₹500", "Micro SIPs on index & flexi-cap"),
        ("2. ETFs", "~₹20 – ₹500", "1 unit NiftyBeES, GoldBeES"),
        ("3. Direct Stocks", "₹10 – ₹5,000+", "Single share purchase (NSE/BSE)"),
        ("4. PPF / EPF / SSY", "₹250 – ₹500/yr", "Guaranteed Sovereign backing"),
        ("5. NPS", "₹500 – ₹1,000", "Tier 1 retirement account"),
        ("6. Bank FDs / RDs", "₹100 – ₹1,000", "Short-term emergency parking")
    ]
    for idx, (name, capital, note) in enumerate(tier1_items):
        p_row = tf8.add_paragraph() if idx > 0 else tf8.paragraphs[0]
        p_row.text = f"{name}  ➔  {capital}"
        p_row.font.size = Pt(20)
        p_row.font.bold = True
        p_row.font.color.rgb = TEXT_DARK
        
        p_sub = tf8.add_paragraph()
        p_sub.text = f"   ({note})"
        p_sub.font.size = Pt(14)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 9: Capital Map Tier 2 (₹10,000 - ₹5 Lakh)
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Capital Map: Tier 2\nEntry: ₹10,000 – ₹5 Lakh", "INVESTMENT BLUEPRINT")
    
    t2_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(7.4), Inches(10.5))
    t2_card.fill.solid()
    t2_card.fill.fore_color.rgb = CARD_BG
    t2_card.line.color.rgb = BLUE_ACCENT
    t2_card.line.width = Pt(2)
    tf9 = t2_card.text_frame
    tf9.word_wrap = True
    
    tier2_items = [
        ("7. Government Securities", "₹10,000", "RBI Retail Direct (T-bills & G-Secs)"),
        ("8. REITs / InvITs", "₹100 – ₹400/unit", "Commercial real estate yield"),
        ("9. Sovereign Gold Bonds", "~₹7,500 – ₹8,500+", "1g Gold issue + 2.5% annual interest"),
        ("10. Corporate Bonds / NCDs", "₹10,000 – ₹1,00,000", "Listed debentures on debt portals"),
        ("11. P2P / Invoice Investing", "₹5,000 – ₹50,000", "High yield alt debt (Higher risk)")
    ]
    for idx, (name, capital, note) in enumerate(tier2_items):
        p_row = tf9.add_paragraph() if idx > 0 else tf9.paragraphs[0]
        p_row.text = f"{name}  ➔  {capital}"
        p_row.font.size = Pt(20)
        p_row.font.bold = True
        p_row.font.color.rgb = TEXT_DARK
        
        p_sub = tf9.add_paragraph()
        p_sub.text = f"   ({note})"
        p_sub.font.size = Pt(14)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 10: Capital Map Tier 3 (₹20 Lakh - ₹1 Crore+)
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Capital Map: Tier 3\nEntry: ₹20 Lakh – ₹1 Crore+", "HNI / SPECIALIZED")
    
    t3_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(7.4), Inches(10.5))
    t3_card.fill.solid()
    t3_card.fill.fore_color.rgb = CARD_BG
    t3_card.line.color.rgb = RGBColor(147, 51, 234) # Purple
    t3_card.line.width = Pt(2)
    tf10 = t3_card.text_frame
    tf10.word_wrap = True
    
    tier3_items = [
        ("12. Real Estate (Physical)", "₹20 Lakh – ₹1 Crore+", "Land / Residential / Commercial property"),
        ("13. PMS (Portfolio Mgmt)", "₹50 Lakh", "SEBI Statutory Minimum per individual"),
        ("14. AIF (Alternative Inv)", "₹1 Crore", "SEBI Statutory Minimum (PE/VC/Hedge)")
    ]
    for idx, (name, capital, note) in enumerate(tier3_items):
        p_row = tf10.add_paragraph() if idx > 0 else tf10.paragraphs[0]
        p_row.text = f"{name}  ➔  {capital}"
        p_row.font.size = Pt(22)
        p_row.font.bold = True
        p_row.font.color.rgb = TEXT_DARK
        
        p_sub = tf10.add_paragraph()
        p_sub.text = f"   ({note})"
        p_sub.font.size = Pt(16)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(25)

    # -------------------------------------------------------------
    # SLIDE 11: Upcoming Teasers
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Coming Up in Next Reels!", "UPCOMING CONTENT")
    
    up_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(7.4), Inches(10.5))
    up_card.fill.solid()
    up_card.fill.fore_color.rgb = CARD_BG
    up_card.line.color.rgb = TEXT_DARK
    tf11 = up_card.text_frame
    tf11.word_wrap = True
    
    teasers = [
        ("Reel 02", "SIP vs Lump Sum: Which Wins in 2026?"),
        ("Reel 03", "FD vs Debt Mutual Funds: Tax Showdown"),
        ("Reel 04", "How Inflation Secretly Destroys Savings"),
        ("Reel 05", "Where to Invest Your First ₹1,000")
    ]
    for idx, (ep, title) in enumerate(teasers):
        p_e = tf11.add_paragraph() if idx > 0 else tf11.paragraphs[0]
        p_e.text = ep
        p_e.font.size = Pt(16)
        p_e.font.bold = True
        p_e.font.color.rgb = GREEN_ACCENT
        
        p_t = tf11.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK
        p_t.space_after = Pt(20)

    # -------------------------------------------------------------
    # SLIDE 12: CTA & Follow
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Become a Financially\nSmart Investor!", "JOIN THE COMMUNITY")
    if os.path.exists(mascot_img):
        s12.shapes.add_picture(mascot_img, Inches(2.2), Inches(4.2), width=Inches(4.6))
        
    cta_btn = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(9.8), Inches(6.0), Inches(1.4))
    cta_btn.fill.solid()
    cta_btn.fill.fore_color.rgb = RED_ACCENT
    cta_btn.line.fill.background()
    tf_cta = cta_btn.text_frame
    p_c = tf_cta.paragraphs[0]
    p_c.text = "👉 TAP FOLLOW"
    p_c.font.size = Pt(36)
    p_c.font.bold = True
    p_c.font.color.rgb = RGBColor(255, 255, 255)
    p_c.alignment = PP_ALIGN.CENTER
    
    disclaimer_box = s12.shapes.add_textbox(Inches(0.8), Inches(12.0), Inches(7.4), Inches(2.5))
    tf_d = disclaimer_box.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = "Disclaimer: For educational purposes only. Securities investments are subject to market risks. Not SEBI registered investment advice."
    p_d.font.size = Pt(14)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    print(f"Presentation saved successfully to: {output_pptx_path}")

if __name__ == "__main__":
    out_path = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/05_SLIDES/reel_001_slides.pptx"
    create_deck(out_path)
