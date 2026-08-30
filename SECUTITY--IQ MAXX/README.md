# <p align="center"><font color="#00d2ff"><b>IQ MAXX</b></font> <small><i><font color="#00ff88">(by dk)</font></i></small></p>

<p align="center">
  <img src="https://img.shields.io/badge/IQ%20MAXX-v2.5.0-00d2ff?style=for-the-badge&logo=wifi&logoColor=white" />
  <img src="https://img.shields.io/badge/Theme-Blue%20%26%20Green-00ff88?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows%20%7C%20Termux-3a7bd5?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge" />
</p>

```
 ██╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗██╗  ██╗
 ██║██╔═══██╗    ████╗ ████║██╔══██╗╚██╗██╔╝╚██╗██╔╝
 ██║██║   ██║    ██╔████╔██║███████║ ╚███╔╝  ╚███╔╝ 
 ██║██║▄▄ ██║    ██║╚██╔╝██║██╔══██║ ██╔██╗  ██╔██╗ 
 ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗██╔╝ ██╗
 ╚═╝ ╚══▀▀═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
       ⚡ I Q   M A X X ─ v2.5.0 │ (by dk)
       Advanced Cross-Platform Wi-Fi Auditing & Password Access Suite
       Supports: Terminal (macOS/Linux) • PowerShell (Windows) • Termux (Android)
```

---

## ⚡ Overview

**`IQ MAXX`** *(by dk)* is a powerful, cross-platform Wi-Fi auditing, password recovery, live spectrum scanner, and wireless security analysis suite designed with an aesthetic **Cyberpunk Blue & Green** visual terminal interface.

Whether you are auditing wireless security on a **Linux server**, inspecting key stores on **macOS**, recovering profiles in **Windows PowerShell**, or conducting mobile wireless assessments in **Android Termux**, **IQ MAXX** provides instant 1-command execution.

---

## 🚀 Key Features

* 🔑 **Instant Saved Wi-Fi Password Extraction**:
  * **Windows**: Extracts cleartext passphrases from all stored WLAN profiles via `netsh` / XML decryption.
  * **Linux**: Dumps NetworkManager connections (`/etc/NetworkManager/system-connections/`), `nmcli`, and `wpa_supplicant`.
  * **macOS**: Queries Apple Keychain Airport database via `security find-generic-password`.
  * **Android (Termux)**: Parses `WifiConfigStore.xml` (root) and live Wi-Fi telemetry via `termux-api`.
* 📡 **Live Spectrum & Airwave Scanner**:
  * Real-time scan of nearby 2.4 GHz, 5.0 GHz, and 6.0 GHz (Wi-Fi 6E) channels.
  * Measures RSSI (dBm), signal quality bars, BSSID MAC addresses, radio standards (802.11ax/ac/n/g/b), and authentication schemes.
* 🛡️ **Cryptographic Entropy & Security Audit**:
  * Evaluates password Shannon entropy ($H = -\sum p_i \log_2(p_i)$), character set diversity, dictionary attacks vulnerability, and weak router default patterns.
  * Identifies vulnerabilities: Open Networks, WEP deprecation, TKIP cipher weaknesses, WPS PIN vectors.
* 📱 **Terminal Wi-Fi QR Code Generator**:
  * Renders scannable ASCII/Unicode Wi-Fi QR codes directly inside the terminal console for seamless mobile connectivity.
* 📊 **Export & Intelligence Reporting**:
  * Generates responsive, modern **HTML Dashboards** styled in Dark Blue & Neon Green with search filters and copy-to-clipboard buttons.
  * Exports machine-readable **JSON** backups and **CSV** spreadsheets.
* ⚙️ **Automatic 1-Command Global Alias**:
  * Automatically registers the `iqmaxx` command globally across PowerShell, CMD, Linux Bash, macOS zsh, and Android Termux.

---

## 📦 1-Command Quick Installation & Setup

### 🪟 Windows (PowerShell & CMD)

Open PowerShell as Administrator or Standard User:

```powershell
# Navigate to the tool directory and run the 1-click installer:
.\install.ps1
```

> **Result**: `iqmaxx` is added to your PowerShell `$PROFILE` and User `PATH`. You can now open any new terminal window and simply type:
> ```powershell
> iqmaxx
> ```

---

### 🍎 macOS & 🐧 Linux (Terminal)

Open your terminal:

```bash
# Grant execution permissions and run the 1-click installer:
chmod +x install.sh
./install.sh
```

> **Result**: `iqmaxx` is linked to `/usr/local/bin/iqmaxx` and configured in `~/.bashrc` / `~/.zshrc`. You can now run from anywhere:
> ```bash
> iqmaxx
> ```

---

### 📱 Android (Termux)

Open the Termux app on your Android device:

```bash
# 1. Update packages and install python/termux-api
pkg update && pkg install -y python git termux-api

# 2. Run the installer
chmod +x install.sh
./install.sh

# 3. Launch IQ MAXX
iqmaxx
```

> 💡 *Note for Rooted Android users*: Grant root access to Termux (`su`) to decrypt and extract all historical Wi-Fi passphrases from `WifiConfigStore.xml`. Non-root mode seamlessly audits active networks.

---

## 💻 Command Reference & Usage

**`IQ MAXX`** can be used either via its interactive menu or with direct CLI flags:

### 1. Interactive Cyberpunk TUI Menu
```bash
iqmaxx
```
*(or `python iqmaxx.py` / `.\iqmaxx.ps1`)*

```
  ╔═══════════════════════════════════════════════════════════════╗
  ║  ⚡ MAIN CONTROL PANEL                                        ║
  ╠═══════════════════════════════════════════════════════════════╣
  ║  [1] Dump Saved Wi-Fi Passwords     Extract stored OS keys    ║
  ║  [2] Live Airwave Wi-Fi Scanner     Scan nearby BSSID/Channels║
  ║  [3] Security & Entropy Audit       Analyze password strength ║
  ║  [4] Generate Terminal Wi-Fi QR     Instant mobile camera link║
  ║  [5] Export Audit (HTML/JSON/CSV)   Generate visual dashboard ║
  ║  [6] System Adapter Information     Display wireless hardware ║
  ║  [0] Exit IQ MAXX                                             ║
  ╚═══════════════════════════════════════════════════════════════╝
```

---

### 2. Dump Saved Wi-Fi Passwords
```bash
iqmaxx dump
```
Outputs a formatted Blue & Green table with SSID, Passphrase, Auth Type, Cipher, and Strength Rating:

```
┌────┬────────────────────────┬──────────────────┬───────────────┬──────────┬────────────────────┐
│ #  │ SSID / Network         │ Passphrase       │ Auth Type     │ Cipher   │ Rating             │
├────┼────────────────────────┼──────────────────┼───────────────┼──────────┼────────────────────┤
│ 1  │ FiberHome_5G           │ S3cureP@ss2026!  │ WPA2-Personal │ CCMP     │ ●●●● EXCELLENT     │
│ 2  │ Office_Guest           │ [Open Network]   │ Open          │ None     │ N/A                │
│ 3  │ Redmi Note 8           │ 12345678         │ WPA2-Personal │ CCMP     │ ●○○○ CRITICAL WEAK │
└────┴────────────────────────┴──────────────────┴───────────────┴──────────┴────────────────────┘
```

---

### 3. Scan Live Nearby Networks
```bash
iqmaxx scan
```
Scans all 2.4 GHz & 5.0 GHz channels, BSSID MACs, signal strength meters, and flags security risks:

```
┌────┬─────────────────┬───────────────────┬──────────────┬───────────────┬───────────────┬──────────┐
│ #  │ SSID            │ BSSID (MAC)       │ Signal       │ Band          │ Security      │ Risk     │
├────┼─────────────────┼───────────────────┼──────────────┼───────────────┼───────────────┼──────────┤
│ 1  │ Home_Mesh_5G    │ 3C:84:6A:11:22:33 │ ████ 92%     │ 5.0 GHz (Ch36)│ WPA2/WPA3-SAE │ Low      │
│ 2  │ Cafe_Free_Wifi  │ A0:04:60:99:88:77 │ ███░ 65%     │ 2.4 GHz (Ch 6)│ Open          │ CRITICAL │
└────┴─────────────────┴───────────────────┴──────────────┴───────────────┴───────────────┴──────────┘
```

---

### 4. Cryptographic Security & Entropy Audit
```bash
iqmaxx audit
```
Calculates password entropy, detects weak default dictionary entries, and gives hardening recommendations:

```
 ┌───[ Network #1: FiberHome_5G ]
 │  Passphrase: S3cureP@ss2026!
 │  Entropy:    84.2 bits  │  Length: 14 chars  │  Score: 90/100
 │  Rating:     ●●●● EXCELLENT
 └───
```

---

### 5. Generate Wi-Fi QR Code in Terminal
```bash
iqmaxx qr -s "MyHomeNetwork"
```
Renders a scannable QR code directly inside your terminal so you can connect your smartphone camera instantly without typing passwords manually.

---

### 6. Export Audit Reports (HTML, JSON, CSV)
```bash
# Generate Dark Cyber Blue & Green HTML Dashboard + JSON + CSV
iqmaxx export --html audit_report.html --json backup.json --csv export.csv
```

---

## 🎨 Theme & Color Palette

**`IQ MAXX`** uses a dedicated **Blue & Green** visual design:
* **Primary**: Electric Cyan (`#00d2ff`) & Vibrant Blue (`#3a7bd5`)
* **Secondary**: Neon Mint Green (`#00ff88`) & Matrix Lime (`#10b981`)
* **Accents**: Alert Amber (`#f59e0b`) & Critical Red (`#ef4444`)

---

## 📂 Project Structure

```
SECUTITY--IQ MAXX/
├── iqmaxx.py              # Main Cross-Platform Python Engine (Zero-dependency ANSI UI)
├── iqmaxx.ps1             # Native Windows PowerShell 5.1/7+ Auditing Engine
├── iqmaxx.sh              # Native Bash Script for macOS, Linux, and Android Termux
├── install.ps1            # Windows 1-Click Installer (Auto PATH & Profile config)
├── install.sh             # macOS / Linux / Termux 1-Click Installer
├── iqmaxx.cmd             # Windows Command-Line Shortcut
├── setup.py               # Python pip distribution packaging
├── README.md              # Documentation & Command Reference
└── modules/
    ├── __init__.py
    ├── banner.py          # Blue & Green ASCII banner with IQ MAXX (highlight) & (by dk)
    ├── wifi_dump.py       # Cross-platform password extraction engine
    ├── wifi_scanner.py    # Live Wi-Fi airwave scanner and signal evaluator
    ├── security_audit.py  # Cryptographic entropy & vulnerability auditor
    ├── qr_generator.py    # Terminal ASCII/Unicode Wi-Fi QR generator
    └── exporter.py        # HTML Dashboard, JSON, and CSV export generators
```

---

## ⚖️ Ethical & Legal Disclaimer

> [!IMPORTANT]
> **IQ MAXX (by dk)** is developed strictly for authorized security auditing, network vulnerability assessment, educational research, and personal credential recovery. Always obtain explicit authorization before assessing networks you do not own or administer.

---

<p align="center">
  <b>IQ MAXX</b> • Developed with ⚡ by <b>dk</b>
</p>
