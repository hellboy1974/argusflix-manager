import os
import re
import time
import json
import logging
import zipfile
import urllib.request
import urllib.error
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger("plugins.dispatcharr_admin_toolbox")

class Plugin:
    name = "Dispatcharr Admin Toolbox"
    version = "1.0.0"
    description = "Die ultimative Admin-Toolbox für Dispatcharr. Vereint Stream-Checker, Senderlogo-Grabber, Logo-Cleanup, Kanalnamen-Optimierer, EPG-Healer, Kanal-Duplikate-Merger und Backup/Restore-Werkzeuge."
    author = "Antigravity"

    def run(self, action: str, params: dict, context: dict):
        settings_dict = context.get("settings", {})
        plugin_logger = context.get("logger", logger)

        if action == "check_streams":
            return self._check_streams(settings_dict, plugin_logger)
        elif action == "grab_logos":
            return self._grab_logos(settings_dict, plugin_logger)
        elif action == "cleanup_logos":
            return self._cleanup_logos(settings_dict, plugin_logger)
        elif action == "optimize_names":
            return self._optimize_names(settings_dict, plugin_logger)
        elif action == "heal_epg":
            return self._heal_epg(settings_dict, plugin_logger)
        elif action == "merge_duplicates":
            return self._merge_duplicates(settings_dict, plugin_logger)
        elif action == "backup_db":
            return self._backup_db(settings_dict, plugin_logger)
        elif action == "restore_db":
            return self._restore_db(settings_dict, plugin_logger)
        elif action == "optimize_db":
            return self._optimize_db(settings_dict, plugin_logger)
        elif action == "clear_logs":
            return self._clear_logs(settings_dict, plugin_logger)
        elif action == "check_vpn":
            return self._check_vpn(settings_dict, plugin_logger)

        return {"status": "error", "message": f"Unbekannte Aktion: {action}"}

    # ----------------------------------------------------------------------
    # Helper: Normalization for leniency
    # ----------------------------------------------------------------------
    def _normalize(self, s):
        if not s:
            return ""
        s = str(s).lower().strip()
        # Remove country codes and symbols
        s = re.sub(r"^\s*[a-z]{2,3}\s*[:|-]\s*", "", s)
        # Remove brackets/parentheses and what's inside (e.g. [HD], (US))
        s = re.sub(r"\[.*?\]|\(.*?\)", "", s)
        # Keep only lowercase alphanumerics
        return re.sub(r"[^a-z0-9]", "", s)

    # ----------------------------------------------------------------------
    # 1. ACTION: IPTV Stream Checker
    # ----------------------------------------------------------------------
    def _check_streams(self, settings_dict, plugin_logger):
        from apps.channels.models import Channel
        
        timeout = int(settings_dict.get("check_timeout", 8))
        workers = min(int(settings_dict.get("check_workers", 5)), 25)
        
        plugin_logger.info(f"Admin Toolbox: Starte Stream-Check mit {workers} Workers und Timeout={timeout}s")
        
        channels = Channel.objects.all().prefetch_related("streams")
        total_channels = channels.count()
        
        if total_channels == 0:
            return {"status": "ok", "message": "Keine Kanäle in der Datenbank vorhanden."}
            
        results = []
        alive_count = 0
        dead_count = 0
        skipped_count = 0

        def check_single_stream(ch_id, ch_name, url):
            if not url:
                return ch_id, ch_name, "Skipped (Keine URL)", None
                
            if url.startswith(('udp://', 'rtp://', 'rtsp://')):
                return ch_id, ch_name, "Alive (Non-HTTP)", 0.0

            start_time = time.time()
            try:
                req = urllib.request.Request(
                    url, 
                    headers={"User-Agent": "Mozilla/5.0 (VLC/3.0.20 LibVLC/3.0.20)"}
                )
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    latency = round((time.time() - start_time) * 1000, 2)
                    if response.status in (200, 206, 302):
                        return ch_id, ch_name, "Alive", latency
                    else:
                        return ch_id, ch_name, f"HTTP {response.status}", latency
            except urllib.error.HTTPError as e:
                latency = round((time.time() - start_time) * 1000, 2)
                return ch_id, ch_name, f"HTTP {e.code}", latency
            except urllib.error.URLError:
                return ch_id, ch_name, "Unreachable", None
            except Exception as e:
                return ch_id, ch_name, f"Error: {str(e)[:40]}", None

        to_check = []
        for ch in channels:
            first_stream = ch.streams.all().order_by("channelstream__order").first()
            if first_stream:
                to_check.append((ch.id, ch.name, first_stream.url))
            else:
                to_check.append((ch.id, ch.name, None))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(check_single_stream, cid, cname, curl): (cid, cname) 
                for cid, cname, curl in to_check
            }
            for future in as_completed(futures):
                try:
                    cid, cname, status, latency = future.result()
                    is_alive = (status == "Alive" or "Non-HTTP" in status)
                    results.append({
                        "id": cid,
                        "name": cname,
                        "status": status,
                        "latency": latency,
                        "is_alive": is_alive
                    })
                    if is_alive:
                        alive_count += 1
                    elif "Skipped" in status:
                        skipped_count += 1
                    else:
                        dead_count += 1
                except Exception as e:
                    plugin_logger.error(f"Fehler bei Streamcheck: {e}")

        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        results_file = os.path.join(data_dir, "last_stream_check.json")
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timezone.now().isoformat(),
                "summary": {"total": total_channels, "alive": alive_count, "dead": dead_count, "skipped": skipped_count},
                "results": results
            }, f, indent=2)

        return {
            "status": "ok",
            "message": f"Stream-Check beendet. Online: {alive_count} | Offline: {dead_count} | Übersprungen: {skipped_count}",
            "summary": {
                "total": total_channels,
                "alive": alive_count,
                "dead": dead_count,
                "skipped": skipped_count,
                "success_rate": f"{round((alive_count / (alive_count + dead_count) * 100), 2) if (alive_count + dead_count) > 0 else 0}%"
            }
        }

    # ----------------------------------------------------------------------
    # 2. ACTION: Logo Auto-Grabber
    # ----------------------------------------------------------------------
    def _grab_logos(self, settings_dict, plugin_logger):
        from apps.channels.models import Channel, Logo

        owner = settings_dict.get("logo_repo_owner", "jesmannstl").strip()
        repo = settings_dict.get("logo_repo_name", "tvlogos").strip()
        
        trees_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/"
        
        logos_dir = os.environ.get("DISPATCHARR_LOGOS_DIR", "/data/logos")
        os.makedirs(logos_dir, exist_ok=True)
        
        plugin_logger.info(f"Admin Toolbox: Hole Index von GitHub Repo '{owner}/{repo}'...")
        
        try:
            req = urllib.request.Request(
                trees_url, 
                headers={"User-Agent": "Dispatcharr-Admin-Toolbox-Plugin/1.0.0"}
            )
            with urllib.request.urlopen(req, timeout=20) as response:
                tree_data = json.load(response)
        except Exception as e:
            plugin_logger.error(f"Fehler beim Laden des TV-Logo-Index: {e}")
            return {"status": "error", "message": f"GitHub-Index konnte nicht geladen werden: {e}"}

        logo_index = {}
        for node in tree_data.get("tree", []):
            if node.get("type") != "blob":
                continue
            path = node.get("path", "")
            lower_path = path.lower()
            if lower_path.endswith((".png", ".svg", ".webp")):
                filename = os.path.basename(path)
                stem = os.path.splitext(filename)[0].lower()
                clean_stem = re.sub(r'[^a-z0-9]', '', stem)
                logo_index[clean_stem] = path

        plugin_logger.info(f"Admin Toolbox: Index geladen ({len(logo_index)} Logos gefunden)")

        channels = Channel.objects.filter(logo__isnull=True)
        total_missing = channels.count()
        
        if total_missing == 0:
            return {"status": "ok", "message": "Alle Kanäle haben bereits ein zugewiesenes Logo."}

        assigned_count = 0
        downloaded_count = 0
        
        for ch in channels:
            norm_name = self._normalize(ch.name)
            match_path = logo_index.get(norm_name)
            
            if not match_path:
                norm_tvg = self._normalize(ch.tvg_id)
                match_path = logo_index.get(norm_tvg)

            if match_path:
                filename = os.path.basename(match_path)
                dest_path = os.path.join(logos_dir, filename)
                url = raw_base + match_path
                
                if not os.path.exists(dest_path):
                    try:
                        d_req = urllib.request.Request(
                            url, 
                            headers={"User-Agent": "Dispatcharr-Admin-Toolbox-Plugin/1.0.0"}
                        )
                        with urllib.request.urlopen(d_req, timeout=15) as res:
                            data = res.read()
                        with open(dest_path, "wb") as f:
                            f.write(data)
                        downloaded_count += 1
                    except Exception as e:
                        plugin_logger.warning(f"Download fehlgeschlagen für {url}: {e}")
                        continue
                
                try:
                    logo_obj, created = Logo.objects.get_or_create(
                        url=dest_path,
                        defaults={"name": filename}
                    )
                    ch.logo = logo_obj
                    ch.save(update_fields=["logo"])
                    assigned_count += 1
                except Exception as e:
                    plugin_logger.error(f"Datenbankfehler beim Speichern des Logos: {e}")

        return {
            "status": "ok",
            "message": f"Zuweisung abgeschlossen. {assigned_count} Kanälen ein Logo zugewiesen ({downloaded_count} neu heruntergeladen)."
        }

    # ----------------------------------------------------------------------
    # 3. ACTION: Logo Cleanup
    # ----------------------------------------------------------------------
    def _cleanup_logos(self, settings_dict, plugin_logger):
        from apps.channels.models import Logo
        from django.db.models import Q

        delete_files = bool(settings_dict.get("delete_files", False))
        delete_vod_logos = bool(settings_dict.get("delete_vod_logos", False))
        
        plugin_logger.info(f"Admin Toolbox: Starte Logo-Cleanup (delete_files={delete_files}, delete_vod_logos={delete_vod_logos})")
        
        total_before = Logo.objects.count()
        
        if delete_vod_logos:
            unused_query = Logo.objects.filter(channels__isnull=True)
        else:
            unused_query = Logo.objects.filter(
                Q(channels__isnull=True) &
                Q(movie__isnull=True) &
                Q(series__isnull=True)
            )
            
        unused_logos = unused_query.distinct()
        unused_count = unused_logos.count()
        
        if unused_count == 0:
            return {"status": "ok", "message": "Keine ungenutzten Logos in der Datenbank gefunden."}
            
        files_deleted = 0
        if delete_files:
            for logo in unused_logos:
                if logo.url and os.path.exists(logo.url):
                    try:
                        os.remove(logo.url)
                        files_deleted += 1
                    except Exception as e:
                        plugin_logger.warning(f"Fehler beim Löschen der Datei {logo.url}: {e}")
                        
        unused_logos.delete()
        total_after = Logo.objects.count()
        
        return {
            "status": "ok",
            "message": f"Bereinigung beendet. {unused_count} Logos gelöscht (Datenbank). {files_deleted} Dateien gelöscht. Logos verbleibend: {total_after}."
        }

    # ----------------------------------------------------------------------
    # 4. ACTION: Channel Name Optimizer
    # ----------------------------------------------------------------------
    def _optimize_names(self, settings_dict, plugin_logger):
        from apps.channels.models import Channel
        
        prefixes_raw = settings_dict.get("prefixes_to_clean", "US:, DE:, UK:, FR:, CA:, US |, DE |, UK |, FR |, CA |")
        prefixes = [p.strip().lower() for p in prefixes_raw.split(",") if p.strip()]
        
        plugin_logger.info(f"Admin Toolbox: Optimiere Kanalnamen...")
        
        channels = Channel.objects.all()
        updated_count = 0
        
        for ch in channels:
            old_name = ch.name
            new_name = old_name.strip()
            
            name_lower = new_name.lower()
            for prefix in prefixes:
                if name_lower.startswith(prefix):
                    new_name = new_name[len(prefix):].strip()
                    name_lower = new_name.lower()
            
            new_name = re.sub(r'\s+', ' ', new_name)
            
            if new_name != old_name:
                ch.name = new_name
                ch.save(update_fields=["name"])
                updated_count += 1

        return {
            "status": "ok",
            "message": f"Kanalnamen bereinigt. {updated_count} von {channels.count()} Kanälen wurden optimiert."
        }

    # ----------------------------------------------------------------------
    # 5. ACTION: EPG Healer (EPG auto-matching & healing)
    # ----------------------------------------------------------------------
    def _heal_epg(self, settings_dict, plugin_logger):
        from apps.channels.models import Channel
        from apps.epg.models import EPGData, ProgramData
        
        dry_run = bool(settings_dict.get("epg_dry_run", True))
        plugin_logger.info(f"Admin Toolbox: Starte EPG-Healer (Dry Run: {dry_run})")
        
        # Query channels without EPG or with EPGs containing 0 programs
        channels = Channel.objects.all()
        healed_count = 0
        scanned_count = 0
        
        # Load all EPGData with prefetch/list to avoid database lookup spam
        all_epg = list(EPGData.objects.all())
        epg_map = {}
        for e in all_epg:
            norm_name = self._normalize(e.name)
            norm_tvg = self._normalize(e.tvg_id)
            if norm_name:
                epg_map[norm_name] = e
            if norm_tvg:
                epg_map[norm_tvg] = e
                
        plugin_logger.info(f"EPG-Healer: {len(epg_map)} EPG-Ziele im Speicher indiziert.")

        for ch in channels:
            # Check if channel has EPG that is valid (has programs)
            has_valid_epg = False
            if ch.epg_data:
                # check if programs exist for this EPG
                if ProgramData.objects.filter(epg=ch.epg_data).exists():
                    has_valid_epg = True
            
            if has_valid_epg:
                continue
                
            scanned_count += 1
            norm_ch_name = self._normalize(ch.name)
            norm_ch_tvg = self._normalize(ch.tvg_id)
            
            # Attempt to find matching EPG
            matched_epg = epg_map.get(norm_ch_name) or epg_map.get(norm_ch_tvg)
            
            if matched_epg:
                # Double check that the matched EPG actually has active program data
                if ProgramData.objects.filter(epg=matched_epg).exists():
                    healed_count += 1
                    plugin_logger.info(f"EPG-Healer Match: Kanal '{ch.name}' -> EPG '{matched_epg.name}' (tvg-id: {matched_epg.tvg_id})")
                    
                    if not dry_run:
                        ch.epg_data = matched_epg
                        ch.save(update_fields=["epg_data"])

        dry_prefix = "[Dry Run] " if dry_run else ""
        return {
            "status": "ok",
            "message": f"{dry_prefix}EPG-Heilung beendet. {healed_count} EPG-Lücken von {scanned_count} unvollständigen Kanälen geheilt."
        }

    # ----------------------------------------------------------------------
    # 6. ACTION: Kanal-Duplikate-Merger
    # ----------------------------------------------------------------------
    def _merge_duplicates(self, settings_dict, plugin_logger):
        from apps.channels.models import Channel, ChannelStream
        from django.db import transaction
        
        dry_run = bool(settings_dict.get("merger_dry_run", True))
        match_by = settings_dict.get("merger_match_by", "both")
        
        plugin_logger.info(f"Admin Toolbox: Starte Kanal-Duplikate-Merger (Dry Run: {dry_run}, Kriterium: {match_by})")
        
        channels = Channel.objects.all().prefetch_related("streams")
        
        # Group channels by their ChannelGroup
        groups = {}
        for ch in channels:
            group_id = ch.channel_group_id or 0
            if group_id not in groups:
                groups[group_id] = []
            groups[group_id].append(ch)
            
        merged_channels_count = 0
        streams_linked_count = 0
        duplicate_channels_deleted = 0
        
        for group_id, group_channels in groups.items():
            # Group by normal key inside this group
            keys = {}
            for ch in group_channels:
                norm_name = self._normalize(ch.name)
                norm_tvg = self._normalize(ch.tvg_id)
                
                # Determine identification keys
                ch_keys = []
                if match_by == "name" or match_by == "both":
                    if norm_name:
                        ch_keys.append(f"name_{norm_name}")
                if match_by == "tvg_id" or match_by == "both":
                    if norm_tvg:
                        ch_keys.append(f"tvg_{norm_tvg}")
                        
                for key in ch_keys:
                    if key not in keys:
                        keys[key] = []
                    keys[key].append(ch)
            
            # Process duplicates
            for key, dup_list in keys.items():
                # Filter out redundant list entries (ensure uniqueness of channel objects in the list)
                unique_dups = list(dict.fromkeys(dup_list))
                if len(unique_dups) <= 1:
                    continue
                    
                # We have duplicates! Sort them so the best channel to keep is first.
                # Keep channel with lowest channel_number, or earliest created
                unique_dups.sort(key=lambda x: (x.channel_number or 999999, x.id))
                primary_channel = unique_dups[0]
                duplicate_channels = unique_dups[1:]
                
                plugin_logger.info(f"Merger: Behalte Kanal '{primary_channel.name}' (ID: {primary_channel.id})")
                
                primary_stream_ids = set(primary_channel.streams.values_list("id", flat=True))
                
                with transaction.atomic():
                    for dup_ch in duplicate_channels:
                        plugin_logger.info(f"Merger: Verschmelze Duplikat-Kanal '{dup_ch.name}' (ID: {dup_ch.id})")
                        
                        # Move all streams from duplicate to primary channel
                        dup_streams = list(dup_ch.streams.all())
                        for stream in dup_streams:
                            if stream.id not in primary_stream_ids:
                                streams_linked_count += 1
                                primary_stream_ids.add(stream.id)
                                
                                if not dry_run:
                                    # Link to primary channel
                                    next_order = ChannelStream.objects.filter(channel=primary_channel).count()
                                    ChannelStream.objects.create(
                                        channel=primary_channel,
                                        stream=stream,
                                        order=next_order
                                    )
                                    plugin_logger.info(f"   -> Stream '{stream.name}' an primären Kanal angehängt.")
                                    
                        if not dry_run:
                            # Delete duplicate channel
                            dup_ch.delete()
                            duplicate_channels_deleted += 1
                            
                        merged_channels_count += 1

        dry_prefix = "[Dry Run] " if dry_run else ""
        return {
            "status": "ok",
            "message": f"{dry_prefix}Zusammenführung beendet. {merged_channels_count} Duplikat-Kanäle verschmolzen, {streams_linked_count} Backup-Streams verknüpft, {duplicate_channels_deleted} Kanäle gelöscht."
        }

    # ----------------------------------------------------------------------
    # 7. ACTION: Schnell-Backup
    # ----------------------------------------------------------------------
    def _backup_db(self, settings_dict, plugin_logger):
        base_dir = Path(settings.BASE_DIR)
        db_file = base_dir / "dispatcharr.db"
        
        if not db_file.exists():
            return {"status": "error", "message": "SQLite-Datenbank 'dispatcharr.db' wurde unter BASE_DIR nicht gefunden."}
            
        backup_dir = base_dir / "data" / "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        zip_name = f"dispatcharr_backup_{timestamp}.zip"
        zip_path = backup_dir / zip_name
        
        plugin_logger.info(f"Admin Toolbox: Erstelle Schnell-Backup '{zip_name}'...")
        
        try:
            # We copy the db to a temp file first to prevent locking issues, then compress
            temp_db = backup_dir / f"dispatcharr_{timestamp}.db.tmp"
            shutil.copy2(db_file, temp_db)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_db, arcname="dispatcharr.db")
                # Also backup .env if exists
                env_file = base_dir / ".env"
                if env_file.exists():
                    zipf.write(env_file, arcname=".env")
                    
            os.remove(temp_db)
            plugin_logger.info(f"Admin Toolbox: Backup erfolgreich erstellt: {zip_path}")
        except Exception as e:
            plugin_logger.error(f"Backup fehlgeschlagen: {e}")
            return {"status": "error", "message": f"Backup fehlgeschlagen: {e}"}

        return {
            "status": "ok",
            "message": f"Backup erfolgreich erstellt: {zip_name}"
        }

    # ----------------------------------------------------------------------
    # 8. ACTION: Schnell-Restore
    # ----------------------------------------------------------------------
    def _restore_db(self, settings_dict, plugin_logger):
        backup_name = settings_dict.get("backup_restore_name", "").strip()
        if not backup_name:
            return {"status": "error", "message": "Bitte geben Sie unter 'Wiederherstellungs-Datei (Dateiname)' den exakten Backup-Dateinamen an."}
            
        base_dir = Path(settings.BASE_DIR)
        backup_file = base_dir / "data" / "backups" / backup_name
        
        if not backup_file.exists():
            return {"status": "error", "message": f"Backup-Datei '{backup_name}' unter data/backups/ nicht gefunden."}
            
        plugin_logger.info(f"Admin Toolbox: Wiederherstellen von Backup '{backup_name}'...")
        
        db_file = base_dir / "dispatcharr.db"
        
        try:
            # Close django database connection to free locks
            from django.db import connection
            connection.close()
            
            # Extract database from zip file
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                # Extract to a temp file, then atomically replace
                temp_db = base_dir / "data" / "backups" / "restore_db.tmp"
                with open(temp_db, "wb") as f:
                    f.write(zipf.read("dispatcharr.db"))
                
                # Replace the active database
                os.replace(temp_db, db_file)
                plugin_logger.info("Admin Toolbox: SQLite-Datenbank erfolgreich wiederhergestellt.")
        except Exception as e:
            plugin_logger.error(f"Wiederherstellung fehlgeschlagen: {e}")
            return {"status": "error", "message": f"Wiederherstellung fehlgeschlagen: {e}"}

        return {
            "status": "ok",
            "message": f"Backup '{backup_name}' wurde erfolgreich wiederhergestellt! Bitte starten Sie das Backend neu, um die Änderungen zu laden."
        }

    # ----------------------------------------------------------------------
    # 9. ACTION: Datenbank Optimieren (VACUUM)
    # ----------------------------------------------------------------------
    def _optimize_db(self, settings_dict, plugin_logger):
        from django.db import connection
        try:
            base_dir = Path(settings.BASE_DIR)
            db_file = base_dir / "dispatcharr.db"
            size_before = 0
            if db_file.exists():
                size_before = os.path.getsize(db_file)
                
            cursor = connection.cursor()
            plugin_logger.info("Admin Toolbox: Führe VACUUM auf SQLite Datenbank aus...")
            cursor.execute("VACUUM")
            
            size_after = 0
            if db_file.exists():
                size_after = os.path.getsize(db_file)
                
            saved_mb = max(0, (size_before - size_after) / (1024 * 1024))
            
            return {
                "status": "ok",
                "message": f"Datenbank erfolgreich optimiert. Eingesparter Speicherplatz: {saved_mb:.2f} MB."
            }
        except Exception as e:
            plugin_logger.error(f"Fehler bei VACUUM: {e}")
            return {"status": "error", "message": f"Datenbank-Optimierung fehlgeschlagen: {e}"}

    # ----------------------------------------------------------------------
    # 10. ACTION: Alte Logs bereinigen
    # ----------------------------------------------------------------------
    def _clear_logs(self, settings_dict, plugin_logger):
        import time
        from pathlib import Path
        
        base_dir = Path(settings.BASE_DIR)
        logs_dir = base_dir / "data" / "logs"
        
        if not logs_dir.exists():
            return {"status": "ok", "message": "Kein Logs-Ordner gefunden, nichts zu löschen."}
            
        now = time.time()
        # 7 days = 604800 seconds
        cutoff = now - 604800
        deleted_count = 0
        freed_bytes = 0
        
        try:
            for f in logs_dir.glob("*.log*"):
                if f.is_file():
                    if f.stat().st_mtime < cutoff:
                        freed_bytes += f.stat().st_size
                        f.unlink()
                        deleted_count += 1
                        
            freed_mb = freed_bytes / (1024 * 1024)
            plugin_logger.info(f"Admin Toolbox: {deleted_count} alte Log-Dateien gelöscht ({freed_mb:.2f} MB freigegeben).")
            return {
                "status": "ok",
                "message": f"Logs bereinigt. {deleted_count} Dateien entfernt ({freed_mb:.2f} MB freigegeben)."
            }
        except Exception as e:
            plugin_logger.error(f"Fehler beim Bereinigen der Logs: {e}")
            return {"status": "error", "message": f"Fehler beim Löschen der Logs: {e}"}

    # ----------------------------------------------------------------------
    # 11. ACTION: VPN-Verbindung prüfen
    # ----------------------------------------------------------------------
    def _check_vpn(self, settings_dict, plugin_logger):
        import urllib.request
        import json
        try:
            req = urllib.request.Request(
                "http://ip-api.com/json/", 
                headers={"User-Agent": "Dispatcharr-Admin-Toolbox-Plugin/1.0.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data.get("status") == "success":
                    ip = data.get("query")
                    country = data.get("country")
                    isp = data.get("isp")
                    return {
                        "status": "ok",
                        "vpn_active": True,
                        "ip": ip,
                        "country": country,
                        "isp": isp,
                        "message": f"Verbindung aktiv (IP: {ip}, Land: {country})"
                    }
                else:
                    raise Exception("Invalid response from ip-api")
        except Exception as e:
            plugin_logger.warning(f"Admin Toolbox VPN-Check fehlgeschlagen: {e}")
            return {
                "status": "ok",
                "vpn_active": False,
                "message": "Verbindung fehlgeschlagen (VPN Tunnel down oder Offline)"
            }
