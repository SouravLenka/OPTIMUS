import time
import socket
import threading
import psutil
import eel
from engine.core.assistant_state import state_manager, AssistantState

class TelemetryMonitor:
    def __init__(self):
        self.running = False
        self.thread = None

    def check_internet(self):
        """
        Fast socket connection probe to a public DNS server to verify internet.
        """
        try:
            # Probe 8.8.8.8 on port 53 (DNS) with a tight 1s timeout
            socket.setdefaulttimeout(1.0)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except Exception:
            return False

    def get_battery(self):
        """
        Queries system battery percentage. Falls back to mock values on desktops.
        """
        try:
            battery = psutil.sensors_battery()
            if battery is not None:
                return int(battery.percent)
            return 100  # Fallback for desktops with no battery cell
        except Exception:
            return 100

    def query_loop(self):
        print("[TELEMETRY] System monitor diagnostic thread started.")
        while self.running:
            try:
                # 1. Query Hardware telemetry values
                cpu = int(psutil.cpu_percent())
                ram = int(psutil.virtual_memory().percent)
                gpu = int(psutil.cpu_percent() * 0.4 + 5)  # Simulated GPU load based on CPU metrics
                
                # 2. Check Internet & Battery parameters
                online = self.check_internet()
                battery = self.get_battery()

                # 3. Synchronize with Javascript UI Circular Gauges
                try:
                    eel.updateTelemetryGauge('cpu', cpu)()
                    eel.updateTelemetryGauge('ram', ram)()
                    eel.updateTelemetryGauge('gpu', gpu)()
                    eel.updateSystemStatus(online, battery)()
                except Exception:
                    # Ignore if frontend hasn't linked yet
                    pass

                # 4. Warn system terminal if severe load spikes
                if cpu > 85:
                    try:
                        eel.logSystemEvent(f"High CPU workload warning: {cpu}% capacity reached.", "WARN")()
                    except Exception:
                        pass

            except Exception as e:
                print(f"[TELEMETRY ERROR] Exception in query loop: {e}")

            time.sleep(3.0)  # Query sensor sweep every 3 seconds

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.query_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

# Global telemetry monitor instance
telemetry_monitor = TelemetryMonitor()
