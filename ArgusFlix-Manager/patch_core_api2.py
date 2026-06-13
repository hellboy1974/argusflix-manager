import re

with open("core/api_views.py", "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_vpn_status(request):
    try:
        from core.utils import RedisClient
        rc = RedisClient()
        status = rc.get("vpn_guard:status")
        if isinstance(status, bytes):
            status = status.decode('utf-8')
        return Response({"status": status or "unknown"})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
"""

content = content + new_endpoints

with open("core/api_views.py", "w", encoding="utf-8") as f:
    f.write(content)

with open("core/api_urls.py", "r", encoding="utf-8") as f:
    content_urls = f.read()

import_orig = "kill_active_connection"
import_new = "kill_active_connection,\n    get_vpn_status"
content_urls = content_urls.replace(import_orig, import_new)

url_orig = "path('admin/connections/<str:client_id>/kill/', kill_active_connection, name='admin-kill-connection'),"
url_new = "path('admin/connections/<str:client_id>/kill/', kill_active_connection, name='admin-kill-connection'),\n    path('admin/vpn-status/', get_vpn_status, name='admin-vpn-status'),"
content_urls = content_urls.replace(url_orig, url_new)

with open("core/api_urls.py", "w", encoding="utf-8") as f:
    f.write(content_urls)

print("Patched core API for VPN status!")
