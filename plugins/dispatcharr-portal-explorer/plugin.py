import os
import re
import json
import logging
import threading
import random
from django.conf import settings
from django.urls import path, get_resolver
from django.http import JsonResponse, HttpResponse
from django.db import transaction

# Core Django models
from apps.m3u.models import M3UAccount
from apps.channels.models import Channel, ChannelGroup, Stream, ChannelStream

logger = logging.getLogger("plugins.portal_explorer")

# ----------------------------------------------------------------------
# DYNAMIC URL REGISTRATION VIEWS & INJECTION
# ----------------------------------------------------------------------

def portal_explorer_index_view(request):
    """Serves the single-page HTML frontend from the plugin folder"""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "portal_explorer", "index.html")
    if os.path.exists(template_path):
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
            return HttpResponse(content, content_type="text/html")
        except Exception as e:
            return HttpResponse(f"Error reading template: {e}", status=500)
    return HttpResponse("Portal Explorer UI Template not found", status=404)


def portal_explorer_tree_api(request):
    """Builds a hierarchical tree-structure of imported M3UAccounts, categories and streams"""
    try:
        accounts = M3UAccount.objects.all()
        tree = []
        
        for acc in accounts:
            # Fetch all streams linked to this account
            streams = Stream.objects.filter(m3u_account=acc).select_related("channel_group")
            
            # Group streams by category/ChannelGroup
            categories_map = {}
            for stream in streams:
                cat_name = "Ungruppiert"
                cat_id = 0
                if stream.channel_group:
                    cat_name = stream.channel_group.name
                    cat_id = stream.channel_group.id
                    
                if cat_id not in categories_map:
                    categories_map[cat_id] = {
                        "id": cat_id,
                        "name": cat_name,
                        "streams": []
                    }
                
                categories_map[cat_id]["streams"].append({
                    "id": stream.id,
                    "name": stream.name or f"Stream {stream.id}",
                    "tvg_id": stream.tvg_id or ""
                })
            
            # Filter out empty categories
            categories = [c for c in categories_map.values() if len(c["streams"]) > 0]
            
            # Sort categories alphabetically
            categories.sort(key=lambda x: x["name"])
            
            if categories:
                tree.append({
                    "key": acc.id,
                    "name": acc.name,
                    "type": acc.account_type,
                    "categories": categories
                })
                
        # Sort accounts alphabetically
        tree.sort(key=lambda x: x["name"])
        
        return JsonResponse({"status": "ok", "tree": tree})
    except Exception as e:
        logger.exception("Portal Explorer: Failed to retrieve portal tree data")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def portal_explorer_groups_api(request):
    """Retrieves all existing custom channel groups from the database"""
    try:
        groups = ChannelGroup.objects.all().order_by("name")
        groups_list = [{"id": g.id, "name": g.name} for g in groups]
        return JsonResponse({"status": "ok", "groups": groups_list})
    except Exception as e:
        logger.exception("Portal Explorer: Failed to retrieve custom groups")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def portal_explorer_import_api(request):
    """Performs bulk transactional import of selected streams into target channel groups"""
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
        
    try:
        data = json.loads(request.body.decode("utf-8"))
        stream_ids = data.get("stream_ids", [])
        target_group_id = data.get("target_group_id")
        new_group_name = data.get("new_group_name")
        keep_categories = bool(data.get("keep_categories", True))
        auto_number = bool(data.get("auto_number", True))
        
        if not stream_ids:
            return JsonResponse({"status": "error", "message": "Keine Stream-IDs angegeben."}, status=400)
            
        # 1. Determine target group
        dest_group = None
        if target_group_id:
            try:
                dest_group = ChannelGroup.objects.get(id=target_group_id)
            except ChannelGroup.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Ausgewählte Kanalgruppe existiert nicht."}, status=404)
        elif new_group_name:
            dest_group, _ = ChannelGroup.objects.get_or_create(name=new_group_name.strip())
            
        streams = Stream.objects.filter(id__in=stream_ids).select_related("channel_group")
        imported_count = 0
        
        # 2. Perform atomic database updates
        with transaction.atomic():
            for stream in streams:
                final_group = dest_group
                
                # Keep provider categories if checked
                if keep_categories and stream.channel_group:
                    final_group, _ = ChannelGroup.objects.get_or_create(name=stream.channel_group.name)
                
                # Check for existing channel with same name and group to prevent duplicate entries
                channel = Channel.objects.filter(name=stream.name, channel_group=final_group).first()
                
                if not channel:
                    # Allocate next available channel number if requested
                    channel_number = None
                    if auto_number:
                        channel_number = Channel.get_next_available_channel_number()
                        
                    channel = Channel.objects.create(
                        name=stream.name,
                        channel_group=final_group,
                        channel_number=channel_number,
                        tvg_id=stream.tvg_id
                    )
                
                # Link stream to channel via ChannelStream M2M model
                if not ChannelStream.objects.filter(channel=channel, stream=stream).exists():
                    next_order = ChannelStream.objects.filter(channel=channel).count()
                    ChannelStream.objects.create(
                        channel=channel,
                        stream=stream,
                        order=next_order
                    )
                
                imported_count += 1
                
        return JsonResponse({
            "status": "ok",
            "imported_count": imported_count,
            "message": f"Erfolgreich {imported_count} Kanäle importiert!"
        })
        
    except Exception as e:
        logger.exception("Portal Explorer: Failed to complete bulk stream import transaction")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# Dynamic route injection variables
_route_lock = threading.Lock()
_route_registered = False

def register_explorer_routes():
    """Injects our plugin routes dynamically into Django's root url patterns at runtime"""
    global _route_registered
    with _route_lock:
        if _route_registered:
            return
        resolver = get_resolver()
        
        # Verify route is not already registered in patterns
        for pattern in resolver.url_patterns:
            if hasattr(pattern, "pattern") and "portal-explorer/" in str(pattern.pattern):
                _route_registered = True
                return
        
        routes = [
            path("portal-explorer/", portal_explorer_index_view, name="portal-explorer-index"),
            path("portal-explorer/api/tree/", portal_explorer_tree_api, name="portal-explorer-tree"),
            path("portal-explorer/api/groups/", portal_explorer_groups_api, name="portal-explorer-groups"),
            path("portal-explorer/api/import/", portal_explorer_import_api, name="portal-explorer-import"),
        ]
        
        # Inject routes into Django url patterns
        resolver.url_patterns.extend(routes)
        _route_registered = True
        logger.info("Portal Explorer: Dynamically registered routes under '/portal-explorer/'.")


# ----------------------------------------------------------------------
# DISPATCHARR EXPLORER PLUGIN CLASS
# ----------------------------------------------------------------------

class Plugin:
    name = "Portal Explorer & Integrator"
    version = "1.0.0"
    description = "Premium-Baumstruktur-Explorer für Stalker-Portale und Xtream-Panels. Ermöglicht das visuelle Ordner-Browsing und den Bulk-Import von Streams direkt in Ihre eigene Kanalliste."
    author = "Antigravity"

    def __init__(self):
        # Register the HTTP routes dynamically on plugin discovery/init
        register_explorer_routes()

    def run(self, action: str, params: dict, context: dict):
        # The explorer runs purely through HTTP requests served by Daphne.
        # No offline run actions required.
        return {"status": "ok", "message": "Portal Explorer is running at http://127.0.0.1:5656/portal-explorer/"}
