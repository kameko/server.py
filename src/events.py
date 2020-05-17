
from typing import Callable

class Events:
    def __init__(self):
        self.system_shutdown_callbacks = []
    
    def on_system_shutdown(self, callback: Callable[[object], None]):
        self.system_shutdown_callbacks.append(callback)
    
    def request_system_shutdown(self, caller):
        for callback in self.system_shutdown_callbacks:
            callback(caller)
    
