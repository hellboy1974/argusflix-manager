import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from core.models import CoreSettings

class TmdbProxyView(APIView):
    """
    Acts as a proxy for TMDB requests to hide the API key from clients.
    Responses are cached to reduce API calls to TMDB.
    """
    
    def get(self, request, path, *args, **kwargs):
        api_key = CoreSettings.get_tmdb_api_key()
        if not api_key:
            return Response(
                {"error": "TMDB API key not configured in Manager settings."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Build the TMDB URL
        # The path parameter will be something like 'movie/123/credits' or 'person/456'
        url = f"https://api.themoviedb.org/3/{path}"
        
        # Forward the language query param if provided, default to 'de'
        language = request.query_params.get("language", "de")
        
        params = {
            "api_key": api_key,
            "language": language
        }
        
        # Forward any other query parameters (e.g. 'query', 'page')
        for key, value in request.query_params.items():
            if key not in ["api_key", "language"]:
                params[key] = value
        
        # Check cache
        # Create a cache key based on path and all query params
        query_string = request.META.get('QUERY_STRING', '')
        cache_key = f"tmdb_{path}_{language}_{query_string}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Cache for 24 hours (86400 seconds) since TMDB cast data doesn't change frequently
            cache.set(cache_key, data, 86400)
            
            return Response(data)
        except requests.exceptions.HTTPError as e:
            return Response(
                {"error": "TMDB API Error", "details": str(e)},
                status=e.response.status_code if e.response else status.HTTP_502_BAD_GATEWAY
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "Failed to connect to TMDB", "details": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )
