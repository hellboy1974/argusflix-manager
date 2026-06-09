# 🚀 Deployment- & Git-Leitfaden für deine angepasste ArgusFlix-Version

Dieses Dokument beschreibt, wie du diese angepasste Version von ArgusFlix in einem **privaten GitHub-Repository** verwaltest und auf verschiedenen Systemen (**Ubuntu Server, Synology NAS, Unraid**) mittels Docker Compose bereitstellst.

---

## 📂 1. Git-Repository vorbereiten (Privat)

Da deine Workspace-Ordnerstruktur wie folgt aussieht:
```text
argusflix_manager_reloaded/
├── .gitignore               <-- Bereits für dich erstellt!
├── ArgusFlix-0.25.1/      <-- Der Core-Code von ArgusFlix
├── plugins/                 <-- Deine custom Plugins
├── scripts/                 <-- Deine custom Scripte
└── docker-templates/        <-- Die Docker-Compose-Dateien
```

### Schritt-für-Schritt Git-Setup:
1. Öffne ein Terminal im Stammverzeichnis `argusflix_manager_reloaded/`.
2. **WICHTIG:** Überprüfe, ob im Unterordner `ArgusFlix-0.25.1/` ein versteckter Ordner namens `.git/` existiert. Wenn ja, lösche ihn (`rmdir /s /q ArgusFlix-0.25.1\.git` unter Windows oder `rm -rf ArgusFlix-0.25.1/.git` unter Linux). Andernfalls wird Git diesen Ordner als "Submodul" betrachten, was das Hinzufügen von Code erschwert.
3. Initialisiere das Git-Repository im Hauptordner:
   ```bash
   git init
   ```
4. Erstelle ein neues **privates** Repository auf GitHub (z. B. `argusflix_manager-custom`).
5. Verbinde dein lokales Verzeichnis mit dem GitHub-Repository:
   ```bash
   git remote add origin https://github.com/DEIN_BENUTZERNAME/DEIN_REPO_NAME.git
   git branch -M main
   ```
6. Füge die Dateien hinzu und committe sie:
   ```bash
   git add .
   git commit -m "Initial commit of custom ArgusFlix, plugins, and scripts"
   ```
7. Pushe den Code in dein privates GitHub-Repository:
   ```bash
   git push -u origin main
   ```

---

## 🐳 2. Deployment-Szenarien (Wie läuft Docker ab?)

Es gibt zwei Möglichkeiten, deine Anpassungen in Docker zu betreiben. Welches Szenario zutrifft, hängt davon ab, ob du den **Core-Code** im Ordner `ArgusFlix-0.25.1` direkt bearbeitet hast.

### 🔹 Szenario A: Du hast NUR eigene Plugins und Scripte hinzugefügt (Core ist unverändert)
*Das ist die einfachste und sauberste Methode.*
* Du nutzt das offizielle, vorgefertigte Docker-Image `ghcr.io/argusflix_manager/argusflix_manager:latest`.
* Du mountest deine Ordner `plugins/` und `scripts/` einfach als Volumes in den Container.
* **Vorteil:** Du musst keine eigenen Docker-Images bauen oder verwalten. Updates sind extrem einfach.

### 🔹 Szenario B: Du hast den Core-Code in `ArgusFlix-0.25.1` selbst verändert
* Du musst dein eigenes Docker-Image bauen, da das offizielle Image deine Codeänderungen im Core nicht enthält.
* Du hast hierbei zwei Möglichkeiten:
  1. **Lokal auf dem Server bauen:** In der `docker-compose.yml` nutzt du `build: ./ArgusFlix-0.25.1` anstelle von `image: ...`. Docker baut das Image dann direkt beim Start auf deinem Server. (Kann auf Synology/Unraid langsam sein).
  2. **GitHub Actions nutzen:** Du richtest eine Pipeline ein, die das Image bei jedem Push baut und in deiner privaten GitHub Container Registry (`ghcr.io`) ablegt. Auf den Servern machst du dann einmal `docker login ghcr.io` mit einem GitHub Token und ziehst das fertige Image.

---

## 🛠️ 3. Bereitstellung auf den Ziel-Systemen

In dem Ordner `docker-templates/` findest du vorgefertigte Konfigurationen für die verschiedenen Systeme. Hier ist die genaue Vorgehensweise für jedes System:

### 🖥️ A. Ubuntu Server
1. Klone dein privates Repository auf den Server:
   ```bash
   git clone https://github.com/DEIN_BENUTZERNAME/DEIN_REPO_NAME.git /opt/argusflix_manager
   cd /opt/argusflix_manager
   ```
2. Kopiere die Vorlage aus `docker-templates/ubuntu-server/docker-compose.yml` in das Hauptverzeichnis:
   ```bash
   cp docker-templates/ubuntu-server/docker-compose.yml docker-compose.yml
   ```
3. Passe bei Bedarf Ports oder Pfade in der `docker-compose.yml` an.
4. Starte den Container:
   ```bash
   docker compose up -d
   ```

### 💾 B. Synology NAS (Container Manager)
Synology nutzt standardmäßig den Ordner `/volume1/docker/` für Container-Daten.
1. Erstelle auf deiner Synology einen Ordner unter `/volume1/docker/argusflix_manager/`.
2. Kopiere deine Ordner `plugins/` und `scripts/` (z. B. via Git oder über die File Station) dorthin:
   - `/volume1/docker/argusflix_manager/plugins/`
   - `/volume1/docker/argusflix_manager/scripts/`
3. Öffne den **Container Manager** (DSM 7.2+) auf deiner Synology.
4. Gehe auf **Projekt** -> **Erstellen**.
5. Wähle als Pfad den erstellten Ordner `/volume1/docker/argusflix_manager`.
6. Wähle **docker-compose.yml erstellen** und füge den Inhalt der Datei `docker-templates/synology-nas/docker-compose.yml` ein.
7. Der Container Manager lädt das Image herunter, bindet deine angepassten Plugins und Scripte ein und startet die App.

### 🧰 C. Unraid
Für Unraid gibt es zwei Wege:
* **Weg 1 (Empfohlen): Docker Compose Plugin**
  1. Installiere das Plugin **Docker Compose** aus dem Unraid Community Applications (CA) Store.
  2. Klone dein Repository oder lade die Ordner in dein Appdata-Verzeichnis (typischerweise `/mnt/user/appdata/argusflix_manager/`).
  3. Erstelle ein neues Compose-Projekt im Unraid-Interface und füge den Inhalt von `docker-templates/unraid/docker-compose.yml` ein.
* **Weg 2: Manuelles Unraid Docker Template (Ohne Compose)**
  1. Gehe im Unraid-Webinterface auf den Reiter **Docker** und klicke unten auf **Add Container**.
  2. Trage folgende Werte ein:
     * **Name:** `argusflix_manager`
     * **Repository:** `ghcr.io/argusflix_manager/argusflix_manager:latest` (oder dein eigenes Image)
     * **WebUI:** `http://[IP]:[PORT:9191]`
     * **Pfad-Mapping 1:** Container-Pfad `/data` -> Host-Pfad `/mnt/user/appdata/argusflix_manager/data`
     * **Pfad-Mapping 2 (Plugins):** Container-Pfad `/data/plugins` -> Host-Pfad `/mnt/user/appdata/argusflix_manager/plugins`
     * **Pfad-Mapping 3 (Scripts):** Container-Pfad `/data/scripts` -> Host-Pfad `/mnt/user/appdata/argusflix_manager/scripts`
     * **Umgebungsvariable 1:** `ARGUSFLIX_ENV` = `aio`
     * **Umgebungsvariable 2:** `ARGUSFLIX_ALLOWED_SCRIPT_DIRS` = `/data/scripts`

---

## 🔒 4. Lizenzhinweis (AGPL-3.0)
ArgusFlix ist unter der **GNU AGPL-3.0** lizenziert. Da du das Repository **privat** hältst und für dich selbst betreibst (bzw. im privaten Kreis), ist das absolut kein Problem. Falls du das Repository jemals öffentlich (Public) machst, stelle sicher, dass du die AGPL-3.0-Lizenzbedingungen einhältst und deine Modifikationen ebenfalls unter derselben Lizenz öffentlich zugänglich machst.
