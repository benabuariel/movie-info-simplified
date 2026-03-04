from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

class MovieSearchService:
    def __init__(self):
        self.api_key = settings.OMDB_API_KEY
        self.base_url = "https://www.omdbapi.com/"
        if not self.api_key:
            logger.error("OMDb API key missing!")
        else:
            logger.info(f"OMDb API ready ({len(self.api_key)} chars)")

    def autocomplete(self, query):
        if len(query) < 2 or not self.api_key:
            return []
        try:
            url = f"{self.base_url}?s={query}&type=movie&apikey={self.api_key}&r=json"
            logger.info(f"🔍 Searching: {query}")
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get('Response') == 'True':
                results = [{
                    'label': f"{m['Title']} ({m['Year']})",
                    'id': m['imdbID'],
                    'value': m['Title'],
                } for m in data.get('Search', [])[:10]]
                logger.info(f"✅ Found {len(results)} movies for '{query}'")
                return results
            logger.error(f"❌ API Error: {data.get('Error')}")
            return []
        except Exception as e:
            logger.error(f"Autocomplete error: {e}")
            return []

    def get_movie_detail(self, imdb_id):
        """Fetch full movie details by IMDb ID."""
        if not self.api_key:
            return {'error': 'No API key configured'}
        try:
            url = f"{self.base_url}?i={imdb_id}&apikey={self.api_key}&plot=full&r=json"
            logger.info(f"🎬 Fetching details for {imdb_id}")
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get('Response') != 'True':
                logger.error(f"❌ Detail API error for {imdb_id}: {data.get('Error')}")
                return {'error': data.get('Error', 'Movie not found')}

            return {
                'title': data.get('Title', 'N/A'),
                'year': data.get('Year', 'N/A'),
                'rating': data.get('imdbRating'),
                'runtime': data.get('Runtime', 'N/A'),
                'genres': data.get('Genre', '').split(', ') if data.get('Genre') else [],
                'plot': data.get('Plot', 'N/A'),
                'cast': data.get('Actors', '').split(', ')[:8],
                'directors': [data.get('Director', 'N/A')] if data.get('Director') else [],
                'producers': [data.get('Writer', 'N/A')] if data.get('Writer') else [],
                'poster': data.get('Poster', ''),
                'imdb_url': f"https://www.imdb.com/title/{imdb_id}/",
            }
        except Exception as e:
            logger.error(f"Detail error for {imdb_id}: {e}")
            return {'error': 'Failed to fetch movie details'}

movie_service = MovieSearchService()
