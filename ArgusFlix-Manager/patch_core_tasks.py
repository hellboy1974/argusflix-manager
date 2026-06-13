import re

with open("core/tasks.py", "r", encoding="utf-8") as f:
    content = f.read()

vpn_task = """
@shared_task(bind=True)
def check_vpn_guard(self):
    from core.models import CoreSettings
    from core.utils import RedisClient
    import requests
    
    rc = RedisClient()
    settings = CoreSettings.get_settings()
    vpn_settings = settings.get('vpn_guard', {})
    
    if not vpn_settings.get('enabled', False):
        rc.delete('vpn_guard:status')
        return "VPN Guard disabled"
        
    gluetun_url = vpn_settings.get('gluetun_url', 'http://gluetun:8000')
    if not gluetun_url:
        return "No Gluetun URL configured"
        
    try:
        # Check Gluetun status API
        resp = requests.get(f"{gluetun_url}/v1/openvpn/status", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        
        status = data.get('status')
        if status in ['running', 'connected']:
            rc.set('vpn_guard:status', 'up', 60)
            return "VPN UP"
        else:
            rc.set('vpn_guard:status', 'down', 60)
            _kill_all_streams()
            return f"VPN DOWN ({status})"
            
    except Exception as e:
        logger.error(f"VPN Guard check failed: {e}")
        rc.set('vpn_guard:status', 'down', 60)
        _kill_all_streams()
        return "VPN DOWN (Error)"

def _kill_all_streams():
    from core.utils import RedisClient
    rc = RedisClient()
    keys = rc.keys("stream:connection:*")
    for key in keys:
        try:
            import json
            data = rc.get(key)
            if data:
                conn = json.loads(data)
                client_id = conn.get('client_id')
                if client_id:
                    rc.set(f"stream:stop:{client_id}", "true", 300)
                    rc.delete(key)
        except Exception:
            pass
"""

content = content + vpn_task

with open("core/tasks.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched core/tasks.py!")
