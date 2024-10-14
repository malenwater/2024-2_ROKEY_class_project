from abc import ABC, abstractmethod

class Robot_abs(ABC):
    def __init__(self,
                 value = "Robot_A_1",
                 product = {"dog","cat","apple"},
                 line_of_process = {"1"},
                 file_product = {"dog":"    / \\__","cat":"  /\\_/\\  ","apple":"   ,--./,-."},
                 current_product = "dog",
                 time_product = {"dog":2,"cat":11,"apple":6},
                 time_change_current_product = {"dog":1,"cat":1,"apple":1},
                 version = "V.1",
                 version_process = {"V.1","V.2","V.3"},
                 parts={"part_ABC1","part_ABC2","part_ABC3","part_ABC4"},
                 parts_lifes={"part_ABC1":9999,"part_ABC2":9999,"part_ABC3":9999,"part_ABC4":9999},
                 parts_wear_level={"part_ABC1":1,"part_ABC2":1,"part_ABC3":1,"part_ABC4":1},
                 failure_state = False
                 ):
        self.active = False
        self.value = value
        self.product = product
        self.line_of_process = line_of_process
        self.current_product = current_product
        self.file_product = file_product
        self.time_product = time_product
        self.time_change_current_product = time_change_current_product
        self.current_time_product = self.time_product[self.current_product]
        self.version = version
        self.version_process = version_process
        self.parts = parts
        self.parts_lifes = parts_lifes
        self.parts_wear_level = parts_wear_level
        self.failure_state = failure_state
    
    def create_product(self):
        pass
    
    
