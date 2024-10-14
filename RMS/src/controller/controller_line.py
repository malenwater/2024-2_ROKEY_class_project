import sys
import os

# src 디렉토리 경로를 sys.path에 추가
current_file_path = os.path.dirname(__file__)  # 현재 파일 경로
parent_dir = os.path.abspath(os.path.join(current_file_path, '..'))  # 한 단계 위로 이동
resoure_path = os.path.abspath(os.path.join(parent_dir, 'product'))
# sys.path에 한 단계 위의 경로 추가
sys.path.append(parent_dir)

if __name__ == "__main__":
    print(current_file_path)
    print(parent_dir)
    print(resoure_path)
    
from tkinter import Tk
from controller_abs import Controller_abs
from controller_process import Controller_Process
from robot.robot_A import Robot_A
from data.data import Data
import threading
import time
import csv

class Controller_line(Controller_abs):
    def __init__(self,root,controllers={},robots={},value="line"):
        super().__init__(controllers,robots,value)
        self.root = root
        self.active = False
        self.failure_states = {}
        self.algorithm = "RR"
        self.time_start = 0
        self.time_end = 0
        self.time_exce = 0
        self.resoure_path = os.path.abspath(os.path.join(resoure_path,value))
        self.log_path = os.path.abspath(os.path.join(resoure_path,"log\\"+value+".csv"))
        self.current_maked_product = {  "dog":0,
                                        "cat":0,
                                        "apple":0} 
        self.assigned_product = {"dog":0,
                                 "cat":0,
                                 "apple":0} 
        
    def send_ui_data(self,flag):
        my_profile = {"text":"잘못된 입력","fg":"red"}
        if flag == "라인정보": # 라인이름 | 프로세스컨트롤러 갯수 | 고장 개수 | 알고리즘 | 동작여부
            my_profile = {"text":"{:>20} | {:>20} | {:>20} | {:>20} | {:>20}".format(self.value,
                                                                             len(self.controllers),
                                                                             len(self.failure_states),
                                                                             self.algorithm,
                                                                             str(self.active)),
                          "fg":'red' if len(self.failure_states) else 'black'}
            
        elif flag == "상세정보":  
            # 라인이름(작동현황) | 할당된 알고리즘 | 제작 갯수 / dog 할당 갯수 | 제작 갯수 / cat 할당 갯수 | 제작 갯수 / apple 할당 갯수 
            my_profile = {"0":{"text":"{:<20} | {:<20} | {:<20} | {:<20} | {:<20}".format("line name(active)",
                                                                                          "algorithm",
                                                                                          "dog : number/order",
                                                                                          "cat : number/order",
                                                                                          "apple : number/order",
                                                                                          ),
                               "fg":'black'},
                          "1":{"text":"{:>20} | {:>20} | {:>20} | {:>20} | {:>20}".format(self.value+"("+str(self.active)+")",
                                                                                          self.algorithm,
                                                                                          str(self.current_maked_product["dog"]) + " / " + str(self.assigned_product["dog"]),
                                                                                          str(self.current_maked_product["cat"]) + " / " + str(self.assigned_product["cat"]),
                                                                                          str(self.current_maked_product["apple"]) + " / " + str(self.assigned_product["apple"]),
                                                                                          ),
                               "fg":'red' if len(self.failure_states) else 'black'}}
            # 프로세스 이름 | 동작 유무 | 고장 유무 
            my_profile.update({"2":{"text":"{:<20} | {:<20} | {:<20}".format("process name",
                                                                              "process state",
                                                                              "part break"
                                                                              ),
                                     "fg":'black'}})
            for key,controller in self.controllers.items():
                my_profile.update({str(int(key) + 2):controller.send_ui_data("공정정보")})
        else:
            pass
        return my_profile
    
    def activate_robot(self):
        self.time_start = time.time()
        self.active = True
        
        def run_fix():
            if self.assigned_product["dog"] != self.current_maked_product["dog"]:
                for index in range(1,self.assigned_product["dog"] + 1):
                    product_name = self.value + "_dog_" + str(index) + ".txt"
                    product_file_path = os.path.abspath(os.path.join(self.resoure_path, product_name))
                    for controller in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                        controller[1].activate_robot(product_file_path,"dog")
                    self.current_maked_product["dog"] += 1
            elif self.assigned_product["cat"] != self.current_maked_product["cat"]:
                for index in range(1,self.assigned_product["cat"] + 1):
                    product_name = self.value + "_cat_" + str(index) + ".txt"
                    product_file_path = os.path.abspath(os.path.join(self.resoure_path, product_name))
                    for controller in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                        controller[1].activate_robot(product_file_path,"cat")
                    self.current_maked_product["cat"] += 1
            elif self.assigned_product["apple"] != self.current_maked_product["apple"]:
                for index in range(1,self.assigned_product["apple"] + 1):
                    product_name = self.value + "_apple_" + str(index) + ".txt"
                    product_file_path = os.path.abspath(os.path.join(self.resoure_path, product_name))
                    for controller in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                        controller[1].activate_robot(product_file_path,"apple")
                    self.current_maked_product["apple"] += 1
            check_finish()
            
        def run_RR():
            product_count = sum(self.assigned_product.values())
            for index in range(1,product_count + 1):
                if index % 3 == 0:
                    product_name = self.value + "_dog_" + str(index) + ".txt"
                    product_file_path = os.path.abspath(os.path.join(self.resoure_path, product_name))
                    for controller in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                        controller[1].activate_robot(product_file_path,"dog")
                    self.current_maked_product["dog"] += 1
                elif index % 3 == 1:
                    product_name = self.value + "_cat_" + str(index) + ".txt"
                    product_file_path = os.path.abspath(os.path.join(self.resoure_path, product_name))
                    for controller in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                        controller[1].activate_robot(product_file_path,"cat")
                    self.current_maked_product["cat"] += 1
                elif index % 3 == 2:
                    product_name = self.value + "_apple_" + str(index) + ".txt"
                    product_file_path = os.path.abspath(os.path.join(self.resoure_path, product_name))
                    for controller in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                        controller[1].activate_robot(product_file_path,"apple")
                    self.current_maked_product["apple"] += 1
                    
            check_finish()
            
        def check_finish():
            if self.current_maked_product == self.assigned_product:
                self.time_end = time.time()
                self.time_exce = self.time_end - self.time_start
                data = {
                    "날짜":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "알고리즘":self.algorithm,
                    "dog":self.assigned_product["dog"],
                    "cat":self.assigned_product["cat"],
                    "apple":self.assigned_product["apple"],
                    "time":self.time_exce,
                }
                # save thing , 날짜 , algorithm , dog, cat, apple , 걸린 시간
                with open(self.log_path, mode='a', newline='', encoding='utf-8') as file:
                    fieldnames = ["날짜","알고리즘","dog","cat","apple","time"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    if file.tell() == 0:
                        writer.writeheader()
                        writer.writeheader()  # 헤더 작성
                    writer.writerow(data)  # 데이터 쓰기
                self.current_maked_product = {"dog": 0, "cat": 0, "apple": 0}
                self.assigned_product = {"dog": 0, "cat": 0, "apple": 0}
                self.active = False
                print("end product process of ",self.value)
            else:
                if self.algorithm == "fix":
                    run_fix()
                elif self.algorithm == "RR":
                    run_RR()
        if self.algorithm == "fix":
            thread = threading.Thread(target=run_fix)
            thread.start()
        elif self.algorithm == "RR":
            thread = threading.Thread(target=run_RR)
            thread.start()

if __name__ == "__main__":
    root = Tk()
    data = Data()
    controller_process1={
        "1":Controller_Process(robots={"1":Robot_A( value = "Robot_A_1",
                                                    line_of_process={"1"},
                                                    file_product=data.process_1,
                                                    )},
                               value="process1"),
        "2":Controller_Process(robots={"1":Robot_A( value = "Robot_A_2",
                                                    line_of_process={"2"},
                                                    file_product=data.process_2,
                                                    )},
                               value="process2"),
        "3":Controller_Process(robots={"1":Robot_A( value = "Robot_A_3",
                                                    line_of_process={"3"},
                                                    file_product=data.process_3,
                                                    )},
                               value="process3"),
        "4":Controller_Process(robots={"1":Robot_A( value = "Robot_A_4",
                                                    line_of_process={"4"},
                                                    file_product=data.process_4,
                                                    )},
                               value="process4"),
        "5":Controller_Process(robots={"1":Robot_A( value = "Robot_A_5",
                                                    line_of_process={"5"},
                                                    file_product=data.process_5,
                                                    )},
                               value="process5"),
    }
    app = Controller_line(root,controllers=controller_process1,value="line1")
    app.algorithm = "RR" 
    app.assigned_product = {    "dog":2,
                                "cat":2,
                                "apple":2} 
    app.activate_robot()
    print("end")