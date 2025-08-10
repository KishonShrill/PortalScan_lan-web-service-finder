#!/usr/bin/env python3
import sys
from colorama import Fore, Style
from portalscan.utils.printing import print_boxed
from portalscan.utils.network import check_dependencies, get_current_wifi
from portalscan.scan.services import run_arp_scan, select_ip, run_port_scan, check_html_ports, list_services, open_to_browser
from portalscan.resources.commands import show_help

__version__ = "0.0.1"
    
# Positive/Success: 
#       Use Fore.GREEN for successful actions, 
#       like finding an HTML service or a successful 
#       connection.
# Informational/Process: 
#       Use Fore.CYAN or Fore.YELLOW for ongoing processes, 
#       such as scanning ports or checking for dependencies.
#       This lets the user know something is happening.
# Warning/Error: 
#       Use Fore.RED for errors and Fore.YELLOW for warnings 
#       or non-critical issues, like a port being open but 
#       not having HTML content.
# User Input/Neutral Text: 
#       Use a neutral color like Fore.WHITE or the default
#       color for the command prompt and general text.

# Main interactive loop
def main():
    if "--version" in sys.argv:
        print(f"portalscan {__version__}")
        sys.exit(0)
    
    check_dependencies()
    
    print_boxed(text=f"LAN Web Service Finder v{__version__}",
                color=Fore.MAGENTA,
                padding_inline=6,
                padding_left=4)
    print(f"{Fore.GREEN}[*] {Style.RESET_ALL}Connected Wi-Fi: {Fore.GREEN}{get_current_wifi()}")
    print("[*] LAN Web Service Finder - Type HELP for commands")
    while True:
        try:
            cmd = input("> ").strip().split()
            if not cmd:
                continue
            action = cmd[0].upper()
            force_scan = "--FORCE" in [arg.upper() for arg in cmd] # Check for --force flag
            
            if action == "SCAN":
                run_arp_scan(force=force_scan)
            elif action == "SELECT" and len(cmd) == 2:
                select_ip(int(cmd[1]))
            elif action == "PORTSCAN":
                run_port_scan(force=force_scan)
            elif action == "CHECK":
                check_html_ports()
            elif action == "LIST":
                list_services()
            elif action == "OPEN" and len(cmd) == 2:
                open_to_browser(int(cmd[1]))
            elif action == "HELP":
                show_help()
            elif action == "QUIT" or action == "EXIT":
                print("[*] Exiting...")
                break
            else:
                print("[!] Unknown command. Type HELP.")
        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            break

if __name__ == "__main__":
    main()