@ECHO OFF
ECHO ---------------------------------------
ECHO Install Start - Windows Shell

REM Run as admin moves use to System32, move to the script directory
PUSHD %~dp0

ECHO ---------------------------------------
ECHO Creating Installation Location
ECHO ---------------------------------------
IF not EXIST "C:\ProgramData\heimdall" MKDIR "C:\ProgramData\heimdall"
IF not EXIST "%HOMEPATH%\heimdall" MKDIR "%HOMEPATH%\heimdall"

ECHO ---------------------------------------
ECHO Copying Installation Files
ECHO ---------------------------------------
COPY /Y "client.py" "C:\ProgramData\heimdall\client.py"
COPY /Y "requirements.txt" "C:\ProgramData\heimdall\requirements.txt"


ECHO ---------------------------------------
ECHO Installing Dependencies
ECHO ---------------------------------------
REM Change to the install location and install our dependencies
PUSHD "C:\ProgramData\heimdall"
python -m pip install -r requirements.txt
POPD

ECHO ---------------------------------------
ECHO Register Script With Startup Daemon
ECHO ---------------------------------------
REM Now we have the script setup, register it to be run on Startup
COPY /Y "heimdall_boot.bat" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\heimdall_boot.bat"

REM Return to the directory
POPD
