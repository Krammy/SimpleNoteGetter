import json
import simplenote
from datetime import datetime
import os

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

sn = simplenote.Simplenote(settings["user"], settings["password"])

note_list = sn.get_note_list(data=True)[0]

# https://simplenotepy.readthedocs.io/en/latest/api.html#simperium-api-note-object

def get_note_path(epoch_time, name):
    timedate = datetime.fromtimestamp(epoch_time)
    note_id = timedate.strftime('%Y%m%d%H%M')
    file_name = note_id + " - " + name + ".md"
    file_location = os.path.join(settings["output"], file_name)

    if os.path.exists(file_location):
        # add one minute to time
        return get_note_path(epoch_time + 60, name)
    
    return file_location

def get_note_text(content, tags):
    # turns first line into a header if one exists
    if content[0] != "\n" and content[:2] != "# ":
        content = "# " + content
    
    # adds new line after header
    partition = content.partition("\n")

    if partition[2][0] != "\n":
        # only add a new line if new line is not already there
        content = partition[0] + partition[1] + partition[1] + partition[2]

    # add tags to the top of the note
    tags_string = ""
    for tag in tags:
        tags_string += "#" + tag + " "
    
    # remove last space
    # not sure if this would work if there are no tags.
    tags_string = tags_string[:-1]

    # add "#" if tags_string is empty
    # this makes it faster to add a tag in Obsidian.
    if tags_string == "":
        tags_string = "#"

    content = tags_string + "\n\n" + content
    return content

def get_note_name(content):
    note_name = content.partition("\n")[0]
    illegal_characters = ['*', '"', '\\', '/', '<', '>', ':', '|', '?']

    for character in illegal_characters:
        note_name = note_name.replace(character, '')

    # remove any spaces at the end
    note_name = note_name.rstrip()
    
    return note_name


def fix_content(content):
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

for note in note_list:
    if note["deleted"] == True or note["content"] == "":
        continue

    # get creation date
    epoch_time = note["createdate"]

    content = fix_content(note["content"])

    note_path = get_note_path(epoch_time, get_note_name(content))

    # create markdown file
    with open(note_path, 'w') as new_note:
        new_note.write(get_note_text(content, note["tags"]))
    
    # delete note
    sn.trash_note(note["key"])

