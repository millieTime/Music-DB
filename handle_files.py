import os
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from song_info import SongInfo
# Gets the current directory
DIR = str(Path(__file__).resolve().parent)
TITLE_TAG = "TIT2"
ALBUM_TAG = "TALB"
CONTRIBUTING_ARTIST_TAG = "TPE1"
ALBUM_ARTIST_TAG = "TPE2"

def file_to_SongInfo(file_path):
    # Get the info from the song file_name.
    # Might have to parse filename if .wav,
    # Otherwise just parse the tag info with eyed3.
    if file_path[-4:] == ".wav":
        # Parse file name.
        file_name = file_path.split("\\")[-1]
        file_name_parts = file_name[:-4].split("-")
        name = file_name_parts[-1].strip()
        artist = ""
        album = ""
        duration = int(WAVE(file_path).info.length) or ""
        if len(file_name_parts) > 1:
            artist = file_name_parts[0].strip()
        if len(file_name_parts) > 2:
            album = file_name_parts[-2].strip()
        song_info = SongInfo(name = name, artist = artist, album = album, duration = duration)
        return song_info
    elif file_path[-4:] == ".mp3":
        # Get info from tags.
        mp3_file = MP3(file_path)
        name_tag = mp3_file.get(TITLE_TAG)
        album_tag = mp3_file.get(ALBUM_TAG)
        album_artist_tag = mp3_file.get(ALBUM_ARTIST_TAG)
        contributing_artist_tag = mp3_file.get(CONTRIBUTING_ARTIST_TAG)
        name = ""
        album = ""
        artist = ""
        if name_tag and name_tag.text[0]:
            name = name_tag.text[0]
        if album_artist_tag and album_artist_tag.text[0]:
            artist = album_artist_tag.text[0]
        elif contributing_artist_tag and contributing_artist_tag.text[0]:
            artist = contributing_artist_tag.text[0]
        if album_tag and album_tag.text[0]:
            album = album_tag.text[0]
        song_info = SongInfo(name=name, album=album, artist=artist, duration=int(mp3_file.info.length))
        return song_info
    else:
        print("Skipping file with unknown filetype:", file_path)

def folder_to_file_list(folder_path):
    # Processes a single folder. All subfolders are searched as well.
    # Adds all found .mp3 and .wav file paths to a list and returns it.
    file_system = [(root, files) for root, dirs, files in os.walk(folder_path)]
    path_list = []
    for path, files in file_system:
        for file in files:
            if file[-4:] in [".mp3", ".wav"]:
                path_list.append(path + "\\" + file)
    return path_list