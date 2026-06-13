import re

with open("core/tasks.py", "r", encoding="utf-8") as f:
    content = f.read()

audit_task = """
@shared_task(bind=True)
def run_provider_audit(self):
    import requests
    import time
    import json
    from core.utils import RedisClient
    from apps.m3u.models import M3UAccount
    
    rc = RedisClient()
    results = []
    
    # Audit M3U Accounts
    accounts = M3UAccount.objects.filter(enabled=True)
    for acc in accounts:
        result = {
            "id": f"m3u_{acc.id}",
            "name": acc.name,
            "type": "M3U / XC",
            "latency_ms": -1,
            "status": "Error",
            "last_checked": time.time()
        }
        
        # Determine the base URL to check
        url_to_check = acc.url
        if acc.username and acc.password:
            # It's XC
            if not url_to_check.endswith('/'):
                url_to_check += '/'
            url_to_check += f"player_api.php?username={acc.username}&password={acc.password}"
            
        try:
            start_time = time.time()
            resp = requests.head(url_to_check, timeout=10, allow_redirects=True)
            if resp.status_code == 405:
                # Fallback to GET if HEAD is not allowed
                resp = requests.get(url_to_check, timeout=10, stream=True)
                resp.close()
            
            end_time = time.time()
            latency = int((end_time - start_time) * 1000)
            
            result["latency_ms"] = latency
            if resp.status_code < 400:
                result["status"] = "OK"
            else:
                result["status"] = f"HTTP {resp.status_code}"
        except Exception as e:
            result["status"] = str(e)[:30]
            
        results.append(result)
        
    rc.set("provider_audit_results", json.dumps(results))
    return f"Audited {len(results)} providers."
"""

content = content + audit_task

with open("core/tasks.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched core/tasks.py with provider auditor!")
