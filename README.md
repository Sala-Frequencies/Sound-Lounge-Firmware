# Sound Lounge — public OTA firmware

Over-the-air update packages for the Sala Sound Lounge three-node system (ESP32 UI, Teensy Player, Teensy Zones).

**Current published version:** **0.10.13** (release and staging channels).

**Current Next test version:** **0.12.8-next-salatweaks**.

Source code and build scripts live in the private [Sound-Lounge-Music](https://github.com/FlashAeronautica/Sound-Lounge-Music) repository. This repo holds **binaries only** so devices can download updates without GitHub authentication.

## Folders

| Folder | Use |
|--------|-----|
| `release/` | Production channel — field rollout |
| `staging/` | Pre-release / test bench channel |
| `next/` | Side-by-side Next firmware test channel |

Each folder contains a `manifest.txt` and the three binary files referenced in that manifest.

The root `manifest.txt` matches the **release** channel.

## Manifest URLs (raw, no auth)

| Channel | URL |
|---------|-----|
| Release | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/release/manifest.txt |
| Staging | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/staging/manifest.txt |
| Next | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/next/manifest.txt |

## SD card mirror (optional offline install)

Copy the same files onto the **Box A Teensy** microSD:

```
/firmware/release/manifest.txt   + lounge_*_v*.bin   (production)
/firmware/staging/manifest.txt   + lounge_*_v*.bin   (testing)
/firmware/next/manifest.txt      + lounge_*_next_v*.bin   (Next testing)
```

Devices with firmware **0.10.10+** verify the full SD package before attempting a GitHub download. WiFi is never turned on automatically for update checks or installs.

## Install order (automatic)

1. Zones (Teensy B)
2. Player (Teensy A)
3. UI (ESP32)

The ESP32 UI orchestrates this order when you tap **Install Updates** in Settings.
