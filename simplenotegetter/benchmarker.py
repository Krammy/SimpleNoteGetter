from datetime import datetime, timezone

class Benchmarker:
    def start_record(self):
        self.start = datetime.now(timezone.utc)
    
    def end_record(self):
        self.end = datetime.now(timezone.utc)
    
    def get_elapsed_seconds(self):
        time_difference = self.end - self.start
        return time_difference.total_seconds()
