import os
from datetime import datetime, timedelta
from settings import settings

class UniqueIDGetter:
    def __init__(self, search_dir_fp):
        self.search_dir_fp = search_dir_fp
        self.existing_ids = []
    
    def get_existing_IDs(self):
        try:
            return self._existing_IDs
        except:
            pass
        existing_IDs = []
        dt = datetime.now()
        now_int_id = int(self.get_id_from_datetime(dt))
        for _, _, filenames in os.walk(self.search_dir_fp):
            for filename in filenames:
                my_id = filename[:12]
                try:
                    my_int_id = int(my_id)
                except:
                    continue
                if my_int_id < now_int_id:
                    continue
                existing_IDs.append(my_id)
        self._existing_IDs = existing_IDs
        return self._existing_IDs

    def ID_exists(self, id: str):
        if id in self.get_existing_IDs():
            return True
        self._existing_IDs.append(id)
        return False

    def get_id_from_datetime(self, dt):
        return dt.strftime('%Y%m%d%H%M')

    def get_unique_id(self, dt=None):
        if dt is None:
            dt = datetime.now()
        while True:
            note_id = self.get_id_from_datetime(dt)
            if not self.ID_exists(note_id):
                return note_id
            dt += timedelta(minutes=1)

unique_id_getter = UniqueIDGetter(settings.search_dir)
