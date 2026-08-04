#!/usr/bin/env python3
"""Render Music Player UI mockups from firmware layout + light theme colors.

Colors and sizes match Sound_Lounge_UI_Next/Config.h (default darkMode=false).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- Config.h (light theme = factory default) ---
SCREEN_W, SCREEN_H = 240, 320
UI_HEADER_H = 50
UI_CONTROLS_H = 76
UI_NOW_PLAY_H = 66
UI_SECTION_GAP = 8
UI_MAIN_MARGIN = 10
UI_LIST_H = SCREEN_H - UI_HEADER_H - UI_NOW_PLAY_H - UI_CONTROLS_H - (UI_SECTION_GAP * 2)
UI_BTN_PREV_W, UI_BTN_PREV_H = 60, 50
UI_BTN_PLAY_W, UI_BTN_PLAY_H = 88, 64
UI_BTN_NEXT_W, UI_BTN_NEXT_H = 60, 50
UI_TRACK_ROW_H = 38
UI_SETTINGS_ROW_H = 54

BG = (0xFA, 0xF6, 0xF2)
PANEL = (0xFF, 0xFF, 0xFF)
PANEL_BORDER = (0xE5, 0xE7, 0xEB)
ACCENT = (0xA6, 0x73, 0x55)
ACCENT_DARK = (0x8B, 0x5D, 0x43)
TEXT = (0x1A, 0x1A, 0x1A)
TEXT_SEC = (0x5C, 0x53, 0x4A)
TEXT_ON_ACCENT = (0xFF, 0xFF, 0xFF)
TRACK_ACTIVE = (0xF3, 0xE8, 0xE0)
ERROR = (0xB8, 0x5C, 0x5C)

OUT = Path(__file__).resolve().parent / "assets"
SCALE = 3  # export at 3× for print sharpness


def font(size):
    for name in (
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ):
        p = Path(name)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


F_SMALL = font(14)
F_BODY = font(16)
F_TITLE = font(18)
F_HERO = font(20)
F_SYM = font(20)


def new_screen():
    img = Image.new("RGB", (SCREEN_W, SCREEN_H), BG)
    return img, ImageDraw.Draw(img)


def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def panel(draw, x, y, w, h, pad_note=False):
    rounded_rect(draw, (x, y, x + w - 1, y + h - 1), 12, PANEL, PANEL_BORDER, 1)


def outline_pill(draw, x, y, w, h, filled=False):
    if filled:
        rounded_rect(draw, (x, y, x + w - 1, y + h - 1), h // 2, ACCENT, None)
    else:
        rounded_rect(draw, (x, y, x + w - 1, y + h - 1), h // 2, PANEL, ACCENT, 2)


def text_left(draw, xy, s, f, fill=TEXT):
    draw.text(xy, s, font=f, fill=fill)


def text_center(draw, box, s, f, fill=TEXT):
    x0, y0, x1, y1 = box
    bbox = draw.textbbox((0, 0), s, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0 - th) / 2), s, font=f, fill=fill)


def draw_header(draw, title, back=False, settings=False):
    panel(draw, 0, 0, SCREEN_W, UI_HEADER_H)
    text_left(draw, (8, 14), title, F_TITLE, TEXT)
    if back:
        outline_pill(draw, SCREEN_W - 76, 3, 72, 44, filled=False)
        text_center(draw, (SCREEN_W - 76, 3, SCREEN_W - 4, 47), "‹", F_SYM, ACCENT_DARK)
    if settings:
        outline_pill(draw, SCREEN_W - 74, 5, 68, 40, filled=False)
        # gear approximation (LV_SYMBOL_SETTINGS)
        cx, cy = SCREEN_W - 40, 25
        draw.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), outline=ACCENT_DARK, width=2)
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=PANEL, outline=ACCENT_DARK, width=1)
        for ang in range(0, 360, 45):
            import math

            rad = math.radians(ang)
            x0 = cx + int(5 * math.cos(rad))
            y0 = cy + int(5 * math.sin(rad))
            x1 = cx + int(10 * math.cos(rad))
            y1 = cy + int(10 * math.sin(rad))
            draw.line((x0, y0, x1, y1), fill=ACCENT_DARK, width=2)


def draw_nav_btn(draw, x, y, w, h, label, filled=False):
    outline_pill(draw, x, y, w, h, filled=filled)
    fill = TEXT_ON_ACCENT if filled else TEXT
    if filled:
        text_center(draw, (x, y, x + w, y + h), label, F_BODY, fill)
    else:
        text_left(draw, (x + 12, y + (h - 18) // 2), label, F_BODY, fill)


def draw_info_row(draw, x, y, w, h, name, value):
    panel(draw, x, y, w, h)
    text_left(draw, (x + 8, y + (h - 18) // 2), name, F_BODY, TEXT)
    bbox = draw.textbbox((0, 0), value, font=F_SMALL)
    tw = bbox[2] - bbox[0]
    draw.text((x + w - 10 - tw, y + (h - 14) // 2), value, font=F_SMALL, fill=TEXT_SEC)


def draw_switch_row(draw, x, y, w, h, name, on=True):
    panel(draw, x, y, w, h)
    text_left(draw, (x + 8, y + (h - 18) // 2), name, F_BODY, TEXT)
    sw_w, sw_h = 44, 24
    sx = x + w - 14 - sw_w
    sy = y + (h - sw_h) // 2
    rounded_rect(draw, (sx, sy, sx + sw_w, sy + sw_h), 12, ACCENT if on else PANEL_BORDER, None)
    knob = 20
    kx = sx + sw_w - knob - 2 if on else sx + 2
    draw.ellipse((kx, sy + 2, kx + knob, sy + 2 + knob), fill=TEXT_ON_ACCENT)


def save(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    big = img.resize((SCREEN_W * SCALE, SCREEN_H * SCALE), Image.Resampling.NEAREST)
    path = OUT / name
    big.save(path, "PNG")
    print(f"wrote {path}")


def render_home():
    img, d = new_screen()
    draw_header(d, "Sala Frequencies", settings=True)

    # Now Playing panel
    y = UI_HEADER_H + 4
    w = SCREEN_W - UI_MAIN_MARGIN * 2
    panel(d, UI_MAIN_MARGIN, y, w, UI_NOW_PLAY_H)
    text_left(d, (UI_MAIN_MARGIN + 10, y + 8), "Now Playing", F_SMALL, ACCENT_DARK)
    text_left(d, (UI_MAIN_MARGIN + 10, y + 26), "Ocean Drift", F_TITLE, TEXT)
    text_left(d, (UI_MAIN_MARGIN + 10, y + 48), "1:24 / 8:00", F_SMALL, TEXT_SEC)

    # Track list panel
    ly = UI_HEADER_H + UI_NOW_PLAY_H + UI_SECTION_GAP + 4
    panel(d, UI_MAIN_MARGIN, ly, w, UI_LIST_H)
    tracks = [("Ocean Drift", True), ("Forest Path", False), ("Still Water", False)]
    row_y = ly + 8
    for name, active in tracks:
        rx, ry, rw, rh = UI_MAIN_MARGIN + 8, row_y, w - 16, UI_TRACK_ROW_H - 4
        fill = TRACK_ACTIVE if active else PANEL
        outline = ACCENT if active else PANEL_BORDER
        rounded_rect(d, (rx, ry, rx + rw, ry + rh), 10, fill, outline, 1)
        text_left(d, (rx + 10, ry + 8), name, F_BODY, TEXT)
        row_y += UI_TRACK_ROW_H

    # Controls
    cy = SCREEN_H - UI_CONTROLS_H - 6
    panel(d, UI_MAIN_MARGIN, cy, w, UI_CONTROLS_H)
    # prev (up)
    px = UI_MAIN_MARGIN + 8
    py = cy + (UI_CONTROLS_H - UI_BTN_PREV_H) // 2
    outline_pill(d, px, py, UI_BTN_PREV_W, UI_BTN_PREV_H, False)
    text_center(d, (px, py, px + UI_BTN_PREV_W, py + UI_BTN_PREV_H), "▲", F_TITLE, ACCENT_DARK)
    # next (down)
    nx = UI_MAIN_MARGIN + w - 8 - UI_BTN_NEXT_W
    outline_pill(d, nx, py, UI_BTN_NEXT_W, UI_BTN_NEXT_H, False)
    text_center(d, (nx, py, nx + UI_BTN_NEXT_W, py + UI_BTN_NEXT_H), "▼", F_TITLE, ACCENT_DARK)
    # play (filled accent) — STOP symbol while playing matches UI when active
    play_x = UI_MAIN_MARGIN + (w - UI_BTN_PLAY_W) // 2
    play_y = cy + (UI_CONTROLS_H - UI_BTN_PLAY_H) // 2 - 2
    outline_pill(d, play_x, play_y, UI_BTN_PLAY_W, UI_BTN_PLAY_H, True)
    # stop square (playing state)
    s = 14
    cxp = play_x + UI_BTN_PLAY_W // 2
    cyp = play_y + UI_BTN_PLAY_H // 2
    d.rectangle((cxp - s // 2, cyp - s // 2, cxp + s // 2, cyp + s // 2), fill=TEXT_ON_ACCENT)

    save(img, "manual-now-playing.png")


def render_settings():
    # Settings body scrolls on device — export full list height so the manual shows every row.
    rows = [
        ("switch", "WiFi"),
        ("nav", "WiFi: Connected"),
        ("nav", "Display Settings"),
        ("nav", "Library"),
        ("nav", "Check for Updates"),
        ("nav", "Information"),
    ]
    content_h = 8 + len(rows) * (UI_SETTINGS_ROW_H + 8)
    h = UI_HEADER_H + content_h + 8
    img = Image.new("RGB", (SCREEN_W, h), BG)
    d = ImageDraw.Draw(img)
    draw_header(d, "Settings", back=True)
    x, y = 12, UI_HEADER_H + 8
    w = SCREEN_W - 24
    for kind, label in rows:
        if kind == "switch":
            draw_switch_row(d, x, y, w, UI_SETTINGS_ROW_H, label, on=True)
        else:
            draw_nav_btn(d, x, y, w, UI_SETTINGS_ROW_H, label, filled=False)
        y += UI_SETTINGS_ROW_H + 8
    save(img, "manual-settings.png")


def render_wifi():
    img, d = new_screen()
    draw_header(d, "Select Network", back=True)
    x, y = 8, UI_HEADER_H + 8
    w = SCREEN_W - 16
    draw_info_row(d, x, y, w, UI_SETTINGS_ROW_H, "WiFi", "Home Network")
    y += UI_SETTINGS_ROW_H + 6
    draw_switch_row(d, x, y, w, UI_SETTINGS_ROW_H, "WiFi", on=True)
    y += UI_SETTINGS_ROW_H + 6
    draw_nav_btn(d, x, y, w, UI_SETTINGS_ROW_H, "Scan Networks", filled=False)
    y += UI_SETTINGS_ROW_H + 8
    # network list wrap
    list_h = SCREEN_H - y - 4
    panel(d, 8, y, SCREEN_W - 16, list_h)
    ny = y + 8
    for name in ("Home Network", "Studio Guest", "SALA Office"):
        rounded_rect(d, (16, ny, SCREEN_W - 16, ny + 34), 10, PANEL, PANEL_BORDER, 1)
        text_left(d, (26, ny + 8), name, F_BODY, TEXT)
        ny += 40
    save(img, "manual-wifi.png")


def render_updates():
    img, d = new_screen()
    draw_header(d, "Updates", back=True)
    x, y = 12, UI_HEADER_H + 8
    w = SCREEN_W - 24
    # check label
    msg = "Update available"
    bbox = d.textbbox((0, 0), msg, font=F_BODY)
    tw = bbox[2] - bbox[0]
    d.text(((SCREEN_W - tw) / 2, y), msg, font=F_BODY, fill=TEXT_SEC)
    y += 24

    # Firmware package panel
    panel(d, x, y, w, 78)
    text_left(d, (x + 8, y + 6), "Firmware", F_BODY, TEXT)
    cols = ["Installed", "Online", "Local"]
    vals = ["1.0.0", "1.0.0", "-"]
    for i, (h, v) in enumerate(zip(cols, vals)):
        cx = x + 12 + i * 72
        text_center(d, (cx, y + 28, cx + 64, y + 44), h, F_SMALL, TEXT_SEC)
        text_center(d, (cx, y + 48, cx + 64, y + 66), v, F_SMALL, ACCENT_DARK)
    y += 86

    draw_nav_btn(d, x, y, w, UI_SETTINGS_ROW_H, "Upgrade Online", filled=True)
    y += UI_SETTINGS_ROW_H + 8
    draw_nav_btn(d, x, y, w, UI_SETTINGS_ROW_H, "Upgrade Local", filled=True)
    y += UI_SETTINGS_ROW_H + 12

    warn = "Do not turn off power during\ndownload or install."
    # wrap manually
    for i, line in enumerate(warn.split("\n")):
        bbox = d.textbbox((0, 0), line, font=F_TITLE)
        tw = bbox[2] - bbox[0]
        d.text(((SCREEN_W - tw) / 2, y + i * 20), line, font=F_TITLE, fill=ERROR)

    save(img, "manual-updates.png")


def render_library():
    img, d = new_screen()
    draw_header(d, "Library", back=True)
    x, y = 12, UI_HEADER_H + 8
    w = SCREEN_W - 24
    draw_nav_btn(d, x, y, w, UI_SETTINGS_ROW_H, "On this player", filled=False)
    y += UI_SETTINGS_ROW_H + 8
    draw_nav_btn(d, x, y, w, UI_SETTINGS_ROW_H, "Get music", filled=False)
    save(img, "manual-library.png")


def render_display():
    img, d = new_screen()
    draw_header(d, "Display Settings", back=True)
    x, y = 12, UI_HEADER_H + 8
    w = SCREEN_W - 24
    draw_switch_row(d, x, y, w, UI_SETTINGS_ROW_H, "Dark Mode", on=False)
    y += UI_SETTINGS_ROW_H + 8
    draw_info_row(d, x, y, w, UI_SETTINGS_ROW_H, "Timeout", "2 min")
    y += UI_SETTINGS_ROW_H + 8
    # timeout slider
    rounded_rect(d, (x, y + 10, x + w, y + 18), 4, PANEL_BORDER, None)
    rounded_rect(d, (x, y + 10, x + int(w * 0.35), y + 18), 4, ACCENT, None)
    kn = x + int(w * 0.35)
    d.ellipse((kn - 8, y + 4, kn + 8, y + 24), fill=ACCENT_DARK)
    y += 36
    draw_info_row(d, x, y, w, UI_SETTINGS_ROW_H, "Brightness", "85%")
    y += UI_SETTINGS_ROW_H + 8
    rounded_rect(d, (x, y + 10, x + w, y + 18), 4, PANEL_BORDER, None)
    rounded_rect(d, (x, y + 10, x + int(w * 0.85), y + 18), 4, ACCENT, None)
    kn = x + int(w * 0.85)
    d.ellipse((kn - 8, y + 4, kn + 8, y + 24), fill=ACCENT_DARK)
    save(img, "manual-display.png")


def render_splash():
    img, d = new_screen()
    bbox = d.textbbox((0, 0), "Sala Frequencies", font=F_HERO)
    tw = bbox[2] - bbox[0]
    d.text(((SCREEN_W - tw) / 2, SCREEN_H // 2 - 28), "Sala Frequencies", font=F_HERO, fill=TEXT)
    bbox = d.textbbox((0, 0), "Music Player", font=F_HERO)
    tw = bbox[2] - bbox[0]
    d.text(((SCREEN_W - tw) / 2, SCREEN_H // 2 + 8), "Music Player", font=F_HERO, fill=ACCENT_DARK)
    save(img, "manual-splash.png")


def render_update_flow():
    """Composite strip: Settings gear → WiFi → Updates → progress — actual UI chrome."""
    # three mini screens side by side
    names = []
    # reuse already-rendered full screens scaled down into a strip
    parts = []
    for fn, label in (
        ("manual-settings.png", "1. Settings"),
        ("manual-wifi.png", "2. Wi‑Fi"),
        ("manual-updates.png", "3. Upgrade Online"),
    ):
        p = OUT / fn
        if p.exists():
            parts.append((Image.open(p), label))

    if not parts:
        return

    # progress / updating screen mini
    img, d = new_screen()
    draw_header(d, "Updating", back=False)
    text_center(d, (0, 70, SCREEN_W, 95), "Installing update...", F_BODY, TEXT)
    panel(d, 12, 110, SCREEN_W - 24, 70)
    text_left(d, (20, 118), "DOWNLOAD", F_SMALL, TEXT_SEC)
    rounded_rect(d, (20, 140, SCREEN_W - 20, 152), 4, PANEL_BORDER, None)
    rounded_rect(d, (20, 140, 20 + int((SCREEN_W - 40) * 1.0), 152), 4, ACCENT, None)
    text_center(d, (0, 158, SCREEN_W, 178), "100%", F_SMALL, TEXT)
    panel(d, 12, 190, SCREEN_W - 24, 70)
    text_left(d, (20, 198), "INSTALL", F_SMALL, TEXT_SEC)
    rounded_rect(d, (20, 220, SCREEN_W - 20, 232), 4, PANEL_BORDER, None)
    rounded_rect(d, (20, 220, 20 + int((SCREEN_W - 40) * 0.6), 232), 4, ACCENT, None)
    text_center(d, (0, 238, SCREEN_W, 258), "60%", F_SMALL, TEXT)
    warn = "Do not turn off power during download or install."
    # wrap
    words = warn.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textbbox((0, 0), t, font=F_SMALL)[2] > SCREEN_W - 20:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    yy = 275
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=F_SMALL)
        tw = bbox[2] - bbox[0]
        d.text(((SCREEN_W - tw) / 2, yy), line, font=F_SMALL, fill=ERROR)
        yy += 14
    save(img, "manual-updating.png")
    parts.append((Image.open(OUT / "manual-updating.png"), "4. Updating"))

    pad = 24
    label_h = 36
    thumb_h = 280
    thumb_w = int(thumb_h * SCREEN_W / SCREEN_H)
    total_w = len(parts) * thumb_w + (len(parts) + 1) * pad
    total_h = thumb_h + label_h + pad * 2
    strip = Image.new("RGB", (total_w, total_h), BG)
    sd = ImageDraw.Draw(strip)
    x = pad
    for im, label in parts:
        thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        # thin device frame
        sd.rounded_rectangle(
            (x - 3, pad - 3, x + thumb_w + 2, pad + thumb_h + 2),
            radius=8,
            outline=PANEL_BORDER,
            width=2,
            fill=PANEL,
        )
        strip.paste(thumb, (x, pad))
        bbox = sd.textbbox((0, 0), label, font=F_BODY)
        tw = bbox[2] - bbox[0]
        sd.text((x + (thumb_w - tw) / 2, pad + thumb_h + 8), label, font=F_BODY, fill=ACCENT_DARK)
        x += thumb_w + pad
    strip.save(OUT / "manual-update-flow.png")
    print(f"wrote {OUT / 'manual-update-flow.png'}")


def main():
    render_home()
    render_settings()
    render_wifi()
    render_updates()
    render_library()
    render_display()
    render_splash()
    render_update_flow()


if __name__ == "__main__":
    main()
