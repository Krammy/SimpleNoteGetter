import os, re
from datetime import datetime, timedelta
from simplenotegetter.note import Note

class NoteCreator:
    def __init__(self, settings):
        self.settings = settings
    
    def get_note_id(self, creation_datetime):
        return creation_datetime.strftime('%Y%m%d%H%M')
    
    def ID_exists(self, id: str):
        for dirpath, dirnames, filenames in os.walk(self.settings.search_dir):
            for filename in filenames:
                my_id = filename[:12]
                if id == my_id:
                    return True
        return False
    
    def get_unique_id(self, note):
        dt = note.creation_datetime
        while True:
            note_id = self.get_note_id(dt)
            if not self.ID_exists(note_id):
                return note_id
            dt += timedelta(minutes=1)

    def get_note_path(self, note):
        name = note.title
        unique_id = self.get_unique_id(note)

        if name == "":
            file_name = unique_id
        else:
            file_name = unique_id + " " + name

        note.file_name = file_name
        file_location = os.path.join(self.settings.output, note.file_name + ".md")
        
        return file_location

    def create_note(self, note: Note):
        # get creation date
        note_path = self.get_note_path(note)

        # create markdown file
        with open(note_path, 'w', encoding='utf-8') as new_note:
            new_note.write(note.content)

        # add note to inbox file
        with open(self.settings.inbox_note, 'a') as inbox_note:
            # Append the line to the file
            link = "[[" + note.file_name + "]]"
            if note.file_name != note.title and note.title != "":
                link = "[[" + note.file_name + "|" + note.title + "]]"
            inbox_note.write("\n- " + link + ".")
        
        print('Created note "' + os.path.basename(note_path) + '"')
