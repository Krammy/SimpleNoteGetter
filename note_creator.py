import os
from note import get_note_id
from note import get_title

def get_fixed_content(content):
    # replaces weird characters with equivalent characters.
    replacements = [
        ("’", "'"),
        ("‘", "'"),
        ('”', '"'),
        ('“', '"'),
        ("�", "--")
    ]

    for replacement in replacements:
        content = content.replace(replacement[0], replacement[1])
    
    return content

def get_note_path(output, epoch_time, name):
    note_id = get_note_id(epoch_time)
    if name == "":
        file_name = note_id + ".md"
    else:
        file_name = note_id + " - " + name + ".md"
    file_location = os.path.join(output, file_name)
    
    # avoids overriding existing files
    if os.path.exists(file_location):
        epoch_time += 60
        return get_note_path(output, epoch_time, name)
    
    return file_location

def create_note(output, note):
    # get creation date
    content = get_fixed_content(note.content)
    note_title = get_title(content)
    note_path = get_note_path(output, note.created_time, note_title)

    # create markdown file
    with open(note_path, 'w') as new_note:
        new_note.write(content)

    print('Created note "' + note_title + '.md"')
    