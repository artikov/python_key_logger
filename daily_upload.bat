@echo off
cd /d "%~dp0"
echo %DATE% %TIME% - Running uploader script >> "%~dp0upload_log.txt"
start "" /min pythonw "%~dp0keys_uploader.pyw"
echo Uploaded! >> testlog.txt
exit
