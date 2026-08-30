# ==============================================================================
# IQ MAXX (by dk) - Windows 1-Click Installer
# Configures the global 'iqmaxx' command function across PowerShell and CMD
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ToolDir = $PSScriptRoot
if (-not $ToolDir) { $ToolDir = (Get-Location).Path }

Write-Host " ===================================================================" -ForegroundColor Cyan
Write-Host "  II  QQQQ      MM   MM   AAAA   XX  XX  XX  XX" -ForegroundColor Cyan
Write-Host "  II QQ  QQ     MMM MMM  AA  AA   XXXX    XXXX" -ForegroundColor Cyan
Write-Host "  II QQ  QQ     MM M MM  AAAAAA    XX      XX" -ForegroundColor Blue
Write-Host "  II QQ  QQ     MM   MM  AA  AA   XXXX    XXXX" -ForegroundColor Blue
Write-Host "  II  QQQQ QQ   MM   MM  AA  AA  XX  XX  XX  XX" -ForegroundColor DarkCyan
Write-Host " ===================================================================" -ForegroundColor Cyan
Write-Host "   * IQ MAXX - Quick Setup & Command Registration" -ForegroundColor Green
Write-Host "   Setting up global 'iqmaxx' command for Windows PowerShell & CMD..." -ForegroundColor DarkCyan
Write-Host " ===================================================================`n" -ForegroundColor Cyan

# 1. Create iqmaxx.cmd launcher in ToolDir for CMD / System PATH execution
$CmdLauncher = Join-Path $ToolDir "iqmaxx.cmd"
$CmdContent = @"
@echo off
if exist "%~dp0\iqmaxx.py" (
    python "%~dp0\iqmaxx.py" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0\iqmaxx.ps1" %*
)
"@
Set-Content -Path $CmdLauncher -Value $CmdContent -Encoding ASCII
Write-Host " [v] Created Windows Command Wrapper: $CmdLauncher" -ForegroundColor Green

# 2. Add Tool Directory to User Environment PATH
try {
    $CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($CurrentPath -notlike "*$ToolDir*") {
        $NewPath = "$CurrentPath;$ToolDir".Trim(';')
        [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
        Write-Host " [v] Added '$ToolDir' to User PATH environment variable." -ForegroundColor Green
    } else {
        Write-Host " [i] '$ToolDir' is already present in User PATH." -ForegroundColor Cyan
    }
} catch {
    Write-Host " [!] Note: Could not modify User PATH automatically. Run as Administrator if needed." -ForegroundColor Yellow
}

# 3. Configure PowerShell Profile Function
try {
    $ProfilePath = $PROFILE.CurrentUserCurrentHost
    if (-not $ProfilePath) { $ProfilePath = $PROFILE }

    $ProfileDir = Split-Path -Parent $ProfilePath
    if (-not (Test-Path $ProfileDir)) {
        New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null
    }

    $FunctionCode = @"

# IQ MAXX (by dk) Command Function
function iqmaxx {
    param([Parameter(ValueFromRemainingArguments=`$true)]`$args)
    if (Test-Path "$ToolDir\iqmaxx.py") {
        python "$ToolDir\iqmaxx.py" `$args
    } else {
        powershell -NoProfile -ExecutionPolicy Bypass -File "$ToolDir\iqmaxx.ps1" `$args
    }
}
"@

    $ExistingProfile = ""
    if (Test-Path $ProfilePath) {
        $ExistingProfile = Get-Content $ProfilePath -Raw
    }

    if ($ExistingProfile -notlike "*function iqmaxx*") {
        Add-Content -Path $ProfilePath -Value $FunctionCode -Encoding UTF8
        Write-Host " [v] Injected 'iqmaxx' function into PowerShell Profile: $ProfilePath" -ForegroundColor Green
    } else {
        Write-Host " [i] 'iqmaxx' function already configured in PowerShell Profile." -ForegroundColor Cyan
    }
} catch {
    Write-Host " [!] Notice: Could not update profile automatically." -ForegroundColor Yellow
}

Write-Host @"
`n===================================================================
 [v] IQ MAXX (by dk) Installation Complete!
===================================================================
 You can now launch IQ MAXX from ANY terminal window by typing:

   iqmaxx               (Launch interactive dashboard)
   iqmaxx dump          (Dump saved Wi-Fi passphrases)
   iqmaxx scan          (Scan nearby networks)
   iqmaxx audit         (Run password security audit)
   iqmaxx export        (Generate HTML / JSON audit reports)
===================================================================
"@ -ForegroundColor Green
