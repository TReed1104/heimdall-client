# Heimdall Push Client
The push client for Heimdall is a small python script used for automating the pushing of data to the Heimdall API.

The script sends the following information about the computer to the API:
* Hostname
* MAC Address
* IP Address
* Operating system
* Operating System's version
* Operating System's build version

<br>

---

## Dependencies
The Heimdall client uses the pip package manager and is written using Python3.

The following packages are used in the project:

### Requests - 2.22.0
Requests is a library used for easily implementing HTTP CRUD requests in python. Its through this package that the local client app (local_client.py) pushes data to the Heimdall API.

### GetMac - 0.8.2
GetMac is a library used for easily getting the Mac address of a machine Ethernet or Wi-Fi adapter.

<br>

---

## Install Guide
To allow for the quick and easy deployment of the local client for Heimdall we have supplied automated installation scripts for different Operating systems.

These scripts automatically download and install the different dependencies and libraries required by the client to work.

**NOTE: There is a known bug with the Window installation script with Anaconda Python.**

<br>

### Windows
To install the local client on Windows 10 based machines please follow the following steps:
1. Clone the repository to a location of your choice
2. Navigate to the client directory within the repository clone in file explorer
3. Run the "install_windows.bat" script by right clicking and selecting "Run as administrator"
4. Wait for the script to finish
5. Verify the installation by checking for a "heimdall_boot.bat" in the Startup tab of Windows Task Manager

#### Known bug - Anaconda Python
There is a known bug on Windows 10 machines with the Anaconda Python suite installed, where the suite prevents standard pip from using TLS/SSL to download pip modules.
1. Open Anaconda Prompt
2. Navigate to the location of your clone of the repository
3. Navigate to the client directory in the repository
4. run the following command:
```bash
pip install -r requirements.txt
```
5. Exit Anaconda Prompt
6. Run the "install_windows.bat" script by right clicking and selecting "Run as administrator"

<br>

### Ubuntu
The client currently supports installation on Ubuntu 16.04 and Ubuntu 18.04.

To install the client on Ubuntu based machines please follow the following steps:
1. Clone the repository to a location of your choice
2. Navigate to the client directory within the repository clone with your terminal of choice
3. Give the script execution rights:
```bash
sudo chmod +x install_ubuntu.sh
```
4. Run the following command to execute the script:
```bash
./install_ubuntu.sh
```
5. Wait for the script to finish execution

<br>

### MacOS
The client does currently supply a very experimental MacOS install script, this script should be taken as <b>EXPERIMENTAL</b> as users should be careful with its execution.



## License

The heimdall client application is open-sourced software licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.
