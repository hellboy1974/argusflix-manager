import re
import sys

with open("apps/output/views.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update xc_get_user
xc_get_user_orig = """def xc_get_user(request):
    username = request.GET.get("username")
    password = request.GET.get("password")

    if not username or not password:
        return None

    user = get_object_or_404(User, username=username)"""

xc_get_user_new = """from apps.output.models import CustomPlaylist

def xc_get_user(request):
    username = request.GET.get("username")
    password = request.GET.get("password")

    if not username or not password:
        return None

    # Check for CustomPlaylist first
    try:
        playlist = CustomPlaylist.objects.get(token=username, is_active=True)
        if password == "custom":
            return playlist
    except CustomPlaylist.DoesNotExist:
        pass

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None"""
content = content.replace(xc_get_user_orig, xc_get_user_new)

# 2. Update network_access_allowed calls for CustomPlaylist
network_access_orig = """    if not network_access_allowed(request, 'XC_API', user):
        return None"""
network_access_new = """    if isinstance(user, User):
        if not network_access_allowed(request, 'XC_API', user):
            return None
    else:
        # CustomPlaylist has no user-specific restrictions for now, but we check global IP bans
        if not network_access_allowed(request, 'XC_API'):
            return None"""
content = content.replace(network_access_orig, network_access_new)

with open("apps/output/views.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched xc_get_user!")
