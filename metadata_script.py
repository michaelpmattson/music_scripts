from mutagen.easyid3 import EasyID3
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from genre_fetcher import GenreFetcher

def get_directory():
    """Prompt the user for the directory containing the MP3 files with path completion."""
    directory = prompt("Enter the path to the album directory: ", completer=PathCompleter())
    if not os.path.isdir(directory):
        print("The provided directory does not exist.")
        return None
    return directory

def get_user_input():
    """Prompt the user for metadata updates."""
    new_title = input("Enter the new album title (leave blank to keep current): ")
    new_artist = input("Enter the new artist name (leave blank to keep current): ")
    new_genre = input("Enter the new genre name (leave blank to keep current): ")
    capitalize_titles = input("Do you want to capitalize all song titles? (Yes/No, default is Yes): ").strip().lower()

    return new_title, new_artist, new_genre, capitalize_titles not in ['no', 'n']

def update_metadata(file_path, new_title, new_artist, new_genre, capitalize_titles):
    """Update metadata for a single MP3 file."""
    audio = EasyID3(file_path)

    if new_title:
        audio['album'] = new_title
    if new_artist:
        audio['artist'] = new_artist
    if new_genre:
        audio['genre'] = new_genre
    if capitalize_titles:
        audio['title'] = audio['title'][0].title() if 'title' in audio else audio['title']

    audio.save()

def process_directory(directory, new_title, new_artist, new_genre, capitalize_titles):
    """Process all MP3 files in the directory and update their metadata."""
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            file_path = os.path.join(directory, filename)
            update_metadata(file_path, new_title, new_artist, new_genre, capitalize_titles)
    print("Metadata updated for all files.")

def main():
    directory = get_directory()
    if directory:
        new_title, new_artist, new_genre, capitalize_titles = get_user_input()
        process_directory(directory, new_title, new_artist, new_genre, capitalize_titles)

if __name__ == "__main__":
    main()
