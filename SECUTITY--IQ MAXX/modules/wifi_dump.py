#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IQ MAXX (by dk) - Wi-Fi Password Extraction Engine
Cross-Platform support: Windows (PowerShell/CMD), Linux (Terminal), macOS (Terminal), Android (Termux)
"""

import os
import sys
import subprocess
import platform
import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional

class WifiCredential:
    def __init__(self, ssid: str, password: str = "", auth: str = "Unknown", cipher: str = "Unknown", platform_src: str = ""):
        self.ssid = ssid.strip()
        self.password = password.strip() if password else "[Open / No Password]"
        self.auth = auth.strip() if auth else "Unknown"
        self.cipher = cipher.strip() if cipher else "Unknown"
        self.platform_src = platform_src or platform.system()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ssid": self.ssid,
            "password": self.password,
            "auth": self.auth,
            "cipher": self.cipher,
            "platform": self.platform_src
        }

def is_android() -> bool:
    """Check if running in Android / Termux environment."""
    return os.path.exists("/data/data/com.termux") or "ANDROID_ROOT" in os.environ or "TERMUX_VERSION" in os.environ

def get_current_platform() -> str:
    if is_android():
        return "Android (Termux)"
    return platform.system()

class WifiDumpEngine:
    """Core engine to dump saved Wi-Fi credentials across all supported operating systems."""

    @staticmethod
    def dump_all() -> List[WifiCredential]:
        plat = get_current_platform()
        if plat == "Windows":
            return WifiDumpEngine.dump_windows()
        elif plat == "Android (Termux)":
            return WifiDumpEngine.dump_android()
        elif plat == "Darwin":
            return WifiDumpEngine.dump_macos()
        elif plat == "Linux":
            return WifiDumpEngine.dump_linux()
        else:
            # Try generic Linux extraction as fallback
            return WifiDumpEngine.dump_linux()

    # ---------------------------------------------------------
    # WINDOWS EXTRACTION (PowerShell / Netsh)
    # ---------------------------------------------------------
    @staticmethod
    def dump_windows() -> List[WifiCredential]:
        credentials: List[WifiCredential] = []
        try:
            # 1. Fetch list of saved profile names
            cmd = ["netsh", "wlan", "show", "profiles"]
            res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
            if res.returncode != 0:
                return credentials

            profile_names = []
            for line in res.stdout.splitlines():
                if ":" in line:
                    parts = line.split(":", 1)
                    if any(k in parts[0].lower() for k in ["all user profile", "profil tous les utilisateurs", "todos los perfiles"]):
                        pname = parts[1].strip()
                        if pname:
                            profile_names.append(pname)
                    elif "user profile" in parts[0].lower() or "profile" in parts[0].lower():
                        pname = parts[1].strip()
                        if pname and pname not in profile_names:
                            profile_names.append(pname)

            # 2. Query each profile with key=clear
            for name in profile_names:
                try:
                    pcmd = ["netsh", "wlan", "show", "profile", f"name={name}", "key=clear"]
                    pres = subprocess.run(pcmd, capture_output=True, text=True, errors="ignore")
                    
                    password = ""
                    auth = "WPA2-Personal"
                    cipher = "CCMP/AES"

                    for pline in pres.stdout.splitlines():
                        if ":" in pline:
                            k, v = [x.strip() for x in pline.split(":", 1)]
                            k_low = k.lower()
                            if "key content" in k_low or "contenu de la clé" in k_low or "contenido de la clave" in k_low or "schlüsselinhalt" in k_low:
                                password = v
                            elif "authentication" in k_low or "authentification" in k_low or "autenticación" in k_low:
                                auth = v
                            elif "cipher" in k_low or "chiffrement" in k_low or "cifrado" in k_low:
                                cipher = v
                            elif "security key" in k_low and ("absent" in v.lower() or "open" in v.lower()):
                                if not password:
                                    password = "[Open Network]"

                    if not password and ("open" in auth.lower() or "none" in auth.lower()):
                        password = "[Open Network]"
                    elif not password:
                        password = "[Password Not Stored / 802.1X]"

                    credentials.append(WifiCredential(
                        ssid=name,
                        password=password,
                        auth=auth,
                        cipher=cipher,
                        platform_src="Windows (Netsh/WLAN)"
                    ))
                except Exception:
                    continue

        except Exception as e:
            print(f"Error in Windows Wi-Fi extraction: {e}")

        return credentials

    # ---------------------------------------------------------
    # LINUX EXTRACTION (NetworkManager & WPA Supplicant)
    # ---------------------------------------------------------
    @staticmethod
    def dump_linux() -> List[WifiCredential]:
        credentials: List[WifiCredential] = []
        seen_ssids = set()

        # Method 1: Inspect /etc/NetworkManager/system-connections/ (Requires sudo / root)
        nm_dir = "/etc/NetworkManager/system-connections"
        if os.path.exists(nm_dir) and os.path.isdir(nm_dir):
            try:
                for fname in os.listdir(nm_dir):
                    fpath = os.path.join(nm_dir, fname)
                    if os.path.isfile(fpath):
                        try:
                            with open(fpath, "r", errors="ignore") as f:
                                content = f.read()
                                ssid_match = re.search(r'ssid=(.+)', content)
                                psk_match = re.search(r'psk=(.+)', content)
                                key_mgmt = re.search(r'key-mgmt=(.+)', content)
                                
                                ssid = ssid_match.group(1).strip() if ssid_match else fname.replace(".nmconnection", "")
                                password = psk_match.group(1).strip() if psk_match else ""
                                auth = key_mgmt.group(1).strip() if key_mgmt else "WPA-PSK"

                                if not password and ("none" in auth.lower() or "open" in content.lower()):
                                    password = "[Open Network]"
                                elif not password:
                                    password = "[Requires Sudo / 802.1X]"

                                if ssid not in seen_ssids:
                                    seen_ssids.add(ssid)
                                    credentials.append(WifiCredential(
                                        ssid=ssid,
                                        password=password,
                                        auth=auth,
                                        cipher="AES/CCMP",
                                        platform_src="Linux (NetworkManager)"
                                    ))
                        except PermissionError:
                            # User doesn't have root read permissions
                            ssid = fname.replace(".nmconnection", "")
                            if ssid not in seen_ssids:
                                seen_ssids.add(ssid)
                                credentials.append(WifiCredential(
                                    ssid=ssid,
                                    password="[Requires Sudo / Root]",
                                    auth="WPA2-PSK",
                                    cipher="AES",
                                    platform_src="Linux (NetworkManager)"
                                ))
            except Exception:
                pass

        # Method 2: nmcli CLI query
        try:
            res = subprocess.run(["nmcli", "-t", "-f", "NAME,TYPE,UUID", "connection", "show"], capture_output=True, text=True, errors="ignore")
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if "802-11-wireless" in line or "wifi" in line.lower():
                        parts = line.split(":")
                        name = parts[0]
                        if name and name not in seen_ssids:
                            # Try retrieving secrets
                            sec_res = subprocess.run(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", name], capture_output=True, text=True, errors="ignore")
                            psk = sec_res.stdout.strip() if sec_res.returncode == 0 else ""
                            
                            seen_ssids.add(name)
                            credentials.append(WifiCredential(
                                ssid=name,
                                password=psk if psk else "[Protected / Sudo Required]",
                                auth="WPA/WPA2-PSK",
                                cipher="AES",
                                platform_src="Linux (nmcli)"
                            ))
        except Exception:
            pass

        # Method 3: /etc/wpa_supplicant/wpa_supplicant.conf
        wpa_paths = ["/etc/wpa_supplicant/wpa_supplicant.conf", "/etc/wpa_supplicant.conf"]
        for wpath in wpa_paths:
            if os.path.exists(wpath):
                try:
                    with open(wpath, "r", errors="ignore") as f:
                        content = f.read()
                        blocks = re.findall(r'network=\{([^}]+)\}', content)
                        for block in blocks:
                            s_match = re.search(r'ssid="([^"]+)"', block)
                            p_match = re.search(r'psk="([^"]+)"|psk=([0-9a-fA-F]{64})', block)
                            if s_match:
                                s_name = s_match.group(1)
                                if s_name not in seen_ssids:
                                    pwd = p_match.group(1) or p_match.group(2) if p_match else "[Open / WEP]"
                                    seen_ssids.add(s_name)
                                    credentials.append(WifiCredential(
                                        ssid=s_name,
                                        password=pwd,
                                        auth="WPA/WPA2-PSK",
                                        cipher="CCMP",
                                        platform_src="Linux (wpa_supplicant)"
                                    ))
                except Exception:
                    pass

        return credentials

    # ---------------------------------------------------------
    # MACOS EXTRACTION (Keychain & Airport)
    # ---------------------------------------------------------
    @staticmethod
    def dump_macos() -> List[WifiCredential]:
        credentials: List[WifiCredential] = []
        seen_ssids = set()

        try:
            # 1. Identify Wi-Fi interface (usually en0)
            iface_cmd = subprocess.run(["networksetup", "-listallhardwareports"], capture_output=True, text=True, errors="ignore")
            wifi_iface = "en0"
            if iface_cmd.returncode == 0:
                lines = iface_cmd.stdout.splitlines()
                for i, l in enumerate(lines):
                    if "Wi-Fi" in l or "AirPort" in l:
                        if i + 1 < len(lines) and "Device:" in lines[i+1]:
                            wifi_iface = lines[i+1].split(":")[1].strip()
                            break

            # 2. Get list of preferred Wi-Fi networks
            pref_cmd = subprocess.run(["networksetup", "-listpreferredwirelessnetworks", wifi_iface], capture_output=True, text=True, errors="ignore")
            if pref_cmd.returncode == 0:
                for line in pref_cmd.stdout.splitlines():
                    ssid = line.strip()
                    if ssid and not ssid.startswith("Preferred networks"):
                        if ssid not in seen_ssids:
                            seen_ssids.add(ssid)
                            
                            # 3. Query macOS Keychain for stored password
                            sec_cmd = subprocess.run(
                                ["security", "find-generic-password", "-D", "AirPort network password", "-wa", ssid],
                                capture_output=True, text=True, errors="ignore"
                            )
                            password = sec_cmd.stdout.strip() if sec_cmd.returncode == 0 else ""
                            if not password:
                                password = "[Protected / Requires Keychain Auth]"

                            credentials.append(WifiCredential(
                                ssid=ssid,
                                password=password,
                                auth="WPA2/WPA3-Personal",
                                cipher="AES-CCMP",
                                platform_src="macOS (Keychain)"
                            ))
        except Exception as e:
            print(f"Error in macOS extraction: {e}")

        return credentials

    # ---------------------------------------------------------
    # ANDROID / TERMUX EXTRACTION
    # ---------------------------------------------------------
    @staticmethod
    def dump_android() -> List[WifiCredential]:
        credentials: List[WifiCredential] = []
        seen_ssids = set()

        # Potential paths for Android Wi-Fi store (requires root or su)
        paths = [
            "/data/misc/apexdata/com.android.wifi/WifiConfigStore.xml",
            "/data/misc/wifi/WifiConfigStore.xml",
            "/data/misc/wifi/wpa_supplicant.conf"
        ]

        # 1. Try reading directly or via su
        for p in paths:
            xml_content = None
            if os.path.exists(p):
                try:
                    with open(p, "r", errors="ignore") as f:
                        xml_content = f.read()
                except PermissionError:
                    pass

            if not xml_content:
                # Try su
                try:
                    res = subprocess.run(["su", "-c", f"cat {p}"], capture_output=True, text=True, errors="ignore")
                    if res.returncode == 0 and res.stdout.strip():
                        xml_content = res.stdout
                except Exception:
                    pass

            if xml_content:
                if "WifiConfigStore" in p or "<WifiConfiguration>" in xml_content or "<NetworkList>" in xml_content:
                    # Parse WifiConfigStore XML
                    try:
                        # Extract SSID and PreSharedKey blocks
                        ssids = re.findall(r'<string name="SSID">&quot;([^&]+)&quot;</string>|<string name="SSID">"([^"]+)"</string>', xml_content)
                        keys = re.findall(r'<string name="PreSharedKey">&quot;([^&]+)&quot;</string>|<string name="PreSharedKey">"([^"]+)"</string>', xml_content)
                        
                        # Match blocks via regex
                        net_blocks = re.findall(r'<Network>(.*?)</Network>', xml_content, re.DOTALL)
                        if net_blocks:
                            for blk in net_blocks:
                                s_match = re.search(r'<string name="SSID">(?:&quot;|")?([^&"<]+)(?:&quot;|")?</string>', blk)
                                p_match = re.search(r'<string name="PreSharedKey">(?:&quot;|")?([^&"<]+)(?:&quot;|")?</string>', blk)
                                auth_match = re.search(r'<string name="ConfigKey">(?:&quot;|")?([^&"<]+)(?:&quot;|")?</string>', blk)
                                
                                if s_match:
                                    s_name = s_match.group(1).replace("&quot;", "").strip('"')
                                    p_val = p_match.group(1).replace("&quot;", "").strip('"') if p_match else "[Open Network]"
                                    auth_val = auth_match.group(1).split("-")[-1] if auth_match else "WPA2"
                                    
                                    if s_name not in seen_ssids:
                                        seen_ssids.add(s_name)
                                        credentials.append(WifiCredential(
                                            ssid=s_name,
                                            password=p_val,
                                            auth=auth_val,
                                            cipher="AES",
                                            platform_src="Android (WifiConfigStore)"
                                        ))
                    except Exception:
                        pass

        # 2. Non-root fallback: Query termux-api wifi-connectioninfo or dumpsys
        if not credentials:
            try:
                res = subprocess.run(["termux-wifi-connectioninfo"], capture_output=True, text=True, errors="ignore")
                if res.returncode == 0 and res.stdout.strip():
                    import json
                    data = json.loads(res.stdout)
                    ssid = data.get("ssid", "").strip('"')
                    bssid = data.get("bssid", "")
                    if ssid and ssid != "<unknown ssid>":
                        credentials.append(WifiCredential(
                            ssid=ssid,
                            password="[Active Network - Root required for stored password]",
                            auth="WPA2/WPA3",
                            cipher="CCMP",
                            platform_src="Android (Termux-API)"
                        ))
            except Exception:
                pass

        return credentials
