from typing import Optional

class SyncProgress:
    def __init__(self):
        self.running = False
        self.cancelled = False
        self.current_page = 0
        self.saved = 0
        self.total = None
        self.error: Optional[str] = None

progress = SyncProgress()