# Sala Frequencies — firmware updates

This repository hosts official firmware updates for the **Sala Frequencies** music player. You do not need a GitHub account to download files or to update a player that is already set up for online updates.

**Current firmware version:** **0.15.09**

---

## Where the firmware lives

The **current** update package is always in the **root** of this repository on the `main` branch:

| File | Purpose |
|------|---------|
| [`manifest.txt`](manifest.txt) | Package index — lists version and every `.bin` file |
| `music_player_ui_<version>.bin` | Music player touchscreen (ESP32) |
| `music_player_sound_<version>.bin` | Music player sound module (Teensy) |
| `sound_lounge_<version>.bin` | Sound Lounge zones module (Teensy) |

Browse or download everything from the [main branch folder](https://github.com/FlashAeronautica/Sound-Lounge-Firmware/tree/main).

**Online updates** — the player checks this manifest automatically when Wi‑Fi is connected:

`https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/manifest.txt`

Individual `.bin` files are downloaded from the same folder using the names listed in `manifest.txt`.

**SD card updates** — copy `manifest.txt` and **all** listed `.bin` files into a folder named **`firmware`** on the player microSD card (see below).

Only the latest package is kept here. Older versions are not stored in this repository.

---

## Update over the air (recommended)

Use this when the player can connect to your Wi‑Fi network.

1. On the player screen, open **Settings**.
2. Turn **Wi‑Fi** on and connect to your network.
3. Open **Updates** and wait until the version check finishes.
4. If an update is available, choose **Upgrade Online**.
5. Leave the player **powered on** until the update completes and the screen restarts.

The player downloads the update, installs it, and reboots automatically. This can take several minutes.

---

## Update using an SD card

Use this when Wi‑Fi is unavailable, or when you prefer to prepare the update on a computer first.

### 1. Download the firmware package

On a computer, open the [firmware package on GitHub](https://github.com/FlashAeronautica/Sound-Lounge-Firmware/tree/main) and download:

- [`manifest.txt`](https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/manifest.txt)
- Every `.bin` file named in that manifest (same folder on GitHub)

Keep all downloaded files together in one folder on your computer.

### 2. Copy the package to the player SD card

1. Safely remove the **microSD card** from the music player.
2. Insert the card into your computer (USB adapter or card reader).
3. Open the card and find or create a folder named **`firmware`** at the root of the card.
4. Copy `manifest.txt` and all `.bin` files into that **`firmware`** folder.
5. Safely eject the card and put it back in the player.

### 3. Install from the SD card

1. On the player screen, open **Settings** → **Updates**.
2. Wait until the version check finishes.
3. Choose **Upgrade Local**.
4. Leave the player **powered on** until the update completes and the screen restarts.

---

## Before you update

- Keep the player **plugged into power** for the whole update.
- Do **not** remove the SD card or switch off power while the **Updating** screen is shown.
- If you use the SD card method, copy the **complete** package (`manifest.txt` plus all `.bin` files). A partial copy can fail or leave the player in a bad state.

---

## Problems?

- **No update offered** — the player may already be on the latest version, or the SD package may be missing or incomplete.
- **Online update fails** — check Wi‑Fi signal and password, then try again or use the SD card method.
- **Update stuck** — leave power connected for at least ten minutes. If nothing changes, power-cycle once and check **Settings** → **Information** for the installed version before trying again.

For product support, contact your Sala / Sound Lounge installer or visit [salanewcastle.com.au](https://www.salanewcastle.com.au/).
