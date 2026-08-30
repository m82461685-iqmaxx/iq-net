#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IQ MAXX (by dk) - Live Wi-Fi Airwave Scanner & Analyzer
Supports: Windows, Linux, macOS, Android (Termux)
"""

import os
import sys
import subprocess
import platform
import re
import math
from typing import List, Dict, Any

class ScannedNetwork:
    def __init__(self, ssid: str, bssid: str, signal_pct: int, channel: str, security: str, cipher: str = "", radio: str = "", rssi_dbm: int = -100):
        self.ssid = ssid.strip() if ssid.strip() else "<Hidden SSID>"
        self.bssid = bssid.strip().upper() if bssid else "00:00:00:00:00:00"
        self.signal_pct = max(0, min(100, signal_pct))
        self.channel = str(channel).strip() if channel else "Unknown"
        self.security = security.strip() if security else "Unknown"
        self.cipher = cipher.strip() if cipher else "Unknown"
        self.radio = radio.strip() if radio else "Unknown"
        self.rssi_dbm = rssi_dbm if rssi_dbm != -100 else self._pct_to_dbm(self.signal_pct)
        self.band = self._determine_band(self.channel)
        self.vulnerabilities = self._analyze_vulnerabilities()

    @staticmethod
    def _pct_to_dbm(pct: int) -> int:
        # Standard approximation: 100% ~ -40 dBm, 0% ~ -100 dBm
        return int(-100 + (pct * 0.6))

    def _determine_band(self, channel: str) -> str:
        try:
            ch = int(channel)
            if 1 <= ch <= 14:
                return "2.4 GHz"
            elif 32 <= ch <= 177:
                return "5.0 GHz"
            elif ch > 177:
                return "6.0 GHz (Wi-Fi 6E)"
        except Exception:
            pass
        return "2.4/5 GHz"

    def _analyze_vulnerabilities(self) -> List[str]:
        vulns = []
        sec_low = self.security.lower()
        ciph_low = self.cipher.lower()

        if "open" in sec_low or "none" in sec_low:
            vulns.append("OPEN NETWORK: No encryption; traffic can be sniffed in plaintext")
        if "wep" in sec_low:
            vulns.append("CRITICAL WEP: Obsolete 64/128-bit RC4 cipher; crackable in minutes")
        if "tkip" in ciph_low:
            vulns.append("WEAK CIPHER (TKIP): Deprecated, vulnerable to Beck-Tews attacks")
        if "wpa " in sec_low or "wpa-personal" in sec_low or "wpa1" in sec_low:
            vulns.append("LEGACY WPA1: Deprecated protocol; upgrade to WPA2/WPA3")
        if "wps" in sec_low or "wps" in ciph_low:
            vulns.append("WPS ENABLED: Potential PIN brute-force (Pixie Dust / Reaver risk)")

        return vulns

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ssid": self.ssid,
            "bssid": self.bssid,
            "signal_pct": self.signal_pct,
            "rssi_dbm": self.rssi_dbm,
            "channel": self.channel,
            "band": self.band,
            "security": self.security,
            "cipher": self.cipher,
            "radio": self.radio,
            "vulnerabilities": self.vulnerabilities
        }

class WifiScannerEngine:
    """Discovers surrounding wireless access points and maps their parameters."""

    @staticmethod
    def scan_all() -> List[ScannedNetwork]:
        plat = platform.system()
        if os.path.exists("/data/data/com.termux") or "ANDROID_ROOT" in os.environ:
            return WifiScannerEngine.scan_android()
        elif plat == "Windows":
            return WifiScannerEngine.scan_windows()
        elif plat == "Darwin":
            return WifiScannerEngine.scan_macos()
        elif plat == "Linux":
            return WifiScannerEngine.scan_linux()
        else:
            return WifiScannerEngine.scan_linux()

    # ---------------------------------------------------------
    # WINDOWS SCANNER (Netsh WLAN)
    # ---------------------------------------------------------
    @staticmethod
    def scan_windows() -> List[ScannedNetwork]:
        networks: List[ScannedNetwork] = []
        try:
            cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
            res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
            if res.returncode != 0:
                return networks

            blocks = res.stdout.split("\nSSID ")
            for idx, blk in enumerate(blocks):
                if idx == 0 and not blk.startswith("1 :"):
                    # Check if first block has SSID
                    if "SSID " in blk:
                        blk = blk.split("SSID ", 1)[-1]
                    else:
                        continue

                lines = blk.splitlines()
                ssid = ""
                auth = "Unknown"
                cipher = "Unknown"
                radio = "802.11"

                # First line usually contains SSID name
                first_line = lines[0]
                if ":" in first_line:
                    ssid = first_line.split(":", 1)[1].strip()

                # Parse BSSID sections within this SSID
                curr_bssid = ""
                curr_signal = 50
                curr_chan = "Unknown"

                for line in lines:
                    if ":" in line:
                        k, v = [x.strip() for x in line.split(":", 1)]
                        k_low = k.lower()
                        if "authentication" in k_low or "authentification" in k_low:
                            auth = v
                        elif "encryption" in k_low or "chiffrement" in k_low:
                            cipher = v
                        elif "radio type" in k_low:
                            radio = v
                        elif "bssid" in k_low:
                            if curr_bssid and ssid:
                                networks.append(ScannedNetwork(
                                    ssid=ssid,
                                    bssid=curr_bssid,
                                    signal_pct=curr_signal,
                                    channel=curr_chan,
                                    security=auth,
                                    cipher=cipher,
                                    radio=radio
                                ))
                            curr_bssid = v
                        elif "signal" in k_low:
                            sig_str = v.replace("%", "").strip()
                            try:
                                curr_signal = int(sig_str)
                            except Exception:
                                curr_signal = 50
                        elif "channel" in k_low or "canal" in k_low:
                            curr_chan = v

                if curr_bssid and ssid:
                    networks.append(ScannedNetwork(
                        ssid=ssid,
                        bssid=curr_bssid,
                        signal_pct=curr_signal,
                        channel=curr_chan,
                        security=auth,
                        cipher=cipher,
                        radio=radio
                    ))

        except Exception as e:
            print(f"Error in Windows Wi-Fi scan: {e}")

        # Sort descending by signal
        networks.sort(key=lambda x: x.signal_pct, reverse=True)
        return networks

    # ---------------------------------------------------------
    # LINUX SCANNER (nmcli & iw)
    # ---------------------------------------------------------
    @staticmethod
    def scan_linux() -> List[ScannedNetwork]:
        networks: List[ScannedNetwork] = []
        # Method 1: nmcli
        try:
            cmd = ["nmcli", "-t", "-f", "SSID,BSSID,CHAN,SIGNAL,SECURITY", "dev", "wifi", "list", "--rescan", "auto"]
            res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
            if res.returncode == 0 and res.stdout.strip():
                for line in res.stdout.splitlines():
                    # Parse escaped colons in nmcli output
                    # nmcli uses \: for colons in BSSID
                    parts = re.split(r'(?<!\\):', line)
                    if len(parts) >= 5:
                        ssid = parts[0].replace(r'\:', ':')
                        bssid = parts[1].replace(r'\:', ':')
                        chan = parts[2]
                        try:
                            sig = int(parts[3])
                        except Exception:
                            sig = 50
                        sec = parts[4] if parts[4] else "Open"
                        networks.append(ScannedNetwork(
                            ssid=ssid,
                            bssid=bssid,
                            signal_pct=sig,
                            channel=chan,
                            security=sec,
                            cipher="WPA2/AES"
                        ))
                if networks:
                    networks.sort(key=lambda x: x.signal_pct, reverse=True)
                    return networks
        except Exception:
            pass

        # Method 2: iw / iwlist fallback
        try:
            res = subprocess.run(["iwlist", "scan"], capture_output=True, text=True, errors="ignore")
            if res.returncode == 0:
                cells = res.stdout.split("Cell ")
                for cell in cells[1:]:
                    bssid_match = re.search(r'Address:\s*([0-9A-Fa-f:]{17})', cell)
                    ssid_match = re.search(r'ESSID:"([^"]*)"', cell)
                    chan_match = re.search(r'Channel:?(\d+)', cell)
                    sig_match = re.search(r'Quality=(\d+)/(\d+)|Signal level=(-\d+) dBm', cell)
                    
                    bssid = bssid_match.group(1) if bssid_match else "00:00:00:00:00:00"
                    ssid = ssid_match.group(1) if ssid_match else "<Hidden>"
                    chan = chan_match.group(1) if chan_match else "1"
                    
                    sig_pct = 50
                    if sig_match:
                        if sig_match.group(1) and sig_match.group(2):
                            sig_pct = int(int(sig_match.group(1)) / int(sig_match.group(2)) * 100)
                        elif sig_match.group(3):
                            dbm = int(sig_match.group(3))
                            sig_pct = int(max(0, min(100, (dbm + 100) * 1.67)))

                    sec = "WPA2" if "WPA2" in cell else ("WPA" if "WPA" in cell else ("WEP" if "Encryption key:on" in cell else "Open"))
                    networks.append(ScannedNetwork(
                        ssid=ssid,
                        bssid=bssid,
                        signal_pct=sig_pct,
                        channel=chan,
                        security=sec
                    ))
        except Exception:
            pass

        networks.sort(key=lambda x: x.signal_pct, reverse=True)
        return networks

    # ---------------------------------------------------------
    # MACOS SCANNER (Airport CLI)
    # ---------------------------------------------------------
    @staticmethod
    def scan_macos() -> List[ScannedNetwork]:
        networks: List[ScannedNetwork] = []
        airport_bin = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        if not os.path.exists(airport_bin):
            airport_bin = "airport"

        try:
            cmd = [airport_bin, "-s"]
            res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
            if res.returncode == 0:
                lines = res.stdout.splitlines()
                # Skip header line
                for line in lines[1:]:
                    # Regex for airport format: SSID BSSID RSSI CHANNEL HT CC SECURITY
                    match = re.match(r'^\s*(.*?)\s+([0-9a-fA-F:]{17})\s+(-\d+)\s+([0-9,+]+)\s+[YyNn]\s+([A-Za-z]+|\-\-)\s+(.*)$', line)
                    if match:
                        ssid = match.group(1).strip()
                        bssid = match.group(2)
                        rssi = int(match.group(3))
                        chan = match.group(4)
                        sec = match.group(6).strip()
                        
                        # Convert RSSI dBm to percentage
                        sig_pct = int(max(0, min(100, (rssi + 100) * 1.67)))
                        networks.append(ScannedNetwork(
                            ssid=ssid,
                            bssid=bssid,
                            signal_pct=sig_pct,
                            channel=chan,
                            security=sec,
                            rssi_dbm=rssi
                        ))
        except Exception as e:
            print(f"Error in macOS scan: {e}")

        networks.sort(key=lambda x: x.signal_pct, reverse=True)
        return networks

    # ---------------------------------------------------------
    # ANDROID / TERMUX SCANNER (Termux-API & Dumpsys)
    # ---------------------------------------------------------
    @staticmethod
    def scan_android() -> List[ScannedNetwork]:
        networks: List[ScannedNetwork] = []
        try:
            # 1. Try termux-wifi-scaninfo
            res = subprocess.run(["termux-wifi-scaninfo"], capture_output=True, text=True, errors="ignore")
            if res.returncode == 0 and res.stdout.strip():
                import json
                items = json.loads(res.stdout)
                for item in items:
                    ssid = item.get("ssid", "").strip('"')
                    bssid = item.get("bssid", "")
                    rssi = item.get("rssi", -70)
                    freq = item.get("frequency", 2412)
                    caps = item.get("capabilities", "WPA2")
                    
                    # Convert frequency to channel
                    ch = 1
                    if 2412 <= freq <= 2484:
                        ch = int((freq - 2407) / 5)
                    elif 5170 <= freq <= 5825:
                        ch = int((freq - 5000) / 5)

                    sig_pct = int(max(0, min(100, (rssi + 100) * 1.67)))
                    networks.append(ScannedNetwork(
                        ssid=ssid,
                        bssid=bssid,
                        signal_pct=sig_pct,
                        channel=str(ch),
                        security=caps,
                        rssi_dbm=rssi
                    ))
        except Exception:
            pass

        networks.sort(key=lambda x: x.signal_pct, reverse=True)
        return networks
