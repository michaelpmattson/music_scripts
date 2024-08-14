from mutagen.easyid3 import EasyID3
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

# Prompt the user for the directory containing the MP3 files with path completion
directory = prompt("Enter the path to the album directory: ", completer=PathCompleter())

# Ensure the directory exists
if not os.path.isdir(directory):
    print("The provided directory does not exist.")
else:
    new_title = input("Enter the new album title (leave blank to keep current): ")
    new_artist = input("Enter the new artist name (leave blank to keep current): ")
    new_genre = input("Enter the new genre name (leave blank to keep current): ")

    # Ask if the user wants to capitalize all song titles
    capitalize_titles = input("Do you want to capitalize all song titles? (Yes/No, default is Yes): ").strip().lower()

    # Set default to 'yes' if input is blank or not 'no'
    if capitalize_titles not in ['no', 'n']:
        capitalize_titles = True
    else:
        capitalize_titles = False

    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            file_path = os.path.join(directory, filename)
            audio = EasyID3(file_path)

            if new_title:
                audio['album'] = new_title

            if new_artist:
                audio['artist'] = new_artist

            if new_genre:
                audio['genre'] = new_genre

            # Capitalize the title if the user opts in
            if capitalize_titles:
                audio['title'] = audio['title'][0].title() if 'title' in audio else audio['title']

            audio.save()

    print("Metadata updated for all files.")
