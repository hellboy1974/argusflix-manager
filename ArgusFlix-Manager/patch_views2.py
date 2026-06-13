import re
import sys

with open("apps/output/views.py", "r", encoding="utf-8") as f:
    content = f.read()

# Update _xc_live_streams_setup
live_setup_orig = """def _xc_live_streams_setup(request, user, category_id):
    from apps.channels.managers import with_effective_values

    if user.user_level < 10:"""

live_setup_new = """def _xc_live_streams_setup(request, user, category_id):
    from apps.channels.managers import with_effective_values
    from apps.output.models import CustomPlaylist

    if isinstance(user, CustomPlaylist):
        # Filter channels by CustomPlaylistLiveMapping
        mapped_group_ids = user.live_mappings.values_list('channel_group_id', flat=True)
        filters = {"channel_group__id__in": mapped_group_ids}
        if category_id is not None:
            filters["channel_group__id"] = category_id
        
        # Hide adult content based on custom properties (assuming CustomPlaylist could have this)
        if (user.custom_properties or {}).get('hide_adult_content', False):
            filters["is_adult"] = False
            
        base_qs = Channel.objects.filter(**filters).select_related('channel_group', 'logo')

    elif user.user_level < 10:"""

content = content.replace(live_setup_orig, live_setup_new)

with open("apps/output/views.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched _xc_live_streams_setup!")
