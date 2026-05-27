import speech_recognition as sr
from engine.core.config import config
from engine.core.assistant_state import state_manager, AssistantState
from engine.ui.logs import logger

class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = None
        self.active = False
        self.initialize_mic()

    def initialize_mic(self):
        """
        Robust microphone verification. Falls back gracefully if audio inputs are missing.
        """
        try:
            # Test listing available microphones
            mics = sr.Microphone.list_microphone_names()
            device_index = config.get("mic_device_index")
            
            # Re-verify device index bounds
            if device_index is not None and (device_index < 0 or device_index >= len(mics)):
                device_index = None

            self.mic = sr.Microphone(device_index=device_index)
            self.active = True
            
            # Calibrate recognizer thresholds
            self.recognizer.dynamic_energy_threshold = True
            print(f"[VOICE] Speech Recognition microphone: ACTIVE (device index: {device_index})")
        except Exception as e:
            self.mic = None
            self.active = False
            print(f"[VOICE WARNING] Failed initializing microphone hardware: {e}. Falling back to text console inputs.")

    def listen(self):
        """
        Listens to vocal capture from the microphone and returns recognized string.
        """
        if not self.active or not self.mic:
            logger.log("Speech recognition unavailable: Microphone inactive.", "WARN")
            return None

        state_manager.set_state(AssistantState.LISTENING)

        try:
            with self.mic as source:
                # 1. Calibrate background hums
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                
                # 2. Open record stream with a 4-second delay before timing out
                logger.log("Microphone audio stream capturing active...", "SYS")
                audio_data = self.recognizer.listen(source, timeout=4.0, phrase_time_limit=6.0)

            # 3. Process voice to text via Google Speech Recognition
            state_manager.set_state(AssistantState.THINKING)
            logger.log("Analyzing captured speech waveforms...", "SYS")
            
            text = self.recognizer.recognize_google(audio_data)
            logger.log(f"Speech recognition matched: \"{text}\"", "OK")
            return text

        except sr.WaitTimeoutError:
            # Silent timeout: user did not speak
            return None
        except sr.UnknownValueError:
            logger.log("Speech recognition failed: OPTIMUS could not resolve the audio.", "WARN")
            return None
        except sr.RequestError as e:
            logger.log(f"Speech recognition network request failed: {e}", "ERROR")
            return None
        except Exception as e:
            logger.log(f"Audio capture failure: {e}", "ERROR")
            return None
        finally:
            # Set state back if not routed further
            if state_manager.get_state() == AssistantState.THINKING:
                state_manager.set_state(AssistantState.IDLE)

# Global voice listener instance
listener = VoiceListener()
