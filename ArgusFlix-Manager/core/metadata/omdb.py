import requests
import logging
from typing import Dict, Any, Optional, List
from core.models import CoreSettings
from .base import BaseMetadataProvider

logger = logging.getLogger(__name__)

class OMDBProvider(BaseMetadataProvider):
    """Open Movie Database (OMDb) metadata provider stub"""
    
    BASE_URL = "http://www.omdbapi.com/"

    @property
    def provider_name(self) -> str:
        return "omdb"

    def _get_api_key(self) -> str:
        settings = CoreSettings.get_metadata_settings()
        return settings.get("omdb_api_key", "").strip()

    def is_configured(self) -> bool:
        return bool(self._get_api_key())

    def search_movies(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        if not self.is_configured() or not title:
            return []
        # Stub implementation
        return []

    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        results = self.search_movies(title, year)
        return results[0] if results else None

    def search_series_list(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        if not self.is_configured() or not title:
            return []
        # Stub implementation
        return []

    def search_series(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        results = self.search_series_list(title, year)
        return results[0] if results else None

    def get_movie_by_id(self, provider_id: str) -> Optional[Dict[str, Any]]:
        return None

    def get_series_by_id(self, provider_id: str) -> Optional[Dict[str, Any]]:
        return None
