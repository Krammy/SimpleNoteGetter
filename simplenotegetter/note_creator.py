import os, re
from datetime import datetime, timedelta
from note import Note
from uniqueidgetter import unique_id_getter

class NoteCreator:
    def __init__(self, settings):
        self.settings = settings
    
    def get_file_name(self, note):
        try:
            return note.file_name
        except:
            pass
        
        note_title = note.title
        unique_id = unique_id_getter.get_unique_id(note.creation_datetime)

        if note_title == "":
            file_name = unique_id
        else:
            file_name = unique_id + " " + note_title

        # limit file name length to 250 characters (255 max, 250 to be safe)
        note.file_name = file_name[:250].rstrip()
        return note.file_name

    def get_note_path(self, note):
        return os.path.join(self.settings.output, self.get_file_name(note) + ".md")

    def create_note(self, note: Note):
        # get creation date
        note_path = self.get_note_path(note)

        # create markdown file
        with open(note_path, 'w', encoding='utf-8') as new_note:
            new_note.write(note.content)

        # add note to inbox file
        with open(self.settings.inbox_note, 'a', encoding='utf-8') as inbox_note:
            # Append the line to the file
            link = "[](<" + note.file_name + ".md>]"
            if note.file_name != note.title and note.title != "":
                link = "[" + note.title + "](<" + note.file_name + ".md>)"
            inbox_note.write("\n- " + link + ".")
        
        print('Created note "' + os.path.basename(note_path) + '"')
