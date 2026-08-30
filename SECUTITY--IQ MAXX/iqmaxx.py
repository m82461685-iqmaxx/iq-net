#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  ██╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗██╗  ██╗
  ██║██╔═══██╗    ████╗ ████║██╔══██╗╚██╗██╔╝╚██╗██╔╝
  ██║██║   ██║    ██╔████╔██║███████║ ╚███╔╝  ╚███╔╝ 
  ██║██║▄▄ ██║    ██║╚██╔╝██║██╔══██║ ██╔██╗  ██╔██╗ 
  ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗██╔╝ ██╗
  ╚═╝ ╚══▀▀═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
       ⚡ IQ MAXX (by dk) - Advanced Wi-Fi Auditing Suite
"""

import sys
import os
import argparse
import time
import platform

# Force UTF-8 stream encoding across consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
elif hasattr(sys.stdout, 'buffer'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ensure modules directory is in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from modules.banner import (
    Colors, get_banner, print_banner, tag_info, tag_success, tag_warn,
    tag_error, tag_plus, print_section, print_table, format_strength,
    format_signal, strip_ansi
)
from modules.wifi_dump import WifiDumpEngine, get_current_platform
from modules.wifi_scanner import WifiScannerEngine
from modules.security_audit import SecurityAuditor
from modules.qr_generator import print_wifi_qr, format_wifi_string
from modules.exporter import Exporter

def run_dump(quiet: bool = False):
    """Extract and display all stored Wi-Fi credentials."""
    c = Colors
    if not quiet:
        print_section("SAVED WI-FI CREDENTIALS DUMP", f"Platform: {get_current_platform()}")
        print(f" {tag_info('Querying operating system wireless configuration store...')}")

    creds = WifiDumpEngine.dump_all()
    if not creds:
        print(f" {tag_warn('No saved Wi-Fi profiles found or elevated permissions required.')}")
        return creds

    headers = ["#", "SSID / Network", "Passphrase", "Auth Type", "Cipher", "Rating"]
    rows = []
    
    for idx, item in enumerate(creds, 1):
        audit = SecurityAuditor.audit_password(item.password)
        strength_badge = format_strength(audit.score // 25 + 1, audit.level) if audit.score > 0 else f"{c.GRAY}N/A{c.RESET}"
        
        # Colorize password
        if "open" in item.password.lower():
            pwd_disp = f"{c.YELLOW}[Open / No Password]{c.RESET}"
        elif item.password.startswith("["):
            pwd_disp = f"{c.GRAY}{item.password}{c.RESET}"
        else:
            pwd_disp = f"{c.GREEN_BRIGHT}{c.BOLD}{item.password}{c.RESET}"

        rows.append([
            f"{c.CYAN}{idx}{c.RESET}",
            f"{c.WHITE}{item.ssid}{c.RESET}",
            pwd_disp,
            f"{c.CYAN}{item.auth}{c.RESET}",
            f"{c.GRAY}{item.cipher}{c.RESET}",
            strength_badge
        ])

    print_table(headers, rows)
    print(f"\n {tag_success(f'Successfully retrieved {c.BOLD}{len(creds)}{c.RESET}{c.GREEN} Wi-Fi profiles.')}\n")
    return creds

def run_scan():
    """Scan and analyze nearby live Wi-Fi networks."""
    c = Colors
    print_section("REAL-TIME AIRWAVE SCANNER", f"OS: {platform.system()}")
    print(f" {tag_info('Scanning 2.4GHz / 5GHz wireless channels for nearby beacons...')}")

    networks = WifiScannerEngine.scan_all()
    if not networks:
        print(f" {tag_warn('No wireless access points detected or Wi-Fi adapter is disabled.')}")
        return networks

    headers = ["#", "SSID", "BSSID (MAC)", "Signal", "Band", "Security", "Risk"]
    rows = []

    for idx, net in enumerate(networks, 1):
        sig_disp = format_signal(net.signal_pct)
        risk_disp = f"{c.GREEN_BRIGHT}Low{c.RESET}"
        if net.vulnerabilities:
            risk_disp = f"{c.RED}{c.BOLD}VULNERABLE ({len(net.vulnerabilities)}){c.RESET}"
        elif "open" in net.security.lower():
            risk_disp = f"{c.RED}CRITICAL (Open){c.RESET}"

        rows.append([
            f"{c.CYAN}{idx}{c.RESET}",
            f"{c.WHITE}{c.BOLD}{net.ssid}{c.RESET}",
            f"{c.GRAY}{net.bssid}{c.RESET}",
            sig_disp,
            f"{c.CYAN_PALE}{net.band} (Ch {net.channel}){c.RESET}",
            f"{c.CYAN}{net.security}{c.RESET}",
            risk_disp
        ])

    print_table(headers, rows)
    print(f"\n {tag_success(f'Discovered {c.BOLD}{len(networks)}{c.RESET}{c.GREEN} active access points.')}\n")
    return networks

def run_audit():
    """Perform in-depth security and password entropy audit."""
    c = Colors
    print_section("SECURITY & ENTROPY POSTURE AUDIT", "Cryptographic Evaluation")
    creds = WifiDumpEngine.dump_all()
    
    if not creds:
        print(f" {tag_warn('No credentials available to audit.')}")
        return

    print(f" {tag_info(f'Auditing {len(creds)} credentials against dictionary patterns & entropy scales...')}\n")
    
    weak_count = 0
    strong_count = 0

    for idx, item in enumerate(creds, 1):
        audit = SecurityAuditor.audit_password(item.password)
        if audit.level in ["CRITICAL WEAK", "MODERATE"]:
            weak_count += 1
        else:
            strong_count += 1

        print(f" {c.CYAN}┌───[{c.BOLD} Network #{idx}: {c.WHITE}{item.ssid} {c.CYAN}]{c.RESET}")
        print(f" {c.CYAN}│{c.RESET}  {c.GRAY}Passphrase:{c.RESET} {c.GREEN_BRIGHT}{item.password}{c.RESET}")
        print(f" {c.CYAN}│{c.RESET}  {c.GRAY}Entropy:{c.RESET}    {c.CYAN}{audit.entropy} bits{c.RESET}  │  {c.GRAY}Length:{c.RESET} {c.CYAN}{audit.length} chars{c.RESET}  │  {c.GRAY}Score:{c.RESET} {c.BOLD}{audit.score}/100{c.RESET}")
        print(f" {c.CYAN}│{c.RESET}  {c.GRAY}Rating:{c.RESET}     {format_strength(audit.score // 25 + 1, audit.level)}")
        
        if audit.recommendations:
            print(f" {c.CYAN}│{c.RESET}  {c.YELLOW}Remediation Suggestions:{c.RESET}")
            for rec in audit.recommendations:
                print(f" {c.CYAN}│{c.RESET}   {c.YELLOW}•{c.RESET} {rec}")
        print(f" {c.CYAN}└───{c.RESET}\n")

    print(f" {tag_info(f'Audit Summary: {c.GREEN_BRIGHT}{strong_count} Strong{c.RESET} │ {c.YELLOW if weak_count > 0 else c.GREEN}{weak_count} Needs Attention{c.RESET}')}\n")

def run_qr(target_ssid: str = None):
    """Generate scannable terminal QR code for a given Wi-Fi network."""
    c = Colors
    print_section("TERMINAL WI-FI QR CODE GENERATOR", "Instant Mobile Connect")
    creds = WifiDumpEngine.dump_all()
    
    selected_cred = None
    if target_ssid:
        for item in creds:
            if item.ssid.lower() == target_ssid.lower():
                selected_cred = item
                break
        if not selected_cred:
            # Custom manual entry
            pwd = input(f" {tag_plus(f'Enter passphrase for \"{target_ssid}\": ')}").strip()
            selected_cred = type("Obj", (), {"ssid": target_ssid, "password": pwd, "auth": "WPA2"})()
    else:
        if not creds:
            ssid = input(f" {tag_plus('Enter Wi-Fi SSID Name: ')}").strip()
            pwd = input(f" {tag_plus('Enter Wi-Fi Passphrase: ')}").strip()
            selected_cred = type("Obj", (), {"ssid": ssid, "password": pwd, "auth": "WPA2"})()
        else:
            print(f" {tag_info('Select a saved network to generate QR code:')}")
            for idx, item in enumerate(creds, 1):
                print(f"   {c.CYAN}[{idx}]{c.RESET} {c.WHITE}{item.ssid}{c.RESET} {c.GRAY}({item.password}){c.RESET}")
            
            try:
                choice = int(input(f"\n {tag_plus('Enter selection number: ')}").strip())
                if 1 <= choice <= len(creds):
                    selected_cred = creds[choice - 1]
                else:
                    print(f" {tag_error('Invalid selection.')}")
                    return
            except Exception:
                print(f" {tag_error('Invalid input.')}")
                return

    if selected_cred:
        print(f"\n {c.CYAN}╔══════════════════════════════════════════════════════════════════╗{c.RESET}")
        print(f" {c.CYAN}║{c.RESET}  {c.BOLD}SSID:{c.RESET} {c.WHITE}{selected_cred.ssid:<25}{c.RESET} {c.BOLD}PWD:{c.RESET} {c.GREEN_BRIGHT}{selected_cred.password:<20}{c.RESET} {c.CYAN}║{c.RESET}")
        print(f" {c.CYAN}╚══════════════════════════════════════════════════════════════════╝{c.RESET}\n")
        print(f" {tag_info('Scan this QR code with any iOS / Android camera to connect:')}\n")
        print_wifi_qr(selected_cred.ssid, selected_cred.password, getattr(selected_cred, "auth", "WPA"))
        print("\n")

def run_export(html_path: str = None, json_path: str = None, csv_path: str = None):
    """Export recovered profiles and security posture to files."""
    c = Colors
    print_section("CREDENTIALS EXPORT ENGINE", "HTML, JSON & CSV Exporter")
    creds = WifiDumpEngine.dump_all()
    if not creds:
        print(f" {tag_warn('No credentials to export.')}")
        return

    data = [c.to_dict() for c in creds]
    
    if html_path:
        if Exporter.export_html(data, html_path):
            print(f" {tag_success(f'HTML Dashboard generated: {c.BOLD}{html_path}{c.RESET}')}")
    if json_path:
        if Exporter.export_json(data, json_path):
            print(f" {tag_success(f'JSON Data exported: {c.BOLD}{json_path}{c.RESET}')}")
    if csv_path:
        if Exporter.export_csv(data, csv_path):
            print(f" {tag_success(f'CSV Spreadsheet exported: {c.BOLD}{csv_path}{c.RESET}')}")

    if not (html_path or json_path or csv_path):
        # Default interactive export
        default_html = "wifi_audit_report.html"
        default_json = "wifi_backup.json"
        Exporter.export_html(data, default_html)
        Exporter.export_json(data, default_json)
        print(f" {tag_success(f'Generated default HTML report: {c.BOLD}{default_html}{c.RESET}')}")
        print(f" {tag_success(f'Generated default JSON backup: {c.BOLD}{default_json}{c.RESET}')}")
    print()

def interactive_menu():
    """Interactive TUI Navigation Menu with Blue & Green Theme."""
    c = Colors
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print(f"  {c.CYAN}╔═══════════════════════════════════════════════════════════════╗{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.BOLD}{c.BLUE}⚡ MAIN CONTROL PANEL{c.RESET}                                      {c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}╠═══════════════════════════════════════════════════════════════╣{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.GREEN_BRIGHT}[1]{c.RESET} {c.WHITE}Dump Saved Wi-Fi Passwords{c.RESET}     {c.GRAY}Extract stored OS keys{c.RESET}    {c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.GREEN_BRIGHT}[2]{c.RESET} {c.WHITE}Live Airwave Wi-Fi Scanner{c.RESET}     {c.GRAY}Scan nearby BSSID/Channels{c.RESET}{c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.GREEN_BRIGHT}[3]{c.RESET} {c.WHITE}Security & Entropy Audit{c.RESET}       {c.GRAY}Analyze password strength{c.RESET} {c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.GREEN_BRIGHT}[4]{c.RESET} {c.WHITE}Generate Terminal Wi-Fi QR{c.RESET}     {c.GRAY}Instant mobile camera link{c.RESET}{c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.GREEN_BRIGHT}[5]{c.RESET} {c.WHITE}Export Audit (HTML/JSON/CSV){c.RESET}   {c.GRAY}Generate visual dashboard{c.RESET} {c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.GREEN_BRIGHT}[6]{c.RESET} {c.WHITE}System Adapter Information{c.RESET}     {c.GRAY}Display wireless hardware{c.RESET} {c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}║{c.RESET}  {c.RED}[0]{c.RESET} {c.WHITE}Exit IQ MAXX{c.RESET}                                               {c.CYAN}║{c.RESET}")
        print(f"  {c.CYAN}╚═══════════════════════════════════════════════════════════════╝{c.RESET}\n")

        choice = input(f"  {c.BLUE}iqmaxx{c.RESET}{c.GREEN}❯{c.RESET} ").strip()

        if choice == "1":
            run_dump()
            input(f" {c.GRAY}Press Enter to return to main menu...{c.RESET}")
        elif choice == "2":
            run_scan()
            input(f" {c.GRAY}Press Enter to return to main menu...{c.RESET}")
        elif choice == "3":
            run_audit()
            input(f" {c.GRAY}Press Enter to return to main menu...{c.RESET}")
        elif choice == "4":
            run_qr()
            input(f" {c.GRAY}Press Enter to return to main menu...{c.RESET}")
        elif choice == "5":
            run_export()
            input(f" {c.GRAY}Press Enter to return to main menu...{c.RESET}")
        elif choice == "6":
            print_section("WIRELESS SYSTEM HARDWARE", f"Platform: {platform.system()} {platform.release()}")
            print(f" {tag_info(f'OS Node: {platform.node()}')}")
            print(f" {tag_info(f'Machine Arch: {platform.machine()}')}")
            print(f" {tag_info(f'Python Runtime: {sys.version.split()[0]}')}")
            print(f" {tag_info(f'Active Engine: IQ MAXX v2.5.0 (by dk)')}\n")
            input(f" {c.GRAY}Press Enter to return to main menu...{c.RESET}")
        elif choice in ["0", "q", "exit"]:
            print(f"\n {tag_info('Exiting IQ MAXX. Stay secure!')}\n")
            break

def main():
    parser = argparse.ArgumentParser(
        description="IQ MAXX (by dk) - Advanced Cross-Platform Wi-Fi Auditing & Password Access Suite",
        add_help=False
    )
    parser.add_argument("command", nargs="?", default="interactive", choices=["dump", "scan", "audit", "qr", "export", "interactive", "banner", "help"], help="Action to execute")
    parser.add_argument("-s", "--ssid", type=str, help="Specific SSID to target for QR code or audit")
    parser.add_argument("--html", type=str, help="Export output path for HTML report")
    parser.add_argument("--json", type=str, help="Export output path for JSON data")
    parser.add_argument("--csv", type=str, help="Export output path for CSV spreadsheet")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")

    args = parser.parse_args()

    if args.help or args.command == "help":
        print_banner()
        c = Colors
        print(f"""
{c.CYAN}{c.BOLD}USAGE:{c.RESET}
  {c.GREEN}iqmaxx{c.RESET}                     {c.GRAY}# Launch Interactive Cyberpunk TUI Menu{c.RESET}
  {c.GREEN}iqmaxx dump{c.RESET}                {c.GRAY}# Extract & display all saved Wi-Fi passphrases{c.RESET}
  {c.GREEN}iqmaxx scan{c.RESET}                {c.GRAY}# Scan nearby wireless access points & signal strength{c.RESET}
  {c.GREEN}iqmaxx audit{c.RESET}               {c.GRAY}# Security entropy audit & weak password detector{c.RESET}
  {c.GREEN}iqmaxx qr [-s SSID]{c.RESET}        {c.GRAY}# Generate scannable terminal QR code for instant connect{c.RESET}
  {c.GREEN}iqmaxx export [options]{c.RESET}    {c.GRAY}# Export credentials to HTML / JSON / CSV{c.RESET}

{c.CYAN}{c.BOLD}EXPORT OPTIONS:{c.RESET}
  {c.CYAN}--html <file.html>{c.RESET}         {c.GRAY}Generate Cyberpunk Dark Theme HTML Dashboard{c.RESET}
  {c.CYAN}--json <file.json>{c.RESET}         {c.GRAY}Save raw credential list as JSON{c.RESET}
  {c.CYAN}--csv  <file.csv>{c.RESET}          {c.GRAY}Save as CSV spreadsheet{c.RESET}

{c.CYAN}{c.BOLD}PLATFORMS SUPPORTED:{c.RESET}
  • {c.WHITE}Windows (PowerShell 5.1/7+, CMD){c.RESET}
  • {c.WHITE}macOS (Terminal / zsh / bash){c.RESET}
  • {c.WHITE}Linux (Terminal / bash / zsh){c.RESET}
  • {c.WHITE}Android (Termux / Termux-API / Root){c.RESET}
""")
        return

    if args.command == "banner":
        print_banner()
        return
    elif args.command == "dump":
        print_banner()
        run_dump()
    elif args.command == "scan":
        print_banner()
        run_scan()
    elif args.command == "audit":
        print_banner()
        run_audit()
    elif args.command == "qr":
        print_banner()
        run_qr(args.ssid)
    elif args.command == "export":
        print_banner()
        run_export(args.html, args.json, args.csv)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
