@echo off
title Pain Points Hunter
echo.
echo ========================================
echo   Pain Points Hunter - Demarrage
echo ========================================
echo.

REM Verifie si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo Telecharge Python sur https://python.org
    pause
    exit /b
)

REM Verifie si Flask est installe
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de Flask...
    pip install -r requirements.txt
)

echo [INFO] Lancement du serveur...
echo.
cd src
python app.py
pause
