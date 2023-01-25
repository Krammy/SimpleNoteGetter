import os, json

class Settings:
    def __init__(self):
        print("Loading settings...")
        script_dir = os.path.dirname(__file__)
        settings_path = os.path.join(script_dir, 'settings.json')

        with open(settings_path, 'r') as settings_file:
            settings = json.load(settings_file)
        
        self.user = settings['user']
        self.password = settings['password']
        self.search_dir = settings['search_dir']
        self.output = settings['output']

settings = Settings()
