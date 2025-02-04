import os, re
from datetime import datetime, timedelta
from note import Note
from uniqueidgetter import unique_id_getter

class NoteCreator:
    def __init__(self, settings):
        self.settings = settings
    
    def get_title_from_content(self, note):
        # get first sentence
        content = note.content
        content = content.lstrip()
        first_line = note.content.split("\n", 1)[0]
        first_line = first_line.split(".", 1)[0]
        first_line = first_line.rstrip()

        # sanitise the title for file names
        new_title = first_line.replace('"', "'")
        new_title = re.sub(r'[/:]', '-', new_title)
        new_title = re.sub(r'[\[\]*\\<>|?]', '', new_title)

        id_length = 13
        max_title_length = 64
        max_total_length = max_title_length - id_length

        if len(new_title) > max_total_length:
            new_title = new_title[:max_total_length]
            # remove any extra if necessary
            new_title = new_title.rstrip()
        
        return new_title

    def get_file_name(self, note):
        try:
            return note.file_name
        except:
            pass
        
        note_title = note.title
        if note_title == "":
            note_title = self.get_title_from_content(note)
        
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
