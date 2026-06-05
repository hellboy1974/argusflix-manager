import customtkinter as ctk
import requests
import threading
import random
import urllib3
import socket
from tkinter import messagebox

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PortalScannerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("KaBoom Discovery Engine 2026 - VPN & Geo-Check")
        self.geometry("850x750")
        ctk.set_appearance_mode("dark")

        # --- Variablen ---
        self.payloads = [
            '/portal.php', '/server/load.php', '/portalstb/', 
            '/stalker_portal/server/load.php', '/c/portal.php',
            '/stalker_portal/c/', '/play/index.php'
        ]
        
        self.user_agents = [
            'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/537.36',
            'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG250 stbapp ver: 2 rev: 250 Safari/537.36'
        ]

        # --- UI Komponenten ---
        self.header_label = ctk.CTkLabel(self, text="PORTAL SCANNER + VPN ANALYZER", font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.pack(pady=20)

        # IP Info Box
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(padx=20, pady=10, fill="x")
        self.ip_info_label = ctk.CTkLabel(self.info_frame, text="Lade Netzwerk-Info...", text_color="gray")
        self.ip_info_label.pack(pady=5)

        # URL Input
        self.entry_url = ctk.CTkEntry(self, placeholder_text="http://beispiel.com:8080", width=500)
        self.entry_url.pack(padx=20, pady=10)

        # Buttons
        self.btn_start = ctk.CTkButton(self, text="SCAN STARTEN", fg_color="#1f538d", command=self.start_scan)
        self.btn_start.pack(pady=10)

        # Log
        self.log_box = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12), height=300)
        self.log_box.pack(padx=20, pady=10, fill="both", expand=True)
        self.log_box.configure(state="disabled")

        # Stats
        self.label_hits = ctk.CTkLabel(self, text="Treffer: 0 | VPN-Status: Unbekannt")
        self.label_hits.pack(pady=10)

        # Initialer IP-Check
        threading.Thread(target=self.check_my_ip, daemon=True).start()

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def check_my_ip(self):
        """Prüft die eigene IP und den Standort."""
        try:
            data = requests.get("http://ip-api.com", timeout=5).json()
            self.current_country = data.get("country", "Unbekannt")
            self.current_isp = data.get("isp", "Unbekannt")
            self.ip_info_label.configure(
                text=f"Deine IP: {data.get('query')} | Land: {self.current_country} | ISP: {self.current_isp}",
                text_color="#3498db"
            )
        except:
            self.ip_info_label.configure(text="Netzwerk-Info konnte nicht geladen werden.", text_color="red")

    def start_scan(self):
        target = self.entry_url.get().strip()
        if not target: return
        
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.configure(state="disabled")
        
        threading.Thread(target=self.run_logic, args=(target,), daemon=True).start()

    def run_logic(self, target):
        if not target.startswith("http"): target = "http://" + target
        target = target.rstrip('/')
        
        self.btn_start.configure(state="disabled", text="Prüfe Verbindung...")
        self.log(f"[*] Analysiere Ziel: {target}")
        
        status_403_count = 0
        timeout_count = 0
        hits = 0

        for path in self.payloads:
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                res = requests.get(target + path, headers=headers, timeout=6, verify=False)
                
                code = res.status_code
                if code == 200:
                    self.log(f"🟢 [200 OK] -> {path}")
                    hits += 1
                elif code == 401:
                    self.log(f"🟡 [401 Auth Required] -> {path}")
                    hits += 1
                elif code == 403:
                    self.log(f"🔴 [403 Forbidden] -> {path}")
                    status_403_count += 1
                else:
                    self.log(f"⚪ [{code}] -> {path}")

            except requests.exceptions.ConnectTimeout:
                self.log(f"⏳ Timeout -> {path}")
                timeout_count += 1
            except Exception as e:
                self.log(f"❌ Fehler -> {path}")

        # --- VPN / GEO-BLOCK ANALYSE ---
        self.log("\n" + "="*30)
        self.log("[!] ANALYSE-ERGEBNIS:")
        
        if hits > 0:
            self.log("✅ Portal erreichbar! Kein VPN zwingend nötig.")
            vpn_status = "Kein VPN nötig"
        elif status_403_count > 3:
            self.log("⚠️ GEO-BLOCK ERKANNT!")
            self.log(f"Der Server blockiert deine IP ({self.current_country}).")
            self.log("💡 EIN VPN (z.B. Niederlande oder UK) IST ERFORDERLICH.")
            vpn_status = "VPN DRINGEND ERFORDERLICH"
        elif timeout_count > 3:
            self.log("⚠️ VERBINDUNG UNMÖGLICH!")
            self.log("Der Server antwortet nicht. Entweder offline oder IP-Blacklist.")
            self.log("💡 Teste einen VPN-Standort.")
            vpn_status = "VPN Empfohlen / Offline"
        else:
            self.log("Keine eindeutigen Portale gefunden.")
            vpn_status = "Keine Treffer"

        self.label_hits.configure(text=f"Treffer: {hits} | VPN-Status: {vpn_status}")
        self.btn_start.configure(state="normal", text="SCAN STARTEN")

if __name__ == "__main__":
    app = PortalScannerGUI()
    app.mainloop()
