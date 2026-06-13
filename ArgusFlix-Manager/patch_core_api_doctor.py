import re

with open("core/api_views.py", "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """
@api_view(['GET'])
@permission_classes([IsAdminUser])
def proxy_doctor_scan(request):
    try:
        from core.utils import RedisClient
        import json
        import time
        rc = RedisClient()
        keys = rc.keys("stream:connection:*")
        zombies = []
        now = time.time()
        
        for key in keys:
            data = rc.get(key)
            if data:
                try:
                    conn = json.loads(data)
                    start_time = conn.get("start_time", now)
                    last_read = conn.get("last_read", start_time)
                    
                    # If last read was more than 60 seconds ago and it's been running for more than 2 minutes, it's a zombie
                    if (now - start_time) > 120 and (now - last_read) > 60:
                        zombies.append(conn)
                except Exception:
                    pass
        return Response({"zombies": zombies, "count": len(zombies)})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def proxy_doctor_clean(request):
    try:
        from core.utils import RedisClient
        import json
        import time
        rc = RedisClient()
        keys = rc.keys("stream:connection:*")
        cleaned = 0
        now = time.time()
        
        for key in keys:
            data = rc.get(key)
            if data:
                try:
                    conn = json.loads(data)
                    start_time = conn.get("start_time", now)
                    last_read = conn.get("last_read", start_time)
                    
                    if (now - start_time) > 120 and (now - last_read) > 60:
                        client_id = conn.get('client_id')
                        if client_id:
                            rc.set(f"stream:stop:{client_id}", "true", 300)
                        rc.delete(key)
                        cleaned += 1
                except Exception:
                    pass
        return Response({"success": True, "cleaned_count": cleaned})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
"""

content = content + new_endpoints

with open("core/api_views.py", "w", encoding="utf-8") as f:
    f.write(content)


with open("core/api_urls.py", "r", encoding="utf-8") as f:
    content_urls = f.read()

import_orig = "clear_system_cache"
import_new = "clear_system_cache,\n    proxy_doctor_scan,\n    proxy_doctor_clean"
content_urls = content_urls.replace(import_orig, import_new)

url_orig = "path('admin/cache/clear/', clear_system_cache, name='admin-cache-clear'),"
url_new = "path('admin/cache/clear/', clear_system_cache, name='admin-cache-clear'),\n    path('admin/doctor/scan/', proxy_doctor_scan, name='admin-doctor-scan'),\n    path('admin/doctor/clean/', proxy_doctor_clean, name='admin-doctor-clean'),"
content_urls = content_urls.replace(url_orig, url_new)

with open("core/api_urls.py", "w", encoding="utf-8") as f:
    f.write(content_urls)

print("Patched core API for Proxy Doctor!")
