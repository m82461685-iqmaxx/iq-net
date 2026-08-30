@echo off
if exist "%~dp0\iqmaxx.py" (
    python "%~dp0\iqmaxx.py" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0\iqmaxx.ps1" %*
)
