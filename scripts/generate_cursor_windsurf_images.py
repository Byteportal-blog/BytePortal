import os
from PIL import Image, ImageDraw, ImageFont

img_dir = r"d:\Blog\BytePortal\assets\images\2026\cursor-vs-windsurf"
os.makedirs(img_dir, exist_ok=True)

# Colors
BG_COLOR = (15, 23, 42)          # Slate 900
CARD_CURSOR = (30, 41, 59)      # Slate 800
CARD_WINDSURF = (15, 32, 39)    # Deep Teal / Slate
ACCENT_CURSOR = (56, 189, 248)   # Sky 400 (Cursor accent)
ACCENT_WINDSURF = (52, 211, 153) # Emerald 400 (Windsurf accent)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
BORDER_COLOR = (51, 65, 85)
DIVIDER_COLOR = (40, 53, 72)
VS_BG = (239, 68, 68)            # Red 500 badge

# Fonts
font_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 35)
font_subtitle = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 19)
font_header = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 26)
font_card_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
font_item_label = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)
font_item_val = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
font_tag = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
font_vs = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)

# ==========================================
# 1. OG BANNER (1200 x 630)
# ==========================================
img = Image.new('RGB', (1200, 630), BG_COLOR)
draw = ImageDraw.Draw(img)

# Background subtle dots pattern
for x in range(0, 1200, 36):
    for y in range(0, 630, 36):
        draw.point((x, y), fill=(30, 41, 59))

# Header pill
draw.rounded_rectangle([40, 26, 180, 54], radius=6, fill=(30, 41, 59), outline=BORDER_COLOR, width=1)
draw.text((53, 33), "BYTEPORTAL.TECH", fill=(148, 163, 184), font=font_tag)

draw.text((40, 68), "Cursor vs Windsurf: Which AI Code Editor Wins in 2026?", fill=TEXT_WHITE, font=font_title)
draw.text((40, 116), "Composer vs Cascade: Multi-file reasoning, terminal autonomy, and real cost.", fill=TEXT_MUTED, font=font_subtitle)

col_y = 160
card_h = 440
card_w = 520

# --- Left Card: Cursor ---
c1_x1, c1_x2 = 40, 40 + card_w
draw.rounded_rectangle([c1_x1, col_y, c1_x2, col_y + card_h], radius=16, fill=CARD_CURSOR, outline=ACCENT_CURSOR, width=2)

# Incumbent Tag
draw.rounded_rectangle([c1_x1 + 24, col_y + 18, c1_x1 + 148, col_y + 44], radius=6, fill=(12, 74, 110))
draw.text((c1_x1 + 35, col_y + 23), "THE INCUMBENT", fill=(186, 230, 253), font=font_tag)

# Title & Architecture subhead
draw.text((c1_x1 + 24, col_y + 54), "Cursor (Anysphere)", fill=TEXT_WHITE, font=font_header)
draw.text((c1_x1 + 24, col_y + 88), "Composer + Shadow Workspace Engine", fill=ACCENT_CURSOR, font=font_card_sub)

# Divider line
draw.line([(c1_x1 + 24, col_y + 118), (c1_x2 - 24, col_y + 118)], fill=DIVIDER_COLOR, width=1)

cursor_rows = [
    ("CORE AGENT", "Composer (Cmd+I) multi-file diff streams"),
    ("MODEL SELECTION", "Claude 3.5 Sonnet, GPT-4o, o1, DeepSeek"),
    ("TERMINAL CONTROL", "Manual inspection & click-to-run execution"),
    ("PLAN LIMITS", "$20/mo (500 fast requests, then queue)"),
    ("BEST SUITED FOR", "Developers demanding full control & model choice")
]

row_y = col_y + 130
for label, val in cursor_rows:
    draw.text((c1_x1 + 24, row_y), label, fill=(125, 211, 252), font=font_item_label)
    draw.text((c1_x1 + 24, row_y + 18), val, fill=TEXT_WHITE, font=font_item_val)
    row_y += 58

# --- Right Card: Windsurf ---
c2_x1, c2_x2 = 640, 640 + card_w
draw.rounded_rectangle([c2_x1, col_y, c2_x2, col_y + card_h], radius=16, fill=CARD_WINDSURF, outline=ACCENT_WINDSURF, width=2)

# Challenger Tag
draw.rounded_rectangle([c2_x1 + 24, col_y + 18, c2_x1 + 154, col_y + 44], radius=6, fill=(6, 78, 59))
draw.text((c2_x1 + 34, col_y + 23), "THE CHALLENGER", fill=(167, 243, 208), font=font_tag)

# Title & Architecture subhead
draw.text((c2_x1 + 24, col_y + 54), "Windsurf (Codeium)", fill=TEXT_WHITE, font=font_header)
draw.text((c2_x1 + 24, col_y + 88), "Cascade Flows + Real-time Terminal Engine", fill=ACCENT_WINDSURF, font=font_card_sub)

# Divider line
draw.line([(c2_x1 + 24, col_y + 118), (c2_x2 - 24, col_y + 118)], fill=DIVIDER_COLOR, width=1)

windsurf_rows = [
    ("CORE AGENT", "Cascade autonomous agent + error observer"),
    ("MODEL SELECTION", "Claude 3.5 Sonnet, GPT-4o, Codeium base"),
    ("TERMINAL CONTROL", "Autonomous command execution & self-healing"),
    ("PLAN LIMITS", "$20/mo (500 fast prompt credits)"),
    ("BEST SUITED FOR", "Developers seeking self-correcting agent loops")
]

row_y = col_y + 130
for label, val in windsurf_rows:
    draw.text((c2_x1 + 24, row_y), label, fill=(110, 231, 183), font=font_item_label)
    draw.text((c2_x1 + 24, row_y + 18), val, fill=TEXT_WHITE, font=font_item_val)
    row_y += 58

# Center VS Badge
vs_cx, vs_cy = 600, col_y + (card_h // 2)
draw.ellipse([vs_cx - 34, vs_cy - 34, vs_cx + 34, vs_cy + 34], fill=VS_BG, outline=TEXT_WHITE, width=3)
draw.text((vs_cx - 15, vs_cy - 14), "VS", fill=TEXT_WHITE, font=font_vs)

og_path = os.path.join(img_dir, 'cursor-vs-windsurf-og.png')
img.save(og_path, 'PNG', optimize=True)
print(f"Generated {og_path}: {os.path.getsize(og_path)} bytes")
