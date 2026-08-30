#!/usr/bin/env bash
# ==============================================================================
# IQ MAXX (by dk) - Wi-Fi Auditing & Password Access Suite
# Native Terminal Edition for macOS, Linux, and Android (Termux)
# Theme: Complete Blue & Green
# ==============================================================================

# ANSI Color Definitions (Cyan / Blue & Neon Green)
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_DIM="\033[2m"
C_CYAN="\033[38;5;51m"
C_BLUE="\033[38;5;39m"
C_DEEP_BLUE="\033[38;5;27m"
C_NAVY="\033[38;5;24m"
C_GREEN="\033[38;5;48m"
C_LIME="\033[38;5;118m"
C_MATRIX="\033[38;5;46m"
C_WHITE="\033[38;5;255m"
C_GRAY="\033[38;5;244m"
C_YELLOW="\033[38;5;220m"
C_RED="\033[38;5;196m"

TAG_INFO="${C_CYAN}[*]${C_RESET}"
TAG_OK="${C_MATRIX}[✓]${C_RESET}"
TAG_WARN="${C_YELLOW}[!]${C_RESET}"
TAG_PLUS="${C_BLUE}[+]${C_RESET}"

show_banner() {
    cat << EOF

${C_CYAN}${C_BOLD} ██╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗██╗  ██╗
${C_CYAN}${C_BOLD} ██║██╔═══██╗    ████╗ ████║██╔══██╗╚██╗██╔╝╚██╗██╔╝
${C_BLUE}${C_BOLD} ██║██║   ██║    ██╔████╔██║███████║ ╚███╔╝  ╚███╔╝ 
${C_BLUE}${C_BOLD} ██║██║▄▄ ██║    ██║╚██╔╝██║██╔══██║ ██╔██╗  ██╔██╗ 
${C_DEEP_BLUE}${C_BOLD} ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗██╔╝ ██╗
${C_NAVY}${C_BOLD} ╚═╝ ╚══▀▀═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝${C_RESET}
       ${C_BLUE}⚡ ${C_CYAN}${C_BOLD}I Q   M A X X${C_RESET} ${C_GRAY}─${C_RESET} ${C_MATRIX}v2.5.0${C_RESET} ${C_GRAY}│${C_RESET} ${C_LIME}(by dk)${C_RESET}
       ${C_CYAN}Advanced Cross-Platform Wi-Fi Auditing & Password Access Suite${C_RESET}
       ${C_GRAY}Native Terminal Edition • ${C_GREEN}macOS / Linux / Termux (Android)${C_RESET}

EOF
}

show_section() {
    local title="$1"
    local subtitle="$2"
    echo -e "\n${C_CYAN}════════════════════════════════════════════════════════════════════${C_RESET}"
    if [ -n "$subtitle" ]; then
        echo -e " ${C_BLUE}⚡ ${C_CYAN}${C_BOLD}${title}${C_RESET} ${C_GRAY}─ ${C_GREEN}${subtitle}${C_RESET}"
    else
        echo -e " ${C_BLUE}⚡ ${C_CYAN}${C_BOLD}${title}${C_RESET}"
    fi
    echo -e "${C_CYAN}════════════════════════════════════════════════════════════════════${C_RESET}\n"
}

detect_platform() {
    if [ -d "/data/data/com.termux" ] || [ -n "$TERMUX_VERSION" ]; then
        echo "termux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]] || [ -f "/etc/os-release" ]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

dump_credentials() {
    show_section "SAVED WI-FI CREDENTIALS DUMP" "Platform: $(detect_platform)"
    echo -e " ${TAG_INFO} ${C_WHITE}Querying stored wireless credentials...${C_RESET}\n"

    # If python3 engine is available, invoke it for highest fidelity rendering
    if command -v python3 >/dev/null 2>&1 && [ -f "$(dirname "$0")/iqmaxx.py" ]; then
        python3 "$(dirname "$0")/iqmaxx.py" dump
        return
    elif command -v python >/dev/null 2>&1 && [ -f "$(dirname "$0")/iqmaxx.py" ]; then
        python "$(dirname "$0")/iqmaxx.py" dump
        return
    fi

    # Native Bash fallback per OS
    local plat
    plat=$(detect_platform)
    local count=0

    printf "${C_CYAN}+----+--------------------------+--------------------------------+-----------------+----------+--------------------+${C_RESET}\n"
    printf "${C_CYAN}|${C_RESET} ${C_CYAN}${C_BOLD}%-2s${C_RESET} ${C_CYAN}|${C_RESET} ${C_CYAN}${C_BOLD}%-24s${C_RESET} ${C_CYAN}|${C_RESET} ${C_CYAN}${C_BOLD}%-30s${C_RESET} ${C_CYAN}|${C_RESET} ${C_CYAN}${C_BOLD}%-15s${C_RESET} ${C_CYAN}|${C_RESET} ${C_CYAN}${C_BOLD}%-8s${C_RESET} ${C_CYAN}|${C_RESET} ${C_CYAN}${C_BOLD}%-18s${C_RESET} ${C_CYAN}|${C_RESET}\n" "#" "SSID / Network" "Passphrase" "Auth Type" "Cipher" "Rating"
    printf "${C_CYAN}+----+--------------------------+--------------------------------+-----------------+----------+--------------------+${C_RESET}\n"

    if [ "$plat" == "linux" ]; then
        if [ -d "/etc/NetworkManager/system-connections" ]; then
            for f in /etc/NetworkManager/system-connections/*; do
                if [ -f "$f" ]; then
                    count=$((count+1))
                    local ssid psk auth
                    ssid=$(grep -E '^ssid=' "$f" | cut -d'=' -f2 | tr -d '\r')
                    [ -z "$ssid" ] && ssid=$(basename "$f" .nmconnection)
                    psk=$(grep -E '^psk=' "$f" | cut -d'=' -f2 | tr -d '\r')
                    [ -z "$psk" ] && psk="[Requires Sudo / Open]"
                    auth=$(grep -E '^key-mgmt=' "$f" | cut -d'=' -f2 | tr -d '\r')
                    [ -z "$auth" ] && auth="WPA-PSK"

                    local rating="MODERATE"
                    [ ${#psk} -ge 12 ] && rating="STRONG"
                    [ ${#psk} -lt 8 ] && rating="CRITICAL WEAK"

                    printf "${C_BLUE}|${C_RESET} ${C_CYAN}%-2s${C_RESET} ${C_BLUE}|${C_RESET} ${C_WHITE}%-24.24s${C_RESET} ${C_BLUE}|${C_RESET} ${C_MATRIX}%-30.30s${C_RESET} ${C_BLUE}|${C_RESET} ${C_CYAN}%-15.15s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GRAY}%-8.8s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GREEN}%-18.18s${C_RESET} ${C_BLUE}|${C_RESET}\n" "$count" "$ssid" "$psk" "$auth" "AES" "$rating"
                fi
            done
        elif command -v nmcli >/dev/null 2>&1; then
            while IFS=: read -r name type uuid; do
                if [[ "$type" == *"wireless"* ]] || [[ "$type" == *"wifi"* ]]; then
                    count=$((count+1))
                    local psk
                    psk=$(nmcli -s -g 802-11-wireless-security.psk connection show "$name" 2>/dev/null)
                    [ -z "$psk" ] && psk="[Requires Sudo / Open]"
                    printf "${C_BLUE}|${C_RESET} ${C_CYAN}%-2s${C_RESET} ${C_BLUE}|${C_RESET} ${C_WHITE}%-24.24s${C_RESET} ${C_BLUE}|${C_RESET} ${C_MATRIX}%-30.30s${C_RESET} ${C_BLUE}|${C_RESET} ${C_CYAN}%-15.15s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GRAY}%-8.8s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GREEN}%-18.18s${C_RESET} ${C_BLUE}|${C_RESET}\n" "$count" "$name" "$psk" "WPA2-PSK" "AES" "MODERATE"
                fi
            done < <(nmcli -t -f NAME,TYPE,UUID connection show 2>/dev/null)
        fi
    elif [ "$plat" == "macos" ]; then
        local iface="en0"
        while IFS= read -r line; do
            local ssid="$line"
            if [ -n "$ssid" ] && [[ "$ssid" != "Preferred networks"* ]]; then
                count=$((count+1))
                local psk
                psk=$(security find-generic-password -D "AirPort network password" -wa "$ssid" 2>/dev/null)
                [ -z "$psk" ] && psk="[Requires Keychain Auth]"
                printf "${C_BLUE}|${C_RESET} ${C_CYAN}%-2s${C_RESET} ${C_BLUE}|${C_RESET} ${C_WHITE}%-24.24s${C_RESET} ${C_BLUE}|${C_RESET} ${C_MATRIX}%-30.30s${C_RESET} ${C_BLUE}|${C_RESET} ${C_CYAN}%-15.15s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GRAY}%-8.8s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GREEN}%-18.18s${C_RESET} ${C_BLUE}|${C_RESET}\n" "$count" "$ssid" "$psk" "WPA2/WPA3" "AES" "MODERATE"
            fi
        done < <(networksetup -listpreferredwirelessnetworks "$iface" 2>/dev/null)
    elif [ "$plat" == "termux" ]; then
        if command -v su >/dev/null 2>&1; then
            # Query android root wifi config store
            local xml_data
            xml_data=$(su -c "cat /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml || cat /data/misc/wifi/WifiConfigStore.xml" 2>/dev/null)
            if [ -n "$xml_data" ]; then
                echo "$xml_data" | grep -E 'name="SSID"|name="PreSharedKey"' | while read -r l1 && read -r l2; do
                    count=$((count+1))
                    local ssid psk
                    ssid=$(echo "$l1" | sed -E 's/.*<string name="SSID">"?(.*)"?<\/string>/\1/')
                    psk=$(echo "$l2" | sed -E 's/.*<string name="PreSharedKey">"?(.*)"?<\/string>/\1/')
                    printf "${C_BLUE}|${C_RESET} ${C_CYAN}%-2s${C_RESET} ${C_BLUE}|${C_RESET} ${C_WHITE}%-24.24s${C_RESET} ${C_BLUE}|${C_RESET} ${C_MATRIX}%-30.30s${C_RESET} ${C_BLUE}|${C_RESET} ${C_CYAN}%-15.15s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GRAY}%-8.8s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GREEN}%-18.18s${C_RESET} ${C_BLUE}|${C_RESET}\n" "$count" "$ssid" "$psk" "WPA2" "AES" "MODERATE"
                done
            fi
        fi
        if [ $count -eq 0 ] && command -v termux-wifi-connectioninfo >/dev/null 2>&1; then
            local curr
            curr=$(termux-wifi-connectioninfo 2>/dev/null)
            local ssid
            ssid=$(echo "$curr" | grep '"ssid"' | cut -d'"' -f4)
            if [ -n "$ssid" ] && [ "$ssid" != "<unknown ssid>" ]; then
                count=1
                printf "${C_BLUE}|${C_RESET} ${C_CYAN}%-2s${C_RESET} ${C_BLUE}|${C_RESET} ${C_WHITE}%-24.24s${C_RESET} ${C_BLUE}|${C_RESET} ${C_MATRIX}%-30.30s${C_RESET} ${C_BLUE}|${C_RESET} ${C_CYAN}%-15.15s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GRAY}%-8.8s${C_RESET} ${C_BLUE}|${C_RESET} ${C_GREEN}%-18.18s${C_RESET} ${C_BLUE}|${C_RESET}\n" "1" "$ssid" "[Connected Network]" "WPA2/WPA3" "AES" "ACTIVE"
            fi
        fi
    fi

    printf "${C_CYAN}+----+--------------------------+--------------------------------+-----------------+----------+--------------------+${C_RESET}\n\n"
    echo -e " ${TAG_OK} Processed saved Wi-Fi profiles.\n"
}

scan_airwaves() {
    show_section "LIVE AIRWAVE SCANNER" "Spectrum Analysis"
    echo -e " ${TAG_INFO} ${C_WHITE}Scanning wireless channels for active beacons...${C_RESET}\n"

    if command -v python3 >/dev/null 2>&1 && [ -f "$(dirname "$0")/iqmaxx.py" ]; then
        python3 "$(dirname "$0")/iqmaxx.py" scan
        return
    fi

    local plat
    plat=$(detect_platform)
    if [ "$plat" == "linux" ] && command -v nmcli >/dev/null 2>&1; then
        nmcli dev wifi list --rescan auto
    elif [ "$plat" == "macos" ]; then
        /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s 2>/dev/null
    elif [ "$plat" == "termux" ] && command -v termux-wifi-scaninfo >/dev/null 2>&1; then
        termux-wifi-scaninfo
    else
        echo -e " ${TAG_WARN} Scanner utility (nmcli / airport / termux-wifi-scaninfo) not detected."
    fi
}

interactive_menu() {
    while true; do
        clear 2>/dev/null || true
        show_banner
        cat << EOF
  ${C_CYAN}╔═══════════════════════════════════════════════════════════════╗${C_RESET}
  ${C_CYAN}║${C_RESET}  ${C_BOLD}${C_BLUE}⚡ TERMINAL CONTROL PANEL${C_RESET}                                   ${C_CYAN}║${C_RESET}
  ${C_CYAN}╠═══════════════════════════════════════════════════════════════╣${C_RESET}
  ${C_CYAN}║${C_RESET}  ${C_MATRIX}[1]${C_RESET} ${C_WHITE}Dump Saved Wi-Fi Passwords${C_RESET}     ${C_GRAY}Extract stored OS keys${C_RESET}    ${C_CYAN}║${C_RESET}
  ${C_CYAN}║${C_RESET}  ${C_MATRIX}[2]${C_RESET} ${C_WHITE}Live Airwave Wi-Fi Scanner${C_RESET}     ${C_GRAY}Scan nearby BSSID/Channels${C_RESET}${C_CYAN}║${C_RESET}
  ${C_CYAN}║${C_RESET}  ${C_MATRIX}[3]${C_RESET} ${C_WHITE}Security & Entropy Audit${C_RESET}       ${C_GRAY}Analyze password strength${C_RESET} ${C_CYAN}║${C_RESET}
  ${C_CYAN}║${C_RESET}  ${C_MATRIX}[4]${C_RESET} ${C_WHITE}Generate Terminal Wi-Fi QR${C_RESET}     ${C_GRAY}Instant mobile camera link${C_RESET}${C_CYAN}║${C_RESET}
  ${C_CYAN}║${C_RESET}  ${C_MATRIX}[5]${C_RESET} ${C_WHITE}Export Audit (HTML/JSON/CSV)$${C_RESET}   ${C_GRAY}Generate visual dashboard${C_RESET} ${C_CYAN}║${C_RESET}
  ${C_CYAN}║${C_RESET}  ${C_RED}[0]${C_RESET} ${C_WHITE}Exit IQ MAXX${C_RESET}                                               ${C_CYAN}║${C_RESET}
  ${C_CYAN}╚═══════════════════════════════════════════════════════════════╝${C_RESET}

EOF
        read -r -p "  iqmaxx❯ " choice
        case "$choice" in
            1) dump_credentials; read -r -p " Press Enter to continue..." ;;
            2) scan_airwaves; read -r -p " Press Enter to continue..." ;;
            3)
                if [ -f "$(dirname "$0")/iqmaxx.py" ]; then
                    python3 "$(dirname "$0")/iqmaxx.py" audit 2>/dev/null || python "$(dirname "$0")/iqmaxx.py" audit
                else
                    echo -e " ${TAG_INFO} Audit requires Python engine."
                fi
                read -r -p " Press Enter to continue..."
                ;;
            4)
                if [ -f "$(dirname "$0")/iqmaxx.py" ]; then
                    python3 "$(dirname "$0")/iqmaxx.py" qr 2>/dev/null || python "$(dirname "$0")/iqmaxx.py" qr
                else
                    echo -e " ${TAG_INFO} QR generator requires Python engine."
                fi
                read -r -p " Press Enter to continue..."
                ;;
            5)
                if [ -f "$(dirname "$0")/iqmaxx.py" ]; then
                    python3 "$(dirname "$0")/iqmaxx.py" export 2>/dev/null || python "$(dirname "$0")/iqmaxx.py" export
                else
                    echo -e " ${TAG_INFO} Exporter requires Python engine."
                fi
                read -r -p " Press Enter to continue..."
                ;;
            0|q|exit)
                echo -e "\n ${TAG_INFO} Exiting IQ MAXX. Stay secure!\n"
                break
                ;;
            *) ;;
        esac
    done
}

# CLI Argument Routing
ACTION="${1:-menu}"
case "$ACTION" in
    banner) show_banner ;;
    dump) show_banner; dump_credentials ;;
    scan) show_banner; scan_airwaves ;;
    audit)
        show_banner
        python3 "$(dirname "$0")/iqmaxx.py" audit 2>/dev/null || python "$(dirname "$0")/iqmaxx.py" audit 2>/dev/null || dump_credentials
        ;;
    qr)
        show_banner
        python3 "$(dirname "$0")/iqmaxx.py" qr "$2" 2>/dev/null || python "$(dirname "$0")/iqmaxx.py" qr "$2"
        ;;
    export)
        show_banner
        python3 "$(dirname "$0")/iqmaxx.py" export 2>/dev/null || python "$(dirname "$0")/iqmaxx.py" export
        ;;
    help|--help|-h)
        show_banner
        cat << EOF
${C_CYAN}${C_BOLD}TERMINAL USAGE:${C_RESET}
  ./iqmaxx.sh               ${C_GRAY}# Launch Interactive Cyberpunk TUI Menu${C_RESET}
  ./iqmaxx.sh dump          ${C_GRAY}# Extract & display all saved Wi-Fi passphrases${C_RESET}
  ./iqmaxx.sh scan          ${C_GRAY}# Scan nearby wireless access points${C_RESET}
  ./iqmaxx.sh audit         ${C_GRAY}# Security entropy audit & weak password detector${C_RESET}
  ./iqmaxx.sh qr [SSID]     ${C_GRAY}# Generate terminal QR code for instant connect${C_RESET}
  ./iqmaxx.sh export        ${C_GRAY}# Export credentials to HTML / JSON / CSV${C_RESET}

EOF
        ;;
    *) interactive_menu ;;
esac
