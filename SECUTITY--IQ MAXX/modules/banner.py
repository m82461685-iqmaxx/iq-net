#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IQ MAXX (by dk) - Banner & Theme Styling Module
Color Palette: Vibrant Blue, Cyan, Emerald & Neon Green
"""

import sys
import os
import platform

# Ensure UTF-8 output encoding across Windows, Mac, Linux, and Android Termux
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

# Enable ANSI escape sequences on Windows console if needed
if platform.system() == "Windows":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        os.system('')

class Colors:
    # Reset
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Blue & Cyan Palette (Theme Primary)
    BLUE = "\033[38;5;39m"         # Bright Neon Blue
    BLUE_DEEP = "\033[38;5;27m"    # Deep Electric Blue
    CYAN = "\033[38;5;51m"         # Bright Aqua Cyan
    CYAN_PALE = "\033[38;5;123m"   # Pale Cyan
    NAVY = "\033[38;5;24m"         # Dark Navy

    # Green Palette (Theme Secondary)
    GREEN = "\033[38;5;48m"        # Neon Mint Green
    GREEN_BRIGHT = "\033[38;5;46m" # Bright Matrix Green
    GREEN_DARK = "\033[38;5;28m"   # Forest Green
    GREEN_LIME = "\033[38;5;118m"  # Electric Lime
    EMERALD = "\033[38;5;35m"      # Emerald Green

    # Accents & Alerts (Complementary)
    WHITE = "\033[38;5;255m"       # Crisp White
    GRAY = "\033[38;5;244m"        # Dim Silver Gray
    YELLOW = "\033[38;5;220m"      # Warning Amber
    RED = "\033[38;5;196m"         # Critical Red

    # Backgrounds
    BG_BLUE = "\033[48;5;24m"
    BG_CYAN = "\033[48;5;30m"
    BG_GREEN = "\033[48;5;22m"
    BG_DARK = "\033[48;5;234m"

def get_banner() -> str:
    """
    Returns the stylized Blue & Green ASCII banner for IQ MAXX (by dk).
    'IQ MAXX' is highlighted in bold electric cyan/blue.
    '(by dk)' is displayed as a sleek small subtitle in neon green.
    """
    c = Colors
    banner = f"""
{c.CYAN}{c.BOLD} ██╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗██╗  ██╗
{c.CYAN}{c.BOLD} ██║██╔═══██╗    ████╗ ████║██╔══██╗╚██╗██╔╝╚██╗██╔╝
{c.BLUE}{c.BOLD} ██║██║   ██║    ██╔████╔██║███████║ ╚███╔╝  ╚███╔╝ 
{c.BLUE}{c.BOLD} ██║██║▄▄ ██║    ██║╚██╔╝██║██╔══██║ ██╔██╗  ██╔██╗ 
{c.BLUE_DEEP}{c.BOLD} ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗██╔╝ ██╗
{c.NAVY}{c.BOLD} ╚═╝ ╚══▀▀═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{c.RESET}
       {c.BLUE}⚡ {c.CYAN}{c.BOLD}I Q   M A X X{c.RESET} {c.DIM}{c.GRAY}─{c.RESET} {c.GREEN_BRIGHT}v2.5.0{c.RESET} {c.GRAY}│{c.RESET} {c.GREEN_LIME}{c.ITALIC}(by dk){c.RESET}
       {c.CYAN_PALE}Advanced Cross-Platform Wi-Fi Auditing & Password Access Suite{c.RESET}
       {c.GRAY}Supports: {c.GREEN}Terminal (macOS/Linux){c.GRAY} • {c.CYAN}PowerShell (Windows){c.GRAY} • {c.GREEN_BRIGHT}Termux (Android){c.RESET}
"""
    return banner

def print_banner():
    """Prints the IQ MAXX banner to stdout."""
    print(get_banner())

def tag_info(msg: str) -> str:
    c = Colors
    return f"{c.CYAN}[{c.BOLD}*{c.RESET}{c.CYAN}]{c.RESET} {c.WHITE}{msg}{c.RESET}"

def tag_success(msg: str) -> str:
    c = Colors
    return f"{c.GREEN_BRIGHT}[{c.BOLD}✓{c.RESET}{c.GREEN_BRIGHT}]{c.RESET} {c.GREEN}{msg}{c.RESET}"

def tag_warn(msg: str) -> str:
    c = Colors
    return f"{c.YELLOW}[{c.BOLD}!{c.RESET}{c.YELLOW}]{c.RESET} {c.YELLOW}{msg}{c.RESET}"

def tag_error(msg: str) -> str:
    c = Colors
    return f"{c.RED}[{c.BOLD}✗{c.RESET}{c.RED}]{c.RESET} {c.RED}{msg}{c.RESET}"

def tag_plus(msg: str) -> str:
    c = Colors
    return f"{c.BLUE}[{c.BOLD}+{c.RESET}{c.BLUE}]{c.RESET} {c.CYAN}{msg}{c.RESET}"

def print_section(title: str, subtitle: str = ""):
    c = Colors
    line = f"{c.CYAN}═" * 68 + f"{c.RESET}"
    print(f"\n{line}")
    print(f" {c.BLUE}⚡ {c.CYAN}{c.BOLD}{title.upper()}{c.RESET}" + (f" {c.GRAY}─ {c.GREEN}{subtitle}{c.RESET}" if subtitle else ""))
    print(f"{line}\n")

def print_table(headers: list, rows: list, alignments: list = None):
    """
    Renders a sleek Cyberpunk Blue & Green ASCII table.
    """
    c = Colors
    if not rows:
        print(f"  {c.GRAY}(No data available){c.RESET}")
        return

    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            # Strip ANSI when calculating width
            raw_len = len(strip_ansi(str(val)))
            if raw_len > col_widths[i]:
                col_widths[i] = raw_len

    # Add padding
    col_widths = [w + 2 for w in col_widths]

    # Top border
    top_line = f"{c.CYAN}┌" + "┬".join("─" * w for w in col_widths) + f"┐{c.RESET}"
    mid_line = f"{c.BLUE}├" + "┼".join("─" * w for w in col_widths) + f"┤{c.RESET}"
    bot_line = f"{c.CYAN}└" + "┴".join("─" * w for w in col_widths) + f"┘{c.RESET}"

    print(top_line)
    
    # Header row
    header_cells = []
    for i, h in enumerate(headers):
        w = col_widths[i]
        header_cells.append(f" {c.CYAN}{c.BOLD}{h:<{w-1}}{c.RESET}")
    print(f"{c.CYAN}│{c.RESET}" + f"{c.CYAN}│{c.RESET}".join(header_cells) + f"{c.CYAN}│{c.RESET}")
    print(mid_line)

    # Data rows
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            w = col_widths[i]
            val_str = str(cell)
            raw_len = len(strip_ansi(val_str))
            padding = " " * (w - raw_len - 1)
            cells.append(f" {val_str}{padding}")
        print(f"{c.BLUE}│{c.RESET}" + f"{c.BLUE}│{c.RESET}".join(cells) + f"{c.BLUE}│{c.RESET}")

    print(bot_line)

def strip_ansi(text: str) -> str:
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def format_strength(score: int, label: str) -> str:
    """Format password strength badge in theme colors."""
    c = Colors
    if score >= 4:
        return f"{c.GREEN_BRIGHT}●●●● {label}{c.RESET}"
    elif score == 3:
        return f"{c.GREEN}●●●○ {label}{c.RESET}"
    elif score == 2:
        return f"{c.YELLOW}●●○○ {label}{c.RESET}"
    else:
        return f"{c.RED}●○○○ {label}{c.RESET}"

def format_signal(signal_pct: int) -> str:
    """Format signal strength meter in theme colors."""
    c = Colors
    if signal_pct >= 75:
        bars = f"{c.GREEN_BRIGHT}████{c.RESET}"
    elif signal_pct >= 50:
        bars = f"{c.GREEN}███{c.GRAY}░{c.RESET}"
    elif signal_pct >= 25:
        bars = f"{c.CYAN}██{c.GRAY}░░{c.RESET}"
    else:
        bars = f"{c.RED}█{c.GRAY}░░░{c.RESET}"
    return f"{bars} {c.WHITE}{signal_pct}%{c.RESET}"
