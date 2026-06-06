import requests
import logging
from typing import Dict, Any, Optional, List
from core.models import CoreSettings
from .base import BaseMetadataProvider

logger = logging.getLogger(__name__)

class TMDBProvider(BaseMetadataProvider):
    """The Movie Database (TMDB) metadata provider"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

    @property
    def provider_name(self) -> str:
        return "tmdb"

    def _get_api_key(self) -> str:
        settings = CoreSettings.get_metadata_settings()
        return settings.get("tmdb_api_key", "").strip()

    def _get_language(self) -> str:
        settings = CoreSettings.get_metadata_settings()
        return settings.get("language", "de-DE")

    def is_configured(self) -> bool:
        return bool(self._get_api_key())

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        api_key = self._get_api_key()
        if not api_key:
            return None

        if params is None:
            params = {}
            
        params["api_key"] = api_key
        params["language"] = self._get_language()

        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"TMDB API Error on {endpoint}: {str(e)}")
            return None

    def search_movies(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        if not self.is_configured() or not title:
            return []

        params = {"query": title}
        if year:
            params["year"] = year

        data = self._make_request("/search/movie", params)
        if not data or not data.get("results"):
            return []

        results = []
        for match in data["results"][:5]:  # return top 5
            tmdb_id = match.get("id")
            if tmdb_id:
                details = self._make_request(f"/movie/{tmdb_id}")
                if not details:
                    details = match
                results.append(self._format_movie_data(details))
        return results

    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        results = self.search_movies(title, year)
        return results[0] if results else None

    def search_series_list(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        if not self.is_configured() or not title:
            return []

        params = {"query": title}
        if year:
            params["first_air_date_year"] = year

        data = self._make_request("/search/tv", params)
        if not data or not data.get("results"):
            return []

        results = []
        for match in data["results"][:5]:
            tmdb_id = match.get("id")
            if tmdb_id:
                details = self._make_request(f"/tv/{tmdb_id}", params={"append_to_response": "external_ids"})
                if not details:
                    details = match
                results.append(self._format_series_data(details))
        return results

    def search_series(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        results = self.search_series_list(title, year)
        return results[0] if results else None

    def get_movie_by_id(self, tmdb_id: str) -> Optional[Dict[str, Any]]:
        if not self.is_configured() or not tmdb_id:
            return None
        details = self._make_request(f"/movie/{tmdb_id}")
        if details:
            return self._format_movie_data(details)
        return None

    def get_series_by_id(self, tmdb_id: str) -> Optional[Dict[str, Any]]:
        if not self.is_configured() or not tmdb_id:
            return None
        details = self._make_request(f"/tv/{tmdb_id}", params={"append_to_response": "external_ids"})
        if details:
            return self._format_series_data(details)
        return None

    def _format_movie_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        poster_path = data.get("poster_path")
        poster_url = f"{self.IMAGE_BASE_URL}{poster_path}" if poster_path else None

        genres = [g.get("name") for g in data.get("genres", [])] if "genres" in data else []
        genre_str = ", ".join(genres) if genres else ""

        # Release date parsing
        release_date = data.get("release_date", "")
        year = int(release_date.split("-")[0]) if release_date else None

        return {
            'title': data.get("title", ""),
            'year': year,
            'description': data.get("overview", ""),
            'rating': str(data.get("vote_average", "")),
            'genre': genre_str,
            'poster_url': poster_url,
            'tmdb_id': str(data.get("id", "")),
            'imdb_id': data.get("imdb_id", "")
        }

    def _format_series_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        poster_path = data.get("poster_path")
        poster_url = f"{self.IMAGE_BASE_URL}{poster_path}" if poster_path else None

        genres = [g.get("name") for g in data.get("genres", [])] if "genres" in data else []
        genre_str = ", ".join(genres) if genres else ""

        # First air date parsing
        first_air_date = data.get("first_air_date", "")
        year = int(first_air_date.split("-")[0]) if first_air_date else None
        
        # Extract external IDs if appended
        imdb_id = ""
        external_ids = data.get("external_ids", {})
        if external_ids:
            imdb_id = external_ids.get("imdb_id", "")

        return {
            'title': data.get("name", ""),
            'year': year,
            'description': data.get("overview", ""),
            'rating': str(data.get("vote_average", "")),
            'genre': genre_str,
            'poster_url': poster_url,
            'tmdb_id': str(data.get("id", "")),
            'imdb_id': imdb_id
        }
