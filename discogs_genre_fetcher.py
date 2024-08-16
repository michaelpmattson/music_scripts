import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
discogs_api_key = os.getenv("DISCOGS_API_KEY")

# Example usage with the API key
def fetch_discogs_genre(artist_name, album_title, user_agent):
    search_url = "https://api.discogs.com/database/search"
    params = {
        'artist': artist_name,
        'release_title': album_title,
        'type': 'release',
        'format': 'album',
        'token': discogs_api_key
    }

    headers = {
        'User-Agent': user_agent
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
artist = "Dead Milkmen"
album = "Big Lizard In My Backyard"
user_agent = "MyDiscogsApp/0.1-dev"

genres, styles = fetch_discogs_genre(artist, album, user_agent)
print(f"Genres: {genres}")
print(f"Styles: {styles}")
