@echo off
setlocal

echo === Seitenrechner Build ===

REM Install build dependencies
uv sync --group dev
if errorlevel 1 (
    echo FEHLER: uv sync fehlgeschlagen.
    pause
    exit /b 1
)

REM Build single-file exe
uv run pyinstaller ^
    --onefile ^
    --windowed ^
    --name Seitenrechner ^
    seitenrechner.py

if errorlevel 1 (
    echo FEHLER: PyInstaller fehlgeschlagen.
    pause
    exit /b 1
)

echo.
echo Fertig! dist\Seitenrechner.exe wurde erstellt.
pause
