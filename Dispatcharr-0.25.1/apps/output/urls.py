from django.urls import path, re_path, include
from .views import (
    m3u_endpoint, epg_endpoint, xc_get, xc_movie_stream, xc_series_stream,
    custom_m3u_endpoint, custom_epg_endpoint, custom_xc_player_api,
    custom_stream_xc, custom_stream_xc_movie, custom_stream_xc_episode
)
from core.views import stream_view

app_name = "output"

urlpatterns = [
    # Allow `/m3u`, `/m3u/`, `/m3u/profile_name`, and `/m3u/profile_name/`
    re_path(r"^m3u(?:/(?P<profile_name>[^/]+))?/?$", m3u_endpoint, name="m3u_endpoint"),
    re_path(r"^m3u(?:/(?P<profile_name>[^/]+))?/?$", m3u_endpoint, name="generate_m3u"),
    # Allow `/epg`, `/epg/`, `/epg/profile_name`, and `/epg/profile_name/`
    re_path(r"^epg(?:/(?P<profile_name>[^/]+))?/?$", epg_endpoint, name="epg_endpoint"),
    re_path(r"^epg(?:/(?P<profile_name>[^/]+))?/?$", epg_endpoint, name="generate_epg"),
    # Allow both `/stream/<int:stream_id>` and `/stream/<int:stream_id>/`
    re_path(r"^stream/(?P<channel_uuid>[0-9a-fA-F\-]+)/?$", stream_view, name="stream"),

    # Custom Playlists Endpoints
    path("custom/<str:token>/m3u", custom_m3u_endpoint, name="custom_m3u"),
    path("custom/<str:token>/xmltv", custom_epg_endpoint, name="custom_epg"),
    path("custom/<str:token>/player_api.php", custom_xc_player_api, name="custom_xc_player_api"),

    # Custom Playlists Streams Proxy
    path("custom/<str:token>/live/<str:username>/<str:password>/<str:channel_id>", custom_stream_xc, name="custom_stream_xc"),
    path("custom/<str:token>/movie/<str:username>/<str:password>/<str:stream_id>.<str:extension>", custom_stream_xc_movie, name="custom_stream_xc_movie"),
    path("custom/<str:token>/series/<str:username>/<str:password>/<str:stream_id>.<str:extension>", custom_stream_xc_episode, name="custom_stream_xc_episode"),
]
