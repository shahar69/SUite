import argparse
import nmap
from colorama import Fore, Style
from prettytable import PrettyTable
from scapy.all import *
from scapy.layers.l2 import ARP, Ether

# Define the network to scan
network = "192.168.1.0/24"

# Create a dictionary to store the devices
devices = {}

# Create an argument parser to customize the behavior
parser = argparse.ArgumentParser(description="Scan the network and display the devices.")
parser.add_argument("-t", "--timeout", type=int, default=3, help="the timeout for the ARP request (default: 3)")
parser.add_argument("-i", "--interval", type=int, default=5, help="the interval between scans (default: 5)")
args = parser.parse_args()


# Create a function to scan the network and update the devices dictionary
def scan_network():
    # Create an ARP request packet
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet1 = ether / arp
    # Send the packet and get the response
    result = srp(packet1, timeout=args.timeout, verbose=0)[0]

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
        table.field_names = [Fore.BLUE + "IP Address" + Style.RESET_ALL, Fore.BLUE + "MAC Address" + Style.RESET_ALL,
                             Fore.BLUE + "Operating System" + Style.RESET_ALL,
                             Fore.BLUE + "Open Ports and Services" + Style.RESET_ALL]

        # Add the devices to the table
        for ip, info in devices.items():
            mac = info["mac"]
            ostype = info.get("os", "")
            ports = ", ".join([f"{k} ({v})" for k, v in info.items() if k.startswith("port")])
            table.add_row([Fore.GREEN + ip + Style.RESET_ALL, Fore.YELLOW + mac + Style.RESET_ALL, ostype, ports])

        # Clear the screen and display the table
        print("\033[H\033[J")
        print(table)

        # Wait for the specified interval before updating the table
        time.sleep(args.interval)


# Create a thread to scan the network continuously

def startmonitoring():
    scan_thread = threading.Thread(target=scan_network)
    scan_thread.start()

    # Display the devices in real-time
    display_devices()
