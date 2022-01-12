# Music-DB
A simple project using python to interact with a Firebase Firestore database containing information on music I like.

## Overview

I'm building new skills interacting with cloud databases. My goal is to learn how to create, edit, delete, and query entries from the database, in addition to other useful commands.

I love Pandora, and I've "liked" over 1000 songs on the platform. But it can be really tedious scrolling through the list of songs I've liked (especially when they're loaded in small chunks)! I wanted to set my own terms for when and how I can check on music I like. In addition, I'd like to add functionality to compare the set of songs I like on Pandora with the set of songs I currently own in order to generate a set of songs I'd like to buy in the future.

## File Descriptions

* get_songs.js - A js script from pastebin.com that will gather all info on liked and disliked songs. To use, navigate to Pandora -> profile -> thumbs up. Open the console via right-click -> Inspect Element -> console. Paste this script in the console and hit enter. After several seconds of processing a message will be printed contianing tab-delimited information on all your liked and disliked songs. Save it to a .txt file in the same directory as music_db.py.

* music_db.py - A python script to interact with the Firestore database.

## Cloud Database

This project uses a Firestore Firebase database named My Music DB.

## Development Environment

This project uses Python 3.8.7 and the pip package firebase-admin 5.0.3.

## Useful Websites

* [Firebase Docs](https://firebase.google.com/docs/guides)
* [Javascript to get a list of liked Pandora songs](https://pastebin.com/9br3VZjX)

## Future Work

* Access database
* Add items to database
* Query items from database
* Edit/delete items in the database
* Scan local directory for the music I own
* Compare locally owned music with music I like.
* Automatically update cloud database.