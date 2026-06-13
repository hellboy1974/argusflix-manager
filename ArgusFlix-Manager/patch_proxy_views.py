import re

# 1. Patch live proxy
with open("apps/proxy/live_proxy/views.py", "r", encoding="utf-8") as f:
    content = f.read()

live_stream_orig = """def stream_ts(request, channel_id, user=None, force_output_format=None):
    if not network_access_allowed(request, "STREAMS"):
        return JsonResponse({"error": "Forbidden"}, status=403)"""
live_stream_new = """def stream_ts(request, channel_id, user=None, force_output_format=None):
    from core.utils import RedisClient
    rc = RedisClient()
    if rc.get("vpn_guard:status") == b"down" or rc.get("vpn_guard:status") == "down":
        return JsonResponse({"error": "Service Unavailable (VPN Guard)"}, status=503)

    if not network_access_allowed(request, "STREAMS"):
        return JsonResponse({"error": "Forbidden"}, status=403)"""
content = content.replace(live_stream_orig, live_stream_new)

with open("apps/proxy/live_proxy/views.py", "w", encoding="utf-8") as f:
    f.write(content)

# 2. Patch VOD proxy
with open("apps/proxy/vod_proxy/views.py", "r", encoding="utf-8") as f:
    content = f.read()

vod_stream_orig = """def stream(request, media_type, media_id, user=None):
    from apps.vod.models import Movie, Episode
    from argusflix_manager.utils import network_access_allowed"""
vod_stream_new = """def stream(request, media_type, media_id, user=None):
    from core.utils import RedisClient
    rc = RedisClient()
    if rc.get("vpn_guard:status") == b"down" or rc.get("vpn_guard:status") == "down":
        from django.http import JsonResponse
        return JsonResponse({"error": "Service Unavailable (VPN Guard)"}, status=503)

    from apps.vod.models import Movie, Episode
    from argusflix_manager.utils import network_access_allowed"""
content = content.replace(vod_stream_orig, vod_stream_new)

with open("apps/proxy/vod_proxy/views.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched proxy views!")
