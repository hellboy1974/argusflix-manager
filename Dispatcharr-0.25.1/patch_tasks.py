import re
import sys

file_path = r"C:\Users\sheng\Documents\dispatcharr_reloaded\Dispatcharr-0.25.1\apps\m3u\tasks.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update existing_channel_streams query (remove channel__auto_created_by=account)
content = re.sub(
    r'existing_channel_streams = \(\n\s*ChannelStream\.objects\.filter\(\n\s*channel__auto_created=True,\n\s*channel__auto_created_by=account,\n\s*stream__m3u_account=account,\n\s*stream__channel_group=channel_group,\n\s*\)',
    r'existing_channel_streams = (\n                ChannelStream.objects.filter(\n                    channel__auto_created=True,\n                    stream__m3u_account=account,\n                    stream__channel_group=channel_group,\n                )',
    content
)

# 2. Update empty group deletion logic (around line 2215)
old_delete_1 = """                if channels_to_delete:
                    deleted_count = len(channels_to_delete)
                    Channel.objects.filter(
                        id__in=[ch.id for ch in channels_to_delete]
                    ).delete()
                    channels_deleted += deleted_count"""
new_delete_1 = """                if channels_to_delete:
                    channels_to_delete_ids = []
                    for ch in channels_to_delete:
                        if not ChannelStream.objects.filter(channel=ch).exclude(stream__m3u_account=account).exists():
                            channels_to_delete_ids.append(ch.id)
                        else:
                            # Just remove our stream mappings
                            ChannelStream.objects.filter(channel=ch, stream__m3u_account=account).delete()
                    
                    if channels_to_delete_ids:
                        deleted_count = len(channels_to_delete_ids)
                        Channel.objects.filter(
                            id__in=channels_to_delete_ids
                        ).delete()
                        channels_deleted += deleted_count
                    else:
                        deleted_count = 0"""
content = content.replace(old_delete_1, new_delete_1)

# 3. Update overflow_delete_ids logic (around line 2336)
old_delete_2 = """                if overflow_delete_ids:
                    deleted = Channel.objects.filter(
                        id__in=overflow_delete_ids
                    ).delete()"""
new_delete_2 = """                if overflow_delete_ids:
                    actual_overflow_delete_ids = []
                    for cid in overflow_delete_ids:
                        if not ChannelStream.objects.filter(channel_id=cid).exclude(stream__m3u_account=account).exists():
                            actual_overflow_delete_ids.append(cid)
                        else:
                            ChannelStream.objects.filter(channel_id=cid, stream__m3u_account=account).delete()
                            
                    deleted = Channel.objects.filter(
                        id__in=actual_overflow_delete_ids
                    ).delete() if actual_overflow_delete_ids else (0, {})"""
content = content.replace(old_delete_2, new_delete_2)

# 4. Insert bundled_channels lookup logic
search_str = """            for stream in current_streams:
                processed_stream_ids.add(stream.id)"""
replace_str = """            # Dictionary to cache bundled channels found during this run
            bundled_channels_by_name = {}

            for stream in current_streams:
                processed_stream_ids.add(stream.id)"""
content = content.replace(search_str, replace_str)

search_str2 = """                    # Check if we already have a channel for this stream
                    existing_channel = existing_channel_map.get(stream.id)

                    if existing_channel:"""
replace_str2 = """                    # Check if we already have a channel for this stream
                    existing_channel = existing_channel_map.get(stream.id)

                    if not existing_channel:
                        # Try to find an existing channel by name to bundle with
                        if new_name in bundled_channels_by_name:
                            existing_channel = bundled_channels_by_name[new_name]
                        else:
                            # Then check the database
                            bundled_ch = Channel.objects.filter(
                                name=new_name,
                                channel_group=target_group,
                                auto_created=True
                            ).first()
                            if bundled_ch:
                                bundled_channels_by_name[new_name] = bundled_ch
                                existing_channel = bundled_ch

                        if existing_channel:
                            # We found a channel to bundle with!
                            existing_channel_map[stream.id] = existing_channel
                            
                            ChannelStream.objects.get_or_create(
                                channel=existing_channel,
                                stream=stream,
                                defaults={'order': getattr(account, 'priority', 0)}
                            )
                            # Now it behaves like an existing channel!

                    if existing_channel:"""
content = content.replace(search_str2, replace_str2)


# 5. Fix order logic for new channels pending
search_str3 = """                        new_channels_pending.append(
                            (
                                Channel(
                                    channel_number=target_number,
                                    name=new_name,
                                    tvg_id=stream.tvg_id,"""
replace_str3 = """                        bundled_channels_by_name[new_name] = None # Will be created
                        new_channels_pending.append(
                            (
                                Channel(
                                    channel_number=target_number,
                                    name=new_name,
                                    tvg_id=stream.tvg_id,"""
content = content.replace(search_str3, replace_str3)

search_str4 = """                        ChannelStream(
                            channel_id=channel_objs[i].id,
                            stream_id=streams_for_new[i].id,
                            order=0,
                        )"""
replace_str4 = """                        ChannelStream(
                            channel_id=channel_objs[i].id,
                            stream_id=streams_for_new[i].id,
                            order=getattr(account, 'priority', 0),
                        )"""
content = content.replace(search_str4, replace_str4)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated tasks.py successfully!")
