import os, re
from datetime import datetime, timedelta
from simplenotegetter.note import Note

id_getter = re.compile(r'^\d{12}')

class NoteCreator:
    def __init__(self, settings):
        self.settings = settings
    
    def get_note_id(self, creation_datetime):
        return creation_datetime.strftime('%Y%m%d%H%M')
    
    def ID_exists(self, id: str):
        if hasattr(self, '_file_ids'):
            return id in self._file_ids
        self._file_ids = []
        for dirpath, dirnames, filenames in os.walk(self.settings.search_dir):
            for filename in filenames:
                my_id = id_getter.search(filename)
                if my_id == None:
                    continue
                self._file_ids.append(my_id.group())
        return id in self._file_ids
    
    def get_note_path(self, dt: datetime, name):
        note_id = self.get_note_id(dt)

        # avoids overriding existing files
        if self.ID_exists(note_id):
            dt += timedelta(minutes=1)
            return self.get_note_path(dt, name)
        
        # ID does not exist, insert into self._file_ids to avoid naming conflicts
        self._file_ids.append(note_id)
        
        if name == "":
            file_name = note_id + ".md"
        else:
            file_name = note_id + " " + name + ".md"
        file_location = os.path.join(self.settings.output, file_name)
        
        return file_location
    
    def create_note(self, note: Note):
        # get free note path
        note_path = self.get_note_path(note.creation_datetime, note.title)
        
        # create markdown file
        with open(note_path, 'w', encoding='utf-8') as new_note:
            new_note.write(note.content)

        print('Created note "' + os.path.basename(note_path) + '"')
