# Import the necessary classes
from wikipedia_genre_fetcher import WikipediaGenreFetcher
from discogs_genre_fetcher import DiscogsFetcher
from genre_mapping import genre_mapping
from genre_hierarchy import genre_hierarchy, ensure_parent_genres

class GenreFetcher:
    def __init__(self, user_agent):
        ####: TODO: test other titles and cleanup
        self.wikipedia_genre_fetcher = WikipediaGenreFetcher()
        self.discogs_genre_fetcher = DiscogsFetcher(user_agent)

    def fetch_genres(self, artist_name, album_title):
        # Fetch genres from Wikipedia
        # wikipedia_genres = self.wikipedia_genre_fetcher.fetch_genre(album_title)
        wikipedia_genres = self.wikipedia_genre_fetcher.fetch_genre(album_title, artist_name)

        # Fetch genres from Discogs
        discogs_genres, discogs_styles = self.discogs_genre_fetcher.fetch_genre(artist_name, album_title)

        # combined = {
        #     "wikipedia": wikipedia_genres,
        #     "discogs": {
        #         "styles": discogs_styles,
        #         "genres": discogs_genres
        #     }
        # }
        # print(combined)

        # Combine results from both sources
        # combined_genres = sorted([genre.capitalize() for genre in set(wikipedia_genres + discogs_genres + discogs_styles)])

        combined_genres = list(set(wikipedia_genres + discogs_genres + discogs_styles))

        def capitalize_genre(genre):
            return genre.capitalize()

        capitalized_genres = list(map(capitalize_genre, combined_genres))
        updated_genres = [genre_mapping.get(genre, genre) for genre in capitalized_genres]
        expanded_genres = ensure_parent_genres(updated_genres, genre_hierarchy)

        def Remove(duplicate):
            final_list = []
            for num in duplicate:
                if num not in final_list:
                    final_list.append(num)
            return final_list

        deduped_genres = Remove(expanded_genres)
        sorted_genres = sorted(deduped_genres)
        joined_genres = '; '.join(sorted_genres)

        return joined_genres

# Example usage
# discogs_api_key = "your_discogs_api_key"
user_agent = "MyApp/0.1-dev"

genre_fetcher = GenreFetcher(user_agent)
# result = genre_fetcher.fetch_genres("Dead Milkmen", "Big Lizard In My Backyard")
# result = genre_fetcher.fetch_genres("Melvins", "Houdini")
# result = genre_fetcher.fetch_genres("Beatles", "Sgt. Pepper's Lonely Hearts Club Band")
# result = genre_fetcher.fetch_genres("Steely Dan", "Countdown To Ecstasy")
# result = genre_fetcher.fetch_genres("Boys Town Gang", "Disc Charge")
result = genre_fetcher.fetch_genres("Jethro Tull", "Minstrel in the gallery")


print(result)
