
# 🔨 TOR HAMMER - Tor Brute Force Tool

TOR HAMMER is a Python penetration testing tool designed for authorized credential brute force assessments against web login forms. The tool leverages Tor for anonymity, implements intelligent IP rotation, multi-threading for efficiency, and real-time colored statistics with tqdm progress tracking. Only successful HTTP 200 responses (potential valid credentials) are captured and exported to JSON.


## Installation




```bash
 #1. Cloning Repo 
 git clone https://github.com/Mstf1112/TorHammer.git
 cd TorHammer

 #2. Tor configuration (/etc/tor/torrc)
ControlPort 9051
CookieAuthentication 0
SocksPort 9050

# 3. Restart Tor
sudo systemctl restart tor

# 4. Python environment
pip install -r requirements.txt
# stem==1.8.2, requests[socks]==2.31.0, colorama==0.4.6, tqdm==4.66.1, PySocks==1.7.1
```
    
## Usage/Examples

```bash
Enter target URL (ex: https://site.com/login): test.com
Credentials file [credentials.txt (USERNAME:PASS)]: test.txt
```



## Screenshots

![App Screenshot](https://dummyimage.com/468x300?text=App+Screenshot+Here)

