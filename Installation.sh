#!/bin/bash

# Update package manager and install necessary dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-nmap 

# Install SSLstrip, arpspoof, and Responder
sudo apt-get install -y sslstrip dsniff responder

# Install sqlmap
sudo apt-get install -y sqlmap

# Install nikto
sudo apt-get install -y nikto

# Install nuclei
sudo apt-get install -y nuclei

# Install Ettercap
sudo apt-get install -y ettercap-graphical

# Install dirb
sudo apt-get install -y dirb

# Install mitmproxy
sudo apt-get install -y mitmproxy

# Clone the repository
git clone https://github.com/example/example.git

# Move into the cloned repository
cd example

# Install necessary Python modules
sudo pip3 install scapy

# Set execute permissions for the Python files
chmod +x main.py
chmod +x mitm.py

echo "Installation complete!"
