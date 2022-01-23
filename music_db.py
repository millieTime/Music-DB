from pathlib import Path
from db_interactor import DB_Interactor as DBI
from song_info import SongInfo
from handle_files import folder_to_file_list, file_to_SongInfo
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
    # Display all songs in the chosen collection.
    user_choice = input("View owned (o) or pandora (p) songs? ")
    if user_choice != "o" and user_choice != "p":
        print("Invalid input, returning to menu. . .")
        return
    if user_choice == "o":
        db_interactor.get_all_songs(DBI.OWNED_COLLECTION, True)
    else: #user_choice == "p"
        db_interactor.get_all_songs(DBI.PANDORA_COLLECTION, True)

def view_certain_songs(db_interactor):
    # Display songs that match user-entered info in the chosen collection.
    user_choice = input("View from owned (o) or pandora (p) songs? ")
    if user_choice != "o" and user_choice != "p":
        print("Invalid input, returning to menu. . .")
        return
    print("Enter the information of the song(s) to search for.")
    song_info = SongInfo()
    song_info.build_song_info()
    if user_choice == "o":
        db_interactor.get_songs_that_match(song_info, DBI.OWNED_COLLECTION, True)
    else: #if user_choice == "p":
        db_interactor.get_songs_that_match(song_info, DBI.PANDORA_COLLECTION, True)

def add_song(db_interactor):
    # Add a song to the chosen collection based on user-entered info.
    user_choice = input("Add to owned (o) or pandora (p) songs? ")
    if user_choice != "o" and user_choice != "p":
        print("Invalid input, returning to menu. . .")
        return
    print("Enter the information of the song to add.")
    song_info = SongInfo()
    song_info.build_song_info()
    if user_choice == "o":
        db_interactor.add_song(song_info, DBI.OWNED_COLLECTION)
    else: #if user_choice == "p":
        db_interactor.add_song(song_info, DBI.PANDORA_COLLECTION)

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

def get_diffs(remote_song_info_list, local_song_info_list):
    # Looks through two alphabetical lists of SongInfo. Returns two lists noting differences.
    # The first list contains songs the remote list is missing.
    # The local list contains songs the local list is missing.
    remote_missing = []
    local_missing = []
    remote_index = 0
    local_index = 0
    while remote_index < len(remote_song_info_list) and local_index < len(local_song_info_list):
        if remote_song_info_list[remote_index] == local_song_info_list[local_index]:
            # Existed in both spaces, next.
            local_index += 1
            remote_index += 1
        elif remote_song_info_list[remote_index] > local_song_info_list[local_index]:
            # Remote list is missing a song.
            remote_missing.append(local_song_info_list[local_index])
            local_index += 1
        else:
            # Local list is missing a song.
            local_missing.append(remote_song_info_list[remote_index])
            remote_index += 1
    # Collect all remaining songs the remote list is missing.
    remote_missing += local_song_info_list[local_index:]
    # Collect all remaining songs the local list is missing.
    local_missing += remote_song_info_list[remote_index:]

    return remote_missing, local_missing

def sync_with_file(db_interactor):
    # Add all songs in a tab-spaced file to the Pandora collection.
    ### STEP 1: Get songs from the Pandora collection.
    remote_doc_list = db_interactor.get_all_songs(DBI.PANDORA_COLLECTION)
    remote_song_info_list = [SongInfo(info_dict = doc.to_dict()) for doc in remote_doc_list]

    ### STEP 2: Get songs from the file.
    local_song_info_list = []
    file_name = DIR + "\\" + input("What is the file name? ")
    try:
        with open(file_name, "r") as song_file:
            # Skip the header line.
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
    
    ### STEP 3: Compare local songs to remote list.
    remote_missing, local_missing = get_diffs(remote_song_info_list, local_song_info_list)
    for song_info in remote_missing:
        db_interactor.add_song(song_info, DBI.PANDORA_COLLECTION)
    for song_info in local_missing:
        db_interactor.remove_song(song_info, DBI.PANDORA_COLLECTION)
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
    user_choice = input("Remove from owned (o) or pandora (p) songs? ")
    if user_choice != "o" and user_choice != "p":
        print("Invalid input, returning to menu. . .")
        return
    print("Enter the information of the song(s) to search for.")
    song_info = SongInfo()
    song_info.build_song_info()
    if user_choice == "o":
        db_interactor.remove_song(song_info, DBI.OWNED_COLLECTION)
    elif user_choice == "p":
        db_interactor.remove_song(song_info, DBI.PANDORA_COLLECTION)

def sync_owned_songs(db_interactor):
    # Updates the owned music database to match all mp3s and wavs in the specified folder and subfolders.
    ### STEP 1: Get songs from the Owned collection.
    remote_doc_list = db_interactor.get_all_songs(DBI.OWNED_COLLECTION)
    remote_song_info_list = [SongInfo(info_dict = doc.to_dict()) for doc in remote_doc_list]

    ### STEP 2: Get songs from the local folder.
    folder_path = input("Enter the complete path to the folder of music to synchronize with: ")
    file_list = folder_to_file_list(folder_path)
    print("Successfully scraped folder, found", len(file_list), "songs.")
    local_song_info_list = []
    for file in file_list:
        song_info = file_to_SongInfo(file)
        insert_song(song_info, local_song_info_list)
    
    ### STEP 3: Add to the Owned collection any songs it's missing.
    # I assume I will not lose music over time, but that it will continue to grow.
    # Liked songs can disappear, which is why it is valid to remove them from
    # the Pandora collection on sync.
    remote_missing, _ = get_diffs(remote_song_info_list, local_song_info_list)
    for song_info in remote_missing:
        db_interactor.add_song(song_info, DBI.OWNED_COLLECTION)
    print("Successfully added songs to remote database.")
    
    ### STEP 4: Update the owned status of the Pandora collection.
    pass
    

def get_unowned_songs(db_interactor):
    pass
    
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
    db_interactor = DBI(CERT_FILE_PATH)
    if not db_interactor.is_ready():
        return

    # Set up the menu options.
    option_list = [
        "View songs",
        "View specific song(s)",
        "Add song",
        "Sync Pandora songs with file",
        "Edit owned status",
        "Remove song(s)",
        "Sync owned songs",
        #"View unowned songs",
        "Exit", # Does not line up with a function, because it needs no function.
    ]
    function_list = [
        view_songs,
        view_certain_songs,
        add_song,
        sync_with_file,
        edit_owned,
        remove_song,
        sync_owned_songs
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