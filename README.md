# Flipper firmware WiFit Mod

**WIFITE 0.8 experimental** for **LilyGo T-Embed CC1101 Plus / ESP32-S3**, based on the WirelessPi build of Sor3nt's Flipper Zero ESP32 port. Firmware version: **2.0.0-pi11-wifite**. No Raspberry Pi is required.

## Download

Get the flashable package and complete source from this repository's [Releases page](https://github.com/salikisazazil/Flipper-firmware-WiFit-Mod/releases).

- `T-Embed-WirelessPi-WIFITE-v0.8-flashable.zip`: firmware, matching FAP, full source, scripts, licenses and validation logs.
- `T-Embed-WirelessPi-WIFITE-v0.8-source.zip`: the complete 5,647-file project, ready to extract and build.
- [SHA256SUMS.txt](SHA256SUMS.txt): checksums for both archives.

## What changed

Version 0.8 recognizes identical WPS requests even when the router changes the EAP identifier. It resends the complete cached response using the current identifier while retaining the authenticated message body, keys and nonces. Fragment acknowledgements cannot overwrite that cached response. Changed requests remain inconclusive and receive a separate diagnostic.

Logs distinguish Pixie capture, offline search and inconclusive online PIN testing. The WIFITE icon, scrolling terminal, SD log export and scan table with WPS, advertised lock state and passively observed client counts remain included.

Auto tests `12345670` first. If it does not verify successfully, Auto attempts Pixie capture and the supported offline search after a valid M3, then online PIN testing when applicable. Three consecutive inconclusive online exchanges pause on the same PIN. This does not mean three rejected PINs or an exhausted search. Confirmed locks, cancellation and initialization failures still stop the job.

## Install

**Flash the firmware and replace the matching FAP.** The protocol fix lives in the firmware; replacing the FAP alone is insufficient.

| File in the release's `firmware/` directory | Flash address |
| --- | --- |
| `bootloader.bin` | `0x0` |
| `partition-table.bin` | `0x8000` |
| `furi_esp32.bin` | `0x10000` |
| `ota_data_initial.bin` | `0xBF0000` |

Settings: ESP32-S3, DIO, 80 MHz, 16 MB. Use `FLASH.ps1` or `flash.sh` from the release. Copy `SD/apps/WiFi/wifite.fap` to `apps/WiFi/wifite.fap` on the SD card. Retain your existing SD data.

## Source layout and building

The simplest source route is to extract the **full source ZIP from Releases**, open its `Flipper-Zero-ESP32-Port/` directory and follow [BUILD-WIFITE.md](BUILD-WIFITE.md). Use ESP-IDF **5.4.1** with submodules and the ESP32-S3 toolchain.

This repository also retains the exact source snapshot as a checked Git bundle, split into two files for direct browser upload. It is a complete source backup, not only the WIFITE app. To unpack it from a Git clone:

```sh
git clone --branch wifite-v0.8 https://github.com/salikisazazil/Flipper-firmware-WiFit-Mod.git
cd Flipper-firmware-WiFit-Mod
python3 unpack_source.py
cd firmware-source
```

`unpack_source.py` validates the bundle SHA-256 and expected source commit, imports it into the local Git object store, and extracts `firmware-source/`. It performs no remote writes and refuses to overwrite an existing source directory. A normal GitHub-generated source download contains the bundle parts; use the separate full source ZIP when you want ordinary extracted source without Git.

Source commit in the bundle: `6b5750e1d697fb552feafd2a50260073ec0cb72a`.

## Validation and limitations

Firmware and FAP builds passed, with all 45 FAP imports resolved. Host regressions cover independent cryptographic exchanges, repeated M1/M3/M5, fragment handling, changed-session rejection, Auto fallback, PIN progression, radio cleanup, scan status and 100,000 parser cases. See [VALIDATION.txt](VALIDATION.txt); full logs and tests accompany the source.

**Version 0.8 remains unverified on physical hardware by the build environment.** Host tests do not prove router compatibility or successful PIN/key recovery. WPS enabled does not imply Pixie vulnerability. Client counts reflect passive observation, not a complete router association list.

This is a custom native implementation, **not a complete Kali Wifite or Reaver port**. See [WIFITE.md](WIFITE.md) for the supported modes and limits. Only test networks you own or are authorized to assess.

## Attribution and licenses

Base firmware: [Sor3nt/Flipper-Zero-ESP32-Port](https://github.com/Sor3nt/Flipper-Zero-ESP32-Port). Existing components retain their licenses and notices in the complete source. Pixiewps-derived code and the integrated WIFITE distribution use GPL-3.0-or-later ([license](COPYING.pixiewps)); the independently written core retains its [MIT license](LICENSE.core). The ESP-IDF adapter retains its [Apache-2.0 license](LICENSE.ESP-IDF), and the font license is [included](LICENSE.font). Exact revisions and scope are recorded in [UPSTREAM.md](UPSTREAM.md).

This project is not affiliated with Kali, Wifite, Reaver or Pixiewps.
