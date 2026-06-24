# Sound Lounge — public OTA firmware

Over-the-air update packages for the Sala Sound Lounge three-node system (ESP32 UI, Teensy Player, Teensy Zones).

**Current Next test version:** **0.12.15-next-loungefix**.

Source code and build scripts live in the private [Sound-Lounge-Music](https://github.com/FlashAeronautica/Sound-Lounge-Music) repository. This repo holds **binaries only** so devices can download updates without GitHub authentication.

## Folders

| Folder | Use |
|--------|-----|
| `next/` | Current Sala Frequencies test channel |
| `release/` | Production channel — field rollout |
| `staging/` | Pre-release / test bench channel |

Each folder contains a `manifest.txt` and the binary files referenced in that manifest (`lounge_ui*_v*.bin`, `lounge_player*_v*.bin`, `lounge_zones*_v*.bin`).

The root `manifest.txt` matches the **release** channel.

## Manifest URLs (raw, no auth)

| Channel | URL |
|---------|-----|
| Next | https://api.github.com/repos/FlashAeronautica/Sound-Lounge-Firmware/contents/next?ref=main |
| Next raw | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/next/manifest.txt |
| Release | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/release/manifest.txt |
| Staging | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/staging/manifest.txt |

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
