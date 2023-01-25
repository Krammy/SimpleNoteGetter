import os
import json
import simplenote
from datetime import datetime
from note_creator import create_note
from note import Note
from settings import settings

# https://simplenotepy.readthedocs.io/en/latest/api.html#simperium-api-note-object

def sort_by_creation_date(note):
    return note.creation_date

if __name__ == "__main__":
    print("Logging into Simplenote...")
    sn = simplenote.Simplenote(settings.user, settings.password)

    print("Fetching notes...")
    simplenote_notes = sn.get_note_list(data=True)[0]

    my_notes = []
    
    # get all notes
    for note in simplenote_notes:
        if note["deleted"] == True or note["content"] == "":
            continue
        my_notes.append(Note(note))

    print("Sorting " + str(len(my_notes)) + " notes...")
    # sort notes list by creation date
    my_notes.sort(key = sort_by_creation_date)

    print("Creating " + str(len(my_notes)) + " notes...")
    for note in my_notes:
        # create note
        create_note(settings["output"], note)
        # trash note in simplenote
        sn.trash_note(note.key)
