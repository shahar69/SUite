import sys
import socket


def scan(ip):
    print("\nScanning ports on " + ip + "...\n")
    open_ports = []
    for port in range(1, 1025):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
                print("Port {}: Open".format(port))
            sock.close()
        except KeyboardInterrupt:
            print("\nExiting program.")
            sys.exit()
        except socket.gaierror:
            print("\nHostname could not be resolved. Exiting")
            sys.exit()
        except socket.error:
            print("\nCould not connect to server.")
            sys.exit()

    if len(open_ports) == 0:
        print("\nNo open ports found.")
    else:
        print("\nScan complete.")
        print("Open ports on " + ip + ":")
        for port in open_ports:
            print(port)
