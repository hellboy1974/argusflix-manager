# Build script for Angina AIO

$ErrorActionPreference = "Stop"

# Navigate to scripts directory if not already there
if (Test-Path "angina_aio.py") {
    $ScriptPath = "angina_aio.py"
} else {
    $ScriptPath = "scripts\angina_aio.py"
}

# Use the .venv Python to run PyInstaller
$PyInstallerPath = "..\ArgusFlix-0.25.1\.venv\Scripts\pyinstaller.exe"
if (-Not (Test-Path $PyInstallerPath)) {
    # Fallback if run from root
    $PyInstallerPath = "ArgusFlix-0.25.1\.venv\Scripts\pyinstaller.exe"
}

Write-Host "Compiling Angina_AIO.exe using PyInstaller..." -ForegroundColor Cyan

& $PyInstallerPath --onefile --windowed --name="Angina_AIO" $ScriptPath

Write-Host "Compilation complete. Executable is located in the 'dist' directory." -ForegroundColor Green
