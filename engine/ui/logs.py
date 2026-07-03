import os
import time
import threading

class AssistantLogger:
    def __init__(self):
        self.lock = threading.Lock()
        # Create persistent log files directory
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.log_dir = os.path.join(self.root_dir, 'data', 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_path = os.path.join(self.log_dir, 'session_runtime.log')

    def log(self, message, category="INFO"):
        """
        Logs an event to file, terminal, and pushes to Eel frontend live terminal.
        Categories: INFO, OK, WARN, ERROR, SYS
        """
        now = time.strftime("%H:%M:%S")
        log_line = f"[{now}] [{category}] {message}\n"
        
        # 1. Print to Python system terminal (strip non‑ASCII to avoid console errors)
        safe_msg = message.encode('ascii', errors='ignore').decode('ascii')
        print(f"[OPTIMUS] [{category}] {safe_msg}")

        # 2. Write to persistent local log file
        with self.lock:
            try:
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write(log_line)
            except Exception as e:
                print(f"[LOG ERROR] Failed writing to file: {e}")

        # 3. Push to Eel frontend UI
        try:
            import eel
            # Invoke exposed JavaScript logger
            eel.logSystemEvent(message, category)()
        except Exception:
            pass

# Global logging instance
logger = AssistantLogger()
