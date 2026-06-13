from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from psutil import cpu_percent, virtual_memory, net_io_counters
from apps.channels.models import Stream
from django.http import JsonResponse
from django.db.models import Count
from apps.vod.models import Movie, Series
from apps.channels.models import Channel
from apps.accounts.models import WatchHistory
from core.models import SystemEvent
  # ADD THIS LINE


@login_required
def dashboard_view(request):
    # Fetch system metrics
    try:
        cpu_usage = cpu_percent(interval=1)
        ram = virtual_memory()
        ram_usage = f"{ram.used / (1024 ** 3):.1f} GB / {ram.total / (1024 ** 3):.1f} GB"
        network = net_io_counters()
        network_traffic = f"{network.bytes_sent / (1024 ** 2):.1f} MB"
    except Exception as e:
        cpu_usage = "N/A"
        ram_usage = "N/A"
        network_traffic = "N/A"
        print(f"Error fetching system metrics: {e}")

    # Fetch active streams and related channels
    active_streams = Stream.objects.filter(current_viewers__gt=0).prefetch_related('channels')
    active_streams_list = [
        f"Stream {i + 1}: {stream.url or 'Unknown'} ({stream.current_viewers} viewers)"
        for i, stream in enumerate(active_streams)
    ]

    # Pass data to the template
    context = {
        "cpu_usage": f"{cpu_usage}%",
        "ram_usage": ram_usage,
        "current_streams": active_streams.count(),
        "network_traffic": network_traffic,
        "active_streams": active_streams_list,
    }
    return render(request, "dashboard/dashboard.html", context)

@login_required
def settings_view(request):
    # Placeholder for settings functionality
    return render(request, 'settings.html')

@login_required
def live_dashboard_data(request):
    try:
        cpu_usage = cpu_percent(interval=1)
        ram = virtual_memory()
        network = net_io_counters()
        ram_usage = f"{ram.used / (1024 ** 3):.1f} GB / {ram.total / (1024 ** 3):.1f} GB"
        network_traffic = f"{network.bytes_sent / (1024 ** 2):.1f} MB"

        # Mocked example data for the charts
        cpu_data = [45, 50, 60, 55, 70, 65]
        ram_data = [6.5, 7.0, 7.5, 8.0, 8.5, 9.0]
        network_data = [120, 125, 130, 128, 126, 124]

        active_streams = Stream.objects.filter(current_viewers__gt=0)
        active_streams_list = [
            f"Stream {i + 1}: {stream.url or 'Unknown'} ({stream.current_viewers} viewers)"
            for i, stream in enumerate(active_streams)
        ]

        data = {
            "cpu_usage": f"{cpu_usage}%",
            "ram_usage": ram_usage,
            "current_streams": active_streams.count(),
            "network_traffic": network_traffic,
            "active_streams": active_streams_list,
            "cpu_data": cpu_data,
            "ram_data": ram_data,
            "network_data": network_data,
        }
    except Exception as e:
        data = {
            "error": str(e)
        }
    return JsonResponse(data)


@login_required
def visual_stats_data(request):
    try:
        # Content counts
        live_tv_count = Channel.objects.filter(is_active=True).count()
        movie_count = Movie.objects.filter(is_active=True).count()
        series_count = Series.objects.filter(is_active=True).count()

        content_counts = {
            "live_tv": live_tv_count,
            "movies": movie_count,
            "series": series_count,
        }

        # Recently played streams (WatchHistory)
        recent_history = WatchHistory.objects.select_related('profile').order_by('-last_watched')[:10]
        recent_streams = []
        for rh in recent_history:
            recent_streams.append({
                "profile": rh.profile.name if rh.profile else "Unknown",
                "type": rh.content_type,
                "content_id": rh.content_id,
                "progress_seconds": rh.progress_seconds,
                "last_watched": rh.last_watched.isoformat() if rh.last_watched else None
            })

        # Most common errors (from SystemEvent)
        # Assuming event_type contains 'error'
        error_events = SystemEvent.objects.filter(event_type__endswith='error')
        # We group by details or just event_type if details is too varied
        common_errors_qs = error_events.values('event_type').annotate(count=Count('id')).order_by('-count')[:5]
        
        common_errors = []
        for err in common_errors_qs:
            common_errors.append({
                "name": err['event_type'],
                "count": err['count']
            })

        # If there are no errors, maybe return some mock data for UI demo purposes, but let's stick to real data
        return JsonResponse({
            "content_counts": content_counts,
            "recent_streams": recent_streams,
            "common_errors": common_errors
        })
    except Exception as e:
        import traceback
        print("Error fetching visual stats:", traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)
