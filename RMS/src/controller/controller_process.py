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
    
from controller_abs import Controller_abs
class Controller_Process(Controller_abs):
    def __init__(self,controllers={},robots={},value="Process"):
        super().__init__(controllers,robots,value)
        self.active = False
        self.failure_state = False
    
    def send_ui_data(self,flag):
        my_profile = {"text":"잘못된 입력","fg":"red"}
        if flag == "공정정보": # 프로세스 이름 | 동작 유무 | 고장 유무 
            my_profile = {"text":"{:>20} | {:>20} | {:>20}".format(self.value,
                                                                    str(self.active),
                                                                    str(self.failure_state),
                                                                              ),
                          "fg":'red' if self.failure_state else 'black'}
        elif flag == "상세정보": # 로봇 이름 | 버전 이름 | 동작 유무 | 고장 유무 
            my_profile = {"0":{"text":"{:<20} | {:<20} | {:<20} | {:<20}".format(   "robot name",
                                                                                    "version",
                                                                                    "active",
                                                                                    "part break"
                                                                              ),
                          "fg":'black'},
                          "1":{"text":"{:>20} | {:>20} | {:>20} | {:>20}".format(   self.robots["1"].value,
                                                                                    self.robots["1"].version,
                                                                                    str(self.robots["1"].active),
                                                                                    str(self.robots["1"].failure_state)
                                                                              ),
                          "fg":'red' if self.failure_state else 'black'}}
            # 부품 정보 | 고장 여부
            my_profile.update({"2":{"text":"{:<20} | {:<20}".format("part name",
                                                                    "break",
                                                                    ),
                                    "fg":'black'}})
            for index in range(len(self.robots["1"].parts)):
                parts = sorted(list(self.robots["1"].parts))
                my_profile.update({str(3 + index):{"text":"{:>20} | {:>20}".format( parts[index],
                                                                                    "False" if self.robots["1"].parts_lifes[parts[index]] > 0 else "True",
                                                                                ),
                            "fg":'red' if self.failure_state else 'black'}})
        else:
            pass
        return my_profile
    def activate_robot(self,product_file_path,product_name):
        self.active = True
        self.robots["1"].create_product(product_file_path,product_name)
        self.active = False
 