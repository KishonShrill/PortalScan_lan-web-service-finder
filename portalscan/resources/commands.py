from colorama import Fore, Style

command_help = {
    "SCAN": "Run arp-scan to find devices on the LAN",
    "SELECT <scan-index>": "Choose an IP from the last scan results",
    "PORTSCAN": "Scan the selected IP for open ports (1024-9999)",
    "CHECK": "Test open ports for HTML content",
    "LIST": "Show all available HTML services found so far",
    "OPEN <list-index>": "Open selected URL in browser",
    "HELP": "Show this help message",
    "QUIT": "Exit the program"
}

def show_help():
    for cmd, desc in command_help.items():
        print(f"{Fore.CYAN}{cmd}{Style.RESET_ALL} - {desc}")
