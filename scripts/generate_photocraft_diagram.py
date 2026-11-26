import os
from PIL import Image, ImageDraw, ImageFont

img_dir = r"d:\Blog\BytePortal\assets\images\2026\photocraft"
os.makedirs(img_dir, exist_ok=True)

# Colors
BG_COLOR = (15, 23, 42)          # Slate 900
CARD_BG = (24, 33, 47)           # Slate 800/900
BORDER_COLOR = (51, 65, 85)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
ACCENT_ORANGE = (249, 115, 22)   # Rust Orange 500
ACCENT_RED = (239, 68, 68)       # Red 500 (Adobe)
ACCENT_YELLOW = (234, 179, 8)    # Amber 500 (Electron)
ACCENT_CYAN = (56, 189, 248)     # Sky 400

# Fonts
font_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 32)
font_subtitle = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
font_card_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
font_badge = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)
font_bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
font_reg = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)
font_val = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)

# Create 1200 x 640 image
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
draw.text((40, 66), "Photo Editing Architecture: PhotoCraft vs Photoshop vs Electron", fill=TEXT_WHITE, font=font_title)
draw.text((40, 112), "Comparing memory footprints, graphics pipelines, and runtime overhead on modern hardware", fill=TEXT_MUTED, font=font_subtitle)

# 3 Columns Layout
card_w = 354
card_h = 445
col_y = 155

columns = [
    {
        "x": 40,
        "tag": "LEGACY DESKTOP",
        "tag_bg": (80, 20, 20),
        "tag_fg": (254, 202, 202),
        "title": "Adobe Photoshop",
        "subtitle": "35-Year C++ Legacy Engine",
        "outline": (185, 28, 28),
        "specs": [
            ("Core Architecture", "Native C++ codebase + Creative Cloud daemons"),
            ("Graphics Engine", "OpenGL / DirectX hybrid with CPU fallbacks"),
            ("Idle RAM Usage", "1.8 GB – 3.5 GB (Heavy background telemetry)"),
            ("Startup Latency", "8 – 15 seconds (Plugin & license verification)"),
            ("Extensibility", "Proprietary CEP / UXP JavaScript plugins"),
            ("Pricing & License", "$239.88/yr subscription ($20-$60/month)")
        ]
    },
    {
        "x": 424,
        "tag": "WEB-WRAPPED",
        "tag_bg": (70, 50, 15),
        "tag_fg": (254, 240, 138),
        "title": "Electron / Web Apps",
        "subtitle": "Chromium + Node.js Bundles",
        "outline": (202, 138, 4),
        "specs": [
            ("Core Architecture", "Embedded Chromium browser + Node runtime"),
            ("Graphics Engine", "HTML5 Canvas2D / WebGL wrapped in IPC"),
            ("Idle RAM Usage", "1.2 GB – 2.4 GB (Multi-process browser engine)"),
            ("Startup Latency", "3 – 6 seconds (V8 runtime boot overhead)"),
            ("Extensibility", "Standard NPM web modules & REST APIs"),
            ("Pricing & License", "Freemium web cloud tiers / monthly plans")
        ]
    },
    {
        "x": 808,
        "tag": "PURE RUST + WGPU",
        "tag_bg": (124, 45, 18),
        "tag_fg": (254, 215, 170),
        "title": "PhotoCraft (ArtCraft)",
        "subtitle": "Clean-Room Systems Engine",
        "outline": (249, 115, 22),
        "specs": [
            ("Core Architecture", "Pure native Rust with zero garbage collector"),
            ("Graphics Engine", "Direct WGPU compute shaders (Metal/Vulkan/DX12)"),
            ("Idle RAM Usage", "95 MB – 180 MB (Ultra-lean footprint)"),
            ("Startup Latency", "Sub-10 milliseconds (Immediate window paint)"),
            ("Extensibility", "Model Context Protocol (MCP) AI agents"),
            ("Pricing & License", "100% Free & Open-Source (No account needed)")
        ]
    }
]

for col in columns:
    cx = col["x"]
    # Outer card
    draw.rounded_rectangle([cx, col_y, cx + card_w, col_y + card_h], radius=14, fill=CARD_BG, outline=col["outline"], width=2)
    
    # Tag
    draw.rounded_rectangle([cx + 18, col_y + 16, cx + 18 + 140, col_y + 40], radius=5, fill=col["tag_bg"])
    draw.text((cx + 26, col_y + 21), col["tag"], fill=col["tag_fg"], font=font_badge)
    
    # Titles
    draw.text((cx + 18, col_y + 50), col["title"], fill=TEXT_WHITE, font=font_card_title)
    draw.text((cx + 18, col_y + 80), col["subtitle"], fill=TEXT_MUTED, font=font_reg)
    
    # Divider line
    draw.line([(cx + 18, col_y + 104), (cx + card_w - 18, col_y + 104)], fill=(45, 58, 77), width=1)
    
    # Specs
    sy = col_y + 114
    for label, val in col["specs"]:
        draw.text((cx + 18, sy), label.upper(), fill=(148, 163, 184), font=font_badge)
        draw.text((cx + 18, sy + 16), val, fill=TEXT_WHITE, font=font_bold)
        sy += 52

arch_path = os.path.join(img_dir, "photocraft-architecture.png")
img.save(arch_path, "PNG", optimize=True)
print(f"Generated architecture diagram: {arch_path} ({os.path.getsize(arch_path)} bytes)")
