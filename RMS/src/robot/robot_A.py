import sys
import os

# src 디렉토리 경로를 sys.path에 추가
current_file_path = os.path.dirname(__file__)  # 현재 파일 경로
parent_dir = os.path.abspath(os.path.join(current_file_path, '..'))  # 한 단계 위로 이동
# sys.path에 한 단계 위의 경로 추가
sys.path.append(parent_dir)

if __name__ == "__main__":
    print(current_file_path)
    print(parent_dir)
    
from robot.robot_abs import Robot_abs
import time

class Robot_A(Robot_abs):
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
                 failure_state = False):
        
        super().__init__(
                 value = value,
                 product = product,
                 line_of_process = line_of_process,
                 file_product = file_product,
                 current_product = current_product,
                 time_product = time_product,
                 time_change_current_product = time_change_current_product,
                 version = version,
                 version_process = version_process,
                 parts=parts,
                 parts_lifes=parts_lifes,
                 parts_wear_level=parts_wear_level,
                 failure_state = failure_state)
        
    def send_ui_data(self,flag):
        my_profile = {"text":"잘못된 입력","fg":"red"}
        if flag == "로봇정보": # 로봇 이름 | 버전 이름 | 동작 유무 | 고장 유무 
            pass
        else:
            pass
        return my_profile
    
    def create_product(self,product_file_path,product_name):
        self.active = True
        print(list(self.line_of_process)[0],"number process",product_file_path)
        
        if product_name != self.current_product:
            self.current_product = product_name
            time.sleep(self.time_change_current_product[product_name])
            
        if list(self.line_of_process)[0] == "1":
            product = open(product_file_path,'w')
        else:
            product = open(product_file_path,'a')
            
        product.write(self.file_product[product_name])
        
        time.sleep(self.time_product[product_name])
        
        product.close()
        self.parts_lifes = {key: self.parts_lifes[key] - self.parts_wear_level[key] for key in self.parts_lifes}
        self.active = False
    
    