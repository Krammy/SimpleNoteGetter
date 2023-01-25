import os, re
from datetime import datetime, timedelta
from settings import settings
from note import Note

id_getter = re.compile(r'^\d{12}')

def get_note_id(creation_datetime):
    return creation_datetime.strftime('%Y%m%d%H%M')

def ID_exists(id: str):
    for dirpath, dirnames, filenames in os.walk(settings.search_dir):
        for filename in filenames:
            my_id = id_getter.search(filename)
            if id == my_id:
                return True
    return False

def get_note_path(output, dt: datetime, name):
    note_id = get_note_id(dt)

    # avoids overriding existing files
    if ID_exists(note_id):
        dt += timedelta(minutes=1)
        return get_note_path(dt, output)
    
    if name == "":
        file_name = note_id + ".md"
    else:
        file_name = note_id + " " + name + ".md"
    file_location = os.path.join(output, file_name)
    
    return file_location

def create_note(output, note: Note):
    # get creation date
    note_path = get_note_path(output, note.creation_datetime, note.title)

    # create markdown file
    with open(note_path, 'w', encoding='utf-8') as new_note:
        new_note.write(note.content)

    print('Created note "' + os.path.basename(note_path) + '"')
