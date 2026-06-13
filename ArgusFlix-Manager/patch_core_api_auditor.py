import re

with open("core/api_views.py", "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def provider_audit_endpoint(request):
    from core.utils import RedisClient
    import json
    rc = RedisClient()
    
    if request.method == 'POST':
        # Trigger the audit task
        from core.tasks import run_provider_audit
        run_provider_audit.delay()
        return Response({"message": "Provider audit started in background."})
        
    elif request.method == 'GET':
        # Fetch latest results
        data = rc.get("provider_audit_results")
        if data:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            try:
                results = json.loads(data)
                return Response(results)
            except Exception:
                pass
        return Response([])
"""

content = content + new_endpoints

with open("core/api_views.py", "w", encoding="utf-8") as f:
    f.write(content)


with open("core/api_urls.py", "r", encoding="utf-8") as f:
    content_urls = f.read()

import_orig = "get_vpn_status"
import_new = "get_vpn_status,\n    provider_audit_endpoint"
content_urls = content_urls.replace(import_orig, import_new)

url_orig = "path('admin/vpn-status/', get_vpn_status, name='admin-vpn-status'),"
url_new = "path('admin/vpn-status/', get_vpn_status, name='admin-vpn-status'),\n    path('admin/audit/', provider_audit_endpoint, name='admin-audit'),"
content_urls = content_urls.replace(url_orig, url_new)

with open("core/api_urls.py", "w", encoding="utf-8") as f:
    f.write(content_urls)

print("Patched core API for Provider Auditor!")
