# IQ MAXX (by dk) - Windows Native PowerShell Wi-Fi Auditing & Password Access Suite

[CmdletBinding()]
param (
    [Parameter(Position=0)]
    [ValidateSet("dump", "scan", "audit", "export", "menu", "help", "banner")]
    [string]$Action = "menu",

    [Parameter()]
    [string]$SSID = "",

    [Parameter()]
    [string]$OutHtml = "wifi_audit_report.html",

    [Parameter()]
    [string]$OutJson = "wifi_backup.json",

    [Parameter()]
    [string]$OutCsv = "wifi_export.csv"
)

function Show-Banner {
    Write-Host " ===================================================================" -ForegroundColor Cyan
    Write-Host "  II  QQQQ      MM   MM   AAAA   XX  XX  XX  XX" -ForegroundColor Cyan
    Write-Host "  II QQ  QQ     MMM MMM  AA  AA   XXXX    XXXX" -ForegroundColor Cyan
    Write-Host "  II QQ  QQ     MM M MM  AAAAAA    XX      XX" -ForegroundColor Blue
    Write-Host "  II QQ  QQ     MM   MM  AA  AA   XXXX    XXXX" -ForegroundColor Blue
    Write-Host "  II  QQQQ QQ   MM   MM  AA  AA  XX  XX  XX  XX" -ForegroundColor DarkCyan
    Write-Host " ===================================================================" -ForegroundColor Cyan
    Write-Host "   * IQ MAXX - v2.5.0 | (by dk)" -ForegroundColor Green
    Write-Host "   Advanced Cross-Platform Wi-Fi Auditing & Password Access Suite" -ForegroundColor Cyan
    Write-Host "   Native Windows PowerShell Edition - Theme: Blue & Green" -ForegroundColor DarkCyan
    Write-Host " ===================================================================`n" -ForegroundColor Cyan
}

function Show-SectionHeader([string]$Title, [string]$Subtitle = "") {
    Write-Host "--------------------------------------------------------------------" -ForegroundColor Cyan
    if ($Subtitle) {
        Write-Host " [*] $Title - $Subtitle" -ForegroundColor Green
    } else {
        Write-Host " [*] $Title" -ForegroundColor Green
    }
    Write-Host "--------------------------------------------------------------------`n" -ForegroundColor Cyan
}

function Get-SavedWifiProfiles {
    $Profiles = @()
    $RawProfiles = netsh wlan show profiles 2>&1

    $ProfileNames = @()
    foreach ($line in $RawProfiles) {
        if ($line -like "*:*" -and ($line -match 'Profile|Profil|Perfil|perfiles')) {
            $parts = $line.Split(":", 2)
            if ($parts.Count -ge 2) {
                $pName = $parts[1].Trim()
                if ($pName -and ($ProfileNames -notcontains $pName)) {
                    $ProfileNames += $pName
                }
            }
        }
    }

    foreach ($name in $ProfileNames) {
        $detail = netsh wlan show profile name="$name" key=clear 2>&1
        $pwd = ""
        $auth = "WPA2-Personal"
        $cipher = "CCMP/AES"

        foreach ($dline in $detail) {
            if ($dline -like "*:*") {
                $dparts = $dline.Split(":", 2)
                $k = $dparts[0].Trim().ToLower()
                $v = $dparts[1].Trim()

                if ($k -match 'key content|contenu de la cl|contenido de la clave|schl.sselinhalt') {
                    $pwd = $v
                }
                elseif ($k -match 'authentication|authentification|autenticaci.n') {
                    $auth = $v
                }
                elseif ($k -match 'cipher|chiffrement|cifrado') {
                    $cipher = $v
                }
                elseif ($k -match 'security key' -and $v -match 'Absent') {
                    if (-not $pwd) { $pwd = "[Open Network]" }
                }
            }
        }

        if (-not $pwd) {
            if ($auth -match 'Open|None') {
                $pwd = "[Open Network]"
            } else {
                $pwd = "[Password Not Stored / 802.1X]"
            }
        }

        $rating = "MODERATE"
        $rateColor = "Yellow"
        if ($pwd -match '^\[') {
            $rating = "N/A"
            $rateColor = "DarkGray"
        } elseif ($pwd.Length -ge 12) {
            $rating = "STRONG"
            $rateColor = "Green"
        } elseif ($pwd.Length -lt 8 -or $pwd -match '^(12345678|00000000|password|admin123)') {
            $rating = "CRITICAL WEAK"
            $rateColor = "Red"
        }

        $Profiles += [PSCustomObject]@{
            Index       = ($Profiles.Count + 1)
            SSID        = $name
            Password    = $pwd
            Auth        = $auth
            Cipher      = $cipher
            Rating      = $rating
            RatingColor = $rateColor
        }
    }

    return $Profiles
}

function Invoke-Dump {
    Show-SectionHeader -Title "SAVED WI-FI CREDENTIALS DUMP" -Subtitle "Windows Netsh Engine"
    Write-Host " [*] Querying stored wireless network profiles..." -ForegroundColor Cyan

    $Profiles = Get-SavedWifiProfiles

    if ($Profiles.Count -eq 0) {
        Write-Host " [!] No Wi-Fi profiles found." -ForegroundColor Yellow
        return
    }

    Write-Host "+----+--------------------------+--------------------------------+-----------------+----------+--------------------+" -ForegroundColor Cyan
    Write-Host ("| {0,-2} | {1,-24} | {2,-30} | {3,-15} | {4,-8} | {5,-18} |" -f "#", "SSID / Network", "Passphrase", "Auth Type", "Cipher", "Rating") -ForegroundColor Green
    Write-Host "+----+--------------------------+--------------------------------+-----------------+----------+--------------------+" -ForegroundColor Cyan

    foreach ($p in $Profiles) {
        $idxStr  = "{0,-2}" -f $p.Index
        $ssidStr = if ($p.SSID.Length -gt 24) { $p.SSID.Substring(0,21) + "..." } else { "{0,-24}" -f $p.SSID }
        $pwdStr  = if ($p.Password.Length -gt 30) { $p.Password.Substring(0,27) + "..." } else { "{0,-30}" -f $p.Password }
        $authStr = if ($p.Auth.Length -gt 15) { $p.Auth.Substring(0,12) + "..." } else { "{0,-15}" -f $p.Auth }
        $ciphStr = if ($p.Cipher.Length -gt 8) { $p.Cipher.Substring(0,8) } else { "{0,-8}" -f $p.Cipher }
        $rateStr = "{0,-18}" -f $p.Rating

        $line = "| $idxStr | $ssidStr | $pwdStr | $authStr | $ciphStr | $rateStr |"
        if ($p.Password -match '^\[') {
            Write-Host $line -ForegroundColor DarkGray
        } else {
            Write-Host $line -ForegroundColor White
        }
    }

    Write-Host "+----+--------------------------+--------------------------------+-----------------+----------+--------------------+" -ForegroundColor Cyan
    Write-Host "`n [v] Successfully dumped $($Profiles.Count) saved Wi-Fi profiles.`n" -ForegroundColor Green
}

function Invoke-Scan {
    Show-SectionHeader -Title "LIVE AIRWAVE SCANNER" -Subtitle "Nearby Access Points"
    Write-Host " [*] Scanning 2.4GHz & 5GHz wireless spectrum...`n" -ForegroundColor Cyan

    $raw = netsh wlan show networks mode=bssid 2>&1
    Write-Host $raw -ForegroundColor Gray
}

function Invoke-Audit {
    Show-SectionHeader -Title "SECURITY & ENTROPY AUDIT" -Subtitle "Password Posture Analysis"
    $Profiles = Get-SavedWifiProfiles

    foreach ($p in $Profiles) {
        Write-Host " +---[ Network #$($p.Index): $($p.SSID) ]" -ForegroundColor Cyan
        Write-Host " |  Passphrase:     $($p.Password)" -ForegroundColor Green
        Write-Host " |  Auth Method:    $($p.Auth)  |  Cipher: $($p.Cipher)" -ForegroundColor Cyan
        Write-Host " |  Security Level: $($p.Rating)" -ForegroundColor $p.RatingColor
        Write-Host " +---`n" -ForegroundColor Cyan
    }
}

function Invoke-ExportAll {
    Show-SectionHeader -Title "CREDENTIALS EXPORTER" -Subtitle "JSON & CSV Exporter"
    $Profiles = Get-SavedWifiProfiles

    $exportData = @()
    foreach ($p in $Profiles) {
        $exportData += [PSCustomObject]@{
            ssid     = $p.SSID
            password = $p.Password
            auth     = $p.Auth
            cipher   = $p.Cipher
            platform = "Windows (PowerShell)"
        }
    }

    $exportData | ConvertTo-Json -Depth 4 | Set-Content -Path $OutJson -Encoding UTF8
    Write-Host " [v] Exported JSON: $OutJson" -ForegroundColor Green

    $exportData | Export-Csv -Path $OutCsv -NoTypeInformation -Encoding UTF8
    Write-Host " [v] Exported CSV:  $OutCsv`n" -ForegroundColor Green
}

# Main Execution Routing
switch ($Action.ToLower()) {
    "banner"  { Show-Banner }
    "dump"    { Show-Banner; Invoke-Dump }
    "scan"    { Show-Banner; Invoke-Scan }
    "audit"   { Show-Banner; Invoke-Audit }
    "export"  { Show-Banner; Invoke-ExportAll }
    "help"    {
        Show-Banner
        Write-Host " POWERSHELL USAGE:" -ForegroundColor Cyan
        Write-Host "   .\iqmaxx.ps1 -Action dump       # Dump all stored Wi-Fi credentials" -ForegroundColor Gray
        Write-Host "   .\iqmaxx.ps1 -Action scan       # Scan live airwaves for nearby access points" -ForegroundColor Gray
        Write-Host "   .\iqmaxx.ps1 -Action audit      # Cryptographic security audit" -ForegroundColor Gray
        Write-Host "   .\iqmaxx.ps1 -Action export     # Export to JSON & CSV" -ForegroundColor Gray
        Write-Host "   .\iqmaxx.ps1                    # Launch interactive menu" -ForegroundColor Gray
    }
    default {
        while ($true) {
            Clear-Host
            Show-Banner
            Write-Host "  +=============================================================+" -ForegroundColor Cyan
            Write-Host "  |  * POWERSHELL CONTROL PANEL                                 |" -ForegroundColor Green
            Write-Host "  +=============================================================+" -ForegroundColor Cyan
            Write-Host "  |  (1) Dump Saved Wi-Fi Passwords   Extract stored OS keys    |" -ForegroundColor White
            Write-Host "  |  (2) Live Airwave Wi-Fi Scanner   Scan nearby BSSID/Channels|" -ForegroundColor White
            Write-Host "  |  (3) Security & Entropy Audit     Analyze password strength |" -ForegroundColor White
            Write-Host "  |  (4) Export Audit (JSON/CSV)      Backup wireless keys      |" -ForegroundColor White
            Write-Host "  |  (0) Exit IQ MAXX                                           |" -ForegroundColor Yellow
            Write-Host "  +=============================================================+" -ForegroundColor Cyan

            $choice = Read-Host "`n  iqmaxx>"
            switch ($choice) {
                "1" { Invoke-Dump; Read-Host "`n Press Enter to continue..." }
                "2" { Invoke-Scan; Read-Host "`n Press Enter to continue..." }
                "3" { Invoke-Audit; Read-Host "`n Press Enter to continue..." }
                "4" { Invoke-ExportAll; Read-Host "`n Press Enter to continue..." }
                "0" { Write-Host "`n [*] Exiting IQ MAXX. Stay secure!`n" -ForegroundColor Cyan; break }
                default { }
            }
            if ($choice -eq "0") { break }
        }
    }
}
