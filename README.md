# Sound Lounge — public OTA firmware

Over-the-air update packages for the Sala Sound Lounge three-node system (ESP32 UI, Teensy Player, Teensy Zones).

**Current Next test version:** **0.15.03** (unified package — all three nodes same version).

Source code and build scripts live in the private [Sound-Lounge-Music](https://github.com/FlashAeronautica/Sound-Lounge-Music) repository. This repo holds **binaries only** so devices can download updates without GitHub authentication.

Every published Next package includes **all three firmware binaries at the same version**. The Music Player UI still installs only components that are older than the package; it does not apply unchanged nodes.

## Folders

| Folder | Use |
|--------|-----|
| `next/` | Sala Frequencies **Next** test channel (`Sound_Lounge_*_Next` sketches) |
| `release/` | Production channel — field rollout |
| `staging/` | Pre-release / test bench channel |

Each folder contains a `manifest.txt` and the binary files referenced in that manifest (`music_player_ui_*.bin`, `music_player_sound_*.bin`, `sound_lounge_*.bin`).

The root `manifest.txt` matches the **release** channel.

A manifest may omit keys for legacy SD packages. **New Next OTA releases must list all three nodes** (`music_player_ui`, `music_player_sound`, `sound_lounge`) at the **same version** as the top-level `version=` field.

## Manifest URLs (raw, no auth)

| Channel | URL |
|---------|-----|
| Next | https://api.github.com/repos/FlashAeronautica/Sound-Lounge-Firmware/contents/next?ref=main |
| Next raw | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/next/manifest.txt |
| Release | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/release/manifest.txt |
| Staging | https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/staging/manifest.txt |

## SD card mirror (optional offline install)

Copy the same files onto the **Box A Teensy 4.1** microSD:

```
/firmware/release/manifest.txt   + lounge_*_v*.bin   (production)
/firmware/staging/manifest.txt   + lounge_*_v*.bin   (testing)
/firmware/next/manifest.txt      + music_player_*.bin   (Next testing)
```

Next firmware verifies the SD package before attempting an Online download. WiFi is never turned on automatically for update checks or installs.

On the device, the UI labels the GitHub channel **Online** and the SD card package **Local**. **Upgrade Online** downloads to SD then installs in one step; **Upgrade Local** installs from SD only. See [NEXT_OPERATOR_UPDATE_GUIDE.md](https://github.com/FlashAeronautica/Sound-Lounge-Music/blob/main/docs/NEXT_OPERATOR_UPDATE_GUIDE.md) in the private Music repo.

## Install order (automatic)

1. Sound Lounge (Teensy 4.0), if selected / listed in manifest
2. Music Player Sound (Teensy 4.1), if selected / listed
3. Music Player UI (ESP32), if selected / listed — reboots last

The Music Player UI orchestrates this order when you tap **Upgrade Online** or **Upgrade Local** on the **Updates** screen. Sound Lounge updates require version verification after reboot.

## Publishing a Next test package

From the `Sound-Lounge-Music` repo on the PC:

1. Bump **`FIRMWARE_VERSION` to the same value** in all three `*_Next/Config.h` files (`Sound_Lounge_UI_Next`, `Sound_Lounge_Player_Next`, `Sound_Lounge_Zones_Next`).
2. `.\build_firmware_next.ps1` (optional `-Summary "Next OTA x.y.zz: change note"`)
3. Copy **all** `.bin` files from `firmware_next/` into this repo's `next/` folder.
4. Copy `firmware_next/manifest.txt` to `next/manifest.txt` (verify all three `*_version=` lines match `version=`).
5. Update the **Current Next test version** line in this README.
6. Commit and push to `main`.

Full detail: [Sound-Lounge-Music/docs/NEXT_FIRMWARE.md](https://github.com/FlashAeronautica/Sound-Lounge-Music/blob/main/docs/NEXT_FIRMWARE.md) (private repo).

## Node mapping

| Manifest key | Product name | MCU |
|--------------|--------------|-----|
| `music_player_ui` | Music Player UI | ESP32-S3 |
| `music_player_sound` | Music Player Sound | **Teensy 4.1** |
| `sound_lounge` | Sound Lounge | **Teensy 4.0** |

Legacy manifest keys (`esp32`, `teensy_a`, `teensy_b`) are still accepted by Next firmware for older SD packages.

Music Player Sound firmware rejects images with the wrong Teensy flash ID (`fw_teensy41` vs `fw_teensy40`).
