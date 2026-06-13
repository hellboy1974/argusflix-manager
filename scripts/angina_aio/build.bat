@echo off
echo ==============================================
echo Installing dependencies...
echo ==============================================
pip install pyinstaller PyQt5 requests urllib3

echo.
echo ==============================================
echo Building Angina AIO Reloaded...
echo ==============================================
pyinstaller --noconsole --onefile --name "Angina_AIO_Reloaded" main.py

echo.
echo ==============================================
echo Build finished! Check the 'dist' folder.
echo ==============================================
pause
