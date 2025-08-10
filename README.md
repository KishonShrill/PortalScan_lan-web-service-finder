# PortalScan - LAN Web Service Finder
A Python-based CLI tool to discover devices and web services available on your local network (LAN).<br /> It uses `arp-scan` for device discovery and `nmap` for port scanning, then checks for active HTTP services.

## Features
- **Device Discovery** — Scan your LAN for active devices using `arp-scan`
- **Port Scanning** — Identify open TCP ports in the range **1024-9999** with `nmap`
- **HTML Service Detection** — Check open ports for HTTP services serving HTML.
- **Service Listing & Browser Opening** — View detected services and open them in your default browser.

## Requirements
- Python 3.8+
- Linux / macOS (tested on Linux)
- Dependencies:
    - `arp-scan`
    - `nmap`
    - Python packages: `requests`, `colorama`

## Installation
**Prerequisite**
Install system packages:
```bash
sudo apt install arp-scan nmap  # Debian/Ubuntu

sudo dnf install arp-scan nmap  # Fedora
```

1. As a package / Terminal app
Install using `uv tool`.
```bash
uv tool install git@github.com:KishonShrill/PortalScan_lan-web-service-finder.git
```

2. (optional) As a developer
Install using `git clone`
```bash
git clone git@github.com:KishonShrill/PortalScan_lan-web-service-finder.git
```
Install the dependencies and run locally
```bash
pip install pipenv          # Python 3.10 is needed for pipenv
pipenv shell
pipenv install --dev        # Install Python packages

python3 -m portalscan.main  # Run portalscan python code
```

## Notes
- This tool requires root privileges for `arp-scan` and `nmap`.
- Intended for `educational and administrative purposes only` on networks you own or have persmission to scan.

## Licence
This repository is using the [MIT Licence](./LICENCE.md)