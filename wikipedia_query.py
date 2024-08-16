import requests
import re
from infobox_parser import InfoboxParser

def fetch_wikipedia_genre(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "revisions",
        "rvprop": "content",
        "rvsection": 0  # Often, genre is in the first section (infobox)
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract the page content
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))  # Get the first (and usually only) page
    content = page.get("revisions", [{}])[0].get('*', '')

    # Print initial content (for debugging)
    print("=== Initial Content ===")
    print(content[:2000])  # Print the first 2000 characters for inspection

    # Instantiate the InfoboxParser and parse the content
    parser = InfoboxParser(content)
    infobox_data = parser.parse_infobox()

    # Pretty print the parsed infobox data
    print("\n=== Parsed Infobox Data ===")
    from pprint import pprint
    pprint(infobox_data)

    # Extract genre information
    genre_field = infobox_data.get("genre", "")
    genres = []

    if genre_field:
        # Remove comments
        genre_field = re.sub(r'<!--.*?-->', '', genre_field, flags=re.DOTALL)

        # Remove reference tags (including multiline <ref> tags)
        genre_field = re.sub(r'<ref[^>]*>[^<]*(?:<[^<]*>)*<\/ref>', '', genre_field, flags=re.DOTALL)

        # Handle hlist template (removing '{{hlist|' and '}}')
        genre_field = re.sub(r'\{\{hlist\|', '', genre_field)
        genre_field = genre_field.replace('}}', '').strip()

        # Extract genre entries, handling wikitext links
        genres = re.findall(r'\[\[(?:[^|\]]*\|)?([^]]+)\]\]', genre_field)
        genres = [genre.strip() for genre in genres if genre]

    # Print final genres (for debugging)
    print("\n=== Final Genres ===")
    print(genres)

    return genres

# Example: Fetch genre for the album "Thriller (Michael Jackson album)"
# album_name = "Thriller_(album)"
# album_genre = fetch_wikipedia_genre(album_name)
# print(f"Album Genre: {album_genre}")

# Example: Fetch genre for a song "Billie Jean"
# song_name = "Billie_Jean"
# song_genre = fetch_wikipedia_genre(song_name)
# print(f"Song Genre: {song_genre}")

# Example: Fetch genre for the album "Lysol (Melvins album)"
album_name = "Lysol_(album)"
album_genre = fetch_wikipedia_genre(album_name)
print(f"Album Genre: {album_genre}")
