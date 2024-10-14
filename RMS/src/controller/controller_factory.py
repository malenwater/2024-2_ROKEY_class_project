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
    
from tkinter import Tk
from controller_abs import Controller_abs
from controller_line import Controller_line
from controller_process import Controller_Process
from ui.ui import UI
from robot.robot_A import Robot_A
from data.data import Data

class Controller_Factory(Controller_abs):
    def __init__(self,root,controllers={},robots={},value="factory"):
        super().__init__(controllers,robots,value)
        self.root = root
        self.UI = UI(root,self.change_terminal)
        self.data_json = {"1":{"text":"예시 데이터 더미이다.","fg":"red"}}
        self.contion_infinite = 0
        self.algorithm = "RR"
        self.previous_input = []
        self.user_input = []
        self.assigned_product = {"dog":10,
                                 "cat":10,
                                 "apple":10}
        self.change_terminal("")
        self.send_ui_data()
        
    def change_terminal(self,user_input):
        user_input = user_input.split(" ")
        command = 0
        if user_input[command] == "라인보기": # 라인보기 line1
            for line in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                if user_input[1] ==  line[1].value:
                    self.user_input = line[1]
                    self.contion_infinite = "해당라인정보"
                    break
        elif user_input[command] == "로봇보기": # 로봇보기 line1 process1
            for line in sorted(list(self.controllers.items()),key=lambda x : int(x[0])):
                if user_input[1] ==  line[1].value:
                    for _line in sorted(list(line[1].controllers.items()), key=lambda x : int(x[0])):
                        if user_input[2] == _line[1].value:
                            self.user_input = _line[1]
                            self.contion_infinite = "로봇상세보기"
                            break
                    break
            
        elif user_input[command] == "알고리즘변경": # 알고리즘변경 line1 fix  # 알고리즘변경 fix 
            self.user_input = []
            for line in list(self.controllers.items()):
                if user_input[1] ==  line[1].value:
                    self.user_input = [line[1], user_input[2]]
                    self.contion_infinite = "알고리즘변경"
                    break
            if not self.user_input:
                self.user_input = user_input[1]
                self.contion_infinite = "공장알고리즘변경"
                
        elif user_input[command] == "상품할당하기": # 상품할당하기 dog 100 cat 100 apple 100
            for index in range(1,(len(user_input) // 2) + 1):
                if user_input[2 * index - 1] in self.assigned_product:
                    self.assigned_product[user_input[2 * index - 1]] = int(user_input[2 * index ])
        
        elif user_input[command] == "상품생산": # 상품생산
            self.scheduler()

        else: # 모든 라인 상태 보기
            self.contion_infinite = "모든라인정보"

    def send_ui_data(self):
        if self.contion_infinite == "모든라인정보": # 공장 이름, 공장 알고리즘, 공장 라인 수
            self.data_json = {"0":{"text":"{:<20} | {:<20} | {:<20}".format("factory name",
                                                                            "factory algorithm", 
                                                                            "line number"),
                                   "fg":"black"},
                              "1":{"text":"{:>20} | {:>20} | {:>20}".format(self.value,
                                                                            self.algorithm, 
                                                                            len(self.controllers)),
                                   "fg":"black"}}
            self.data_json.update({"4":{"text":"{:<20} | {:<20} | {:<20} | {:<20} | {:<20}".format("line name",
                                                                                     "controller count", 
                                                                                     "part break number",
                                                                                     "algorithm",
                                                                                     "active"),
                                   "fg":"black"}})
            # 상품할당 수 | dog | cat | apple
            self.data_json.update({"2":{"text":"{:<20} | {:<20} | {:<20} | {:<20}".format(
                                                                                "assigned product", 
                                                                                "dog",
                                                                                "cat",
                                                                                "apple"),
                                   "fg":"black"}})
            self.data_json.update({"3":{"text":"{:>20} | {:>20} | {:>20} | {:>20}".format(sum(map(int, self.assigned_product.values())),
                                                                                self.assigned_product["dog"], 
                                                                                self.assigned_product["cat"], 
                                                                                self.assigned_product["apple"], 
                                                                                ),
                                   "fg":"black"}})
            for index, line in enumerate(sorted(list(self.controllers.items()),key=lambda x : int(x[0]))):
                json = line[1].send_ui_data("라인정보")
                self.data_json.update({str(index + 5):{"text":json['text'],"fg":json['fg']}})
        
        elif self.contion_infinite == "해당라인정보":
            self.data_json = self.user_input.send_ui_data("상세정보")
        
        elif self.contion_infinite == "로봇상세보기":
            self.data_json = self.user_input.send_ui_data("상세정보")
            
        elif self.contion_infinite == "알고리즘변경":
            self.user_input[0].algorithm = self.user_input[1]
            self.contion_infinite = "모든라인정보"
        elif self.contion_infinite == "공장알고리즘변경":
            self.algorithm = self.user_input
            for line in list(self.controllers.items()):
                line[1].algorithm = self.user_input
            self.contion_infinite = "모든라인정보"

        else: # 0 == 굳이 매번 계산할 필요 없을 경우
            pass
        
        self.UI.update_terminal_lab(self.data_json)
        self.root.after(100, self.send_ui_data)

    def scheduler(self):
        if self.algorithm == "fix":
            self.scheduler_fix()
        elif self.algorithm == "RR":
            self.scheduler_RR()
        elif self.algorithm == "fix_opt":
            pass
        elif self.algorithm == "opt":
            pass
        else:
            pass
        
    def scheduler_fix(self):
        schedule ={"dog":[],
                    "cat":[],
                    "apple":[],}
        count = 0
        for line_key in sorted(self.controllers.keys(),key=lambda x : int(x)):
            if count == 0:
                schedule["dog"].append(line_key)
            elif count == 1:
                schedule["cat"].append(line_key)
            elif count == 2:
                schedule["apple"].append(line_key)
            count += 1
            if count % 3 == 0:
                count = 0
                
        for line_keys in schedule.keys():
            if not schedule[line_keys]:
                break
            length = len(schedule[line_keys])
            share = self.assigned_product[line_keys] // length
            rmain = self.assigned_product[line_keys] % length
            for line in schedule[line_keys]:
                self.controllers[line].assigned_product[line_keys] += share
                if rmain > 0:
                    self.controllers[line].assigned_product[line_keys] += 1
                    rmain -= 1
                self.controllers[line].activate_robot()
                
    def scheduler_RR(self):
        length = len(self.controllers)
        shares = {}
        rmains = {}
        schedule = {}
        for key in self.assigned_product.keys():
            shares[key] = self.assigned_product[key] // length
            rmains[key] = self.assigned_product[key] % length
        for key in self.controllers.keys():
            schedule[key] = {}
            for key_name in self.assigned_product.keys():
                if rmains[key_name] > 0 :
                    schedule[key][key_name] = shares[key_name] + 1
                    rmains[key_name] -= 1
                else:
                    schedule[key][key_name] = shares[key_name]
        
        for key in self.controllers.keys():
            self.controllers[key].assigned_product.update(schedule[key])
            self.controllers[key].activate_robot()
if __name__ == "__main__":
    root = Tk()
    data = Data()
    
    controller_process1={
        "1":Controller_Process(robots={"1":Robot_A( value = "Robot_A_1",
                                                    line_of_process={"1"},
                                                    file_product=data.process_1,
                                                    time_product = {"dog":2,"cat":12,"apple":6},
                                                    )},
                               value="process1"),
        "2":Controller_Process(robots={"1":Robot_A( value = "Robot_A_2",
                                                    line_of_process={"2"},
                                                    file_product=data.process_2,
                                                    time_product = {"dog":2,"cat":12,"apple":6},
                                                    )},
                               value="process2"),
        "3":Controller_Process(robots={"1":Robot_A( value = "Robot_A_3",
                                                    line_of_process={"3"},
                                                    file_product=data.process_3,
                                                    time_product = {"dog":2,"cat":12,"apple":6},
                                                    )},
                               value="process3"),
        "4":Controller_Process(robots={"1":Robot_A( value = "Robot_A_4",
                                                    line_of_process={"4"},
                                                    file_product=data.process_4,
                                                    time_product = {"dog":2,"cat":12,"apple":6},
                                                    )},
                               value="process4"),
        "5":Controller_Process(robots={"1":Robot_A( value = "Robot_A_5",
                                                    line_of_process={"5"},
                                                    file_product=data.process_5,
                                                    time_product = {"dog":2,"cat":12,"apple":6},
                                                    )},
                               value="process5"),
    }
    controller_process2={
        "1":Controller_Process(robots={"1":Robot_A( value = "Robot_B_1",
                                                    line_of_process={"1"},
                                                    file_product=data.process_1,
                                                    time_product = {"dog":12,"cat":2,"apple":6},
                                                    )},
                               value="process1"),
        "2":Controller_Process(robots={"1":Robot_A( value = "Robot_B_2",
                                                    line_of_process={"2"},
                                                    file_product=data.process_2,
                                                    time_product = {"dog":12,"cat":2,"apple":6},
                                                    )},
                               value="process2"),
        "3":Controller_Process(robots={"1":Robot_A( value = "Robot_B_3",
                                                    line_of_process={"3"},
                                                    file_product=data.process_3,
                                                    time_product = {"dog":12,"cat":2,"apple":6},
                                                    )},
                               value="process3"),
        "4":Controller_Process(robots={"1":Robot_A( value = "Robot_B_4",
                                                    line_of_process={"4"},
                                                    file_product=data.process_4,
                                                    time_product = {"dog":12,"cat":2,"apple":6},
                                                    )},
                               value="process4"),
        "5":Controller_Process(robots={"1":Robot_A( value = "Robot_B_5",
                                                    line_of_process={"5"},
                                                    file_product=data.process_5,
                                                    time_product = {"dog":12,"cat":2,"apple":6},
                                                    )},
                               value="process5"),
    }
    controller_process3={
        "1":Controller_Process(robots={"1":Robot_A( value = "Robot_C_1",
                                                    line_of_process={"1"},
                                                    file_product=data.process_1,
                                                    time_product = {"dog":6,"cat":6,"apple":6},
                                                    )},
                               value="process1"),
        "2":Controller_Process(robots={"1":Robot_A( value = "Robot_C_2",
                                                    line_of_process={"2"},
                                                    file_product=data.process_2,
                                                    time_product = {"dog":6,"cat":6,"apple":6},
                                                    )},
                               value="process2"),
        "3":Controller_Process(robots={"1":Robot_A( value = "Robot_C_3",
                                                    line_of_process={"3"},
                                                    file_product=data.process_3,
                                                    time_product = {"dog":6,"cat":6,"apple":6},
                                                    )},
                               value="process3"),
        "4":Controller_Process(robots={"1":Robot_A( value = "Robot_C_4",
                                                    line_of_process={"4"},
                                                    file_product=data.process_4,
                                                    time_product = {"dog":6,"cat":6,"apple":6},
                                                    )},
                               value="process4"),
        "5":Controller_Process(robots={"1":Robot_A( value = "Robot_C_5",
                                                    line_of_process={"5"},
                                                    file_product=data.process_5,
                                                    time_product = {"dog":6,"cat":6,"apple":6},
                                                    )},
                               value="process5"),
    }
    controller_lines = {
        "1":Controller_line(root=root,controllers=controller_process1,value="line1"), 
        "2":Controller_line(root=root,controllers=controller_process2,value="line2"),
        "3":Controller_line(root=root,controllers=controller_process3,value="line3"),
    }
    app = Controller_Factory(root,controller_lines,{})
    root.mainloop()
