import requests
import os
from dotenv import load_dotenv

class DiscogsFetcher:
    def __init__(self, user_agent):
        load_dotenv()
        self.api_key = os.getenv("DISCOGS_API_KEY")
        self.user_agent = user_agent

    def fetch_master_id(self, artist_name, album_title):
        """Fetch the master_id using the search API."""
        search_url = "https://api.discogs.com/database/search"
        params = {
            'artist': artist_name,
            'release_title': album_title,
            'type': 'release',
            'format': 'album',
            'token': self.api_key
        }

        headers = {
            'User-Agent': self.user_agent
        }

        response = requests.get(search_url, headers=headers, params=params)
        data = response.json()

        if data['results']:
            for result in data['results']:
                master_id = result.get('master_id')
                if master_id:
                    return master_id

        return None

    def fetch_master_release_info(self, master_id):
        """Fetch genres and styles using the master release API."""
        master_url = f"https://api.discogs.com/masters/{master_id}"
        headers = {
            'User-Agent': self.user_agent
        }

        response = requests.get(master_url, headers=headers)
        data = response.json()

        genres = data.get('genres', [])
        styles = data.get('styles', [])
        return genres, styles

    def fetch_genre(self, artist_name, album_title):
        """Main method to fetch genres and styles."""
        master_id = self.fetch_master_id(artist_name, album_title)
        if master_id:
            return self.fetch_master_release_info(master_id)
        else:
            return [], []

# Example usage
# user_agent = "MyDiscogsApp/0.1-dev"
# discogs_fetcher = DiscogsFetcher(user_agent)
# artist = "Eric Clapton"
# album = "461 Ocean Boulevard"
#
# genres, styles = discogs_fetcher.fetch_genre(artist, album)
# print(f"Genres: {genres}")
# print(f"Styles: {styles}")
