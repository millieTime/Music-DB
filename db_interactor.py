# Used to interact with Firebase.
import firebase_admin
from firebase_admin import credentials, firestore
# Get current directory. Helps for file access.
from pathlib import Path
# Gets the current directory
DIR = str(Path(__file__).resolve().parent)

class DB_Interactor():
    # These are the names of my top-level collections in Firestore.
    PANDORA_COLLECTION = u"Pandora Song Info"
    OWNED_COLLECTION = u"Owned Song Info"
    __db = None

    def __init__(self, filepath):
        # filepath is the path to the json certificate for firebase.
        assert filepath
        self.__db = self.get_database_ref(filepath)

    def get_database_ref(self, filepath):
        # filepath is the path to the json certificate for firebase.
        cred = credentials.Certificate(filepath)
        firebase_admin.initialize_app(cred)
        database = firestore.client()
        return database

    def is_ready(self):
        # If the database reference is set up, then this Interactor is ready.
        return not self.__db == None

    def display_doc_list(self, doc_list):
        # Tries to print a list of docs prettily.
        dict_list = [doc.to_dict() for doc in doc_list]
        if not dict_list:
            print("No songs found")
        else:
            # Print header
            keys = ["name", "artist", "album", "duration", "owned_status"]
            print("{:>50}  {:>36}  {:>40} {:>8} {}".format(*keys))
            # Print songs. Use .get in case a field is missing.
            for entry in dict_list:
                print("{:>50.50}  {:>36.36}  {:>40.40} {:^8} {:>6}".format(*[entry.get(key) or "" for key in keys]))

    def get_all_songs(self, collection_name, display = False):
        # Gets all song documents in the database, in alphabetical order.
        song_collection = self.__db.collection(collection_name)
        song_docs = [*song_collection.order_by(u"name").order_by(u"artist").get()]
        if not song_docs:
            print("No songs found")
        elif display:
            self.display_doc_list(song_docs)
        return song_docs

    def get_songs_that_match(self, song_info, collection_name, display = False):
        # Gets song documents that match the given song info from the database.
        if song_info.is_empty():
            # Nothing to filter by, just return all of them.
            return self.get_all_songs(collection_name, display)
        
        song_collection = self.__db.collection(collection_name)
        for key in song_info.get_keys():
            val = song_info.get(key)
            if val:
                song_collection = song_collection.where(key, u"==", val)
        
        song_docs = [*song_collection.get()]
        if not song_docs:
            print("No matches found")
        elif display:
            self.display_doc_list(song_docs)
        return song_docs

    def add_song(self, song_info, collection_name):
        # Adds a song to the database.
        self.__db.collection(collection_name).add(song_info.get_data_dict())

    def edit_owned(self, search_info, owned):
        # Updates whether I own a song. 'owned' must be "T" or "F".
        assert(owned in ["T", "F"])
        matches = self.get_songs_that_match(search_info, DB_Interactor.PANDORA_COLLECTION)
        if len(matches) == 0:
            print("Couldn't update.")
        elif len(matches) > 1:
            print("More than one match exists")
            self.display_doc_list(matches)
            if input("Update all (y/n)? ") == "y":
                for song in matches:
                    song_id = song.id
                    self.__db.collection(DB_Interactor.PANDORA_COLLECTION).document(song_id).update({u'owned_status': owned})
        else:
            song_id = matches[0].id
            self.__db.collection(DB_Interactor.PANDORA_COLLECTION).document(song_id).update({u'owned_status': owned})

    def remove_song(self, search_info, collection_name):
        # Removes a song (or songs) from the database.
        matches = self.get_songs_that_match(search_info, collection_name)
        if len(matches) == 0:
            print("Can't delete.")
        elif len(matches) > 1:
            print("More than one match exists")
            self.display_doc_list(matches)
            if input("Delete all (y/n)? ") == "y":
                for song in matches:
                    song_id = song.id
                    self.__db.collection(collection_name).document(song_id).delete()
        else:
            song_id = matches[0].id
            self.__db.collection(collection_name).document(song_id).delete()