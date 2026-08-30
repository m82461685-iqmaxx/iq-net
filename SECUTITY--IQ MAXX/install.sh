#!/usr/bin/env bash
# ==============================================================================
# IQ MAXX (by dk) - Linux, macOS & Android (Termux) 1-Click Installer
# Automatically sets up the 'iqmaxx' global command
# ==============================================================================

C_RESET="\033[0m"
C_BOLD="\033[1m"
C_CYAN="\033[38;5;51m"
C_BLUE="\033[38;5;39m"
C_GREEN="\033[38;5;48m"
C_MATRIX="\033[38;5;46m"
C_WHITE="\033[38;5;255m"
C_GRAY="\033[38;5;244m"
C_YELLOW="\033[38;5;220m"

echo -e "${C_CYAN}${C_BOLD}"
echo " ██╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗██╗  ██╗"
echo " ██║██╔═══██╗    ████╗ ████║██╔══██╗╚██╗██╔╝╚██╗██╔╝"
echo " ██║██║   ██║    ██╔████╔██║███████║ ╚███╔╝  ╚███╔╝ "
echo " ██║██║▄▄ ██║    ██║╚██╔╝██║██╔══██║ ██╔██╗  ██╔██╗ "
echo " ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗██╔╝ ██╗"
echo " ╚═╝ ╚══▀▀═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝"
echo -e "${C_RESET}"
echo -e "       ${C_BLUE}⚡ ${C_CYAN}${C_BOLD}IQ MAXX INSTALLER${C_RESET} ${C_GRAY}│${C_RESET} ${C_GREEN}(by dk)${C_RESET}"
echo -e "       ${C_GRAY}Configuring 1-Command Access across macOS / Linux / Termux...${C_RESET}\n"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Grant execute permissions
chmod +x "$SCRIPT_DIR/iqmaxx.sh" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/iqmaxx.py" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/install.sh" 2>/dev/null || true
echo -e " ${C_MATRIX}[✓]${C_RESET} Granted executable permissions to scripts."

# 2. Determine target binary path
TARGET_BIN=""
if [ -d "/data/data/com.termux" ] || [ -n "$TERMUX_VERSION" ]; then
    TARGET_BIN="$PREFIX/bin/iqmaxx"
elif [ -w "/usr/local/bin" ]; then
    TARGET_BIN="/usr/local/bin/iqmaxx"
elif [ -d "$HOME/.local/bin" ]; then
    TARGET_BIN="$HOME/.local/bin/iqmaxx"
elif [ -d "$HOME/bin" ]; then
    TARGET_BIN="$HOME/bin/iqmaxx"
fi

# Create launcher wrapper
LAUNCHER_SCRIPT="#!/usr/bin/env bash
if command -v python3 >/dev/null 2>&1 && [ -f \"$SCRIPT_DIR/iqmaxx.py\" ]; then
    python3 \"$SCRIPT_DIR/iqmaxx.py\" \"\$@\"
else
    bash \"$SCRIPT_DIR/iqmaxx.sh\" \"\$@\"
fi
"

if [ -n "$TARGET_BIN" ]; then
    echo "$LAUNCHER_SCRIPT" > "$TARGET_BIN"
    chmod +x "$TARGET_BIN"
    echo -e " ${C_MATRIX}[✓]${C_RESET} Created binary link at: ${C_CYAN}$TARGET_BIN${C_RESET}"
else
    # Fallback to shell aliases
    echo -e " ${C_YELLOW}[!]${C_RESET} System bin directory requires root; configuring user shell aliases..."
fi

# 3. Add alias to shell profiles (.bashrc, .zshrc)
ALIAS_CMD="alias iqmaxx='bash \"$SCRIPT_DIR/iqmaxx.sh\"'"
for rc_file in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile" "$HOME/.bash_profile"; do
    if [ -f "$rc_file" ]; then
        if ! grep -q "alias iqmaxx=" "$rc_file"; then
            echo "" >> "$rc_file"
            echo "# IQ MAXX (by dk) Wi-Fi Auditing Suite" >> "$rc_file"
            echo "$ALIAS_CMD" >> "$rc_file"
            echo -e " ${C_MATRIX}[✓]${C_RESET} Configured alias in: ${C_CYAN}$rc_file${C_RESET}"
        fi
    fi
done

echo -e "\n${C_CYAN}════════════════════════════════════════════════════════════════════${C_RESET}"
echo -e " ${C_MATRIX}${C_BOLD}[✓] IQ MAXX (by dk) Installation Complete!${C_RESET}"
echo -e "${C_CYAN}════════════════════════════════════════════════════════════════════${C_RESET}"
echo -e " You can now execute IQ MAXX from any terminal prompt:"
echo -e "   ${C_CYAN}iqmaxx${C_RESET}               ${C_GRAY}# Interactive TUI dashboard${C_RESET}"
echo -e "   ${C_CYAN}iqmaxx dump${C_RESET}          ${C_GRAY}# Extract saved Wi-Fi passphrases${C_RESET}"
echo -e "   ${C_CYAN}iqmaxx scan${C_RESET}          ${C_GRAY}# Scan nearby wireless networks${C_RESET}"
echo -e "   ${C_CYAN}iqmaxx audit${C_RESET}         ${C_GRAY}# Run password security audit${C_RESET}"
echo -e "   ${C_CYAN}iqmaxx qr${C_RESET}            ${C_GRAY}# Generate terminal QR connection code${C_RESET}"
echo -e "   ${C_CYAN}iqmaxx export${C_RESET}        ${C_GRAY}# Generate HTML / JSON audit reports${C_RESET}"
echo -e "${C_CYAN}════════════════════════════════════════════════════════════════════${C_RESET}\n"
