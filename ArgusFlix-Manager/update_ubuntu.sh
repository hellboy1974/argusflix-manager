#!/bin/bash

# ==============================================================================
# ArgusFlix Manager - Update Script für Ubuntu Server
# ==============================================================================
# Dieses Script aktualisiert eine laufende Installation auf dem Server.
# Es holt sich die neuesten Änderungen des Original-Entwicklers (Dispatcharr),
# verschmilzt diese sicher mit euren Anpassungen (Git Merge), aktualisiert
# Abhängigkeiten, führt Datenbank-Migrationen durch und startet den Service neu.
# ==============================================================================

# --- KONFIGURATION (Bitte an euren Server anpassen) ---
PROJECT_DIR="/opt/ArgusFlix-Manager"                     # Der Pfad zur Installation auf dem Server
UPSTREAM_REPO="https://github.com/Start-Automating/Dispatcharr.git"
UPSTREAM_BRANCH="main"                                   # Haupt-Branch des Entwicklers
VENV_DIR="venv"                                          # Name des Virtual Environments im Projektordner
SERVICE_NAME="argusflix.service"                         # Name des Systemd-Dienstes (falls nativ)
# ------------------------------------------------------

# 1. Root-Rechte prüfen
if [ "$EUID" -ne 0 ]; then
  echo "⚠️ Bitte führe dieses Script mit sudo aus (z.B. sudo ./update_ubuntu.sh)"
  exit 1
fi

echo "🚀 Starte Update für ArgusFlix Manager..."

# 2. In das Projektverzeichnis wechseln
cd "$PROJECT_DIR" || { echo "❌ Fehler: Projektverzeichnis $PROJECT_DIR nicht gefunden."; exit 1; }

# 3. Upstream Remote prüfen und ggf. hinzufügen
if ! git remote -v | grep -q "upstream"; then
    echo "🔗 Füge Upstream-Repository hinzu..."
    git remote add upstream "$UPSTREAM_REPO"
fi

# 4. Ungespeicherte Änderungen sichern
if ! git diff-index --quiet HEAD --; then
    echo "💾 Sichere ungespeicherte lokale Änderungen..."
    git add .
    git commit -m "Auto-Commit: Lokale Server-Änderungen vor Update"
fi

# 5. Git Merge (Updates des Entwicklers reinziehen)
echo "📥 Lade Updates vom Original-Entwickler herunter..."
git fetch upstream

echo "🔀 Führe Änderungen zusammen..."
git merge "upstream/$UPSTREAM_BRANCH" --no-edit

if [ $? -ne 0 ]; then
    echo "❌ ACHTUNG: Es gab Merge-Konflikte!"
    echo "Das Update wurde pausiert. Bitte die Konflikte manuell auflösen,"
    echo "danach committen und dieses Script erneut ausführen."
    exit 1
fi

# 6. Prüfen ob Docker oder Native Installation
if [ -f "docker-compose.yml" ]; then
    echo "🐳 Docker-Installation erkannt. Baue und starte Container neu..."
    docker compose build
    docker compose up -d
else
    echo "💻 Native Installation erkannt."
    echo "🐍 Aktiviere Virtual Environment..."
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    else
        echo "⚠️ Virtual Environment nicht gefunden, überspringe pip install."
    fi

    echo "📦 Aktualisiere Python-Abhängigkeiten..."
    pip install -r requirements.txt || true

    echo "🗄️ Führe Datenbank-Migrationen durch..."
    python manage.py migrate || true

    echo "🎨 Aktualisiere statische Dateien..."
    python manage.py collectstatic --noinput || true

    echo "🔄 Starte ArgusFlix-Service neu..."
    systemctl restart "$SERVICE_NAME" || echo "⚠️ Service konnte nicht neugestartet werden. Bitte manuell prüfen."
fi

echo "✅ Update erfolgreich abgeschlossen! ArgusFlix Manager ist nun auf dem neuesten Stand."
