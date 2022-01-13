import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
# Gets the current directory
DIR = str(Path(__file__).resolve().parent)


class SongInfo():
    # A struct to represent a song and its information
    name = ""
    artist = ""
    album = ""
    def __init__(self, artist = "", album = "", name = ""):
        self.artist = artist
        self.album = album
        self.name = name

def get_database_ref():
    file_name = DIR + "\\cert.json" ##### REPLACE WITH YOUR ADMIN SDK CERT FILENAME.
    cred = credentials.Certificate(file_name)
    firebase_admin.initialize_app(cred)
    database = firestore.client()
    return database

def add_entry(db, song_info):
    # Adds a song to the database.
    db.collection(u"Pandora Song Info").add({
        u"artist": song_info.artist,
        u"album": song_info.album,
        u"name": song_info.name
    })

def display_doc_list(doc_list):
    # prints a list of docs prettily.
    dict_list = [doc.to_dict() for doc in doc_list]
    if not dict_list:
        print("No songs found")
    else:
        print("{:>15}  {:>15}  {:>15}".format("Name", "Album", "Artist"))
        for entry in dict_list:
            print("{:>15}  {:>15}  {:>15}".format(entry["name"], entry["album"], entry["artist"]))

def get_songs(db):
    # Gets all song documents in the database.
    song_collection = db.collection(u"Pandora Song Info")
    song_docs = [doc.get() for doc in song_collection.list_documents()]
    if not song_docs:
        print("No songs found")
    return song_docs

def get_matches(db, song_info):
    # Gets song documents that match the given song info from the database.
    song_collection = db.collection(u"Pandora Song Info")
    if song_info.artist:
        song_collection = song_collection.where(u"artist", u"==", song_info.artist)
    if song_info.album:
        song_collection = song_collection.where(u"album", u"==", song_info.album)
    if song_info.name:
        song_collection = song_collection.where(u"name", u"==", song_info.name)
    
    song_docs = [*song_collection.get()]
    if not song_docs:
        print("No matches found")
    return song_docs

def edit_song(db, search_song_info, updated_song_info):
    # Edits a song's info
    matches = get_matches(db, search_song_info)
    if len(matches) == 0:
        print("Cannot update nonexistent song.")
    elif len(matches) > 1:
        print("Too many matches. Be more specific.")
        print("Matched songs:")
        display_doc_list(matches)
    else:
        song_id = matches[0].id
        if updated_song_info.artist:
            db.collection(u"Pandora Song Info").document(song_id).update({u'artist': updated_song_info.artist})
        if updated_song_info.album:
            db.collection(u"Pandora Song Info").document(song_id).update({u'album': updated_song_info.album})
        if updated_song_info.name:
            db.collection(u"Pandora Song Info").document(song_id).update({u'name': updated_song_info.name})
        print("Successfully updated song info.")
        
def remove_song(db, search_song_info):
    # Removes a song (or songs) from the database.
    matches = get_matches(db, search_song_info)
    if len(matches) == 0:
        print("No such song exists.")
    elif len(matches) > 1:
        print("More than one match exists")
        display_doc_list(matches)
        if input("delete all (y/n)? ") == "y":
            for song in matches:
                song_id = song.id
                db.collection(u"Pandora Song Info").document(song_id).delete()
    else:
        # Delete the one song.
        song_id = matches[0].id
        db.collection(u"Pandora Song Info").document(song_id).delete()

def build_song_info():
    print("For any field, leave it blank to not search by it.")
    name = input("What is the song's name? ")
    artist = input("What is the song's artist? ")
    album = input("What is the song's album? ")
    return SongInfo(artist, album, name)

def main():
    database = get_database_ref()
    selection = -1
    while selection != 7:
        print("Select an option")
        print("\t1: View songs")
        print("\t2: View specific song(s)")
        print("\t3: Add default song")
        print("\t4: Add song")
        print("\t5: Edit song")
        print("\t6: Remove song(s)")
        print("\t7: Exit")
        selection = input(">")

        if selection.isdigit() and 1 <= int(selection) <= 7:
            selection = int(selection)
        else:
            print("Invalid input")
            continue

        if selection == 1:
            display_doc_list(get_songs(database))
        elif selection == 2:
            print("Enter the information of the song(s) to search for.")
            song_info = build_song_info()
            display_doc_list(get_matches(database, song_info))
        elif selection == 3:
            song_info = SongInfo("artist_name", "album_name", "song_name")
            add_entry(database, song_info)
        elif selection == 4:
            print("Enter the information of the song to add.")
            song_info = build_song_info()
            add_entry(database, song_info)
        elif selection == 5:
            print("Enter the information of the song to search for.")
            song_info = build_song_info()
            print("Enter the song's updated information.")
            updated_info = build_song_info()
            edit_song(database, song_info, updated_info)
        elif selection == 6:
            print("Enter the information of the song(s) to search for.")
            song_info = build_song_info()
            remove_song(database, song_info)


if __name__ == "__main__":
    main()