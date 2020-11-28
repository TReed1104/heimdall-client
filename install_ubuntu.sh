#!/bin/sh
echo ---------------------------------------
echo Install Start - Ubuntu

echo ---------------------------------------
echo Creating Installation Location
echo ---------------------------------------
## Create the install directory
sudo mkdir /usr/local/heimdall
sudo mkdir -m 777 ~/heimdall

echo ---------------------------------------
echo Copying Installation Files
echo ---------------------------------------
## Copy the client script and its dependencies setup
sudo cp -rv client.py /usr/local/heimdall/client.py
sudo cp -rv requirements.txt /usr/local/heimdall/requirements.txt

echo ---------------------------------------
echo Installing Dependencies
echo ---------------------------------------
cd /usr/local/heimdall                      ## Change to the install directory
sudo apt-get install -y python3             ## Make sure we have the right Python version
sudo apt-get install -y python3-pip         ## Install Pip3
pip3 install -r requirements.txt            ## Install the pip modules for the client
sudo apt-get install -y xprintidle          ## Install xprintidle, our package for getting the OS idle time in Ubuntu
cd -                                        ## Back to where the user was

echo ---------------------------------------
echo Register Script With Startup Daemon
echo ---------------------------------------
## Write the script call to the system crontab configuration
## TODO: Check if the crontab call is already present before just writing it again
(crontab -l ; echo "@reboot (/usr/bin/python3 /usr/local/heimdall/client.py -ip 10.5.11.20)") | crontab -
