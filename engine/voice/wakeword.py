import time
import speech_recognition as sr
from engine.core.config import config
from engine.core.assistant_state import state_manager, AssistantState
from engine.voice.listener import listener
from engine.ui.logs import logger

class WakeWordDetector:
    def __init__(self):
        self.stop_listening_fn = None
        self.active = False

    def wake_word_callback(self, recognizer, audio):
        """
        Non-blocking background audio segment callback.
        Called by SpeechRecognition worker threads.
        """
        # Ignore wake words if the assistant is busy (Prevents self-triggering!)
        if state_manager.get_state() != AssistantState.IDLE:
            return

        # Skip if user turned off continuous listening
        if not config.get("continuous_listening", True):
            return

        try:
            # Perform rapid lightweight search online
            text = recognizer.recognize_google(audio).lower().strip()
            
            if "optimus" in text:
                logger.log("Holographic wake-word directive recognized: \"Optimus\"", "SYS")
                
                # Command UI to trigger voice recording
                from engine.ui.ui_controller import trigger_voice_listening
                trigger_voice_listening()
                
        except sr.UnknownValueError:
            # Silent fallback for background chatter
            pass
        except Exception:
            pass

    def start(self):
        """
        Spawns background listener thread.
        """
        if self.active:
            return

        if not listener.active or not listener.mic:
            print("[WAKEWORD] Background wake word listener unavailable: Microphone offline.")
            return

        try:
            self.active = True
            # Spawn background listener thread using speech_recognition's built-in framework
            self.stop_listening_fn = listener.recognizer.listen_in_background(
                listener.mic, 
                self.wake_word_callback,
                phrase_time_limit=3.0
            )
            print("[WAKEWORD] Background wake word monitor active: Listening for 'Optimus'...")
        except Exception as e:
            self.active = False
            print(f"[WAKEWORD ERROR] Failed launching background listener thread: {e}")

    def stop(self):
        """
        Stops background listening.
        """
        if self.stop_listening_fn:
            # Call returned function to tear down thread
            self.stop_listening_fn(wait_for_stop=False)
            self.stop_listening_fn = None
        self.active = False
        print("[WAKEWORD] Background wake word monitor paused.")

# Global wake word detector instance
wakeword_detector = WakeWordDetector()
