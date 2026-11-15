#!/usr/bin/env python3
"""
Automated 9:16 Vertical PowerPoint (PPTX) Deck & Slide Generator.
Builds editable professional presentation decks (.pptx) with:
- 9:16 vertical ratio (9" x 16" = 1080x1920)
- High-contrast visual cards, badges, and comparison grids
- Integrated viral Cat Meme reactions (Mascot, Crying Cat, Rich Cat, Confused Cat)
- Synchronized rendering to both editable .pptx and high-res PNG slide deck.
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.templates import (
    template_hook,
    template_comparison,
    template_alert,
    template_stat,
    template_tier_list,
    template_outro,
    template_cat_meme
)

def build_pptx_deck(project_id, title, output_pptx_path, cat_theme="viral_cats"):
    """
    Creates an editable 9:16 PowerPoint deck with 6 core viral slides and cat memes.
    """
    os.makedirs(os.path.dirname(output_pptx_path), exist_ok=True)
    
    prs = Presentation()
    prs.slide_width = Inches(9.0)
    prs.slide_height = Inches(16.0)
    blank_layout = prs.slide_layouts[6]
    
    # Brand Color Palette
    BG_COLOR = RGBColor(244, 235, 221)      # #F4EBDD Warm Canvas
    TEXT_DARK = RGBColor(26, 26, 26)        # #1A1A1A
    GREEN_ACCENT = RGBColor(22, 163, 74)    # #16A34A (SIP/Bullish)
    RED_ACCENT = RGBColor(220, 38, 38)      # #DC2626 (Risk/Trap)
    BLUE_ACCENT = RGBColor(37, 99, 235)     # #2563EB (FD)
    CARD_BG = RGBColor(255, 255, 255)       # Card container
    
    cats_dir = os.path.join(BASE_DIR, "assets", "cats")
    mascot_img = os.path.join(cats_dir, "mascot_cat.png")
    crying_img = os.path.join(cats_dir, "crying_cat.png")
    rich_img = os.path.join(cats_dir, "rich_cat.png")
    confused_img = os.path.join(cats_dir, "confused_cat.png")
    thinking_img = os.path.join(cats_dir, "thinking_cat.png")
    shocked_img = os.path.join(cats_dir, "shocked_cat.png")

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, heading, tag="FINANCE REALITY CHECK"):
        # Top Badge Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(0.8), Inches(6.0), Inches(0.6))
        pill.fill.solid()
        pill.fill.fore_color.rgb = TEXT_DARK
        pill.line.fill.background()
        tf = pill.text_frame
        tf.text = tag
        tf.paragraphs[0].font.size = Pt(16)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        # Heading
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(7.4), Inches(2.0))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p = tf_title.paragraphs[0]
        p.text = heading
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p.alignment = PP_ALIGN.CENTER

    # --------------------------------------------------------------------------
    # SLIDE 1: Hook with Mascot Cat
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)
    add_header(s1, title, "🚨 CRITICAL MONEY DECISION")
    if os.path.exists(mascot_img):
        s1.shapes.add_picture(mascot_img, Inches(2.2), Inches(4.2), width=Inches(4.6))
    
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(10.0), Inches(7.0), Inches(4.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = TEXT_DARK
    card1.line.width = Pt(3)
    p1 = card1.text_frame.paragraphs[0]
    p1.text = "Agar aap SIP ya FD kar rahe ho,\ntoh yeh 95 seconds aapke hazaron bacha sakte hain!"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_DARK
    p1.alignment = PP_ALIGN.CENTER

    # --------------------------------------------------------------------------
    # SLIDE 2: The Mystery / Confused Cat
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Bank me paisa sach me SAFE hai?\nYa illusion hai?", "THE BIG QUESTION")
    if os.path.exists(confused_img):
        s2.shapes.add_picture(confused_img, Inches(2.2), Inches(4.5), width=Inches(4.6))
        
    card2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(10.2), Inches(7.0), Inches(4.2))
    card2.fill.solid()
    card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = TEXT_DARK
    card2.line.width = Pt(3)
    p2 = card2.text_frame.paragraphs[0]
    p2.text = "Inflation चुपके से आपकी savings की value ख़त्म कर रहा है..."
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = RED_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    # --------------------------------------------------------------------------
    # SLIDE 3: Comparison Matrix (SIP vs FD)
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "SIP vs FD: The Battle", "REAL NUMBERS")
    
    # Left Card (SIP)
    sip_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(3.5), Inches(10.0))
    sip_card.fill.solid()
    sip_card.fill.fore_color.rgb = RGBColor(240, 253, 244)
    sip_card.line.color.rgb = GREEN_ACCENT
    sip_card.line.width = Pt(3)
    tf_sip = sip_card.text_frame
    tf_sip.text = "📈 SIP (Equity)\n\n• 12-14% CAGR\n• ₹1,000/month\n• Beats Inflation\n• Top 50 Companies\n• Long-term Wealth"
    for p in tf_sip.paragraphs:
        p.font.size = Pt(20)
        p.font.color.rgb = TEXT_DARK

    # Right Card (FD)
    fd_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(4.2), Inches(3.5), Inches(10.0))
    fd_card.fill.solid()
    fd_card.fill.fore_color.rgb = RGBColor(254, 242, 242)
    fd_card.line.color.rgb = RED_ACCENT
    fd_card.line.width = Pt(3)
    tf_fd = fd_card.text_frame
    tf_fd.text = "🏦 FD (Fixed Deposit)\n\n• 6.5-7.0% Return\n• 30% Tax Deducted\n• Real Return ~ 0%\n• Only ₹5L DICGC\n• Inflation Risk"
    for p in tf_fd.paragraphs:
        p.font.size = Pt(20)
        p.font.color.rgb = TEXT_DARK

    # --------------------------------------------------------------------------
    # SLIDE 4: Reality Check & Crying Cat
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "30% Tax Slab Reality:\nReal Return Negative!", "⚠️ TAX & INFLATION TRAP")
    if os.path.exists(crying_img):
        s4.shapes.add_picture(crying_img, Inches(2.2), Inches(4.2), width=Inches(4.6))
        
    tax_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(10.0), Inches(7.0), Inches(4.6))
    tax_card.fill.solid()
    tax_card.fill.fore_color.rgb = CARD_BG
    tax_card.line.color.rgb = RED_ACCENT
    tax_card.line.width = Pt(3)
    p4 = tax_card.text_frame.paragraphs[0]
    p4.text = "7% FD - 30% Tax - 6% Inflation =\n📉 NEGATIVE PURCHASING POWER!"
    p4.font.size = Pt(26)
    p4.font.bold = True
    p4.font.color.rgb = RED_ACCENT
    p4.alignment = PP_ALIGN.CENTER

    # --------------------------------------------------------------------------
    # SLIDE 5: Rich Cat Outro & Follow CTA
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Follow For Smart Money Hacks!", "FINANCIAL FREEDOM")
    if os.path.exists(rich_img):
        s5.shapes.add_picture(rich_img, Inches(2.2), Inches(4.2), width=Inches(4.6))
        
    cta_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(10.0), Inches(7.0), Inches(4.5))
    cta_card.fill.solid()
    cta_card.fill.fore_color.rgb = TEXT_DARK
    cta_card.line.color.rgb = RGBColor(255, 215, 0)
    cta_card.line.width = Pt(4)
    p5 = cta_card.text_frame.paragraphs[0]
    p5.text = "👉 Hit Follow & Share with a friend\nwho keeps all their money in FD!"
    p5.font.size = Pt(26)
    p5.font.bold = True
    p5.font.color.rgb = RGBColor(255, 255, 255)
    p5.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    print(f"PowerPoint Presentation Deck built: {output_pptx_path}")
    return output_pptx_path

def generate_slides_from_deck(project_id, title, output_dir):
    """
    Renders high-res 1080x1920 PNG slides using the modular template engine
    and integrates the Cat Meme assets so they stay perfectly in sync.
    """
    os.makedirs(output_dir, exist_ok=True)
    cats_dir = os.path.join(BASE_DIR, "assets", "cats")
    mascot_img = os.path.join(cats_dir, "mascot_cat.png")
    crying_img = os.path.join(cats_dir, "crying_cat.png")
    rich_img = os.path.join(cats_dir, "rich_cat.png")
    confused_img = os.path.join(cats_dir, "confused_cat.png")
    
    slide_paths = []
    
    # Slide 1: Hook with Mascot Cat
    s1 = template_hook(
        tag="🚨 CRITICAL MONEY DECISION",
        title=title,
        body_text="Agar aap SIP ya FD kar rahe ho,\ntoh yeh 95 seconds aapke hazaron bacha sakte hain!",
        image_path=mascot_img if os.path.exists(mascot_img) else None
    )
    p1 = os.path.join(output_dir, "slide-01.png")
    s1.save(p1)
    slide_paths.append(p1)

    # Slide 2: Dilemma with Confused Cat Meme
    s2 = template_cat_meme(
        tag="THE BIG QUESTION",
        title="Bank me paisa sach me SAFE hai?",
        cat_image_path=confused_img if os.path.exists(confused_img) else mascot_img,
        top_caption="Me thinking my money is safe in bank...",
        bottom_caption="Inflation silently eating 6% every year! 😱"
    )
    p2 = os.path.join(output_dir, "slide-02.png")
    s2.save(p2)
    slide_paths.append(p2)

    # Slide 3: Comparison Matrix
    s3 = template_comparison(
        tag="REAL NUMBERS",
        title="SIP vs FD: The Reality",
        opt_a_name="📈 SIP (Index Equity)",
        opt_a_rows=[("Returns", "12-14% CAGR"), ("Tax", "12.5% LTCG"), ("Inflation", "Beats Inflation")],
        opt_b_name="🏦 FD (Bank Deposit)",
        opt_b_rows=[("Returns", "6.5-7.0%"), ("Tax", "Up to 30% Slab"), ("Real Return", "Negative purchasing power")]
    )
    p3 = os.path.join(output_dir, "slide-03.png")
    s3.save(p3)
    slide_paths.append(p3)

    # Slide 4: Reality Check with Crying Cat Meme
    s4 = template_cat_meme(
        tag="⚠️ TAX & INFLATION TRAP",
        title="30% Tax Slab Reality",
        cat_image_path=crying_img if os.path.exists(crying_img) else mascot_img,
        top_caption="Me after calculating real FD returns...",
        bottom_caption="7% FD - 30% Tax - 6% Inflation = NEGATIVE! 😭"
    )
    p4 = os.path.join(output_dir, "slide-04.png")
    s4.save(p4)
    slide_paths.append(p4)

    # Slide 5: Strategy / Allocation Tier List
    s5 = template_tier_list(
        tag="SMART ALLOCATION",
        title="Where To Put Your Money?",
        tier_name="TIER 1 ASSETS",
        tier_color=(22, 163, 74),
        items=[
            ("Nifty 50 Index", "₹1,000/mo", "Long term compounding"),
            ("Sovereign Gold Bond", "₹6,000/g", "2.5% interest + Gold gain"),
            ("Emergency Liquid FD", "₹50,000", "Instant access only")
        ]
    )
    p5 = os.path.join(output_dir, "slide-05.png")
    s5.save(p5)
    slide_paths.append(p5)

    # Slide 6: Outro / Follow CTA with Rich Cat
    s6 = template_outro(
        tag="FINANCIAL FREEDOM",
        title="Follow For Daily Money Hacks!",
        cta_headline="👉 HIT FOLLOW NOW",
        upcoming_list=[
            "Gold vs Real Estate Reality",
            "How to save 30% Tax legally",
            "Mutual Fund vs Direct Stock"
        ],
        disclaimer="Educational content only.\nNot SEBI registered financial advice."
    )
    p6 = os.path.join(output_dir, "slide-06.png")
    s6.save(p6)
    slide_paths.append(p6)

    print(f"Rendered {len(slide_paths)} high-res PNG slides to {output_dir}")
    return slide_paths

if __name__ == "__main__":
    out_dir = "PROJECTS/REEL_001_SIP_FD_REALITY_CHECK/05_SLIDES"
    build_pptx_deck("REEL_001_SIP_FD_REALITY_CHECK", "SIP & FD Reality Check", os.path.join(out_dir, "presentation.pptx"))
    generate_slides_from_deck("REEL_001_SIP_FD_REALITY_CHECK", "SIP & FD Reality Check", out_dir)
