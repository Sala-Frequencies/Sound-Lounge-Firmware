#!/usr/bin/env python3
"""Build the Sala Frequencies Music Player user manual PDF."""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(__file__).resolve().parent / "assets"
OUT = Path(__file__).resolve().parent / "Sala_Frequencies_Music_Player_User_Guide.pdf"

# Match Sound_Lounge_UI_Next light theme (factory default).
ACCENT = HexColor("#A67355")
ACCENT_DARK = HexColor("#8B5D43")
TEXT = HexColor("#1A1A1A")
SOFT = HexColor("#FAF6F2")
MUTED = HexColor("#5C534A")
WARN = HexColor("#B85C5C")
LINE = HexColor("#E5E7EB")
PANEL = HexColor("#FFFFFF")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_brand": ParagraphStyle(
            "cover_brand",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            textColor=ACCENT_DARK,
            alignment=TA_CENTER,
            spaceAfter=6,
            leading=34,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=TEXT,
            alignment=TA_CENTER,
            spaceAfter=8,
            leading=28,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=4,
            leading=16,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=ACCENT_DARK,
            spaceBefore=0,
            spaceAfter=10,
            leading=22,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=TEXT,
            spaceBefore=12,
            spaceAfter=6,
            leading=16,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            textColor=TEXT,
            leading=15,
            spaceAfter=6,
        ),
        "step": ParagraphStyle(
            "step",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            textColor=TEXT,
            leading=15,
            leftIndent=4,
            spaceAfter=3,
        ),
        "tip": ParagraphStyle(
            "tip",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=ACCENT_DARK,
            leading=14,
            spaceAfter=6,
        ),
        "warn": ParagraphStyle(
            "warn",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=WARN,
            leading=14,
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=10,
        ),
        "toc": ParagraphStyle(
            "toc",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            textColor=TEXT,
            leading=18,
            leftIndent=8,
            spaceAfter=2,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "menu": ParagraphStyle(
            "menu",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=TEXT,
            leading=14,
        ),
    }


def banner(text, S):
    data = [[Paragraph(f"<b>{text}</b>", ParagraphStyle("b", parent=S["body"], textColor=white, alignment=TA_CENTER))]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return t


def callout(text, S, kind="tip"):
    style = S["tip"] if kind == "tip" else S["warn"]
    bg = HexColor("#F3E8E0") if kind == "tip" else HexColor("#F8E8E8")
    data = [[Paragraph(text, style)]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.5, ACCENT if kind == "tip" else WARN),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def img(name, max_w=None, max_h=None):
    path = ASSETS / name
    if not path.exists():
        return Paragraph(f"[Missing image: {name}]", styles()["caption"])
    im = Image(str(path))
    iw, ih = im.imageWidth, im.imageHeight
    max_w = max_w or (PAGE_W - 2 * MARGIN)
    max_h = max_h or 95 * mm
    scale = min(max_w / iw, max_h / ih, 1.0)
    im.drawWidth = iw * scale
    im.drawHeight = ih * scale
    return im


def two_col_images(left, right, cap_l, cap_r, S, max_h=78 * mm):
    col_w = (PAGE_W - 2 * MARGIN - 8 * mm) / 2
    a = img(left, max_w=col_w, max_h=max_h)
    b = img(right, max_w=col_w, max_h=max_h)
    t = Table(
        [
            [a, b],
            [Paragraph(cap_l, S["caption"]), Paragraph(cap_r, S["caption"])],
        ],
        colWidths=[col_w + 4 * mm, col_w + 4 * mm],
    )
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return t


def steps(items, S):
    flow = []
    for i, text in enumerate(items, 1):
        flow.append(Paragraph(f"<b>{i}.</b>  {text}", S["step"]))
    return flow


def menu_map_table(S):
    rows = [
        [Paragraph("<b>Screen</b>", S["menu"]), Paragraph("<b>What you can do</b>", S["menu"])],
        [Paragraph("Home", S["menu"]), Paragraph("See Now Playing, browse tracks, play / pause, scroll the list", S["menu"])],
        [Paragraph("Settings", S["menu"]), Paragraph("Wi‑Fi, display, library, updates, information", S["menu"])],
        [Paragraph("Select Network", S["menu"]), Paragraph("Turn Wi‑Fi on, scan, choose a network", S["menu"])],
        [Paragraph("WiFi Password", S["menu"]), Paragraph("Enter password and Connect &amp; Save", S["menu"])],
        [Paragraph("Display Settings", S["menu"]), Paragraph("Dark Mode, screen timeout, brightness", S["menu"])],
        [Paragraph("Library", S["menu"]), Paragraph("Manage songs on the player or download new ones", S["menu"])],
        [Paragraph("Updates", S["menu"]), Paragraph("Upgrade Online or Upgrade Local (SD card)", S["menu"])],
        [Paragraph("Information", S["menu"]), Paragraph("Version details and Factory Reset", S["menu"])],
    ]
    t = Table(rows, colWidths=[42 * mm, PAGE_W - 2 * MARGIN - 42 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, 1), SOFT),
                ("BACKGROUND", (0, 3), (-1, 3), SOFT),
                ("BACKGROUND", (0, 5), (-1, 5), SOFT),
                ("BACKGROUND", (0, 7), (-1, 7), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    # Fix header text color for Paragraphs
    rows[0][0] = Paragraph("<b>Screen</b>", ParagraphStyle("mh", parent=S["menu"], textColor=white))
    rows[0][1] = Paragraph("<b>What you can do</b>", ParagraphStyle("mh2", parent=S["menu"], textColor=white))
    t = Table(rows, colWidths=[42 * mm, PAGE_W - 2 * MARGIN - 42 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                ("BACKGROUND", (0, 1), (-1, 1), SOFT),
                ("BACKGROUND", (0, 3), (-1, 3), SOFT),
                ("BACKGROUND", (0, 5), (-1, 5), SOFT),
                ("BACKGROUND", (0, 7), (-1, 7), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(ACCENT)
    canvas.rect(0, PAGE_H - 6 * mm, PAGE_W, 6 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 10 * mm, "Sala Frequencies · Music Player User Guide")
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def on_first(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, PAGE_W, 28 * mm, fill=1, stroke=0)
    canvas.rect(0, PAGE_H - 28 * mm, PAGE_W, 28 * mm, fill=1, stroke=0)
    canvas.restoreState()


def build():
    S = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Sala Frequencies Music Player User Guide",
        author="Sala Frequencies",
    )
    story = []

    # Cover
    story.append(Spacer(1, 42 * mm))
    story.append(Paragraph("SALA FREQUENCIES", S["cover_brand"]))
    story.append(Paragraph("Music Player", S["cover_title"]))
    story.append(Paragraph("User Guide", S["cover_title"]))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Play music · Manage your library · Stay up to date", S["cover_sub"]))
    story.append(Paragraph("Firmware version <b>1.0.0</b>", S["cover_sub"]))
    story.append(Spacer(1, 10 * mm))
    story.append(
        two_col_images(
            "manual-splash.png",
            "manual-now-playing.png",
            "Startup splash",
            "Home — Now Playing",
            S,
            max_h=88 * mm,
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("salanewcastle.com.au · info@sala.au · Newcastle, NSW", S["cover_sub"]))
    story.append(PageBreak())

    # Contents
    story.append(banner("Contents", S))
    story.append(Spacer(1, 6 * mm))
    for line in [
        "1. Welcome &amp; quick start",
        "2. Playing music",
        "3. Settings at a glance",
        "4. Wi‑Fi setup",
        "5. Display settings",
        "6. Music library",
        "7. Online updates (recommended)",
        "8. SD card updates",
        "9. Information &amp; Factory Reset",
        "10. Helpful tips",
    ]:
        story.append(Paragraph(line, S["toc"]))
    story.append(Spacer(1, 8 * mm))
    story.append(callout("Tip: Use the gear icon on the home screen to open Settings.", S))
    story.append(PageBreak())

    # 1 Welcome
    story.append(banner("1. Welcome & quick start", S))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "When you switch the music player on, you will see the <b>Sala Frequencies</b> splash screen, "
            "then the home screen with <b>Now Playing</b>, your track list, and playback controls.",
            S["body"],
        )
    )
    story.append(Paragraph("<b>Quick start</b>", S["h2"]))
    story.extend(
        steps(
            [
                "Switch the player on and wait for the home screen.",
                "Tap a track in the list to select it (highlight only).",
                "Tap the large <b>Play</b> button to start.",
                "Tap <b>Play</b> again to pause; tap once more to resume.",
                "Use the up / down buttons to scroll through the track list.",
                "Tap the <b>gear</b> icon (top right) for Settings, Wi‑Fi, Library, and Updates.",
            ],
            S,
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(two_col_images("manual-now-playing.png", "manual-settings.png", "Home — Now Playing", "Settings menu", S))
    story.append(PageBreak())

    # 2 Playing
    story.append(banner("2. Playing music", S))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("<b>Home screen layout</b>", S["h2"]))
    story.extend(
        steps(
            [
                "<b>Sala Frequencies</b> header — gear opens Settings.",
                "<b>Now Playing</b> — current track name and elapsed / total time.",
                "<b>Track list</b> — tap a row to select it. Selecting alone does not start playback.",
                "<b>Controls</b> — up/down scroll the list; centre button plays, pauses, or switches to the selected track.",
            ],
            S,
        )
    )
    story.append(Paragraph("<b>Playback tips</b>", S["h2"]))
    story.append(
        Paragraph(
            "• Opening Settings or browsing menus does not change whether music is playing.<br/>"
            "• To switch songs: select the new track, then press Play.<br/>"
            "• If the list shows “Loading music…”, wait a moment for tracks to appear from the player’s storage.<br/>"
            "• While music is playing, the centre button shows a stop square; when paused it shows play.",
            S["body"],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(img("manual-now-playing.png", max_w=70 * mm, max_h=95 * mm))
    story.append(Paragraph("Home screen — layout matches the player display (240×320)", S["caption"]))
    story.append(PageBreak())

    # 3 Settings map
    story.append(banner("3. Settings at a glance", S))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "From the home screen, tap the gear icon. Settings includes:",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "• <b>WiFi</b> switch — turn wireless on or off<br/>"
            "• <b>WiFi Settings</b> — scan and connect to a network<br/>"
            "• <b>Display Settings</b> — dark mode, timeout, brightness<br/>"
            "• <b>Library</b> — songs on this player and download new music<br/>"
            "• <b>Check for Updates</b> — online or SD card firmware updates<br/>"
            "• <b>Information</b> — versions and Factory Reset",
            S["body"],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(menu_map_table(S))
    story.append(Spacer(1, 3 * mm))
    story.append(img("manual-settings.png", max_w=70 * mm, max_h=95 * mm))
    story.append(Paragraph("Settings — same labels and button style as on the player", S["caption"]))
    story.append(Paragraph("Use the back arrow (top right) on any menu to return one step.", S["body"]))
    story.append(PageBreak())

    # 4 WiFi
    story.append(banner("4. Wi‑Fi setup", S))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Wi‑Fi is needed for <b>online updates</b> and for <b>Get music</b> downloads. "
            "You only need to set it up once; the player remembers your network.",
            S["body"],
        )
    )
    story.append(Paragraph("<b>Connect step by step</b>", S["h2"]))
    story.extend(
        steps(
            [
                "Open <b>Settings</b> (gear on the home screen).",
                "Turn the <b>WiFi</b> switch on.",
                "Tap <b>WiFi Settings</b> to open <b>Select Network</b>.",
                "Tap <b>Scan Networks</b> and wait for the list.",
                "Tap your network name.",
                "On <b>WiFi Password</b>, type the password on the on-screen keyboard.",
                "Tap <b>Connect &amp; Save</b> (or the keyboard checkmark).",
                "Wait for a status such as <b>Connected: your-network</b>.",
            ],
            S,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(img("manual-wifi.png", max_w=85 * mm, max_h=100 * mm))
    story.append(Paragraph("Select Network — scan and choose your Wi‑Fi", S["caption"]))
    story.append(
        callout(
            "If connection fails: check the password, move closer to the router, then try Scan Networks again.",
            S,
            "tip",
        )
    )
    story.append(
        Paragraph(
            "The Settings row shows <b>WiFi: Connected</b>, <b>WiFi: Off (saved)</b>, or <b>WiFi Setup</b> "
            "so you can see the current state at a glance.",
            S["body"],
        )
    )
    story.append(PageBreak())

    # 5 Display
    story.append(banner("5. Display settings", S))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Path: <b>Settings → Display Settings</b>",
            S["body"],
        )
    )
    story.extend(
        steps(
            [
                "<b>Dark Mode</b> — switch between light and dark appearance.",
                "<b>Timeout</b> — how long the screen stays awake after you stop touching it. Drag the slider to change.",
                "<b>Brightness</b> — drag the slider; the percentage updates as you move it.",
            ],
            S,
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(img("manual-display.png", max_w=70 * mm, max_h=95 * mm))
    story.append(Paragraph("Display Settings — Dark Mode, Timeout, Brightness", S["caption"]))
    story.append(callout("Changes apply immediately and are remembered the next time you use the player.", S))
    story.append(PageBreak())

    # 6 Library
    story.append(banner("6. Music library", S))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Path: <b>Settings → Library</b>", S["body"]))
    story.append(img("manual-library.png", max_w=70 * mm, max_h=80 * mm))
    story.append(Paragraph("Library hub — On this player / Get music", S["caption"]))
    story.append(
        Paragraph(
            "The Library hub has two choices:",
            S["body"],
        )
    )
    story.append(Paragraph("<b>On this player</b>", S["h2"]))
    story.append(
        Paragraph(
            "Browse songs already stored on the player. Use <b>Previous</b> / <b>Next</b> to move between tracks. "
            "Tap <b>Remove song</b> to delete the song currently shown. "
            "Removed songs disappear from the home-screen list after a short refresh.",
            S["body"],
        )
    )
    story.append(Paragraph("<b>Get music</b>", S["h2"]))
    story.append(
        Paragraph(
            "Download new songs when Wi‑Fi is connected.",
            S["body"],
        )
    )
    story.extend(
        steps(
            [
                "Turn <b>WiFi</b> on and make sure you are connected.",
                "Open <b>Library → Get music</b>.",
                "Wait while the player checks for available songs.",
                "Use <b>Previous</b> / <b>Next</b> to browse, then <b>Select</b> the song you want.",
                "Tap <b>Download</b>.",
                "On <b>Confirm download</b>, review the estimate, then tap <b>Start download</b> — or <b>Back</b> to cancel.",
                "Keep power on while the <b>Updating</b> screen shows download progress. You can tap <b>Cancel download</b> if needed.",
            ],
            S,
        )
    )
    story.append(
        callout(
            "If you see “Turn WiFi on first” or “No new songs available”, fix the connection or check again later.",
            S,
        )
    )
    story.append(PageBreak())

    # 7 Online updates
    story.append(banner("7. Online updates (recommended)", S))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "When Wi‑Fi is connected, the player can download the latest software automatically. "
            "Current package version on the official update channel: <b>1.0.0</b>.",
            S["body"],
        )
    )
    story.append(img("manual-update-flow.png", max_w=PAGE_W - 2 * MARGIN, max_h=42 * mm))
    story.append(Paragraph("Online update path — Settings → Wi‑Fi → Upgrade Online", S["caption"]))
    story.append(Paragraph("<b>Steps</b>", S["h2"]))
    story.extend(
        steps(
            [
                "Connect to Wi‑Fi (see section 4).",
                "Open <b>Settings → Check for Updates</b>.",
                "Wait for <b>Checking for Updates, please wait</b> to finish.",
                "Compare the <b>Installed</b>, <b>Online</b>, and <b>Local</b> version columns.",
                "If an online update is available, tap <b>Upgrade Online</b>.",
                "Leave the player powered on through the <b>Updating</b> screen (download, then install). The screen restarts when finished.",
            ],
            S,
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(img("manual-updates.png", max_w=85 * mm, max_h=95 * mm))
    story.append(Paragraph("Updates screen — Upgrade Online / Upgrade Local", S["caption"]))
    story.append(
        callout(
            "Do not turn off power during download or install. Keep the player plugged in until the home screen returns.",
            S,
            "warn",
        )
    )
    story.append(PageBreak())

    # 8 SD updates
    story.append(banner("8. SD card updates", S))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Use this when Wi‑Fi is unavailable, or when you prefer to prepare the update on a computer first.",
            S["body"],
        )
    )
    story.append(Paragraph("<b>A. Download the package on a computer</b>", S["h2"]))
    story.append(
        Paragraph(
            "Open the official firmware page and download <b>manifest.txt</b> plus every "
            "<b>.bin</b> file named in that file (same folder):",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "<link href='https://github.com/Sala-Frequencies/Sound-Lounge-Firmware'>"
            "github.com/Sala-Frequencies/Sound-Lounge-Firmware</link>",
            S["tip"],
        )
    )
    story.append(Paragraph("<b>B. Copy files onto the microSD card</b>", S["h2"]))
    story.extend(
        steps(
            [
                "Switch the music player <b>completely off</b> before removing or inserting the microSD card.",
                "Remove the card and insert it into your computer.",
                "At the root of the card, create or open a folder named <b>firmware</b>.",
                "Copy <b>manifest.txt</b> and all matching <b>.bin</b> files into that <b>firmware</b> folder.",
                "Safely eject the card, put it back in the player, then switch the player on.",
            ],
            S,
        )
    )
    story.append(Paragraph("<b>C. Install from the card</b>", S["h2"]))
    story.extend(
        steps(
            [
                "Open <b>Settings → Check for Updates</b>.",
                "Wait for the version check to finish. The <b>Local</b> column should show the package version from the card.",
                "Tap <b>Upgrade Local</b>.",
                "Leave power on until install finishes and the screen restarts.",
            ],
            S,
        )
    )
    story.append(
        callout(
            "Always remove or insert the microSD card only while the music player is switched off. "
            "Copy the complete package — a partial copy can fail.",
            S,
            "warn",
        )
    )
    story.append(PageBreak())

    # 9 Information
    story.append(banner("9. Information & Factory Reset", S))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Path: <b>Settings → Information</b>", S["body"]))
    story.append(
        Paragraph(
            "This screen shows useful status for support and updates:",
            S["body"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Temperature</b><br/>"
            "• <b>Player ID</b><br/>"
            "• <b>Music Player UI</b> version<br/>"
            "• <b>Music Player Sound</b> version<br/>"
            "• <b>Sound Lounge</b> version<br/>"
            "• <b>Player HW</b> / <b>Lounge HW</b> revision labels",
            S["body"],
        )
    )
    story.append(Paragraph("<b>Factory Reset</b>", S["h2"]))
    story.append(
        Paragraph(
            "Factory Reset clears saved preferences on the display (for example Wi‑Fi settings and display options). "
            "It does not remove your music library from the player’s storage.",
            S["body"],
        )
    )
    story.extend(
        steps(
            [
                "Open <b>Information</b>.",
                "Tap <b>Factory Reset</b> once — the button changes to <b>Tap again to confirm</b>.",
                "Tap again within a few seconds to confirm. The button shows <b>Resetting...</b>, then preferences are cleared.",
            ],
            S,
        )
    )
    story.append(callout("You will need to set up Wi‑Fi again after a factory reset if you use online features.", S))
    story.append(PageBreak())

    # 10 Tips
    story.append(banner("10. Helpful tips", S))
    story.append(Spacer(1, 4 * mm))
    tips = [
        (
            "No update offered",
            "You may already be on the latest version, or the SD <b>firmware</b> folder may be missing or incomplete.",
        ),
        (
            "Online update fails",
            "Check Wi‑Fi signal and password, then try again — or use the SD card method in section 8.",
        ),
        (
            "Update seems stuck",
            "Leave power connected for several minutes. If nothing changes, power-cycle once, then check "
            "<b>Settings → Information</b> for the installed version before trying again.",
        ),
        (
            "Cannot get music",
            "Turn Wi‑Fi on and confirm Connected, then open <b>Library → Get music</b> again.",
        ),
        (
            "Screen went dark",
            "Tap the screen to wake it. Adjust Timeout and Brightness under Display Settings if needed.",
        ),
    ]
    for title, body in tips:
        story.append(Paragraph(f"<b>{title}</b>", S["h2"]))
        story.append(Paragraph(body, S["body"]))

    story.append(Spacer(1, 8 * mm))
    story.append(banner("Need help?", S))
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "SALA Frequencies — Newcastle, NSW, Australia<br/>"
            "<link href='https://www.salanewcastle.com.au/'>salanewcastle.com.au</link> · "
            "<link href='mailto:info@sala.au'>info@sala.au</link><br/><br/>"
            "Firmware updates: "
            "<link href='https://github.com/Sala-Frequencies/Sound-Lounge-Firmware'>"
            "github.com/Sala-Frequencies/Sound-Lounge-Firmware</link>",
            S["body"],
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("© Sala Frequencies · User Guide for firmware 1.0.0", S["caption"]))

    doc.build(story, onFirstPage=on_first, onLaterPages=on_page)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
