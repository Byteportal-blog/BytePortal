import os
from PIL import Image, ImageDraw, ImageFont

img_dir = r"d:\Blog\BytePortal\assets\images\2026\craft-anything"
os.makedirs(img_dir, exist_ok=True)

# Colors
BG_COLOR = (15, 23, 42)          # Slate 900
CARD_BG = (24, 33, 47)           # Slate 800/900
BORDER_COLOR = (51, 65, 85)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
ACCENT_CYAN = (56, 189, 248)     # Sky 400
ACCENT_VIOLET = (168, 85, 247)   # Purple 400
ACCENT_EMERALD = (52, 211, 153)  # Emerald 400
ACCENT_AMBER = (251, 191, 36)    # Amber 400

# Fonts
font_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 31)
font_subtitle = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
font_card_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 20)
font_badge = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)
font_bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14)
font_reg = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)

img = Image.new('RGB', (1200, 640), BG_COLOR)
draw = ImageDraw.Draw(img)

# Background subtle dots pattern
for x in range(0, 1200, 36):
    for y in range(0, 640, 36):
        draw.point((x, y), fill=(30, 41, 59))

# Header pill
draw.rounded_rectangle([40, 25, 180, 53], radius=6, fill=(30, 41, 59), outline=BORDER_COLOR, width=1)
draw.text((53, 32), "BYTEPORTAL.TECH", fill=(148, 163, 184), font=font_badge)

# Title & Subtitle
draw.text((40, 66), "Craft Anything Architecture: The Clean-Room AI Reconstruction Loop", fill=TEXT_WHITE, font=font_title)
draw.text((40, 112), "How 320+ Rust decoders, MCP agent tools, and visual diff engines recreate software safely", fill=TEXT_MUTED, font=font_subtitle)

# 4 Columns Layout
card_w = 262
card_h = 445
col_y = 155
spacing = 24
start_x = 40

stages = [
    {
        "step": "STAGE 01",
        "tag_bg": (12, 74, 110),
        "tag_fg": (186, 230, 253),
        "title": "1. Study & Decode",
        "subtitle": "Evidence Extraction",
        "outline": ACCENT_CYAN,
        "items": [
            ("Target Ingestion", "Websites, binaries, APKs, Electron ASAR, file formats"),
            ("320+ Rust Decoders", "Disassembles layout, AST, tokens, and network APIs"),
            ("Clean-Room Guard", "Extracts behavior contracts without copying source code")
        ]
    },
    {
        "step": "STAGE 02",
        "tag_bg": (88, 28, 135),
        "tag_fg": (233, 213, 255),
        "title": "2. Agent Build",
        "subtitle": "MCP Synthesis",
        "outline": ACCENT_VIOLET,
        "items": [
            ("MCP Interface", "Connects Claude Code, Cursor, OpenCode, and Codex"),
            ("Ground-Truth Specs", "Feeds deterministic tokens & metrics to LLM context"),
            ("Stack Freedom", "Recreates target in Rust, React, Go, or your chosen stack")
        ]
    },
    {
        "step": "STAGE 03",
        "tag_bg": (6, 78, 59),
        "tag_fg": (167, 243, 208),
        "title": "3. Compare & Diff",
        "subtitle": "Automated Validation",
        "outline": ACCENT_EMERALD,
        "items": [
            ("Computer Vision", "Automated pixel-by-pixel visual diff regression"),
            ("DOM & AST Checks", "Verifies component hierarchy and structural parity"),
            ("Discrepancy Log", "Pinpoints missing features and styling misalignments")
        ]
    },
    {
        "step": "STAGE 04",
        "tag_bg": (120, 53, 15),
        "tag_fg": (254, 215, 170),
        "title": "4. Refine Loop",
        "subtitle": "Autonomous Healing",
        "outline": ACCENT_AMBER,
        "items": [
            ("Feedback Loop", "Passes precise diff vectors back to the coding agent"),
            ("Targeted Patches", "Iteratively repairs discrepancies without hallucinations"),
            ("Standalone Export", "Delivers clean, production-ready, copyright-safe repo")
        ]
    }
]

for i, stage in enumerate(stages):
    cx = start_x + i * (card_w + spacing)
    # Outer card
    draw.rounded_rectangle([cx, col_y, cx + card_w, col_y + card_h], radius=14, fill=CARD_BG, outline=stage["outline"], width=2)
    
    # Step Badge
    draw.rounded_rectangle([cx + 16, col_y + 16, cx + 16 + 85, col_y + 38], radius=5, fill=stage["tag_bg"])
    draw.text((cx + 24, col_y + 20), stage["step"], fill=stage["tag_fg"], font=font_badge)
    
    # Titles
    draw.text((cx + 16, col_y + 48), stage["title"], fill=TEXT_WHITE, font=font_card_title)
    draw.text((cx + 16, col_y + 76), stage["subtitle"], fill=TEXT_MUTED, font=font_reg)
    
    # Divider line
    draw.line([(cx + 16, col_y + 98), (cx + card_w - 16, col_y + 98)], fill=(45, 58, 77), width=1)
    
    # Items
    sy = col_y + 110
    for label, desc in stage["items"]:
        draw.text((cx + 16, sy), label.upper(), fill=stage["outline"], font=font_badge)
        
        # Word wrap desc in card_w - 32
        words = desc.split()
        lines = []
        cur_line = []
        for w in words:
            test_line = " ".join(cur_line + [w])
            bbox = draw.textbbox((0, 0), test_line, font=font_reg)
            if bbox[2] - bbox[0] <= card_w - 32:
                cur_line.append(w)
            else:
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))
            
        ly = sy + 18
        for line in lines:
            draw.text((cx + 16, ly), line, fill=TEXT_WHITE, font=font_reg)
            ly += 18
        sy += 105

workflow_path = os.path.join(img_dir, "craft-anything-workflow.png")
img.save(workflow_path, "PNG", optimize=True)
print(f"Generated workflow diagram: {workflow_path} ({os.path.getsize(workflow_path)} bytes)")
