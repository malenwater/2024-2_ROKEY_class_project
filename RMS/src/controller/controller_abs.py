from abc import ABC, abstractmethod

class Controller_abs(ABC):
    def __init__(self,controllers={},robots={},value="None"):
        self.controllers = controllers
        self.robots = robots
        self.value = value
        
    def send_ui_data(self):
        pass
    
    def activate_robot(self):
        pass
    
