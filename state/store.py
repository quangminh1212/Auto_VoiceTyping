from rx.subject import BehaviorSubject

class StateStore:
    def __init__(self):
        self.is_logged_in = BehaviorSubject(False)
        self.is_recording = BehaviorSubject(False)
    
    def set_logged_in(self, value):
        self.is_logged_in.on_next(value)
    
    def set_recording(self, value):
        self.is_recording.on_next(value)