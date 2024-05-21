@echo off
setlocal

rem Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Installation en cours...
    REM Télécharger et installer Python 3.11.9
    bitsadmin /transfer pythonDownloadJob /download /priority normal https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe %TEMP%\python-3.11.9-amd64.exe
    %TEMP%\python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1
    
    rem Mettre à jour le PATH pour la session actuelle
    set "PATH=%PATH%;C:\Program Files\Python311\Scripts;C:\Program Files\Python311\"
    
    rem Vérifier si l'installation de Python a réussi
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo L'installation de Python a échoué.
        pause
        exit /b 1
    )
) else (
    echo Python est bien installé
)

rem Vérifier si Pygame est installé
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame n'est pas installé. Installation en cours...
    rem Installer Pygame
    python -m pip install pygame
    if %errorlevel% neq 0 (
        echo L'installation de Pygame a échoué.
        pause
        exit /b 1
    )
) else (
    echo Pygame est bien installé
)

rem Lancer votre jeu
python main.py

pause
