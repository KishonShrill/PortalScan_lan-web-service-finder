import re
import requests
import webbrowser
import subprocess
from colorama import Fore, Style
from ..utils.printing import print_boxed, print_columns


available_services = []
ips = []
scanned_ips = set()
selected_ip = None
open_ports = []
port_scanned_ips = {}


def run_arp_scan(force=False):
    global ips, scanned_ips
    if not force and scanned_ips:
        print(Fore.YELLOW + "\n[!] ARP scan already performed. Use 'SCAN --force' to rescan.")
        if ips:
            print(Fore.CYAN + "[+] Using cached scan results:")
            print_columns(ips)
            print("-" * 30)
        return
    if force:
        print(Fore.YELLOW + "[*] Forcing a new ARP scan...")
        scanned_ips.clear()
        ips.clear()
    print_boxed("Discovering devices on your LAN...", Fore.CYAN)
    result = subprocess.run(["sudo", "arp-scan", "--localnet"], capture_output=True, text=True)
    new_ips = re.findall(r"\b\d+\.\d+\.\d+\.\d+\b", result.stdout)
    new_ips = list(dict.fromkeys(new_ips))
    if new_ips:
        ips = new_ips
        scanned_ips.update(new_ips)
        print(Fore.CYAN + "\n[+] Found the following active IPs:")        
        print_columns(ips)
        print("-" * 30)
    else:
        print(Fore.RED + "[!] No active devices found on the network.")

def select_ip(index):
    global selected_ip
    if 1 <= index <= len(ips):
        selected_ip = ips[index-1]
        print_boxed(f"[+] Selected IP: {selected_ip}", Fore.GREEN)
        print(Fore.YELLOW + "[!] You can now use 'PORTSCAN'.\n")
    else:
        print(Fore.RED + "[!] Invalid index.\n")

def run_port_scan(force=False):
    global open_ports, port_scanned_ips
    if not selected_ip:
        print(Fore.RED + "[!] No IP selected. Please use 'SELECT' first.\n")
        return
    if not force and selected_ip in port_scanned_ips:
        print(Fore.YELLOW + f"[!] Port scan already performed for {selected_ip}. Use 'PORTSCAN --force' to rescan.")
        open_ports = port_scanned_ips[selected_ip]
        if open_ports:
            print(Fore.GREEN + f"[+] Last known open ports for {selected_ip}:")
            print(Fore.MAGENTA + ", ".join(open_ports) + "\n")
        else:
            print(Fore.YELLOW + "[-] No open ports were found in the last scan for this IP.\n")
        return
    if force:
        print(Fore.YELLOW + f"[*] Forcing a new port scan on {selected_ip}...")
    print_boxed(f"Scanning for open ports on {selected_ip}...", Fore.CYAN)
    result = subprocess.run(
        ["sudo", "nmap", "-p", "1024-9999", "--open", selected_ip],
        capture_output=True, text=True
    )
    newly_found_ports = re.findall(r"(\d+)/tcp\s+open", result.stdout)
    if newly_found_ports:
        open_ports = newly_found_ports
        port_scanned_ips[selected_ip] = open_ports
        print(Fore.GREEN + f"[+] Found {len(open_ports)} open ports:")
        print(Fore.MAGENTA + ", ".join(open_ports))
        print(Fore.YELLOW + "[!] You can now use 'CHECK'.\n")
    else:
        open_ports = []
        port_scanned_ips[selected_ip] = []
        print(Fore.YELLOW + "[-] No open ports found.\n")


def check_html_ports():
    print_boxed(f"Checking for HTML services on {selected_ip}...", Fore.CYAN)
    if not open_ports:
        print(Fore.RED + "[!] No open ports to check. Please run 'PORTSCAN' first.")
        return
    found_services = False
    for port in open_ports:
        url = f"http://{selected_ip}:{port}"
        try:
            r = requests.get(url, timeout=2)
            if "<html" in r.text.lower():
                available_services.append(f"{selected_ip}:{port}")
                print(Fore.GREEN + f"[HTML]" + Style.RESET_ALL + f" {url}" + Fore.GREEN + " [*] Found HTML service")
                found_services = True
            else:
                print(Fore.YELLOW + f"[No HTML]" + Style.RESET_ALL + f" {url}")
        except requests.RequestException:
            print(Fore.RED + f"[Error]" + Style.RESET_ALL + f" {url}")
    print(Fore.YELLOW + "[!] You can now use 'LIST'.\n")
    if not found_services:
        print(Fore.YELLOW + "[-] No HTML services found.")

def list_services():
    if not available_services:
        print(Fore.RED + "[!] No HTML services found.\n")
        return
    print_boxed("[+] Available HTML services:", Fore.YELLOW)
    for i, svc in enumerate(available_services, 1):
        print(Fore.CYAN + f"[{i}]" + Style.RESET_ALL + f" {svc}")
    print(Fore.YELLOW + "[!] You can now use 'OPEN <list-index>'.\n")

def open_to_browser(index):
    if 1 <= index <= len(available_services):
        url = f"http://{available_services[index - 1]}"
        print(f"[*] Opening {url} in your default browser...")
        webbrowser.open(url)
    else:
        print(Fore.RED + "[!] Invalid service number.")
