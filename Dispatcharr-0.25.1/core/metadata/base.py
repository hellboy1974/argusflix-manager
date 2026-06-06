from typing import Dict, Any, Optional, List

class BaseMetadataProvider:
    """Base interface for all metadata providers (TMDB, OMDb, etc.)"""
    
    @property
    def provider_name(self) -> str:
        """Name of the provider, e.g., 'tmdb', 'omdb'"""
        raise NotImplementedError

    def is_configured(self) -> bool:
        """Check if the provider has necessary API keys/config to run."""
        raise NotImplementedError

    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Search for a movie and return standardized metadata.
        Standard return format:
        {
            'title': str,
            'year': int,
            'description': str,
            'rating': str,
            'genre': str,
            'poster_url': str,
            'tmdb_id': str,
            'imdb_id': str
        }
        """
        raise NotImplementedError

    def search_movies(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search for movies and return a list of matches."""
        raise NotImplementedError

    def search_series_list(self, title: str, year: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search for TV series and return a list of matches."""
        raise NotImplementedError

    def get_movie_by_id(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """Get a movie directly by the provider's specific ID."""
        raise NotImplementedError

    def get_series_by_id(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """Get a TV series directly by the provider's specific ID."""
        raise NotImplementedError

    def search_series(self, title: str, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Search for a TV series and return standardized metadata.
        Standard return format is same as search_movie.
        """
        raise NotImplementedError
