from pathlib import Path
import re
from threading import local
from db_interactor import DB_Interactor
from song_info import SongInfo
# Gets the current directory
DIR = str(Path(__file__).resolve().parent)

STATIONS_OF_INTEREST = ["Seven Lions Radio",
                        "Imagine Dragons Radio",
                        "Radioactive Radio",
                        "Turbo Penguin Radio",
                        "The Glitch Mob Radio",
                        "GameChops & Holder Radio"]
CERT_FILE_PATH = DIR + "\\" + "cert.json" ##### REPLACE WITH YOUR ADMIN SDK CERT FILENAME.

def view_songs(db_interactor):
    # Display all songs.
    db_interactor.get_all_songs(True)

def view_certain_songs(db_interactor):
    # Display songs that match user-entered info.
    print("Enter the information of the song(s) to search for.")
    song_info = SongInfo()
    song_info.build_song_info()
    db_interactor.get_songs_that_match(song_info, True)

def add_song(db_interactor):
    # Add a song to the database based on user-entered info.
    print("Enter the information of the song to add.")
    song_info = SongInfo()
    song_info.build_song_info()
    db_interactor.add_song(song_info)

def insert_song(song, lst):
    # Insert a song_info item into a list of song_infos alphabetically.
    # Find the correct index.
    up = 0
    down = len(lst)
    while up < down:
        mid = (up + down) // 2
        if lst[mid] == song:
            # Song already exists - Don't insert!
            return
        elif lst[mid] < song:
            up = mid + 1
        else:
            down = mid
    # Swap all the elements down one so song is at the right spot.
    lst.append(song)
    while up < len(lst) - 1:
        lst[up], lst[-1] = lst[-1], lst[up]
        up += 1


def sync_with_file(db_interactor):
    # Add all songs in a tab-spaced file to the database.

    ### STEP 1: Get songs from the database.
    remote_doc_list = db_interactor.get_all_songs()
    remote_song_info_list = [SongInfo(info_dict = doc.to_dict()) for doc in remote_doc_list]

    ### STEP 2: Get songs from the file.
    local_song_info_list = []
    file_name = DIR + "\\" + input("What is the file name? ")
    try:
        with open(file_name, "r") as song_file:
            # Skip the header line.
            next(song_file)
            # Read file info and add to database.
            for line in song_file.readlines()[1:]:
                # Take off the \n and split at tabs.
                line_data = line[:-1].split("\t")
                # We only want songs from some of the stations.
                if len(line_data) == 5 and line_data[3] in STATIONS_OF_INTEREST:
                    song_info = SongInfo(
                        artist=line_data[0],
                        album=line_data[1],
                        name=line_data[2],
                        duration=line_data[4],
                        owned_status="F"
                    )
                    # Insert the song_info item alphabetically.
                    insert_song(song_info, local_song_info_list)
        print("Successfully read songs from the file.")
    except Exception as e:
        print(e)
        print("Unable to load songs from file, returning to menu.")
        return
    
    ### STEP 3: Compare local song to remote list.
    local_index = 0
    remote_index = 0
    while local_index < len(local_song_info_list) and remote_index < len(remote_song_info_list):
        if local_song_info_list[local_index] == remote_song_info_list[remote_index]:
            # Existed in both spaces, next.
            local_index += 1
            remote_index += 1
        elif local_song_info_list[local_index] < remote_song_info_list[remote_index]:
            # Remote missing a song, need to add a local song to the remote database.
            db_interactor.add_song(local_song_info_list[local_index])
            local_index += 1
        else:
            # Remote has an extra song, need to remove a remote song from the remote database.
            db_interactor.remove_song(remote_song_info_list[remote_index])
            remote_index += 1
    while local_index < len(local_song_info_list):
        # Add any remaining songs to the remote database.
        db_interactor.add_song(local_song_info_list[local_index])
        local_index += 1
    while remote_index < len(remote_song_info_list):
        # Remove any remaining songs from the remote database.
        db_interactor.remove_song(remote_song_info_list[remote_index])
        remote_index += 1

    print("Successfully updated remote database.")

def edit_owned(db_interactor):
    # Edit the owned status of a song.
    print("Enter the information of the song to search for.")
    song_info = SongInfo()
    song_info.build_song_info()
    owned = input("\nIs the song owned (T/F)? ")
    if owned in ["T", "F"]:
        db_interactor.edit_owned(song_info, owned)
    else:
        print("Invalid input, returning to menu.")

def remove_song(db_interactor):
    # Remove a song or songs.
    print("Enter the information of the song(s) to search for.")
    song_info = SongInfo()
    song_info.build_song_info()
    db_interactor.remove_song(song_info)

def get_user_request(options):
    # Figure out what the user wants to do from the list of options.
    print("\nSelect an option")
    # Print all the options
    for indx in range(len(options)):
        print(f"\t{indx+1}: {options[indx]}")

    # Request a selection until it's valid.
    selection = input(">")
    while not selection.isdigit() or int(selection) < 1 or int(selection) > len(options):
            print("Invalid input")
            selection = input(">")
    
    return int(selection)

def main():
    # Set up the database interactor.
    db_interactor = DB_Interactor(CERT_FILE_PATH)
    if not db_interactor.is_ready():
        return

    # Set up the menu options.
    option_list = [
        "View songs",
        "View specific song(s)",
        "Add song",
        "Sync songs with file",
        "Edit owned status",
        "Remove song(s)",
        "Exit", # Does not line up with a function, because it needs no function.
    ]
    function_list = [
        view_songs,
        view_certain_songs,
        add_song,
        sync_with_file,
        edit_owned,
        remove_song,
    ]

    # Interact with the user.
    selection = get_user_request(option_list)
    while selection != len(option_list):
        # User has made their choice, call the function!
        function_list[selection - 1](db_interactor)
        # Ask what they want to do now.
        selection = get_user_request(option_list)
    
    print("Goodbye")

if __name__ == "__main__":
    main()