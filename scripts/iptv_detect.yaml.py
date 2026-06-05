import subprocess
import os
import json

# --- KONFIGURATION ---
TEMPLATE_NAME = "iptv_detect.yaml"
OUTPUT_FILE = "nuclei_iptv_results.json"

# Erstellung des Nuclei-Templates (YAML) direkt aus Python
NUCLEI_TEMPLATE = """
id: iptv-detection-2026
info:
  name: IPTV M3U & Xtream Detection
  author: Auto-Generated
  severity: info
http:
  - method: GET
    path:
      - "{{BaseURL}}/player_api.php"
      - "{{BaseURL}}/get.php"
      - "{{BaseURL}}/playlist.m3u"
    matchers-condition: or
    matchers:
      - type: word
        words:
          - "user_info"
          - "#EXTM3U"
          - "xtream codes"
      - type: status
        status:
          - 200
"""

def create_template():
    """Erstellt das Nuclei-Template auf der Festplatte."""
    with open(TEMPLATE_NAME, "w") as f:
        f.write(NUCLEI_TEMPLATE)
    print(f"[*] Template {TEMPLATE_NAME} wurde erstellt.")

def run_nuclei_scan(target_input):
    """
    Führt Nuclei gegen ein Ziel oder eine Liste aus.
    target_input kann eine IP, eine URL oder ein CIDR (1.2.3.0/24) sein.
    """
    print(f"[*] Starte Nuclei-Scan für: {target_input}...")
    
    # Befehl zusammenbauen
    # -u für Ziel, -t für Template, -jsonl für maschinenlesbaren Output
    cmd = [
        "nuclei",
        "-u", target_input,
        "-t", TEMPLATE_NAME,
        "-jsonl", 
        "-o", OUTPUT_FILE
    ]

    try:
        # Scan ausführen
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Echtzeit-Ausgabe der Nuclei-Ergebnisse
        for line in process.stdout:
            try:
                data = json.loads(line)
                print(f"[+] IPTV PANEL GEFUNDEN: {data.get('matched-at')} | Template: {data.get('template-id')}")
            except:
                print(line.strip())
                
        process.wait()
    except FileNotFoundError:
        print("[-] Fehler: Nuclei ist nicht installiert oder nicht im PATH.")
    except Exception as e:
        print(f"[-] Ein Fehler ist aufgetreten: {e}")

def cleanup():
    """Löscht das temporäre Template."""
    if os.path.exists(TEMPLATE_NAME):
        os.remove(TEMPLATE_NAME)
        print("[*] Bereinigung abgeschlossen.")

if __name__ == "__main__":
    # 1. Template vorbereiten
    create_template()
    
    # 2. Eingabe abfragen (Beispiel: 185.10.21.0/24)
    target = input("Geben Sie die Ziel-IP oder CIDR ein: ").strip()
    
    if target:
        run_nuclei_scan(target)
    else:
        print("[-] Keine Eingabe erhalten.")
    
    # 3. Aufräumen
    # cleanup() # Auskommentieren, wenn du das Template behalten willst
