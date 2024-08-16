import requests
import os
from dotenv import load_dotenv

class DiscogsFetcher:
    def __init__(self, user_agent):
        load_dotenv()
        self.api_key = os.getenv("DISCOGS_API_KEY")
        self.user_agent = user_agent

    def fetch_genre(self, artist_name, album_title):
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
            first_result = data['results'][0]
            genres = first_result.get('genre', [])
            styles = first_result.get('style', [])
            return genres, styles
        else:
            return [], []

# Example usage
# user_agent = "MyDiscogsApp/0.1-dev"
# discogs_fetcher = DiscogsFetcher(user_agent)
# artist = "Dead Milkmen"
# album = "Big Lizard In My Backyard"
#
# genres, styles = discogs_fetcher.fetch_genre(artist, album)
# print(f"Genres: {genres}")
# print(f"Styles: {styles}")
