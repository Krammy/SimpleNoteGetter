import simplenote, os
from simplenotegetter.note_creator import NoteCreator
from simplenotegetter.note import Note
from simplenotegetter.settings import Settings

# https://simplenotepy.readthedocs.io/en/latest/api.html#simperium-api-note-object

def sort_by_creation_date(note: Note):
    return note.creation_datetime

def fetch_simplenote_notes(settings_path):
    print("Logging into Simplenote...")
    settings = Settings(settings_path)
    
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
    
    nc = NoteCreator(settings)
    
    print("Creating " + str(len(my_notes)) + " notes...")
    for note in my_notes:
        # create note
        nc.create_note(note)
        # trash note in simplenote
        sn.trash_note(note.key)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(current_dir, 'settings.json')
    fetch_simplenote_notes(settings_path)
