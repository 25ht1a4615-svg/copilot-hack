@echo off
REM Lighting AI - Windows Batch Launcher

setlocal enabledelayedexpansion

echo.
echo ===================================
echo   AI Lighting Controller
echo ===================================
echo.

if "%1"=="" (
    echo Usage: run.bat [command]
    echo.
    echo Commands:
    echo   run        - Start the lighting AI
    echo   install    - Install as Windows startup service (Admin required)
    echo   uninstall  - Remove from startup service (Admin required)
    echo   start      - Start the service (Admin required)
    echo.
    exit /b 1
)

if "%1"=="run" (
    echo [*] Starting Lighting AI...
    echo [*] Listening for voice commands...
    echo.
    python lighting_ai.py
    goto :end
)

if "%1"=="install" (
    echo [*] Installing as Windows startup service...
    python service_installer.py install
    if !errorlevel! equ 0 (
        echo [OK] Installation complete!
    ) else (
        echo [ERROR] Installation failed. Run as Administrator.
    )
    goto :end
)

if "%1"=="uninstall" (
    echo [*] Removing from startup service...
    python service_installer.py uninstall
    if !errorlevel! equ 0 (
        echo [OK] Uninstalled successfully!
    ) else (
        echo [ERROR] Uninstall failed. Run as Administrator.
    )
    goto :end
)

if "%1"=="start" (
    echo [*] Starting service...
    python service_installer.py start
    goto :end
)

echo [ERROR] Unknown command: %1
exit /b 1

:end
pause
