#!/bin/bash
echo '[*] Checking for Updates'
yum -y update
if [ $? -ne 0 ]; then
    echo "[!] Unable to update, check your internet connection!"
    exit 0
fi

echo '[*] Disabling Network Manager'
systemctl stop NetworkManager
systemctl disable NetworkManager
systemctl enable network

echo '[*] Setting up RDO repositories'
yum install -y https://rdoproject.org/repos/rdo-release.rpm
if [ $? -ne 0 ]; then
    echo "[!] Unable to setup RDO repos, check your internet connection!"
    exit 0
fi

echo '[*] Installing Packstack-Installer'
yum install -y openstack-packstack
if [ $? -ne 0 ]; then
    echo "[!] Unable to install packstack installer, check your internet connection!"
    exit 0
fi

echo '[*] Starting packstack'
packstack --allinone
if [ $? -ne 0 ]; then
    echo "[!] Something went wrong while starting packstack!!"
    exit 0
fi
