class StateStore:
    def __init__(self):
        self.state = {
            'is_recording': False,
            'current_document_id': None,
            'user_preferences': {},
        }

    def get_state(self, key):
        return self.state.get(key)

    def set_state(self, key, value):
        self.state[key] = value

    def update_state(self, updates):
        self.state.update(updates)