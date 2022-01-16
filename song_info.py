class SongInfo():
    # A simple class to represent a song and its information
    __data_dict = None
    __is_empty = True

    def __init__(self, name = "", album = "", artist = "", duration = "", owned_status = "", info_dict = None):
        # Initializes the SongInfo object with specified values.
        # Note, specified values will override values in info_dict, if provided.
        self.__data_dict = {
            "name":         name         or (info_dict.get("name") if info_dict else ""),
            "album":        album        or (info_dict.get("album") if info_dict else ""),
            "artist":       artist       or (info_dict.get("artist") if info_dict else ""),
            "duration":     duration     or (info_dict.get("duration") if info_dict else ""),
            "owned_status": owned_status or (info_dict.get("owned_status") if info_dict else "")
        }

        if any(self.__data_dict.values()):
            self.__is_empty = False

    def is_empty(self):
        # Whether this SongInfo has any useful information
        return self.__is_empty
    
    def get_data_dict(self):
        # Returns a copy of the data_dict to prevent modification.
        return self.__data_dict.copy()

    def get(self, key):
        # Returns the requested value from the __data_dict
        if key in self.__data_dict.keys():
            return self.__data_dict[key]

    def get_keys(self):
        # Returns a list of keys in the __data_dict
        return self.__data_dict.keys()

    def build_song_info(self):
        # Get values for this SongInfo from the user.
        print("For any field, leave it blank if not important.")
        for key in self.__data_dict.keys():
            self.__data_dict[key] = input("What is the song's " + key + "? ")
        
        if any(self.__data_dict.values()):
            self.__is_empty = False

    def __eq__(self, other):
        # Defines whether this is equal to another SongInfo.
        if type(other) != SongInfo:
            return NotImplemented
        return (other.get("name") == self.get("name")
                and other.get("artist") == self.get("artist"))

    def __lt__(self, other):
        # Defines whether this is less than another SongInfo.
        if type(other) != SongInfo:
            return NotImplemented
        if self.get("name") != other.get("name"):
            return self.get("name") < other.get("name")
        if self.get("artist") != other.get("artist"):
            return self.get("artist") < other.get("artist")
        # At this point, they're pretty much the same song, so no.
        return False