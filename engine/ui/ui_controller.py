import eel
import threading
from engine.core.assistant_state import state_manager, AssistantState
from engine.ui.logs import logger
from engine.core.config import config
class UIController:
    """High‑level interface for the frontend.

    Holds the configuration and provides a simple logging wrapper used by the
    rest of the backend. All Eel RPC functions in this module operate on the
    globally‑registered instance created by ``app.py``.
    """
    def __init__(self, config):
        self.config = config
        self.logger = logger

    def log(self, message: str, level: str = "INFO"):
        """Forward a log message to the unified logger."""
        self.logger.log(message, level)

# We import the command handler lazily to avoid circular dependencies at boot time
command_handler_ref = None

def register_command_handler(handler):
    global command_handler_ref
    command_handler_ref = handler

# --------------------------------------------------------------------------
# EEL EXPOSED ENDPOINTS (CALLED FROM THE FRONTEND JAVASCRIPT HUD)
# --------------------------------------------------------------------------
@eel.expose
def call_python_nlp(prompt):
    """
    Exposed RPC called when user submits a command text prompt or voice capture.
    """
    logger.log(f"Received user directive: \"{prompt}\"", "USER")
    
    # Process the command in a background thread to prevent UI freezing
    def run():
        state_manager.set_state(AssistantState.THINKING)
        if command_handler_ref:
            try:
                response = command_handler_ref.process_command(prompt)
                import engine.eel.eel_manager as eel_manager
                eel_manager.call_js('displayResponse', response)
                from engine.voice.speaker import speaker
                speaker.speak(response)
            except Exception as e:
                logger.log(f"Error executing directive: {e}", "ERROR")
                state_manager.set_state(AssistantState.ERROR)
                # Fail-safe speech
                from engine.voice.speaker import speaker
                speaker.speak("I encountered an error executing that directive.")
        else:
            logger.log("Command handler registry is empty.", "ERROR")
            state_manager.set_state(AssistantState.IDLE)
            
    threading.Thread(target=run, daemon=True).start()

@eel.expose
def trigger_settings_save(settings_dict):
    """
    Exposed RPC called when user saves preference parameters in settings modal.
    """
    logger.log("Updating system configuration parameters...", "SYS")
    try:
        # Map frontend settings keys to config format
        mapped_settings = {
            "model": settings_dict.get('model'),
            "continuous_listening": settings_dict.get('continuousLearning'),
            "voice_rate": int(settings_dict.get('voice_rate', 175)) if settings_dict.get('voice_rate') else 175,
            "voice_volume": float(settings_dict.get('voice_volume', 1.0)) if settings_dict.get('voice_volume') else 1.0,
            "voice_profile": settings_dict.get('voiceProfile'),
            "sound_effects": settings_dict.get('soundEffects'),
            "mic_sensitivity": int(settings_dict.get('micSensitivity', 70)) if settings_dict.get('micSensitivity') else 70,
            "theme": settings_dict.get('theme'),
            "scanlines": settings_dict.get('scanlines'),
            "bg_particles": settings_dict.get('bgParticles'),
            "eel_rpc": settings_dict.get('eelRPC'),
            "start_minimised": settings_dict.get('startTray')
        }
        
        # Filter None values
        filtered_settings = {k: v for k, v in mapped_settings.items() if v is not None}
        config.update_settings(filtered_settings)
        
        # Apply voice synthesizer speed updates live
        from engine.voice.speaker import speaker
        speaker.reconfigure()

        logger.log("Optimus configurations successfully saved.", "OK")
    except Exception as e:
        logger.log(f"Failed updating settings registry: {e}", "ERROR")

@eel.expose
def trigger_voice_listening():
    """
    Exposed RPC triggered when user clicks the AI orb or bottom mic button.
    """
    from engine.voice.listener import listener
    
    if state_manager.get_state() == AssistantState.IDLE:
        logger.log("Voice channel activation requested.", "SYS")
        
        def run():
            # Set state to Listening
            state_manager.set_state(AssistantState.LISTENING)
            # Listen to mic
            prompt = listener.listen()
            
            if prompt:
                # Dispatch string to NLP processor
                call_python_nlp(prompt)
            else:
                logger.log("Speech capture stream empty. Returning to idle.", "SYS")
                state_manager.set_state(AssistantState.IDLE)
                
        threading.Thread(target=run, daemon=True).start()
    else:
        # Force return to idle if button is clicked while active
        state_manager.set_state(AssistantState.IDLE)

@eel.expose
def run_macro_task(task_name):
    """
    Exposed RPC triggered from index.html automation macro cards.
    """
    logger.log(f"Dispatching automation macro: \"{task_name}\"", "SYS")
    
    def run():
        state_manager.set_state(AssistantState.EXECUTING)
        try:
            # Let NLP command resolver handle the macro action
            if command_handler_ref:
                command_handler_ref.process_command(task_name)
            else:
                logger.log("Macro engine unlinked.", "ERROR")
                state_manager.set_state(AssistantState.IDLE)
        except Exception as e:
            logger.log(f"Macro failure: {e}", "ERROR")
            state_manager.set_state(AssistantState.ERROR)
            
    threading.Thread(target=run, daemon=True).start()
