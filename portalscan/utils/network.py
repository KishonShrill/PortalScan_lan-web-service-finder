import shutil
import subprocess
import sys
from colorama import Fore, Style, init

init(autoreset=True)


def check_dependencies():
    for cmd in ["nmap", "arp-scan", "nmcli"]:
        if shutil.which(cmd) is None:
            print(Fore.RED + f"[!] ERROR: '{cmd}' is not installed or not found in PATH. Please install it first.")
            sys.exit(1)


def get_current_wifi():
    try:
        result = subprocess.check_output(
            "nmcli -t -f active,ssid dev wifi | grep -E '^yes' | cut -d: -f2",
            shell=True, text=True
        ).strip()
        return result if result else "Not connected to Wi-Fi"
    except subprocess.CalledProcessError:
        return "Wi-Fi info unavailable"