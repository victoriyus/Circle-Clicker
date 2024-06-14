"""
Date: 06/14/2024
Name: Song Class
Description: Defines the song class and creates song objects for Circle Clicker
"""
import json

# songs path
path = "res/songs/"


class song():

    def __init__(self, song_name, bpm, offset):

        self.song_directory = song_name
        self.bpm = bpm
        self.offset = offset
        self.name = song_name

        # Load song notes
        with open(path + f"{song_name}/notes.json") as f:

            data = json.load(f)

        self.note_list = data["notes"]

    # Get notes at an index
    def get_current_notes(self, index):

        return self.note_list[index]


# Making song objects ---------------------------------------------

song_1 = song("stompin_at_the_savoy", 154.5, 0)
