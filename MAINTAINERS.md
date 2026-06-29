# Maintainer notes — Sound-Lounge-Firmware

Customer-facing instructions: [README.md](README.md).

Build and publish workflow: **Sound-Lounge-Music** → `docs/NEXT_FIRMWARE.md`.

---

## Repository layout

```
Sound-Lounge-Firmware/
  README.md
  MAINTAINERS.md
  manifest.txt
  music_player_ui_<ver>.bin
  music_player_sound_<ver>.bin
  sound_lounge_<ver>.bin
```

Only the **current** firmware package lives in this repo. Older binaries are not kept in git.

Online updates load from:

`https://raw.githubusercontent.com/FlashAeronautica/Sound-Lounge-Firmware/main/manifest.txt`

---

## Publishing checklist

1. Bump **`FIRMWARE_VERSION` to the same value** in all three `*_Next/Config.h` files.
2. `.\build_firmware_next.ps1 -Summary "Next OTA x.y.zz: …"` (copies to `../Sound-Lounge-Firmware` when the sibling repo exists).
3. Update **Current firmware version** in [README.md](README.md).
4. Commit and push `Sound-Lounge-Firmware` to `main`.

`build_firmware_next.ps1` removes previous `.bin` files from the firmware repo root before copying the new package.

All three `*_version=` lines in `manifest.txt` must match top-level `version=`.
