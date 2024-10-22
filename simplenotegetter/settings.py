import json

class Settings:
    def __init__(self, settings_path):
        print("Loading settings...")
        with open(settings_path, 'r') as settings_file:
            settings = json.load(settings_file)
        
        self.user = settings['user']
        self.password = settings['password']
        self.search_dir = settings['search_dir']
        self.output = settings['output']
        self.inbox_note = settings['inbox_note']
