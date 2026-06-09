import logging
import os
import requests
from django.utils import timezone
from django.db import transaction

# Setup logging
logger = logging.getLogger("xtream_toolbox")

# Disable warnings for insecure SSL requests (helpful for local test/flaky cert panels)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class Plugin:
    name = "Xtream Toolbox"
    version = "1.0.0"
    description = "Manage, test, and import Xtream Codes IPTV panels into ArgusFlix."
    has_ui = True
    icon = "Wrench"
    admin_only = True

    def run(self, action_id, params, context):
        if action_id == "get_panels":
            return self.get_panels()
        elif action_id == "test_connection":
            return self.test_connection(params)
        elif action_id == "import_panel":
            return self.import_panel(params)
        elif action_id == "delete_panel":
            return self.delete_panel(params)
        elif action_id == "refresh_panel":
            return self.refresh_panel(params)
        else:
            raise ValueError(f"Unknown action: {action_id}")

    def stop(self, context=None):
        pass

    def get_panels(self):
        from apps.m3u.models import M3UAccount
        
        panels = []
        try:
            # Fetch all accounts of type XC (Xtream Codes)
            accounts = M3UAccount.objects.filter(account_type=M3UAccount.Types.XC).prefetch_related("profiles")
            for acc in accounts:
                profile = acc.profiles.filter(is_default=True).first()
                
                exp_date_str = None
                max_connections = None
                active_connections = None
                account_status = None
                
                if profile:
                    exp_date = profile.get_account_expiration()
                    if exp_date:
                        # Convert datetime to string or check if it's unlimited
                        exp_date_str = exp_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(exp_date, "strftime") else str(exp_date)
                    
                    max_connections = profile.get_max_connections()
                    active_connections = profile.get_active_connections()
                    account_status = profile.get_account_status()

                panels.append({
                    "id": acc.id,
                    "name": acc.name,
                    "server_url": acc.server_url,
                    "username": acc.username,
                    "is_active": acc.is_active,
                    "status": acc.status,
                    "last_message": acc.last_message,
                    "exp_date": exp_date_str,
                    "max_connections": max_connections,
                    "active_connections": active_connections,
                    "account_status": account_status,
                    "refresh_interval": acc.refresh_interval,
                    "updated_at": acc.updated_at.strftime("%Y-%m-%d %H:%M:%S") if acc.updated_at else None
                })
            return {"status": "ok", "panels": panels}
        except Exception as e:
            logger.exception("Failed to retrieve Xtream Codes panels")
            return {"status": "error", "message": f"Failed to retrieve panels: {str(e)}"}

    def test_connection(self, params):
        server_url = params.get("server_url", "").strip().rstrip("/")
        username = params.get("username", "").strip()
        password = params.get("password", "").strip()

        if not server_url or not username or not password:
            return {"status": "error", "message": "Server URL, Username, and Password are required."}

        # Normalize server_url
        if not server_url.startswith(("http://", "https://")):
            server_url = f"http://{server_url}"

        test_url = f"{server_url}/player_api.php?username={username}&password={password}"
        logger.info(f"Testing connection to Xtream Codes server: {server_url} with user '{username}'")

        try:
            response = requests.get(test_url, timeout=10, verify=False)
            if response.status_code != 200:
                return {
                    "status": "error", 
                    "message": f"Server returned status code {response.status_code}. Make sure player_api.php endpoint is accessible."
                }

            data = response.json()
            user_info = data.get("user_info", {})
            auth = user_info.get("auth")
            
            # Note: auth might be 1 (success) or 0 (failed). In some older panels, it might be a boolean.
            if auth != 1 and auth != True and str(auth) != "1":
                return {
                    "status": "error",
                    "message": "Authentication failed. Please verify your Username and Password."
                }

            # If authenticated successfully, parse details
            status = user_info.get("status", "Unknown")
            max_connections = user_info.get("max_connections", "0")
            active_cons = user_info.get("active_cons", "0")
            
            # Parse exp_date
            exp_date_raw = user_info.get("exp_date")
            exp_date_formatted = "Unlimited"
            if exp_date_raw:
                try:
                    import datetime
                    ts = float(exp_date_raw)
                    # Some systems return exp_date = 0 or null for unlimited
                    if ts > 0:
                        exp_date_formatted = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        exp_date_formatted = "Unlimited"
                except Exception:
                    exp_date_formatted = str(exp_date_raw)

            server_info = data.get("server_info", {})
            server_timezone = server_info.get("timezone", "UTC")

            return {
                "status": "ok",
                "message": "Connection tested successfully!",
                "details": {
                    "account_status": status,
                    "max_connections": max_connections,
                    "active_connections": active_cons,
                    "exp_date": exp_date_formatted,
                    "timezone": server_timezone
                }
            }
        except requests.RequestException as e:
            logger.warning(f"Connection test failed: {e}")
            return {"status": "error", "message": f"Connection failed: {str(e)}"}
        except ValueError:
            logger.warning("Connection test returned invalid JSON response")
            return {
                "status": "error", 
                "message": "Successfully reached the server, but it did not return a valid Xtream Codes JSON response. Verify the URL."
            }

    def import_panel(self, params):
        from apps.m3u.models import M3UAccount
        from apps.m3u.tasks import refresh_m3u_groups
        
        name = params.get("name", "").strip()
        server_url = params.get("server_url", "").strip().rstrip("/")
        username = params.get("username", "").strip()
        password = params.get("password", "").strip()
        enable_vod = bool(params.get("enable_vod", False))
        enable_series = bool(params.get("enable_series", False))
        refresh_interval = params.get("refresh_interval", 3600)

        if not name or not server_url or not username or not password:
            return {"status": "error", "message": "All fields (Name, Server URL, Username, Password) are required."}

        # Normalize server_url
        if not server_url.startswith(("http://", "https://")):
            server_url = f"http://{server_url}"

        # Ensure name uniqueness
        if M3UAccount.objects.filter(name=name).exists():
            return {"status": "error", "message": f"An IPTV source named '{name}' already exists."}

        try:
            with transaction.atomic():
                account = M3UAccount.objects.create(
                    name=name,
                    server_url=server_url,
                    account_type=M3UAccount.Types.XC,
                    username=username,
                    password=password,
                    is_active=True,
                    refresh_interval=int(refresh_interval) if refresh_interval else 0,
                    custom_properties={
                        "enable_vod": enable_vod,
                        "enable_series": enable_series,
                        "auto_enable_new_groups_vod": True
                    }
                )
            
            logger.info(f"IPTV Panel '{name}' imported successfully. Triggering background tasks...")
            
            # 1. Trigger background task to fetch groups and channels
            refresh_m3u_groups.delay(account.id)
            
            # 2. Trigger VOD sync if enabled
            if enable_vod:
                try:
                    from apps.vod.tasks import refresh_categories
                    refresh_categories.delay(account.id)
                except ImportError:
                    pass

            return {
                "status": "ok",
                "message": f"IPTV Panel '{name}' was imported successfully! Syncing has been started in the background.",
                "id": account.id
            }
        except Exception as e:
            logger.exception("Failed to import IPTV panel")
            return {"status": "error", "message": f"Failed to import panel: {str(e)}"}

    def delete_panel(self, params):
        from apps.m3u.models import M3UAccount
        from apps.channels.models import Channel
        from apps.proxy.live_proxy.services.channel_service import ChannelService
        
        account_id = params.get("id")
        if not account_id:
            return {"status": "error", "message": "Missing panel ID."}

        try:
            account = M3UAccount.objects.get(id=account_id)
            if account.locked:
                return {"status": "error", "message": "This account is protected and cannot be deleted."}

            logger.info(f"Deleting IPTV Panel '{account.name}'...")

            # Replicate standard deletion cleanup cascade
            channels_to_delete = list(
                Channel.objects.filter(
                    auto_created=True,
                    auto_created_by=account,
                ).values_list("id", "uuid")
            )
            
            # Stop proxy sessions for these channels
            for _, channel_uuid in channels_to_delete:
                if not channel_uuid:
                    continue
                try:
                    ChannelService.stop_channel(str(channel_uuid))
                except Exception as e:
                    logger.warning(f"Failed to stop proxy session for channel {channel_uuid}: {e}")

            channel_ids = [cid for cid, _ in channels_to_delete]
            
            # Atomic deletion of channels and M3UAccount
            with transaction.atomic():
                if channel_ids:
                    Channel.objects.filter(id__in=channel_ids).delete()
                account.delete()

            return {
                "status": "ok",
                "message": f"IPTV Panel '{account.name}' and all associated channels were successfully deleted."
            }
        except M3UAccount.DoesNotExist:
            return {"status": "error", "message": "Panel not found."}
        except Exception as e:
            logger.exception("Failed to delete IPTV panel")
            return {"status": "error", "message": f"Failed to delete panel: {str(e)}"}

    def refresh_panel(self, params):
        from apps.m3u.models import M3UAccount
        from apps.m3u.tasks import refresh_single_m3u_account
        
        account_id = params.get("id")
        if not account_id:
            return {"status": "error", "message": "Missing panel ID."}

        try:
            account = M3UAccount.objects.get(id=account_id)
            if not account.is_active:
                return {"status": "error", "message": "Cannot refresh a deactivated source."}

            # Trigger background celery task
            refresh_single_m3u_account.delay(account.id)
            
            return {
                "status": "ok",
                "message": f"Refresh initiated for panel '{account.name}'. Sync runs in the background."
            }
        except M3UAccount.DoesNotExist:
            return {"status": "error", "message": "Panel not found."}
        except Exception as e:
            logger.exception("Failed to trigger refresh task")
            return {"status": "error", "message": f"Failed to trigger refresh: {str(e)}"}
