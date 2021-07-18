import json
import simplenote
from datetime import datetime
import os

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

sn = simplenote.Simplenote(settings["user"], settings["password"])

note_list = sn.get_note_list(data=True)[0]

# https://simplenotepy.readthedocs.io/en/latest/api.html#simperium-api-note-object

for note in note_list:
    if note["deleted"] == True:
        continue
    # get creation date
    timedate = datetime.fromtimestamp(note["createdate"])
    note_id = timedate.strftime('%Y%m%d%H%M')
    file_name = note_id + " - .md"
    file_location = os.path.join(settings["output"], file_name)
    with open(file_location, 'w') as new_note:
        new_note.write(note["content"])

