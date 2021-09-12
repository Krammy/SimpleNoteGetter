from datetime import datetime
import os

def get_note_id(creation_date):
    timedate = datetime.fromtimestamp(creation_date)
    return timedate.strftime('%Y%m%d%H%M')

def get_title(content):
    note_title = content.partition("\n")[0]
    illegal_characters = ['*', '"', '\\', '/', '<', '>', ':', '|', '?']

    for character in illegal_characters:
        note_title = note_title.replace(character, '')
    
    # remove any spaces at the end
    note_title = note_title.rstrip()
    
    return note_title

def get_body(content):
    partition = content.partition("\n")
    # removes trailing new lines before and after
    return partition[2].strip()

def get_tags_string(tags):
    # add tags to the top of the note
    tags_string = ""
    for tag in tags:
        tags_string += "#" + tag + " "
    
    # remove last space
    # not sure if this would work if there are no tags.
    tags_string = tags_string[:-1]

    return tags_string

def get_note_text(content):
    
    title = get_title(content)
    body = get_body(content)
    tags_string = get_tags_string(content)
    
    note_text = ""

    if tags_string != "":
        note_text += tags_string

        if title != "" or body != "":
            note_text += "\n\n"
    
    if title != "":
        note_text += "# " + title

        if body != "":
            note_text += "\n\n"
    
    if body != "":
        note_text += body

    return note_text

class Note:
    def __init__(self, note):
        self.creation_date = note["createdate"]

        self.note_id = get_note_id(self.creation_date)
        
        self.content = note["content"]
        self.key = note["key"]
        
