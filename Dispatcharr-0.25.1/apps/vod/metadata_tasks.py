import logging
from typing import List, Dict, Any
from apps.vod.models import Movie, Series, VODLogo
from core.metadata import MetadataManager

logger = logging.getLogger(__name__)

def update_movie_with_metadata(movie: Movie, meta: Dict[str, Any], force_override: bool = False) -> bool:
    """Updates a Movie object with metadata and handles poster creation"""
    changed = False
    
    # Update fields if provided and not already set (unless forced)
    if meta.get("tmdb_id") and (force_override or not movie.tmdb_id):
        movie.tmdb_id = meta["tmdb_id"]
        changed = True
        
    if meta.get("imdb_id") and (force_override or not movie.imdb_id):
        movie.imdb_id = meta["imdb_id"]
        changed = True
        
    if meta.get("description") and (force_override or not movie.description):
        movie.description = meta["description"]
        changed = True
        
    if meta.get("rating") and (force_override or not movie.rating):
        movie.rating = meta["rating"]
        changed = True
        
    if meta.get("genre") and (force_override or not movie.genre):
        movie.genre = meta["genre"]
        changed = True
        
    if meta.get("year") and (force_override or not movie.year):
        movie.year = meta["year"]
        changed = True

    # Handle Poster
    if meta.get("poster_url") and (force_override or not movie.logo):
        logo_url = meta["poster_url"]
        logo_name = f"Poster - {movie.name}"
        
        logo, created = VODLogo.objects.get_or_create(
            url=logo_url,
            defaults={"name": logo_name}
        )
        movie.logo = logo
        changed = True
        
    if changed:
        movie.save()
        
    return changed

def update_series_with_metadata(series: Series, meta: Dict[str, Any], force_override: bool = False) -> bool:
    """Updates a Series object with metadata and handles poster creation"""
    changed = False
    
    # Update fields if provided and not already set (unless forced)
    if meta.get("tmdb_id") and (force_override or not series.tmdb_id):
        series.tmdb_id = meta["tmdb_id"]
        changed = True
        
    if meta.get("imdb_id") and (force_override or not series.imdb_id):
        series.imdb_id = meta["imdb_id"]
        changed = True
        
    if meta.get("description") and (force_override or not series.description):
        series.description = meta["description"]
        changed = True
        
    if meta.get("rating") and (force_override or not series.rating):
        series.rating = meta["rating"]
        changed = True
        
    if meta.get("genre") and (force_override or not series.genre):
        series.genre = meta["genre"]
        changed = True
        
    if meta.get("year") and (force_override or not series.year):
        series.year = meta["year"]
        changed = True

    # Handle Poster
    if meta.get("poster_url") and (force_override or not series.logo):
        logo_url = meta["poster_url"]
        logo_name = f"Poster - {series.name}"
        
        logo, created = VODLogo.objects.get_or_create(
            url=logo_url,
            defaults={"name": logo_name}
        )
        series.logo = logo
        changed = True
        
    if changed:
        series.save()
        
    return changed

def smart_match_movies(movie_ids: List[int]) -> int:
    """Matches given movies against metadata providers."""
    if not movie_ids:
        return 0
        
    movies = Movie.objects.filter(id__in=movie_ids)
    manager = MetadataManager()
    
    matched_count = 0
    for movie in movies:
        # Don't try to match if we already have full info
        if movie.tmdb_id and movie.description and movie.logo:
            continue
            
        result = manager.search_movie(movie.name, movie.year)
        if result:
            if update_movie_with_metadata(movie, result):
                matched_count += 1
                
    return matched_count

def smart_match_series(series_ids: List[int]) -> int:
    """Matches given series against metadata providers."""
    if not series_ids:
        return 0
        
    series_queryset = Series.objects.filter(id__in=series_ids)
    manager = MetadataManager()
    
    matched_count = 0
    for series in series_queryset:
        # Don't try to match if we already have full info
        if series.tmdb_id and series.description and series.logo:
            continue
            
        result = manager.search_series(series.name, series.year)
        if result:
            if update_series_with_metadata(series, result):
                matched_count += 1
                
    return matched_count
