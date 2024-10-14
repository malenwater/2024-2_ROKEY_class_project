import sys
import os
from tkinter import Tk, Button, Label, Frame, Entry, Canvas, Scrollbar

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from controller import kiosk_controller as controller

class user_UI:
    def __init__(self, root, select_page_function):
        self.root = root
        self.select_page_function = select_page_function
        self.root.geometry("800x600") 

        self.info_frame, self.info_canvas, self.info_scrollbar = self.create_scrollable_canvas_frame(height=200)
        self.info_label = self.create_info_label()

        self.menu_frame, self.menu_canvas, self.menu_scrollbar = self.create_scrollable_canvas_frame(height=200)
        self.menu_label = self.create_menu_label()

        self.entry_frame = self.create_entry_frame()
        self.entry_label = self.create_entry_label()
        self.entry = self.create_entry_widget()
        self.submit_button = self.create_submit_button()

    def create_scrollable_canvas_frame(self, height):
        """스크롤 가능한 프레임을 생성"""
        frame = Frame(self.root, height=height)
        frame.pack(pady=20)

        canvas = Canvas(frame, bg="lightblue", width=600, height=height)  
        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview, bg="lightblue")  
        scrollable_frame = Frame(canvas, bg="lightblue")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((300, 0), window=scrollable_frame, anchor="center")  
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame, canvas, scrollbar

    def create_info_label(self):
        """프레임의 text label 생성"""
        self.info_label = Label(self.info_frame, text="", bg="lightblue", justify='center', wraplength=580)  
        self.info_label.pack(pady=20)
        return self.info_label

    def create_menu_label(self):
        """프레임의 text label 생성"""
        self.menu_label = Label(self.menu_frame, text="", bg="lightblue", justify='center', wraplength=580)  
        self.menu_label.pack(pady=20)  
        return self.menu_label

    def create_entry_frame(self):
        """입력 프레임 생성"""
        self.entry_frame = Frame(self.root)
        self.entry_frame.pack(pady=20)
        return self.entry_frame

    def create_entry_label(self):
        """입력 프레임 라벨 생성"""
        self.entry_label = Label(self.entry_frame, text="입력하세요:", font=("Arial", 12))
        self.entry_label.pack(side='left')
        return self.entry_label

    def create_entry_widget(self):
        """입력 프레임 라벨의 서브 함수 생성"""
        self.entry = Entry(self.entry_frame, width=20)
        self.entry.pack(side='left')
        return self.entry

    def create_submit_button(self):
        """입력 프레임의 입력 버튼 생성"""
        self.submit_button = Button(self.entry_frame, text="입력", command=self.handle_user_input)
        self.submit_button.pack(side='left')
        return self.submit_button

    def handle_user_input(self):
        """입력된 텍스트를 처리하고 레이블 업데이트"""
        user_input = self.entry.get()
        self.entry.delete(0, 'end')  
        self.select_page_function(user_input)

    def update_menu_label(self, text):
        """받은 텍스트를 메뉴 라벨에 업데이트"""
        self.menu_label.config(text=text)

    def update_info_label(self, info):
        """받은 텍스트를 info 라벨에 업데이트"""
        self.info_label.config(text=info)