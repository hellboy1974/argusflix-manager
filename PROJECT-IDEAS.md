# ðŸ“� Projektentwurf: Die sieben geplanten ArgusFlix- & Script-Erweiterungen

Dieses Dokument dient als Ideen- und Architektur-Speicher fÃ¼r die sieben geplanten Projekte. Wir dokumentieren hier die technischen Konzepte, um sie nacheinander strukturiert umzusetzen.

---

## ðŸ”— Projekt 1: Dynamisches Iframe-UI-System (Update-Sicherheit)

Um zu verhindern, dass bei zukÃ¼nftigen offiziellen Updates deine geÃ¤nderten Frontend-Dateien (`navigation.js` und `App.jsx`) Ã¼berschrieben oder beschÃ¤digt werden, implementieren wir eine generische Schnittstelle fÃ¼r Plugins mit eigener BenutzeroberflÃ¤che.

### ðŸ› ï¸� Technische Umsetzung
* **Backend (Django):** Eine Django-Route in `apps/plugins/api_urls.py`, die statische Dateien (HTML/JS/CSS) direkt aus dem Ordner `plugins/<plugin_name>/ui/` ausliefert.
* **Frontend (React):** Eine universelle Route `/toolbox/:pluginKey` in `App.jsx`, die ein Vollbild-Iframe lÃ¤dt und das JWT-Authentifizierungstoken Ã¼bergibt.
* **Sidebar:** Dynamische Abfrage der aktiven Plugins. Plugins mit `"has_ui": true` in ihrer `plugin.json` werden automatisch als Sidebar-Eintrag gerendert.

---

## ðŸ”Œ Projekt 2: Die Xtream Toolbox (Neues Import-Feature)

Das nÃ¤chste groÃŸe Ingest-Werkzeug fÃ¼r Xtream-Codes-Panels.
* **Kernaufgabe:** Ein eigenstÃ¤ndiges Plugin mit Backend-Logik und einer separaten Web-OberflÃ¤che (HTML/JS) im Ordner `plugins/xtream_toolbox/ui/`, das Ã¼ber das neue Iframe-System geladen wird.
* **Vorteil:** Keine Core-Code-Ã„nderungen im React-Frontend nÃ¶tig!

---

## ðŸŽ›ï¸� Projekt 3: Das Hybride Admin-Center (Wartungs-Zentrale)

Ein zentraler Ort in deiner Sidebar, der administrative Wartungsfunktionen bÃ¼ndelt (ein MenÃ¼eintrag links mit interner Tab-Struktur):
* ðŸ©º **Modul 1: Live-Client-Monitor & Stream-Killer:** Echtzeit-Client-Verbindungsanzeige mit Button zum sofortigen Trennen aktiver Streams.
* ðŸ”’ **Modul 2: VPN-Guard & Kill-Switch:** Stoppt Stream-Proxys sofort, falls der VPN-Tunnel (Gluetun) abbricht.
* ðŸ“Š **Modul 3: Provider-Auditor:** NÃ¤chtlicher Uptime- und Latenz-Benchmark fÃ¼r mehrere IPTV-Anbieter.
* ðŸ•’ **Modul 4: EPG Timezone-Shifter:** Zeitanpassung fÃ¼r asynchrone EPG-Feeds.
* âœ‚ï¸� **Modul 5: Playlist-Slicer:** Filterung von M3U-Playlists vor dem Import (z. B. Ausschluss von SD- oder Adult-Sendern).
* ðŸ§¹ **Modul 6: SQLite DB-Optimizer:** `VACUUM`-Pflege fÃ¼r die SQLite-Datenbank und automatische Log-Bereinigung.

---

## ðŸ–¥ï¸� Projekt 4: Angina AIO (All-in-One) Desktop-Anwendung (PyQt5 & EXE)

Konsolidierung der drei einzelnen Standalone-Python-Scripte (`angina_mac_generator.py`, `angina_portal_status_checker.py` und `angina_portal-detective.py`) in einer einzigen PyQt5-Anwendung, die fÃ¼r Windows als `.exe` kompiliert werden kann.

### ðŸŽ¨ Design & Layout (Angina Theme)
* Ein einheitliches GUI-Fenster mit dem charakteristischen dunklen Angina-Theme (Dunkelgrauer Hintergrund, weiÃŸe Schrift, lila Akzente).
* Strukturierung Ã¼ber ein **Tab-System (QTabWidget)** mit drei Registern:
  1. **ðŸš¥ Portal Checker:** Multithreaded StatusprÃ¼fer fÃ¼r Listen von Portalen mit Import/Export-Optionen.
  2. **ðŸ•µï¸� Portal Detective:** Forensic-PrÃ¼fung einzelner Portale (Subdomains, Ports, SSL, Headers, Admin-Panels, Cloudflare, STB-Fingerprint).
  3. **ðŸ”¢ MAC Generator:** Schneller MAC-Adressen-Generator mit PrÃ¤fix-Checkboxen und Start/End-Suffix-Auswahl.

### ðŸ“¦ EXE-Kompilierung (PyInstaller)
Das Script wird so aufgebaut, dass es problemlos mit folgendem Befehl in eine einzelne, fensterbasierte Windows-AusfÃ¼hrungsdatei gepackt werden kann:
```powershell
pyinstaller --onefile --windowed --name="Angina_AIO" scripts/angina_aio.py
```

---

## ðŸ—‚ï¸� Projekt 5: Custom Sidebar-Editor (MenÃ¼-Personalisierung & Berechtigungssystem)

Erweiterung der Navigationseinstellungen, um dem Benutzer eine vollstÃ¤ndige Kontrolle Ã¼ber die Sidebar-EintrÃ¤ge im Frontend zu geben â€“ inklusive eines Administrations-Berechtigungssystems fÃ¼r Multi-User-Umgebungen.

### ðŸ› ï¸� Technische Umsetzung
* **Backend (Django):** 
  * Erweiterung des `User`-Modells ([models.py](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/apps/accounts/models.py)) um ein neues Feld/Berechtigung `can_edit_navigation` (Boolean, standardmÃ¤ÃŸig `False` fÃ¼r Streamer/Standard-User, `True` fÃ¼r Admins) oder als Eigenschaft in `custom_properties`.
  * Erweiterung des `custom_properties` JSON-Feldes um:
    * `navLabels`: Ein Mapping von MenÃ¼-ID zu neuem Namen (z. B. `{"channels": "Meine KanÃ¤le"}`).
    * `navIcons`: Ein Mapping von MenÃ¼-ID zu einem Lucide-Icon-Namen (z. B. `{"vods": "Film"}`).
* **Frontend (React):**
  * **Icon-Registry:** Eine vordefinierte Liste/Map von nutzbaren Lucide-Icons im Frontend, um String-Namen dynamisch in React-Komponenten aufzulÃ¶sen.
  * **Navigations-Config ([navigation.js](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/config/navigation.js)):** Dynamisches Ãœberschreiben von `label` und `icon` der Navigationsobjekte anhand der im User-Profil ([auth.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/store/auth.jsx)) gespeicherten Preferences.
  * **Einstellungs-UI ([NavOrderForm.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/components/forms/settings/NavOrderForm.jsx)):** Die Einstellungsseite prÃ¼ft, ob der User Admin-Rechte besitzt ODER `can_edit_navigation === true` ist. Falls nicht, wird das Bearbeitungs-Formular ausgeblendet.
  * **Admin-User-Verwaltung ([Users.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/pages/Users.jsx)):** In der Benutzerverwaltung kÃ¶nnen Administratoren Ã¼ber ein KontrollkÃ¤stchen / eine Switch-Option pro Benutzer festlegen, ob dieser das Recht besitzt, seine eigenen MenÃ¼eintrÃ¤ge anzupassen.

---

## ðŸ“º Projekt 6: Unified Media UI System (Live-TV, VOD & Serien)

Vereinheitlichung der BenutzeroberflÃ¤chen fÃ¼r die drei Kern-Medienbereiche. VODs und Serien werden aus der gemeinsamen VODs-Seite herausgelÃ¶st, erhalten eigene MenÃ¼eintrÃ¤ge mit passenden Icons und werden optisch an das Ã¼bersichtliche Split-Layout der Live-TV (Channels)-Seite angepasst.

### ðŸ› ï¸� Technische Umsetzung
* **Frontend-Navigation ([navigation.js](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/config/navigation.js)):**
  * Aufteilung des `vods`-Eintrags in zwei separate Root-EintrÃ¤ge:
    * **Movies / VODs:** z. B. Icon `Film` oder `Video`, Pfad `/movies`.
    * **Series / Serien:** z. B. Icon `Tv` oder `Clapperboard`, Pfad `/series`.
* **Frontend-Routing ([App.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/App.jsx)):**
  * Erstellung neuer Routen `/movies` und `/series` anstelle der generischen `/vods`-Route.
* **UI Layout (Basierend auf [Channels.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/pages/Channels.jsx)):**
  * **Unified Grid/Table Split-View (Allotment):**
    * Verwendung des `Allotment`-Splitters in den neuen Seiten.
    * **Linke Spalte:** Eine Ã¼bersichtliche, durchsuch- und filterbare Tabelle aller Filme bzw. Serien (analog zur `ChannelsTable` in Live-TV).
    * **Rechte Spalte:** Die Detail- und Stream-Ansicht fÃ¼r das ausgewÃ¤hlte Element.
      * FÃ¼r **Movies:** Filmdetails, Poster, Beschreibungen, Stream-Links und Zuweisungen.
      * FÃ¼r **Series:** Serienbeschreibung, Staffel-Auswahl und die Episodenliste mit ihren jeweiligen Streams (analog zur `StreamsTable`).
  * Beibehalt des reaktiven Designs und des automatischen Speicherns der Spaltenaufteilung in `localStorage`.

---

## ðŸ”Œ Projekt 7: Custom Playlist-Engine (Hybrid M3U- & Xtream-Codes-Exporter)

ErmÃ¶glicht die Erstellung und den Export von benutzerdefinierten Playlists, die eine hybride Mischung aus Live-TV, VOD (Filmen) und Serien enthalten. Diese Inhalte werden dynamisch aus verschiedenen Upstream-Quellen wie Stalker-Portalen (MAG/STB) und Xtream-Codes-Panels importiert und zusammengefÃ¼hrt.

### ðŸ› ï¸� Technische Umsetzung
* **Backend (Django & Apps):**
  * **Daten-Aggregation:** Integration einer Abfragelogik, die KanÃ¤le, VODs und Serien aus Stalker-Modulen (`apps/plugins`) und Xtream-Modulen (`apps/m3u` / custom apps) importieren kann.
  * **Dynamic Sync & Cron-Scheduler:** Ein Hintergrund-Task-System (z. B. via Celery/Django-Q oder Cron-Jobs), das Upstream-Quellen zeitgesteuert oder manuell abgleicht. Wenn ein Upstream-Provider einen Stream-Link erneuert (z. B. durch geÃ¤nderte Session-Tokens oder Server-Routing), werden die betroffenen Live-KanÃ¤le, Filme und Serien in der ArgusFlix-Datenbank automatisch auf den neuesten Stand gebracht, um Link-AusfÃ¤lle zu vermeiden.
  * **Export-Endpunkte ([urls.py](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/apps/output/urls.py) & [views.py](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/apps/output/views.py)):**
    * Generierung dynamischer `.m3u` / `.m3u8` Playlist-Dateien.
    * Bereitstellung einer Xtream-Codes-kompatiblen API-Emulation (`/player_api.php`), damit EndgerÃ¤te die Stream-Typen (Live, Movie, Series) und EPG-Daten vollautomatisch zuordnen kÃ¶nnen.
  * **Session- & Token-Caching:** Da Stalker-Portale oft sitzungsbasierte Port-Links verwenden, verwaltet das Backend temporÃ¤re Streaming-URLs transparent im Hintergrund und liefert sie Ã¼ber einen internen Proxy aus.
* **Frontend (React):**
  * **Playlist-Builder UI:** Ein intuitiver Baukasten, in dem Admins per Drag-and-Drop oder Multi-Select Streams, Filme und Serien zu einer neuen Playlist hinzufÃ¼gen kÃ¶nnen.
  * **Source Mapper:** Eine Zuweisungs-OberflÃ¤che, auf der festgelegt wird, welcher Upstream-Provider (Stalker-Portal X oder Xtream-Panel Y) fÃ¼r welchen Ziel-Kanal/VOD in der Custom Playlist genutzt werden soll (inkl. Fallbacks).
  * **Scheduler & Sync UI:** Eine Zeitauswahl (Timepicker / Intervall-Dropdown) zur Definition automatischer AktualisierungsplÃ¤ne pro Upstream-Quelle, kombiniert mit einem Button fÃ¼r die sofortige manuelle Synchronisation.

---

## ðŸ“… Projekt 8: Ãœberarbeitung der EPG-Verwaltung

Optimierung und Flexibilisierung des EPG-Imports und der EPG-Zuordnung fÃ¼r eine verbesserte Handhabung von Programmdaten.

### ðŸ› ï¸� Technische Umsetzung
* **Backend (Django):**
  * **EPG-Zuweisung & Mapping:** Optimierung des Algorithmus zur automatischen Zuordnung von EPG-KanÃ¤len zu Stream-KanÃ¤len basierend auf Ã„hnlichkeitsmetriken.
  * **Multi-Source-EPG-Aggregator:** Importieren und Mergen von mehreren XMLTV-, GZ- oder ZIP-EPG-Quellen.
  * **PrÃ¤zises Offset-Management:** Einstellbarer Zeitversatz (Timezone Offset) pro EPG-Quelle und zusÃ¤tzlich pro Einzelkanal im Backend.
* **Frontend (React):**
  * **Visueller EPG-Inspektor & Editor:** Eine BenutzeroberflÃ¤che zur direkten Vorschau des EPG-Programms pro Kanal, mit der MÃ¶glichkeit zur manuellen Korrektur von Zuordnungen und EPG-IDs.
  * **EPG-Status-Monitor:** Ãœbersichtliche Anzeige der Aktualisierungszeiten aller EPG-Quellen, der Anzahl geladener Sendungen und eventueller Parse-Fehler.

---

## ðŸ”Œ Projekt 9: Ãœberarbeitung der M3U- und Xtream-ZugÃ¤nge (Original-Feature-Redesign)

Komplette Neugestaltung und Erweiterung der integrierten Import-Funktionen fÃ¼r M3U-Playlists und Xtream-Codes-ZugÃ¤nge im Core-System, um mehr Kontrolle Ã¼ber Verbindungsparameter und ImportablÃ¤ufe zu ermÃ¶glichen.

### ðŸ› ï¸� Technische Umsetzung
* **Backend (Django):**
  * **Erweitertes Connection-Management:** Optionale Einstellungen fÃ¼r HTTP User-Agent, Timeout-Werte, SSL-ZertifikatsprÃ¼fung umgehen, und Proxy-Routing pro M3U-Account.
  * **Automatisches Stream-Validieren:** Hintergrund-Tasks, die Stream-URLs auf Erreichbarkeit prÃ¼fen und defekte Streams automatisch deaktivieren oder markieren.
  * **FeinkÃ¶rniger Filter-Mechanismus:** Ausschluss oder Filterung bestimmter Gruppen (LÃ¤nder, Genres) oder Stream-Typen (SD vs. HD) direkt auf Datenbank-Ebene beim Sync.
* **Frontend (React):**
  * **Modernisiertes Dashboard:** Ein Ã¼bersichtlicheres und ansprechenderes Redesign der Seiten zur Verwaltung von M3U-Playlists und Xtream-Verbindungen, mit direkter Visualisierung von Verbindungsstatus und Anzahl der Streams.
  * **Detaillierte Import-Logs:** Ein Echtzeit-Import-Inspector, der Logs und Fehlerberichte wÃ¤hrend einer Synchronisierung Ã¼bersichtlich anzeigt.

---

## ðŸŒ� Projekt 10: Mehrsprachigkeit (Internationalisierung / i18n)

Implementierung einer vollstÃ¤ndigen Mehrsprachigkeit (z. B. Deutsch und Englisch) sowohl im React-Frontend als auch im Django-Backend.

### ðŸ› ï¸� Technische Umsetzung
* **Frontend (React - i18next):**
  - **Bibliotheken:** Integration von `i18next`, `react-i18next` und `i18next-browser-languagedetector`.
  - **Lokalisierungsdateien:** Erstellung von JSON-WÃ¶rterbÃ¼chern fÃ¼r jede Sprache im Frontend (z. B. `frontend/src/locales/de.json` und `en.json`).
  - **Komponenten-Refactoring:** Ersetzung statischer Texte durch Ãœbersetzungs-Hooks: `const { t } = useTranslation();` und `{t('key')}`.
  - **Language-Selector:** Ein Dropdown-MenÃ¼ in der Sidebar oder den Benutzereinstellungen zur Sprachwahl. Die ausgewÃ¤hlte Sprache wird in den `custom_properties` des Benutzers im Backend gespeichert, sodass sie auf allen GerÃ¤ten synchronisiert wird.
* **Backend (Django - i18n):**
  - **Django Translation:** Verwendung von `gettext_lazy` in Modellen, Serializern und Views fÃ¼r Ã¼bersetzbare Fehlermeldungen und System-Benachrichtigungen.
  - **Spracherkennung:** Aktivierung der Django LocaleMiddleware, um die Sprache automatisch anhand des `Accept-Language` Headers oder eines benutzerdefinierten Cookies/Settings zu wÃ¤hlen.
  - **Lokalisierungs-Kompilierung:** Ãœbersetzung Ã¼ber Standard-Ãœbersetzungsdateien (`django.po` / `django.mo`), die mittels Djangos `makemessages` und `compilemessages` verwaltet werden.


---

## ðŸ“± Projekt 11: Argus IPTV Player Companion-System (Device Management)

Ausbau von ArgusFlix Manager zu einem zentralen Management-Backend (MDM) fÃ¼r den kommenden "Argus IPTV Player" (Android TV App).

### ðŸ› ï¸� Technische Umsetzung
* **Backend (Django) & Architektur:**
  * **Pairing-System:** Ein sicheres Kopplungsverfahren mittels Server-URL (lokal oder VPS) und generiertem API-Key/Token, welches in der Argus-App eingetragen wird.
  * **Live-Kommunikation (WebSockets):** Integration von `Django Channels` fÃ¼r eine dauerhafte, bidirektionale Verbindung zwischen ArgusFlix und dem Fernseher. Dies ermÃ¶glicht Echtzeit-Push-Kommandos hinter NAT-Routern.
  * **Provider-Transfer:** Konvertierung von Zugangsdaten (Stalker, Xtream, M3U, Custom Playlists) in strukturierte JSON-Payloads, die direkt an die gekoppelte Argus-App gepusht werden.
  * **Remote Backup & Restore:** API-Endpoints fÃ¼r das Empfangen verschlÃ¼sselter SQLite-App-Backups vom Fernseher und das Senden von Restore-Befehlen an den TV.
* **Frontend (React) - Device Manager:**
  * Eine neue Sidebar-Kategorie ("Argus GerÃ¤te") zur Ãœbersicht aller gekoppelten TVs (Status, IP, installierte Playlisten).
  * Eine grafische OberflÃ¤che, um gezielt Playlisten zu pushen und Backups zu erstellen/wiederherzustellen.
* **App-Technologie (Empfehlung fÃ¼r Argus):**
  * Natives Android (Kotlin) kombiniert mit **Jetpack Compose for TV** fÃ¼r die UI und **ExoPlayer** fÃ¼r maximale Performance bei IPTV-Streams.

---

## ðŸŽ¬ Projekt 12: Media-Server-Management (Plex / Emby / Jellyfin)

Integration und Verwaltung von Drittanbieter-Mediaservern, damit deren ZugÃ¤nge komfortabel Ã¼ber ArgusFlix gesammelt und an externe Clients (wie den Argus IPTV Player) Ã¼bergeben werden kÃ¶nnen.

### ðŸ› ï¸� Technische Umsetzung
* **Backend (Django):**
  * Neues Datenmodell zur Speicherung von Server-Typ (Plex, Emby, Jellyfin), Basis-URL und Authentication-Tokens.
  * API-Routen fÃ¼r "Connection Checks", um die Erreichbarkeit der Mediaserver und die GÃ¼ltigkeit der Tokens zu verifizieren.
* **Frontend (React):**
  * Eine Einstellungsseite zur Verwaltung dieser Mediaserver-Profile.
# 📌 Projektentwurf: Die sieben geplanten ArgusFlix- & Script-Erweiterungen

Dieses Dokument dient als Ideen- und Architektur-Speicher für die sieben geplanten Projekte. Wir dokumentieren hier die technischen Konzepte, um sie nacheinander strukturiert umzusetzen.

---

## 🔗 Projekt 1: Dynamisches Iframe-UI-System (Update-Sicherheit)

Um zu verhindern, dass bei zukünftigen offiziellen Updates deine geänderten Frontend-Dateien (`navigation.js` und `App.jsx`) überschrieben oder beschädigt werden, implementieren wir eine generische Schnittstelle für Plugins mit eigener Benutzeroberfläche.

### 🛠 Technische Umsetzung
* **Backend (Django):** Eine Django-Route in `apps/plugins/api_urls.py`, die statische Dateien (HTML/JS/CSS) direkt aus dem Ordner `plugins/<plugin_name>/ui/` ausliefert.
* **Frontend (React):** Eine universelle Route `/toolbox/:pluginKey` in `App.jsx`, die ein Vollbild-Iframe lädt und das JWT-Authentifizierungstoken übergibt.
* **Sidebar:** Dynamische Abfrage der aktiven Plugins. Plugins mit `"has_ui": true` in ihrer `plugin.json` werden automatisch als Sidebar-Eintrag gerendert.

---

## 🔌 Projekt 2: Die Xtream Toolbox (Neues Import-Feature)

Das nächste große Ingest-Werkzeug für Xtream-Codes-Panels.
* **Kernaufgabe:** Ein eigenständiges Plugin mit Backend-Logik und einer separaten Web-Oberfläche (HTML/JS) im Ordner `plugins/xtream_toolbox/ui/`, das über das neue Iframe-System geladen wird.
* **Vorteil:** Keine Core-Code-Änderungen im React-Frontend nötig!

---

## ⛴️ Projekt 3: Das Hybride Admin-Center (Wartungs-Zentrale)

Ein zentraler Ort in deiner Sidebar, der administrative Wartungsfunktionen bündelt (ein Menüeintrag links mit interner Tab-Struktur):
* 🩺 **Modul 1: Live-Client-Monitor & Stream-Killer:** Echtzeit-Client-Verbindungsanzeige mit Button zum sofortigen Trennen aktiver Streams.
* 🔒 **Modul 2: VPN-Guard & Kill-Switch:** Stoppt Stream-Proxys sofort, falls der VPN-Tunnel (Gluetun) abbricht.
* 📊 **Modul 3: Provider-Auditor:** Nächtlicher Uptime- und Latenz-Benchmark für mehrere IPTV-Anbieter.
* ⌚ **Modul 4: EPG Timezone-Shifter:** Zeitanpassung für asynchrone EPG-Feeds.
* ✂️ **Modul 5: Playlist-Slicer:** Filterung von M3U-Playlists vor dem Import (z. B. Ausschluss von SD- oder Adult-Sendern).
* 🧹 **Modul 6: SQLite DB-Optimizer:** `VACUUM`-Pflege für die SQLite-Datenbank und automatische Log-Bereinigung.

---

## 🖥️ Projekt 4: Angina AIO (All-in-One) Desktop-Anwendung (PyQt5 & EXE)

Konsolidierung der drei einzelnen Standalone-Python-Scripte (`angina_mac_generator.py`, `angina_portal_status_checker.py` und `angina_portal-detective.py`) in einer einzigen PyQt5-Anwendung, die für Windows als `.exe` kompiliert werden kann.

### 🎨 Design & Layout (Angina Theme)
* Ein einheitliches GUI-Fenster mit dem charakteristischen dunklen Angina-Theme (Dunkelgrauer Hintergrund, weiße Schrift, lila Akzente).
* Strukturierung über ein **Tab-System (QTabWidget)** mit drei Registern:
  1. **🚨 Portal Checker:** Multithreaded Statusprüfer für Listen von Portalen mit Import/Export-Optionen.
  2. **🕵️ Portal Detective:** Forensic-Prüfung einzelner Portale (Subdomains, Ports, SSL, Headers, Admin-Panels, Cloudflare, STB-Fingerprint).
  3. **📠 MAC Generator:** Schneller MAC-Adressen-Generator mit Präfix-Checkboxen und Start/End-Suffix-Auswahl.

### 📦 EXE-Kompilierung (PyInstaller)
Das Script wird so aufgebaut, dass es problemlos mit folgendem Befehl in eine einzelne, fensterbasierte Windows-Ausführungsdatei gepackt werden kann:
```powershell
pyinstaller --onefile --windowed --name="Angina_AIO" scripts/angina_aio.py
```

---

## 📂 Projekt 5: Custom Sidebar-Editor (Menü-Personalisierung & Berechtigungssystem)

Erweiterung der Navigationseinstellungen, um dem Benutzer eine vollständige Kontrolle über die Sidebar-Einträge im Frontend zu geben – inklusive eines Administrations-Berechtigungssystems für Multi-User-Umgebungen.

### 🛠 Technische Umsetzung
* **Backend (Django):** 
  * Erweiterung des `User`-Modells ([models.py](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/apps/accounts/models.py)) um ein neues Feld/Berechtigung `can_edit_navigation` (Boolean, standardmäßig `False` für Streamer/Standard-User, `True` für Admins) oder als Eigenschaft in `custom_properties`.
  * Erweiterung des `custom_properties` JSON-Feldes um:
    * `navLabels`: Ein Mapping von Menü-ID zu neuem Namen (z. B. `{"channels": "Meine Kanäle"}`).
    * `navIcons`: Ein Mapping von Menü-ID zu einem Lucide-Icon-Namen (z. B. `{"vods": "Film"}`).
* **Frontend (React):**
  * **Icon-Registry:** Eine vordefinierte Liste/Map von nutzbaren Lucide-Icons im Frontend, um String-Namen dynamisch in React-Komponenten aufzulösen.
  * **Navigations-Config ([navigation.js](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/config/navigation.js)):** Dynamisches Überschreiben von `label` und `icon` der Navigationsobjekte anhand der im User-Profil ([auth.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/store/auth.jsx)) gespeicherten Preferences.
  * **Einstellungs-UI ([NavOrderForm.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/components/forms/settings/NavOrderForm.jsx)):** Die Einstellungsseite prüft, ob der User Admin-Rechte besitzt ODER `can_edit_navigation === true` ist. Falls nicht, wird das Bearbeitungs-Formular ausgeblendet.
  * **Admin-User-Verwaltung ([Users.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/pages/Users.jsx)):** In der Benutzerverwaltung können Administratoren über ein Kontrollkästchen / eine Switch-Option pro Benutzer festlegen, ob dieser das Recht besitzt, seine eigenen Menüeinträge anzupassen.

---

## 📺 Projekt 6: Unified Media UI System (Live-TV, VOD & Serien)

Vereinheitlichung der Benutzeroberflächen für die drei Kern-Medienbereiche. VODs und Serien werden aus der gemeinsamen VODs-Seite herausgelöst, erhalten eigene Menüeinträge mit passenden Icons und werden optisch an das übersichtliche Split-Layout der Live-TV (Channels)-Seite angepasst.

### 🛠 Technische Umsetzung
* **Frontend-Navigation ([navigation.js](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/config/navigation.js)):**
  * Aufteilung des `vods`-Eintrags in zwei separate Root-Einträge:
    * **Movies / VODs:** z. B. Icon `Film` oder `Video`, Pfad `/movies`.
    * **Series / Serien:** z. B. Icon `Tv` oder `Clapperboard`, Pfad `/series`.
* **Frontend-Routing ([App.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/App.jsx)):**
  * Erstellung neuer Routen `/movies` und `/series` anstelle der generischen `/vods`-Route.
* **UI Layout (Basierend auf [Channels.jsx](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/frontend/src/pages/Channels.jsx)):**
  * **Unified Grid/Table Split-View (Allotment):**
    * Verwendung des `Allotment`-Splitters in den neuen Seiten.
    * **Linke Spalte:** Eine übersichtliche, durchsuch- und filterbare Tabelle aller Filme bzw. Serien (analog zur `ChannelsTable` in Live-TV).
    * **Rechte Spalte:** Die Detail- und Stream-Ansicht für das ausgewählte Element.
      * Für **Movies:** Filmdetails, Poster, Beschreibungen, Stream-Links und Zuweisungen.
      * Für **Series:** Serienbeschreibung, Staffel-Auswahl und die Episodenliste mit ihren jeweiligen Streams (analog zur `StreamsTable`).
  * Beibehalt des reaktiven Designs und des automatischen Speicherns der Spaltenaufteilung in `localStorage`.

---

## 🔌 Projekt 7: Custom Playlist-Engine (Hybrid M3U- & Xtream-Codes-Exporter)

Ermöglicht die Erstellung und den Export von benutzerdefinierten Playlists, die eine hybride Mischung aus Live-TV, VOD (Filmen) und Serien enthalten. Diese Inhalte werden dynamisch aus verschiedenen Upstream-Quellen wie Stalker-Portalen (MAG/STB) und Xtream-Codes-Panels importiert und zusammengeführt.

### 🛠 Technische Umsetzung
* **Backend (Django & Apps):**
  * **Daten-Aggregation:** Integration einer Abfragelogik, die Kanäle, VODs und Serien aus Stalker-Modulen (`apps/plugins`) und Xtream-Modulen (`apps/m3u` / custom apps) importieren kann.
  * **Dynamic Sync & Cron-Scheduler:** Ein Hintergrund-Task-System (z. B. via Celery/Django-Q oder Cron-Jobs), das Upstream-Quellen zeitgesteuert oder manuell abgleicht. Wenn ein Upstream-Provider einen Stream-Link erneuert (z. B. durch geänderte Session-Tokens oder Server-Routing), werden die betroffenen Live-Kanäle, Filme und Serien in der ArgusFlix-Datenbank automatisch auf den neuesten Stand gebracht, um Link-Ausfälle zu vermeiden.
  * **Export-Endpunkte ([urls.py](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/apps/output/urls.py) & [views.py](file:///c:/Users/sheng/Documents/argusflix_manager_reloaded/ArgusFlix-0.25.1/apps/output/views.py)):**
    * Generierung dynamischer `.m3u` / `.m3u8` Playlist-Dateien.
    * Bereitstellung einer Xtream-Codes-kompatiblen API-Emulation (`/player_api.php`), damit Endgeräte die Stream-Typen (Live, Movie, Series) und EPG-Daten vollautomatisch zuordnen können.
  * **Session- & Token-Caching:** Da Stalker-Portale oft sitzungsbasierte Port-Links verwenden, verwaltet das Backend temporäre Streaming-URLs transparent im Hintergrund und liefert sie über einen internen Proxy aus.
* **Frontend (React):**
  * **Playlist-Builder UI:** Ein intuitiver Baukasten, in dem Admins per Drag-and-Drop oder Multi-Select Streams, Filme und Serien zu einer neuen Playlist hinzufügen können.
  * **Source Mapper:** Eine Zuweisungs-Oberfläche, auf der festgelegt wird, welcher Upstream-Provider (Stalker-Portal X oder Xtream-Panel Y) für welchen Ziel-Kanal/VOD in der Custom Playlist genutzt werden soll (inkl. Fallbacks).
  * **Scheduler & Sync UI:** Eine Zeitauswahl (Timepicker / Intervall-Dropdown) zur Definition automatischer Aktualisierungspläne pro Upstream-Quelle, kombiniert mit einem Button für die sofortige manuelle Synchronisation.

---

## 📅 Projekt 8: Überarbeitung der EPG-Verwaltung

Optimierung und Flexibilisierung des EPG-Imports und der EPG-Zuordnung für eine verbesserte Handhabung von Programmdaten.

### 🛠 Technische Umsetzung
* **Backend (Django):**
  * **EPG-Zuweisung & Mapping:** Optimierung des Algorithmus zur automatischen Zuordnung von EPG-Kanälen zu Stream-Kanälen basierend auf Ähnlichkeitsmetriken.
  * **Multi-Source-EPG-Aggregator:** Importieren und Mergen von mehreren XMLTV-, GZ- oder ZIP-EPG-Quellen.
  * **Präzises Offset-Management:** Einstellbarer Zeitversatz (Timezone Offset) pro EPG-Quelle und zusätzlich pro Einzelkanal im Backend.
* **Frontend (React):**
  * **Visueller EPG-Inspektor & Editor:** Eine Benutzeroberfläche zur direkten Vorschau des EPG-Programms pro Kanal, mit der Möglichkeit zur manuellen Korrektur von Zuordnungen und EPG-IDs.
  * **EPG-Status-Monitor:** Übersichtliche Anzeige der Aktualisierungszeiten aller EPG-Quellen, der Anzahl geladener Sendungen und eventueller Parse-Fehler.

---

## 🔌 Projekt 9: Überarbeitung der M3U- und Xtream-Zugänge (Original-Feature-Redesign)

Komplette Neugestaltung und Erweiterung der integrierten Import-Funktionen für M3U-Playlists und Xtream-Codes-Zugänge im Core-System, um mehr Kontrolle über Verbindungsparameter und Importabläufe zu ermöglichen.

### 🛠 Technische Umsetzung
* **Backend (Django):**
  * **Erweitertes Connection-Management:** Optionale Einstellungen für HTTP User-Agent, Timeout-Werte, SSL-Zertifikatsprüfung umgehen, und Proxy-Routing pro M3U-Account.
  * **Automatisches Stream-Validieren:** Hintergrund-Tasks, die Stream-URLs auf Erreichbarkeit prüfen und defekte Streams automatisch deaktivieren oder markieren.
  * **Feinkörniger Filter-Mechanismus:** Ausschluss oder Filterung bestimmter Gruppen (Länder, Genres) oder Stream-Typen (SD vs. HD) direkt auf Datenbank-Ebene beim Sync.
* **Frontend (React):**
  * **Modernisiertes Dashboard:** Ein übersichtlicheres und ansprechenderes Redesign der Seiten zur Verwaltung von M3U-Playlists und Xtream-Verbindungen, mit direkter Visualisierung von Verbindungsstatus und Anzahl der Streams.
  * **Detaillierte Import-Logs:** Ein Echtzeit-Import-Inspector, der Logs und Fehlerberichte während einer Synchronisierung übersichtlich anzeigt.

---

## 🌍 Projekt 10: Mehrsprachigkeit (Internationalisierung / i18n)

Implementierung einer vollständigen Mehrsprachigkeit (z. B. Deutsch und Englisch) sowohl im React-Frontend als auch im Django-Backend.

### 🛠 Technische Umsetzung
* **Frontend (React - i18next):**
  - **Bibliotheken:** Integration von `i18next`, `react-i18next` und `i18next-browser-languagedetector`.
  - **Lokalisierungsdateien:** Erstellung von JSON-Wörterbüchern für jede Sprache im Frontend (z. B. `frontend/src/locales/de.json` und `en.json`).
  - **Komponenten-Refactoring:** Ersetzung statischer Texte durch Übersetzungs-Hooks: `const { t } = useTranslation();` und `{t('key')}`.
  - **Language-Selector:** Ein Dropdown-Menü in der Sidebar oder den Benutzereinstellungen zur Sprachwahl. Die ausgewählte Sprache wird in den `custom_properties` des Benutzers im Backend gespeichert, sodass sie auf allen Geräten synchronisiert wird.
* **Backend (Django - i18n):**
  - **Django Translation:** Verwendung von `gettext_lazy` in Modellen, Serializern und Views für übersetzbare Fehlermeldungen und System-Benachrichtigungen.
  - **Spracherkennung:** Aktivierung der Django LocaleMiddleware, um die Sprache automatisch anhand des `Accept-Language` Headers oder eines benutzerdefinierten Cookies/Settings zu wählen.
  - **Lokalisierungs-Kompilierung:** Übersetzung über Standard-Übersetzungsdateien (`django.po` / `django.mo`), die mittels Djangos `makemessages` und `compilemessages` verwaltet werden.


---

## 📲 Projekt 11: Argus IPTV Player Companion-System (Device Management)

Ausbau von ArgusFlix Manager zu einem zentralen Management-Backend (MDM) für den kommenden "Argus IPTV Player" (Android TV App).

### 🛠 Technische Umsetzung
* **Backend (Django) & Architektur:**
  * **Pairing-System:** Ein sicheres Kopplungsverfahren mittels Server-URL (lokal oder VPS) und generiertem API-Key/Token, welches in der Argus-App eingetragen wird.
  * **Live-Kommunikation (WebSockets):** Integration von `Django Channels` für eine dauerhafte, bidirektionale Verbindung zwischen ArgusFlix und dem Fernseher. Dies ermöglicht Echtzeit-Push-Kommandos hinter NAT-Routern.
  * **Provider-Transfer:** Konvertierung von Zugangsdaten (Stalker, Xtream, M3U, Custom Playlists) in strukturierte JSON-Payloads, die direkt an die gekoppelte Argus-App gepusht werden.
  * **Remote Backup & Restore:** API-Endpoints für das Empfangen verschlüsselter SQLite-App-Backups vom Fernseher und das Senden von Restore-Befehlen an den TV.
* **Frontend (React) - Device Manager:**
  * Eine neue Sidebar-Kategorie ("Argus Geräte") zur Übersicht aller gekoppelten TVs (Status, IP, installierte Playlisten).
  * Eine grafische Oberfläche, um gezielt Playlisten zu pushen und Backups zu erstellen/wiederherzustellen.
* **App-Technologie (Empfehlung für Argus):**
  * Natives Android (Kotlin) kombiniert mit **Jetpack Compose for TV** für die UI und **ExoPlayer** für maximale Performance bei IPTV-Streams.

---

## 🎬 Projekt 12: Media-Server-Management (Plex / Emby / Jellyfin)

Integration und Verwaltung von Drittanbieter-Mediaservern, damit deren Zugänge komfortabel über ArgusFlix gesammelt und an externe Clients (wie den Argus IPTV Player) übergeben werden können.

### 🛠 Technische Umsetzung
* **Backend (Django):**
  * Neues Datenmodell zur Speicherung von Server-Typ (Plex, Emby, Jellyfin), Basis-URL und Authentication-Tokens.
  * API-Routen für "Connection Checks", um die Erreichbarkeit der Mediaserver und die Gültigkeit der Tokens zu verifizieren.
* **Frontend (React):**
  * Eine Einstellungsseite zur Verwaltung dieser Mediaserver-Profile.
  * Ein Klick-Mechanismus ("An Argus senden"), der die Zugangsdaten über das WebSocket-System aus Projekt 11 direkt in die lokale Datenbank der Android TV App pusht.

### Projekt 13: Dynamischer App-Page-Builder (Widgets & Profile)
*   **Konzept:** Ein Editor im ArgusFlix Manager, um die App-Oberflächen (Homescreen, Filme, Serien, Live TV) wie eine Art Homepage-Baukasten anzupassen.
*   **Profile:** Unterstützung für verschiedene Layout-Profile (z.B. Profil A bekommt Layout X, Profil B bekommt Layout Y).
*   **Widgets:** Einzelne Reihen, Quellen oder Ansichten können als Widgets auf verschiedenen Seiten (Home, Movies, Series, Live TV) platziert werden.
*   **Live-Push:** Speichern der Layouts pusht die Updates in Echtzeit via WebSocket an die TV-Geräte, die sich ohne Neustart sofort aktualisieren.

---

## 🚀 Projekt 14: Automatisierte Deployments & EPG Pre-Seeding

Vollautomatisierte Installations-Routinen für den ArgusFlix Manager und Vorkonfiguration von EPG-Daten, sodass das System nach der Installation sofort startklar ("Out of the Box") ist.

### 🛠 Technische Umsetzung
* **Ubuntu / Debian Auto-Installer:** Ein intelligentes Bash-Skript (`install_ubuntu.sh`), das Docker installiert, das GitHub-Repository klont, sichere `.env`-Standards generiert und den Manager startet.
* **Unraid Community Template:** Eine Unraid-kompatible XML-Datei (`argusflix.xml`), die alle Ports, Volumes und Environment-Variablen für ein echtes "One-Click"-Deployment über die Unraid Web-GUI vorbereitet.
* **EPG Fixtures Pre-Loading:** Erweiterung der `fixtures.json` um eine vom User vordefinierte, nach Ländern gruppierte Liste von XMLTV/EPG-URLs. Nach der automatisierten Installation lädt der Manager diese Fixtures direkt in die Datenbank. Der Nutzer wählt bei der Sender-Zuweisung nur noch die Gruppe (z.B. "Deutschland") und hat direkt Zugriff auf alle vorkonfigurierten EPG-Daten.

### Projekt 14: App UI für Profil-Auswahl & PIN-Schutz
*   **Konzept:** Umsetzung der Cloud-Profile in der Android TV App.
*   **Profilauswahl:** Beim Start der App (oder beim Wechsel) soll ein ansprechender Bildschirm zur Auswahl des aktiven Profils angezeigt werden.
*   **PIN-Schutz:** Wenn im Manager für ein Profil eine 4-stellige PIN hinterlegt wurde, muss die App einen Nummernblock oder einen einfachen PIN-Dialog einblenden. Erst bei korrekter Eingabe wird das Profil aktiv.
*   **Sync:** Nach der Profilwahl werden Watch History und Favoriten des gewählten Profils heruntergeladen bzw. lokal synchronisiert.

---

## 📻 Projekt 15: Internetradio Integration (Chora-Vorbild)

Zentrale Verwaltung von Internetradio-Sendern im ArgusFlix Manager und nahtlose Synchronisation an die ArgusFlix App mit speziellem Audio-Fokus.

### 🛠 Technische Umsetzung
* **Backend (Django):**
  * **Neues Modul:** `RadioStation` Modell zur Speicherung von Stream-URLs, Logos, Sendername und Metadaten/Genres.
  * **Manager-UI:** Eine neue Oberfläche im React-Frontend zur Verwaltung (Hinzufügen, Sortieren, Gruppieren) von Internetradios.
  * **Sync-Schnittstelle:** Bereitstellung der Radio-Liste als dynamische M3U-Playlist oder über den bestehenden WebSocket/API-Kanal an die App.
* **Frontend (React / Android App):**
  * **Wiedergabe:** Nutzung von `Media3` (ExoPlayer), um MP3, AAC und HLS Audio-Streams nativ abzuspielen.
  * **App-UI:** Umsetzung eines neuen Radio-Bereichs (ähnlich wie Chora) mit Kacheln für Senderlogos und einer TV-freundlichen "Now Playing"-Ansicht für Audio-Content.

---

## 📋 Projekt 16: M3U Editor (Erweitertes Playlist-Management)

Ausbau der bestehenden M3U-Fähigkeiten zu einem visuellen und smarten Editor.
* **Visueller Drag & Drop Editor (Frontend):** Eine interaktive React-Oberfläche (z.B. mit `dnd-kit`), auf der man Kanäle zwischen Gruppen verschieben, verstecken (`hidden_from_output`) und EPG-IDs (`tvg_id`) anpassen kann.
* **Automatischer Link-Validator (Dead Link Checker):** Ein Celery-Hintergrund-Task, der die `Stream`-URLs regelmäßig anpingt (HEAD-Request) und bei Timeouts/404 den Kanal automatisch versteckt oder als "offline" markiert.
* **Auto-EPG & Logo Matcher:** Wenn ein Kanal importiert wird und keine `tvg_id` hat, soll der Manager versuchen, den Namen per Fuzzy-Search mit einer internen/globalen EPG-Datenbank abzugleichen.

---

## 🕵️ Projekt 17: Stalkerhek (Stalker Portal & MAC Management)

Das Scannen von Portalen (`StalkerPortalScan`) existiert bereits, soll aber für Ausfallsicherheit erweitert werden.
* **Automatischer MAC-Failover (Rotation):** Wenn die `authenticate()` Methode eines Stalker-Accounts fehlschlägt (z.B. "Account blocked"), sucht der Manager in `StalkerPortalScanResult` nach einer neuen "Approved" MAC-Adresse für dasselbe Portal und updatet das Profil.
* **Automatisierter Portal-Health-Check:** Ein Cronjob, der wöchentlich die aktiven MAC-Adressen prüft und Warnungen (Webhooks/Notifications) ausgibt, falls Accounts bald ablaufen (`expires_at`).
* **Catchup/Timeshift-Extraktor:** Automatische Analyse der Stalker-Kanäle (im `get_all_channels` Response), ob ein Catchup-Typ vorliegt, und entsprechende Konfiguration der Catchup-URL-Parameter.

---

## 🎬 Projekt 18: Cinephage (VOD & Cinema Library Management)

Erweiterung der bestehenden `Movie`/`Series` Modelle um automatisierte Metadaten-Anreicherung (TMDB/IMDb).
* **TMDB/IMDb Auto-Enrichment (Metadata Scraper):** Celery-Task, der nach dem Import für neue Filme ohne TMDB-ID die offizielle TMDB-API nach dem Namen (`name` + `year`) abfragt, um `description`, `rating` und hochauflösende `logo_url` zu ergänzen.
* **"Missing Episode" Tracker:** Abgleich der lokal vorhandenen Episoden einer Serie mit der TMDB-API zur Anzeige fehlender Episoden.
* **Stream-Qualitäts-Scanner (Bitrate/Resolution):** Asynchroner Task, der `ffprobe` auf die VOD-Links ansetzt, um die echte Auflösung, Video-Codec und Audio-Spuren zu speichern und als Badges in der UI darzustellen.

---

## 🔄 Projekt 19: Bidirektionale History- & Favoriten-Synchronisation

Ausbau der bestehenden Synchronisation (CompanionSyncRepository) zwischen ArgusFlix App und Manager zu einem echten Two-Way-Sync.
* **App-seitiger Sync-Push:** Die Android TV App sendet (POST/PUT via Companion-API) in Echtzeit oder regelmäßigen Abständen den Fortschritt (`progress_seconds`) eines Films/einer Serie sowie neu markierte Favoriten zurück an den Manager.
* **Manager-Endpoint Erweiterungen:** Erstellung oder Anpassung der REST-Endpoints (`/api/v1/accounts/profiles/{id}/history/update` etc.) im Backend, um eingehende Watch-History- und Favoriten-Updates zu empfangen und konfliktfrei in die Datenbank zu mergen.
* **Profil-übergreifendes Fortsetzen:** Ermöglicht es, einen Film auf dem TV im Wohnzimmer zu pausieren (der Fortschritt wird an den Manager gesendet) und nahtlos auf einem zweiten TV im Schlafzimmer fortzusetzen (da dieser den Sync-Status vom Manager lädt).

---

## 🛠️ Projekt 20: Stalker Combo/MAC Generator im Manager

Integration der Funktionalität der Standalone-Skripte (`combo_multi_gen.py`, `angina_mac_generator.py`) direkt in den ArgusFlix Manager, um Millionen von MAC-Combos auf Knopfdruck zu erstellen, zu speichern und für Portal-Scans zu nutzen.
* **Backend Combo-Engine (Django/Celery):** Ausbau von `core/stalker_mac_gen.py` (oder neues Modul `combo_gen.py`), das MAC-Listen basierend auf Prefix-Auswahl, Mengen (z.B. 2 Millionen) und Generierungs-Logik (Random, Sequentiell, Mixed) extrem schnell und arbeitsspeicherschonend generiert.
* **Combo-Datenbank & Storage:** Generierte Listen werden entweder direkt in der Datenbank (`StalkerComboList` Model) oder als persistente `.txt`-Dateien im Manager-Dateisystem gespeichert.
* **React Frontend UI (Generator & Manager):** Eine neue Seite/Tab im Manager (z.B. unter "Stalker Scanner"), auf der man über Checkboxen Prefixe auswählt, die Menge eingibt (z.B. 2.000.000) und den Generierungsprozess startet. Die fertigen Combo-Listen lassen sich dort herunterladen oder mit einem Klick direkt als Input für einen neuen "Stalker Portal Scan" (Projekt 17) verwenden.

