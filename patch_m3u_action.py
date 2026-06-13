# -*- coding: utf-8 -*-
import re

file_path = 'ArgusFlix-Manager/apps/m3u/api_views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'def acknowledge_categories(' not in content:
    new_action = '''
    @action(detail=True, methods=["post"], url_path="acknowledge-categories")
    def acknowledge_categories(self, request, pk=None):
        """
        Acknowledge new categories for this provider.
        Accepts: {"categories": [{"id": 1, "type": "live|vod|series"}], "acknowledge_all": true/false}
        """
        account = self.get_object()
        acknowledge_all = request.data.get("acknowledge_all", False)
        categories = request.data.get("categories", [])

        from apps.channels.models import ChannelGroupM3UAccount
        from apps.vod.models import M3UVODCategoryRelation

        if acknowledge_all:
            ChannelGroupM3UAccount.objects.filter(m3u_account=account, is_acknowledged=False).update(is_acknowledged=True)
            M3UVODCategoryRelation.objects.filter(m3u_account=account, is_acknowledged=False).update(is_acknowledged=True)
        else:
            for cat in categories:
                cat_id = cat.get("id")
                cat_type = cat.get("type")
                if cat_type == "live":
                    ChannelGroupM3UAccount.objects.filter(m3u_account=account, channel_group_id=cat_id).update(is_acknowledged=True, enabled=True)
                elif cat_type in ["vod", "movie", "series"]:
                    M3UVODCategoryRelation.objects.filter(m3u_account=account, category_id=cat_id).update(is_acknowledged=True, enabled=True)

        return Response({"status": "acknowledged"})
'''
    # Append the action to the M3UAccountViewSet
    # Find a good spot, e.g. before "class ServerGroupViewSet"
    search_str = 'class ServerGroupViewSet(viewsets.ModelViewSet):'
    content = content.replace(search_str, new_action + '\n\n' + search_str)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print("M3UAccountViewSet patched with acknowledge_categories.")
