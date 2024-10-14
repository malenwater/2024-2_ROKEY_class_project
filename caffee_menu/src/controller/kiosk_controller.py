
import sys
import os
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
from tkinter import Tk, Button, Label, Frame, Entry
from services import info_service,menu_service
from UI import user_UI as UI
from data import menu_data

class Kiosk_controller:
    """_summary_
        키오스크 info 패널 및 메뉴바를 띄우며 여러 페이지를 컨트롤하는 메인 클래스
    """
    def __init__(self, root):
        self.root = root
        self.admin = False
        self.selected_page = "초기화면"
        self.menu_kind = ""
        self.selected_menu = {}
        self.root.title("Kiosk Application")  
        self.info_service_object = info_service.Info()
        self.menu_service_object = menu_service.Menu()
        self.user_UI_object = UI.user_UI(root,self.handle_page_selection)
        self.menu_data_object = menu_data.Data()
        
        self.handle_page_selection(self.selected_page)
        
    def handle_page_selection(self, page):
        """
        사용자 입력시 핸들러
        """
        page_list = page.split(" ")
        if page_list[0] in self.menu_data_object.get_menu_bar_list_with_first_page() and not self.admin:
            self.selected_page = page_list[0]
        elif page_list[0] in self.menu_data_object.get_menu_list_including_first_page_for_admin() and self.admin:
            self.selected_page = page_list[0]
        elif page_list[0] in self.info_service_object.get_order_items_list() and self.is_valid_integer(page_list[1]) and not self.admin:
            self.info_service_object.update_order_quantity(page_list[0], int(page_list[1]))
        elif page_list[0] == "root" and page_list[1] == "root":
            self.admin = True
            self.selected_page = "초기화면"
        elif self.admin and page_list[0] == "exit":
            self.admin = False
            self.selected_page = "초기화면"
        elif page_list[0] == "결제":
            self.info_service_object.finalize_order()
        elif page_list[0] == "주문취소":
            self.info_service_object.reset_order()
        elif page_list[0] == "메뉴추가" and self.admin:
            self.menu_service_object.add_menu_item(self.selected_page,page_list[1],page_list[2])
            self.info_service_object.reset_order()
        elif page_list[0] == "메뉴제거" and self.admin:
            self.menu_service_object.remove_menu_item(self.selected_page,page_list[1])
            self.info_service_object.reset_order()
            
        if self.admin:
            self.user_UI_object.update_info_label(self.info_service_object.generate_payment_log())
        else:
            self.user_UI_object.update_info_label(self.info_service_object.generate_order_summary())
        self.display_menu(self.selected_page )

    def is_valid_integer(self,value):
        """
        value 가 정수로 반환해줌
        """
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def display_menu(self,page):
        """
        메뉴 출력 함수
        """
        menu = self.menu_service_object.get_menu_by_page(page,self.admin)
        text=""
        for items in menu:
            text += items +"\n"
        self.user_UI_object.update_menu_label(text)
    
    
if __name__ == "__main__":
    root = Tk()
    app = Kiosk_controller(root)
    root.mainloop()
