# Music-DB
A simple project using python to interact with a Firebase Firestore database containing information on music I like.

## Overview

I'm building new skills interacting with cloud databases. My goal is to learn how to create, edit, delete, and query entries from the database, in addition to other useful commands.

I love Pandora, and I've "liked" over 1000 songs on the platform. But it can be really tedious scrolling through the list of songs I've liked (especially when they're loaded in small chunks)! I wanted to set my own terms for when and how I can check on music I like. In addition, I'd like to add functionality to compare the set of songs I like on Pandora with the set of songs I currently own in order to generate a set of songs I'd like to buy in the future.

To use this software, you'll need to do the following:
1. Set up a free Firebase account. This includes creating a pair of collections and saving your .json certification file.

2. There are two variables in the db_interactor.py file that you'll need to update based on your database. They are PANDORA_COLLECTION and OWNED_COLLECTION. Replace their values with the names of your Pandora collection and owned music collection.

3. Copy the code in the get_songs.js file and navigate to your liked songs on Pandora (it's in your profile) in a web browser. Open the browser console, paste in the code, and hit enter. The console should begin populating with your stations, and then a single message containing all your liked music. Copy the full contents of that message and save it to a .txt file in the same folder as the rest of these python scripts.

3. Run music_db.py. It should load up a nice menu for you to interact with and several options. You can pick any of them in any order and fill out any requested information to view, selectively view, add, sync, update, and remove songs from your database.

To sync the songs you've liked on Pandora, you'll need to have the .txt file in the same folder as the python scripts. Enter the file's name, and they should all be synchronized automatically.

To sync the songs you own, you'll need to provide the complete path to the folder that contains all the music you have downloaded. Currently, only .wav files following a specific naming convention (author - album - name.wav) and .mp3 files are accepted.

**Here is a demonstration video of the program:**
[Software Demo Video](https://youtu.be/hmGcvTf1F94)
## File Descriptions

* get_songs.js - A js script from pastebin.com that will gather all info on liked and disliked songs. To use, navigate to Pandora -> profile -> thumbs up. Open the console via right-click -> Inspect Element -> console. Paste this script in the console and hit enter. After several seconds of processing a message will be printed contianing tab-delimited information on all your liked and disliked songs. Save it to a .txt file in the same directory as music_db.py.

* music_db.py - A python script to provide an easy interface for the user to interact with the database.

* db_interactor.py - a class that handles the interface between music_db and the actual cloud database.

* handle_files.py - a par of functions that handle crawling through a folder's contents and picking out music files and their information.

* song_info.py - a class designed to hold information on a song.

## Cloud Database

This project uses a Firestore Firebase database named My Music DB. It has two collections named Pandora Song Info and Owned Song Info. Each contain a list of documents with randomly assigned ids. The documents in Owned Song Info contain fields for the song's name, artist, album, and duration. The documents in Pandora Song Info contain an additional flag for whether they are owned or not.

## Development Environment

All code was written and tested in Visual Studio Code 1.63.2 on Windows. Firebase and Pandora were accessed via Firefox Browser for Windows.

This project uses Python 3.8.7 and the pip packages firebase-admin 5.0.3 and mutagen 1.45.1.

## Useful Websites

* [Firebase Docs](https://firebase.google.com/docs/guides)
* [Javascript to get a list of liked Pandora songs](https://pastebin.com/9br3VZjX)
* [Mutagen Docs](https://mutagen.readthedocs.io/en/latest/)

## Future Work

* Compare locally owned music with music I like to get a list of songs I still need to buy.
* Use selenium or other to automatically grab the list of liked songs from Pandora.
* Automatically update cloud database at regular intervals of time.
