import re

with open("apps/output/views.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Patch generate_m3u
m3u_orig = """    if user is not None:
        if user.user_level < 10:
            user_profile_count = user.channel_profiles.count()"""
m3u_new = """    is_custom_playlist = False
    custom_playlist = None

    if user is not None:
        if user.user_level < 10:
            user_profile_count = user.channel_profiles.count()"""
content = content.replace(m3u_orig, m3u_new)

m3u_qs_orig = """    else:
        if profile_name is not None:
            try:
                channel_profile = ChannelProfile.objects.get(name=profile_name)
            except ChannelProfile.DoesNotExist:
                logger.warning("Requested channel profile (%s) during m3u generation does not exist", profile_name)
                raise Http404(f"Channel profile '{profile_name}' not found")
            base_qs = Channel.objects.filter(
                channelprofilemembership__channel_profile=channel_profile,
                channelprofilemembership__enabled=True
            ).select_related('channel_group', 'logo')
        else:
            base_qs = Channel.objects.select_related('channel_group', 'logo')"""
m3u_qs_new = """    else:
        if profile_name is not None:
            from apps.output.models import CustomPlaylist
            try:
                channel_profile = ChannelProfile.objects.get(name=profile_name)
                base_qs = Channel.objects.filter(
                    channelprofilemembership__channel_profile=channel_profile,
                    channelprofilemembership__enabled=True
                ).select_related('channel_group', 'logo')
            except ChannelProfile.DoesNotExist:
                # Check for Custom Playlist
                from django.db.models import Q
                custom_playlist = CustomPlaylist.objects.filter(Q(token=profile_name) | Q(slug=profile_name), is_active=True).first()
                if custom_playlist:
                    is_custom_playlist = True
                    mapped_group_ids = custom_playlist.live_mappings.values_list('channel_group_id', flat=True)
                    base_qs = Channel.objects.filter(channel_group_id__in=mapped_group_ids).select_related('channel_group', 'logo')
                else:
                    logger.warning("Requested channel profile (%s) during m3u generation does not exist", profile_name)
                    raise Http404(f"Channel profile '{profile_name}' not found")
        else:
            base_qs = Channel.objects.select_related('channel_group', 'logo')"""
content = content.replace(m3u_qs_orig, m3u_qs_new)

m3u_vod_orig = """    # Cache the generated content for 2 seconds to handle double-GET requests
    cache.set(content_cache_key, m3u_content, 2)"""
m3u_vod_new = """    if is_custom_playlist and custom_playlist:
        from apps.vod.models import Movie, Series
        mapped_cat_ids = custom_playlist.vod_mappings.values_list('vod_category_id', flat=True)
        if mapped_cat_ids.exists():
            # Add Movies
            movies = Movie.objects.filter(category_id__in=mapped_cat_ids).select_related('category')
            for movie in movies:
                group_title = movie.category.name if movie.category else "VOD"
                extinf = f'#EXTINF:-1 tvg-id="" tvg-name="{movie.name}" tvg-logo="{movie.poster_url}" group-title="{group_title}",{movie.name}\\n'
                stream_url = request.build_absolute_uri(reverse('vod:stream_movie', args=[movie.id]))
                m3u_content += extinf + stream_url + "\\n"
            
            # Add Series/Episodes
            series_qs = Series.objects.filter(category_id__in=mapped_cat_ids).prefetch_related('seasons__episodes').select_related('category')
            for series in series_qs:
                group_title = series.category.name if series.category else "Series"
                for season in series.seasons.all():
                    for ep in season.episodes.all():
                        name = f"{series.name} S{season.season_number:02d}E{ep.episode_number:02d} {ep.name}"
                        extinf = f'#EXTINF:-1 tvg-id="" tvg-name="{name}" tvg-logo="{series.poster_url}" group-title="{group_title}",{name}\\n'
                        stream_url = request.build_absolute_uri(reverse('vod:stream_episode', args=[ep.id]))
                        m3u_content += extinf + stream_url + "\\n"

    # Cache the generated content for 2 seconds to handle double-GET requests
    cache.set(content_cache_key, m3u_content, 2)"""
content = content.replace(m3u_vod_orig, m3u_vod_new)


# 2. Patch generate_epg
epg_qs_orig = """        else:
            if profile_name is not None:
                try:
                    channel_profile = ChannelProfile.objects.get(name=profile_name)
                except ChannelProfile.DoesNotExist:
                    logger.warning("Requested channel profile (%s) during epg generation does not exist", profile_name)
                    raise Http404(f"Channel profile '{profile_name}' not found")
                base_qs = Channel.objects.filter(
                    channelprofilemembership__channel_profile=channel_profile,
                    channelprofilemembership__enabled=True,
                ).select_related('logo', 'epg_data__epg_source')
            else:
                base_qs = Channel.objects.all().select_related('logo', 'epg_data__epg_source')"""
epg_qs_new = """        else:
            if profile_name is not None:
                from apps.output.models import CustomPlaylist
                try:
                    channel_profile = ChannelProfile.objects.get(name=profile_name)
                    base_qs = Channel.objects.filter(
                        channelprofilemembership__channel_profile=channel_profile,
                        channelprofilemembership__enabled=True,
                    ).select_related('logo', 'epg_data__epg_source')
                except ChannelProfile.DoesNotExist:
                    from django.db.models import Q
                    custom_playlist = CustomPlaylist.objects.filter(Q(token=profile_name) | Q(slug=profile_name), is_active=True).first()
                    if custom_playlist:
                        mapped_group_ids = custom_playlist.live_mappings.values_list('channel_group_id', flat=True)
                        base_qs = Channel.objects.filter(channel_group_id__in=mapped_group_ids).select_related('logo', 'epg_data__epg_source')
                    else:
                        logger.warning("Requested channel profile (%s) during epg generation does not exist", profile_name)
                        raise Http404(f"Channel profile '{profile_name}' not found")
            else:
                base_qs = Channel.objects.all().select_related('logo', 'epg_data__epg_source')"""
content = content.replace(epg_qs_orig, epg_qs_new)


with open("apps/output/views.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched M3U and EPG endpoints!")
