# Import the necessary classes
from wikipedia_genre_fetcher import WikipediaGenreFetcher
from discogs_genre_fetcher import DiscogsFetcher

class GenreFetcher:
    def __init__(self, user_agent):
        ####: TODO: test other titles and cleanup
        self.wikipedia_genre_fetcher = WikipediaGenreFetcher("Big Lizard in My Backyard")
        self.discogs_genre_fetcher = DiscogsFetcher(user_agent)

    def fetch_genres(self, artist_name, album_title):
        # Fetch genres from Wikipedia
        wikipedia_genres = self.wikipedia_genre_fetcher.fetch_genre()

        # Fetch genres from Discogs
        discogs_genres, discogs_styles = self.discogs_genre_fetcher.fetch_genre(artist_name, album_title)

        # Combine results from both sources
        # combined_genres = sorted([genre.capitalize() for genre in set(wikipedia_genres + discogs_genres + discogs_styles)])

        combined_genres = list(set(wikipedia_genres + discogs_genres + discogs_styles))

        def capitalize_genre(genre):
            return genre.capitalize()

        capitalized_genres = list(map(capitalize_genre, combined_genres))
        sorted_genres = sorted(capitalized_genres)

        return sorted_genres

# Example usage
# discogs_api_key = "your_discogs_api_key"
user_agent = "MyApp/0.1-dev"

genre_fetcher = GenreFetcher(user_agent)
result = genre_fetcher.fetch_genres("Dead Milkmen", "Big Lizard in My Backyard")

print(result)
