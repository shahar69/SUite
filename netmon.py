import threading
import time
import nmap
from scapy.all import ARP, Ether, srp
from prettytable import PrettyTable

# Define the network to scan
network = "192.168.1.0/24"

# Create a dictionary to store the devices
devices = {}


# Create a function to scan the network and update the devices dictionary
def scan_network():
    # Create an ARP request packet
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and get the response
    result = srp(packet, timeout=3, verbose=0)[0]

    # Update the devices dictionary with the response
    for sent, received in result:
        devices[received.psrc] = {"mac": received.hwsrc}

        # Use nmap to get information about the open ports and services
        nm = nmap.PortScanner()
        nm.scan(received.psrc, arguments="-O -sV")
        if "osclass" in nm[received.psrc]:
            devices[received.psrc]["os"] = nm[received.psrc]["osclass"][0]["osfamily"]
        if "tcp" in nm[received.psrc]:
            for port in nm[received.psrc]["tcp"]:
                devices[received.psrc][f"port {port}"] = nm[received.psrc]["tcp"][port]["name"]


# Create a function to display the devices in a neat and organized way
def display_devices():
    while True:
        # Create a table to display the devices
        table = PrettyTable()
        table.field_names = ["IP Address", "MAC Address", "Operating System", "Open Ports and Services"]

        # Add the devices to the table
        for ip, info in devices.items():
            mac = info["mac"]
            os = info.get("os", "")
            ports = ", ".join([f"{k} ({v})" for k, v in info.items() if k.startswith("port")])
            table.add_row([ip, mac, os, ports])

        # Clear the screen and display the table
        print("\033[H\033[J")
        print(table)

        # Wait for 5 seconds before updating the table
        time.sleep(5)


# Create a thread to scan the network continuously
scan_thread = threading.Thread(target=scan_network)
scan_thread.start()

# Display the devices in real-time
display_devices()
