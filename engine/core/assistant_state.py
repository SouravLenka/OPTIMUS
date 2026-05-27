from enum import Enum
import threading

class AssistantState(Enum):
    IDLE = 'IDLE'
    LISTENING = 'LISTENING'
    THINKING = 'THINKING'
    SPEAKING = 'SPEAKING'
    EXECUTING = 'EXECUTING'
    ERROR = 'ERROR'

class StateController:
    def __init__(self):
        self.lock = threading.Lock()
        self.current_state = AssistantState.IDLE

    def get_state(self):
        with self.lock:
            return self.current_state

    def set_state(self, new_state):
        if not isinstance(new_state, AssistantState):
            print(f"[ERROR] Invalid state instance: {new_state}")
            return

        with self.lock:
            prev_state = self.current_state
            self.current_state = new_state

        print(f"[STATE] {prev_state.name} -> {self.current_state.name}")
        
        # Trigger frontend visual sync
        self.sync_with_ui()

    def sync_with_ui(self):
        try:
            import eel
            # Ensure Eel server has active clients before pushing
            # eel.updateAssistantState is exposed in JS
            eel.updateAssistantState(self.current_state.value)()
        except Exception as e:
            # Fallback if Eel is booting up or offline
            pass

# Global state controller instance
state_manager = StateController()
