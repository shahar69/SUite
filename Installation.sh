#!/bin/bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print a message with the specified color
print_color() {
    printf "${1}${2}${NC}\n"
}

# Initialize error counter
total_steps=17
failed_steps=0

# Function to execute a command and check for errors
execute_step() {
    print_color $YELLOW "${2}"
    eval "${1}"
    if [ $? -ne 0 ]; then
        print_color $RED "Error: ${2} failed."
        failed_steps=$((failed_steps + 1))
    fi
}

# Update package manager and install necessary dependencies
execute_step "sudo apt-get update" "Updating package manager..."
execute_step "sudo apt-get install -y python3-pip python3-nmap" "Installing dependencies..."

# Install SSLstrip, arpspoof, Responder, sqlmap, nikto, nuclei, Ettercap, dirb, and mitmproxy
tools=("sslstrip" "dsniff" "responder" "sqlmap" "nikto" "nuclei" "ettercap-graphical" "dirb" "python-nmap")
for tool in "${tools[@]}"; do
    execute_step "sudo apt-get install -y ${tool}" "Installing ${tool}..."
done

# Install Pi Camera and hand recognition dependencies
execute_step "sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test" "Installing Pi Camera and hand recognition dependencies..."
execute_step "pip3 install opencv-python opencv-python-headless" "Installing OpenCV for Python..."
execute_step "pip3 install imutils" "Installing imutils..."

# Install necessary Python modules
python_modules=("scapy" "base64" "zlib" "prettytable" "colorama" "argparse")
for module in "${python_modules[@]}"; do
    execute_step "sudo pip3 install ${module}" "Installing Python module ${module}..."
done

# Set execute permissions for the Python files
execute_step "chmod +x main.py" "Setting execute permissions for main.py..."
execute_step "chmod +x mitm.py" "Setting execute permissions for mitm.py..."

# Print the installation summary
print_color $GREEN "Installation complete!"
print_color $YELLOW "Summary: ${failed_steps}/${total_steps} steps failed."
