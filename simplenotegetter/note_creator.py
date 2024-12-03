import os, re
from datetime import datetime, timedelta
from note import Note

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

    def get_file_name(self, note):
        try:
            return note.file_name
        except:
            pass
        
        note_title = note.title
        unique_id = self.get_unique_id(note)

        if note_title == "":
            file_name = unique_id
        else:
            file_name = unique_id + " " + note_title

        # limit file name length to 255 characters
        note.file_name = file_name[:255].rstrip()
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
            link = "[[" + note.file_name + "]]"
            if note.file_name != note.title and note.title != "":
                link = "[[" + note.file_name + "|" + note.title + "]]"
            inbox_note.write("\n- " + link + ".")
        
        print('Created note "' + os.path.basename(note_path) + '"')
