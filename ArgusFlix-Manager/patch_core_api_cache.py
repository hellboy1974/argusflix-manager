import re

with open("core/api_views.py", "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """
@api_view(['POST'])
@permission_classes([IsAdminUser])
def clear_system_cache(request):
    try:
        from django.core.cache import cache
        from core.utils import RedisClient
        
        # Clear Django default cache
        cache.clear()
        
        # Clear Redis cache keys
        rc = RedisClient()
        cache_keys = rc.keys("*cache*")
        for key in cache_keys:
            rc.delete(key)
            
        return Response({"success": True, "message": "System cache cleared successfully."})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
"""

content = content + new_endpoints

with open("core/api_views.py", "w", encoding="utf-8") as f:
    f.write(content)


with open("core/api_urls.py", "r", encoding="utf-8") as f:
    content_urls = f.read()

import_orig = "provider_audit_endpoint"
import_new = "provider_audit_endpoint,\n    clear_system_cache"
content_urls = content_urls.replace(import_orig, import_new)

url_orig = "path('admin/audit/', provider_audit_endpoint, name='admin-audit'),"
url_new = "path('admin/audit/', provider_audit_endpoint, name='admin-audit'),\n    path('admin/cache/clear/', clear_system_cache, name='admin-cache-clear'),"
content_urls = content_urls.replace(url_orig, url_new)

with open("core/api_urls.py", "w", encoding="utf-8") as f:
    f.write(content_urls)

print("Patched core API for Cache Buster!")
