import threading
import pyttsx3
import eel
from engine.core.config import config
from engine.core.assistant_state import state_manager, AssistantState
from engine.ui.logs import logger

class VoiceSpeaker:
    def __init__(self):
        self.lock = threading.Lock()
        self.engine = None
        self.active = False
        self.initialize_engine()

    def initialize_engine(self):
        """
        Safe pyttsx3 synthesizer initialization wrapped in fail-safes.
        """
        with self.lock:
            try:
                self.engine = pyttsx3.init()
                self.active = True
                self.reconfigure_unsafe()
                print("[VOICE] Text-to-Speech synthesis engine: ACTIVE")
            except Exception as e:
                self.engine = None
                self.active = False
                print(f"[VOICE WARNING] Failed initializing pyttsx3 audio drivers: {e}. Falling back to silent UI logs mode.")

    def reconfigure(self):
        with self.lock:
            if not self.active:
                return
            try:
                self.reconfigure_unsafe()
            except Exception as e:
                logger.log(f"Failed reconfiguring synthesizer: {e}", "ERROR")

    def reconfigure_unsafe(self):
        """
        Applies speed, volume, and voice profile selections from config.
        """
        if not self.engine:
            return
        rate = config.get("voice_rate", 175)
        volume = config.get("voice_volume", 1.0)
        profile = config.get("voice_profile", "male-deep")

        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

        # Retrieve available voices
        voices = self.engine.getProperty('voices')
        if voices:
            # Set default profiles
            if "female" in profile.lower() and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            else:
                self.engine.setProperty('voice', voices[0].id)

    def speak(self, text):
        """
        Converts text string into synthesized speech and pushes logs to UI.
        """
        if not text:
            return

        # 1. Shift states to Speaking
        state_manager.set_state(AssistantState.SPEAKING)

        # 2. Command frontend to show visual dialogue response lines
        try:
            eel.displayResponse(text)()
        except Exception:
            pass

        # 3. If pyttsx3 audio driver is active, speak vocals
        if self.active and self.engine:
            def speak_worker():
                with self.lock:
                    try:
                        self.engine.say(text)
                        self.engine.runAndWait()
                    except Exception as err:
                        print(f"[SPEAKER ERROR] Exception during say execution: {err}")
            
            # Run in a separate thread so it doesn't freeze background processors
            t = threading.Thread(target=speak_worker)
            t.start()
            t.join()  # Block background worker to match dialogue durations
        else:
            # Silence mode: wait slightly to simulate speaking duration
            time_delay = max(1.5, len(text) * 0.05)
            import time
            time.sleep(time_delay)
            state_manager.set_state(AssistantState.IDLE)

    def stop_speaking(self):
        with self.lock:
            if self.active and self.engine:
                try:
                    self.engine.stop()
                except Exception:
                    pass
            state_manager.set_state(AssistantState.IDLE)

# Global voice speaker instance
speaker = VoiceSpeaker()
