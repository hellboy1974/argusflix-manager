from typing import Dict, Any, Optional, List
from core.models import CoreSettings
from .tmdb import TMDBProvider
from .omdb import OMDBProvider

class MetadataManager:
    """Manages metadata providers and priority-based fallback"""

    def __init__(self):
        self.providers = {
            'tmdb': TMDBProvider(),
            'omdb': OMDBProvider()
        }

    def _get_active_providers(self) -> List[str]:
        settings = CoreSettings.get_metadata_settings()
        priority = settings.get("provider_priority", ["tmdb", "omdb"])
        
        active = []
        for p in priority:
            if p in self.providers and self.providers[p].is_configured():
                active.append(p)
                
        return active

    def search_movies(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        active_providers = self._get_active_providers()
        all_results = []
        
        for provider_name in active_providers:
            provider = self.providers[provider_name]
            results = provider.search_movies(title, year)
            if results:
                all_results.extend(results)
                
        return all_results

    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        results = self.search_movies(title, year)
        return results[0] if results else None

    def search_series_list(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        active_providers = self._get_active_providers()
        all_results = []
        
        for provider_name in active_providers:
            provider = self.providers[provider_name]
            results = provider.search_series_list(title, year)
            if results:
                all_results.extend(results)
                
        return all_results

    def search_series(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        results = self.search_series_list(title, year)
        return results[0] if results else None

    def get_movie_by_id(self, provider_id: str, provider_name: str = 'tmdb') -> Optional[Dict[str, Any]]:
        if provider_name in self.providers:
            return self.providers[provider_name].get_movie_by_id(provider_id)
        return None

    def get_series_by_id(self, provider_id: str, provider_name: str = 'tmdb') -> Optional[Dict[str, Any]]:
        if provider_name in self.providers:
            return self.providers[provider_name].get_series_by_id(provider_id)
        return None
