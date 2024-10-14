import sys
import os
from tkinter import Tk,Button, Label, Frame, Entry, Canvas, Scrollbar

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class UI:
    def __init__(self, root,change_terminal):
        self.root = root
        self.change_terminal = change_terminal
        self.root.geometry("1200x600") 

        self.terminal_fra, self.terminal_can, self.terminal_scr = self.create_scrollable_canvas_frame(height=400)
        self.terminal_labs = []

        self.prompt_fra, self.prompt_lab,self.prompt_ent,self.prompt_but = self.create_prompt()

    def create_scrollable_canvas_frame(self, height):
        """스크롤 가능한 프레임을 생성"""
        frame = Frame(self.root, height=height)
        frame.pack(pady=20)

        canvas = Canvas(frame, bg="lightblue", width=1000, height=height)  
        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview, bg="lightblue")  
        scrollable_frame = Frame(canvas, bg="lightblue")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame, canvas, scrollbar

    def create_terminal_lab(self, text, fg):
        """프레임의 text label 생성"""
        terminal_lab = Label(self.terminal_fra, text=text, fg=fg, bg="lightblue", justify='left', wraplength=990, font=("Courier New", 10), anchor='w')  
        terminal_lab.pack(pady=3, anchor='w')
        
        self.terminal_labs.append(terminal_lab)

    def create_prompt(self):
        """입력 프레임 생성"""
        self.prompt_fra = Frame(self.root)
        self.prompt_fra.pack(pady=20)
        self.prompt_lab = Label(self.prompt_fra, text="입력하세요:", font=("Arial", 12))
        self.prompt_lab.pack(side='left')
        self.prompt_ent = Entry(self.prompt_fra, width=20)
        self.prompt_ent.pack(side='left')
        self.prompt_but = Button(self.prompt_fra, text="입력", command=self.handle_user_input)
        self.prompt_but.pack(side='left')
        return self.prompt_fra, self.prompt_lab, self.prompt_ent, self.prompt_but

    def handle_user_input(self):
        """입력된 텍스트를 처리하고 레이블 업데이트"""
        user_input = self.prompt_ent.get()
        self.prompt_ent.delete(0, 'end')  
        self.change_terminal(user_input)

    def update_terminal_lab(self, json):
        """받은 텍스트를 info 라벨에 업데이트"""
        for label in self.terminal_labs:
            label.destroy() 
        self.terminal_labs.clear() 
        
        json_to_list = sorted(list(json.items()),key=lambda x : int(x[0]))
        for item in json_to_list:
            text = item[1]["text"]
            fg = item[1]["fg"]
            self.create_terminal_lab(text,fg)
            
if __name__ == "__main__":
    root = Tk()
    app = UI(root,None)
    app.create_terminal_lab("a"*1000,"red")
    app.update_terminal_lab({
        "11":{"text":"E"*100,"fg":"blue"},
        "3":{"text":"d"*100,"fg":"black"},
        "2":{"text":"c"*100,"fg":"green"},
        "1":{"text":"b"*100,"fg":"red"},
        })
    root.mainloop()
    