class StateStore:
    def __init__(self):
        self._state = {
            'is_recording': False,
            'window_geometry': (100, 100, 600, 400),
            'last_used_device': 'Microphone (Default)'
        }
    
    def get_state(self, key):
        return self._state.get(key)
        
    def set_state(self, key, value):
        self._state[key] = value
        print(f"State {key} được cập nhật: {value}") 