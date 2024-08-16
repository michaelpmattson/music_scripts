import requests
import re
from infobox_parser import InfoboxParser  # Assuming InfoboxParser is in infobox_parser.py

class WikipediaGenreFetcher:
    def __init__(self, title):
        self.title = title
        self.content = self.fetch_wikipedia_content()
        self.infobox_data = None

    def fetch_wikipedia_content(self):
        """Fetch the content of a Wikipedia page."""
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": self.title,
            "prop": "revisions",
            "rvprop": "content",
            "rvsection": 0
        }
        response = requests.get(url, params=params)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()), {})
        return page.get("revisions", [{}])[0].get('*', '')

    def parse_infobox(self):
        """Parse the infobox content."""
        parser = InfoboxParser(self.content)
        self.infobox_data = parser.parse_infobox()

    def extract_genre(self):
        """Extract and clean the genre information."""
        genre_field = self.infobox_data.get("genre", "")
        if not genre_field:
            return []

        genre_field = self.clean_genre_field(genre_field)
        return self.extract_genres_from_field(genre_field)

    @staticmethod
    def clean_genre_field(genre_field):
        """Clean the genre field by removing unwanted tags and templates."""
        genre_field = re.sub(r'<!--.*?-->', '', genre_field, flags=re.DOTALL)
        genre_field = re.sub(r'<ref[^>]*>[^<]*(?:<[^<]*>)*<\/ref>', '', genre_field, flags=re.DOTALL)
        genre_field = re.sub(r'\{\{hlist\|', '', genre_field)
        genre_field = genre_field.replace('}}', '').strip()
        return genre_field

    @staticmethod
    def extract_genres_from_field(genre_field):
        """Extract genres from the cleaned genre field."""
        genres = re.findall(r'\[\[(?:[^|\]]*\|)?([^]]+)\]\]', genre_field)
        return [genre.strip() for genre in genres if genre]

    def fetch_genre(self):
        """Main method to fetch and return the genres."""
        self.parse_infobox()
        return self.extract_genre()

# Example usage
fetcher = WikipediaGenreFetcher("Billie_Jean")
album_genre = fetcher.fetch_genre()
print(f"Album Genre: {album_genre}")


# Example: Fetch genre for the album "Thriller (Michael Jackson album)"
# album_name = "Thriller_(album)"
# album_genre = fetch_wikipedia_genre(album_name)
# print(f"Album Genre: {album_genre}")

# Example: Fetch genre for a song "Billie Jean"
# song_name = "Billie_Jean"
# song_genre = fetch_wikipedia_genre(song_name)
# print(f"Song Genre: {song_genre}")

# Example: Fetch genre for the album "Lysol (Melvins album)"
# album_name = "Lysol_(album)"
# album_genre = fetch_wikipedia_genre(album_name)
# print(f"Album Genre: {album_genre}")
