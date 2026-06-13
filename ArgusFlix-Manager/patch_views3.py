import re

with open("apps/output/views.py", "r", encoding="utf-8") as f:
    content = f.read()

# xc_get_live_categories
orig_live_cat = """def xc_get_live_categories(user):
    from apps.channels.models import ChannelGroup
    if user.user_level < 10:"""
new_live_cat = """def xc_get_live_categories(user):
    from apps.channels.models import ChannelGroup
    from apps.output.models import CustomPlaylist
    if isinstance(user, CustomPlaylist):
        mapped_group_ids = user.live_mappings.values_list('channel_group_id', flat=True)
        groups = ChannelGroup.objects.filter(id__in=mapped_group_ids)
    elif user.user_level < 10:"""
content = content.replace(orig_live_cat, new_live_cat)

# xc_get_vod_categories
orig_vod_cat = """def xc_get_vod_categories(user):
    from apps.vod.models import VODCategory
    
    # Hide adult content if user preference is set
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False)

    filters = {'category_type': 'movie'}"""
new_vod_cat = """def xc_get_vod_categories(user):
    from apps.vod.models import VODCategory
    from apps.output.models import CustomPlaylist
    
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False) if hasattr(user, 'custom_properties') else False

    filters = {'category_type': 'movie'}
    if isinstance(user, CustomPlaylist):
        mapped_cat_ids = user.vod_mappings.values_list('vod_category_id', flat=True)
        filters['id__in'] = mapped_cat_ids"""
content = content.replace(orig_vod_cat, new_vod_cat)

# xc_get_series_categories
orig_series_cat = """def xc_get_series_categories(user):
    from apps.vod.models import VODCategory
    
    # Hide adult content if user preference is set
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False)

    filters = {'category_type': 'series'}"""
new_series_cat = """def xc_get_series_categories(user):
    from apps.vod.models import VODCategory
    from apps.output.models import CustomPlaylist
    
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False) if hasattr(user, 'custom_properties') else False

    filters = {'category_type': 'series'}
    if isinstance(user, CustomPlaylist):
        mapped_cat_ids = user.vod_mappings.values_list('vod_category_id', flat=True)
        filters['id__in'] = mapped_cat_ids"""
content = content.replace(orig_series_cat, new_series_cat)

# xc_get_vod_streams
orig_vod_stream = """def xc_get_vod_streams(request, user, category_id=None):
    from apps.vod.models import Movie
    
    # Hide adult content if user preference is set
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False)

    filters = {}"""
new_vod_stream = """def xc_get_vod_streams(request, user, category_id=None):
    from apps.vod.models import Movie
    from apps.output.models import CustomPlaylist
    
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False) if hasattr(user, 'custom_properties') else False

    filters = {}
    if isinstance(user, CustomPlaylist):
        mapped_cat_ids = user.vod_mappings.values_list('vod_category_id', flat=True)
        filters['category_id__in'] = mapped_cat_ids"""
content = content.replace(orig_vod_stream, new_vod_stream)

# xc_get_series
orig_series = """def xc_get_series(request, user, category_id=None):
    from apps.vod.models import Series
    
    # Hide adult content if user preference is set
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False)

    filters = {}"""
new_series = """def xc_get_series(request, user, category_id=None):
    from apps.vod.models import Series
    from apps.output.models import CustomPlaylist
    
    hide_adult = (user.custom_properties or {}).get('hide_adult_content', False) if hasattr(user, 'custom_properties') else False

    filters = {}
    if isinstance(user, CustomPlaylist):
        mapped_cat_ids = user.vod_mappings.values_list('vod_category_id', flat=True)
        filters['category_id__in'] = mapped_cat_ids"""
content = content.replace(orig_series, new_series)


with open("apps/output/views.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched all remaining xc_get functions!")
