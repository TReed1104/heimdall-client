from datetime import datetime
from argparse import ArgumentParser
from time import sleep
from datetime import datetime
import sys
import socket
import re
import platform
import requests
from getmac import get_mac_address
from pathlib import Path

## Controls the runtime loop of the app
isRunning = True

## Set OS Logging Location
sys.stdout = open(str(Path.home()) + "/heimdall/logs.txt", "w")
sys.stderr = open(str(Path.home()) + "/heimdall/errors.txt", "w")

## If Windows
if sys.platform == 'win32':
    from ctypes import c_uint, c_int, windll, Structure, sizeof, byref

    ## C-struct required by the Windows OS API to get the idle timer
    class LastInputInfo(Structure):
        _fields_ = [
            ('cbSize', c_uint),
            ('dwTime', c_int),
        ]

    ## Windows Idle Duration calculation
    def getIdleDuration():
        ## Create our struct for the Win-API
        lastInputInfo = LastInputInfo()
        lastInputInfo.cbSize = sizeof(lastInputInfo)
        ## Win-API - GetLastInputInfo() returns a non-zero value when successful (https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getlastinputinfo)
        if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
            return (windll.kernel32.GetTickCount() - lastInputInfo.dwTime) / 1000.0    ## Convert to Seconds
        else:
            return 0

## If Linux
elif sys.platform == 'linux':
    print("Linux detected")
    import subprocess

    ## Ubuntu Implementation
    def getIdleDuration():
        try:
            ## Get the x session display
            displayResult = subprocess.Popen("w -oush | grep -Eo ':[0-9]+' | uniq", shell=True, stdout=subprocess.PIPE).stdout
            displayParsed = displayResult.read().decode("utf-8").split('\n')[0]

            ## Idle Timing
            xPrintIdleCommand = "DISPLAY=%s xprintidle" % displayParsed
            ##print(xPrintIdleCommand)
            idleTimeResult = subprocess.Popen(xPrintIdleCommand, shell=True, stdout=subprocess.PIPE).stdout
            idleTimeParsed = idleTimeResult.read().decode("utf-8")
            idleTime = float(idleTimeParsed) / 1000   ## Convert from Milliseconds to Seconds

            return idleTime
        except:
            ## Failed to get Display, return a value higher than the max idle time
            return 500

## If MacOS
elif sys.platform == 'darwin':
    import subprocess

    ## MacOS Implementation
    def getIdleDuration():
        rawResultOutput = subprocess.Popen("ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}'", shell=True, stdout=subprocess.PIPE).stdout
        strippedAndDecodedResult = rawResultOutput.read().rstrip().decode("utf-8")
        return float(strippedAndDecodedResult)

## Catch any unknown OS
else:
    ## Unknown OS kernel, kill the app
    print("Unknown OS detected")
    isRunning = False

    ## Default Implementation
    def getIdleDuration():
        return 0

def getIPAddress():
    socketConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketConnection.connect(("8.8.8.8", 80))
    return socketConnection.getsockname()[0]

def submitComputerData(serverAddress):
    ## Request payload
    payload = {}

    ## Create our payload
    platformDetails = platform.uname()
    if socket.gethostname().find('.') == 0:
        payload['machine_name'] = socket.gethostname()
    else:
        payload['machine_name'] = socket.gethostname().split('.')[0]
    payload['os_name'] = platformDetails[0]
    payload['os_release'] = platformDetails[2]
    payload['os_build'] = platformDetails[3]
    payload['mac_address'] = get_mac_address()
    payload['ip_address'] = getIPAddress()

    ## Send our request
    print("Sending PUT request")
    connectionURL = "http://" + serverAddress + "/heimdall-api/computer_handler"  ## URL of the API + endpoint
    response = requests.put(connectionURL, data=payload)
    print("Returned:", response.status_code)
    if response.status_code == 202:
        print("Computer data updated\n------------------------------")
        return

    ## PUT failed due to the machine not existing in the system, lets create its record instead
    if response.status_code == 405:
        print("Computer was not registered with the system, Sending POST request")
        response = requests.post(connectionURL, data=payload)
        if response.status_code == 201:
            print("Computer registered successfully\n------------------------------")
            return

def main():
    ## Register the program's command line arguments
    argParser = ArgumentParser(description='Version 2 of the Heimdall Client Script')
    argParser.add_argument("-ip", "--ip-address", dest="ip", help="Heimdall Server Address", type=str, required=True)
    arguments = argParser.parse_args()

    ## Program Entry Text
    print("------------------------------\nHeimdall Client v2 - Server Address: %s\n------------------------------" % arguments.ip )

    ## Loop until killed
    while isRunning:
        idleDuration = getIdleDuration()
        maxIdleTime = 600   ## Idle time - 10 Minutes
        print('Script Iteration Called at: %s' % str(datetime.now()))
        print('Idle for %.2fs\n------------------------------' % idleDuration)
        ## If the keyboard or mouse has been used in the last 10 minutes, send an update
        if (idleDuration <= maxIdleTime):
            try:
                submitComputerData(arguments.ip)
            except:
                if sys.platform == 'win32':
                    sys.stdout.write("An error occured, please check the error log: ~/heimdall/errors.txt\n------------------------------\r\n")
                else:
                    sys.stdout.write("An error occured, please check the error log: ~/heimdall/errors.txt\n------------------------------\n")
                sys.stderr.write(str(sys.exc_info()))

        ## Flush the outputs
        sys.stdout.flush()
        sys.stderr.flush()

        ## sleep for a minute
        sleep(60)

## Main app thread entry
if __name__ == '__main__':
    main()
