import os
from note import get_note_id

def get_note_path(output, epoch_time, name):
    note_id = get_note_id(epoch_time)
    if name == "":
        file_name = note_id + ".md"
    else:
        file_name = note_id + " " + name + ".md"
    file_location = os.path.join(output, file_name)
    
    # avoids overriding existing files
    if os.path.exists(file_location):
        epoch_time += 60
        return get_note_path(output, epoch_time, name)
    
    return file_location

def create_note(output, note):
    # get creation date
    note_path = get_note_path(output, note.creation_date, note.title)

    # create markdown file
    with open(note_path, 'w') as new_note:
        new_note.write(note.content)

    print('Created note "' + os.path.basename(note_path) + '"')
