#!/bin/sh
echo ---------------------------------------
echo Install Start - MacOS

echo ---------------------------------------
echo Creating Installation Location
echo ---------------------------------------
## Create the install directory
sudo mkdir /usr/local/heimdall

echo ---------------------------------------
echo Copying Installation Files
echo ---------------------------------------
## Copy the client script and its dependencies setup
sudo cp -rv client.py /usr/local/heimdall/client.py
sudo cp -rv requirements.txt /usr/local/heimdall/requirements.txt

echo ---------------------------------------
echo Installing Dependencies
echo ---------------------------------------
## Change to the install directory
cd /usr/local/heimdall

## Setup Xcode utils
xcode-select --install

## Install Brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

## Install pip3 and our packages for the script
pip3 install -r requirements.txt

## Back to where the user was
cd -

echo ---------------------------------------
echo Register Script With Startup Daemon
echo ---------------------------------------
(crontab -l ; echo "@reboot /usr/bin/python3 /usr/local/heimdall/client.py -ip 10.5.11.30") | crontab -
