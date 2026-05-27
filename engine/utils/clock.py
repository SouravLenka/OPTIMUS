// engine/utils/clock.py
"""Clock module providing a 12‑hour time update thread.
It periodically calls the JavaScript function `updateClock` with a formatted string.
"""
import threading
import datetime
from .helpers import to_json
import eel

class Clock:
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def _run(self):
        while not self._stop_event.is_set():
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M:%S %p")  # 12‑hour format with leading zero
            try:
                eel.updateClock(time_str)()
            except Exception:
                # Frontend may not be ready yet – ignore silently
                pass
            self._stop_event.wait(self.interval)

# Global instance for easy import
clock = Clock()
