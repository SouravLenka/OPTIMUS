import pyttsx3
import threading
from engine.core.config import config
from engine.core.assistant_state import state_manager, AssistantState

class VoiceSpeaker:
    """Simple wrapper around pyttsx3 for speech synthesis.
    Handles async speaking and updates assistant state.
    """
    def __init__(self):
        self.engine = pyttsx3.init()
        self.lock = threading.Lock()
        self._apply_config()
        self.speaking = False

    def _apply_config(self):
        """Apply voice settings from the global config.
        Called at init and when config changes.
        """
        rate = config.get("voice_rate", 175)
        volume = config.get("voice_volume", 1.0)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        # Voice profile selection (basic implementation)
        voice_profile = config.get("voice_profile", "male-deep")
        for v in self.engine.getProperty('voices'):
            if voice_profile.lower() in v.name.lower():
                self.engine.setProperty('voice', v.id)
                break

    def reconfigure(self):
        """Public method to reload config at runtime."""
        with self.lock:
            self._apply_config()

    def speak(self, text: str, block: bool = False):
        """Speak the supplied text.
        If ``block`` is False, speech runs in a background thread.
        """
        def _run():
            with self.lock:
                self.speaking = True
                state_manager.set_state(AssistantState.SPEAKING)
                self.engine.say(text)
                self.engine.runAndWait()
                self.speaking = False
                state_manager.set_state(AssistantState.IDLE)
        if block:
            _run()
        else:
            threading.Thread(target=_run, daemon=True).start()

    def stop(self):
        """Stop any ongoing speech immediately."""
        with self.lock:
            if self.speaking:
                self.engine.stop()
                self.speaking = False
                state_manager.set_state(AssistantState.IDLE)

# Global speaker instance for easy import throughout the project
speaker = VoiceSpeaker()
