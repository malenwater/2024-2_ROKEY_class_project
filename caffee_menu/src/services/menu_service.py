import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from data import menu_data

class Menu:
    def __init__(self):
        self.menu_bar = menu_data.Data()
        self.back_text ="뒤로 가길 원할 경우, '초기화면'을 입력해주세요."
        self.first_text = "주문 리스트 : 주문 리스트를 입력하여 메뉴를 확인하거나 결제할 수 있습니다."
        self.pay_text = "'결제하기'를 입력해 결제하거나 '주문취소'를 입력해 주문한 음료를 취소할 수 있습니다."
        self.order_text = "원하는 음료가 있을 경우, '음료이름 갯수'를 입력하여 주문해 주세요. 주문 취소의 경우, '음료이름 -갯수'를 통해 주문 취소가 가능합니다."    

        self.root_first = "root 권한입니다."
        self.root_second = "메뉴 추가의 경우입니다. 해당 위치에 맞는 메뉴바에 들어가서, '메뉴추가 메뉴이름 가격'을 입력해주세요."
        self.root_third = "메뉴 제거의 경우입니다. 해당 위치에 맞는 메뉴바에 들어가서, '메뉴제거 메뉴이름'을 입력해주세요."
        
    def get_menu_by_page(self,page,admin):
        """메뉴를 각 페이지와 관리자인지에 따라 출력할 text를 만들어 리턴하는 함수"""
        current_menu = self.menu_bar.get_menu_data()
        selected_menu = []
        if not admin:
            if page == "초기화면":
                selected_menu.append(self.first_text)
                selected_menu += self.menu_bar.get_menu_bar_list_with_payment()
            elif page == "결제하기":
                selected_menu.extend([self.pay_text, self.back_text, "초기화면","결제","주문취소"])
            else:
                for menu in current_menu.keys():
                    if page == menu:
                        selected_menu.extend([self.order_text,self.back_text])
                        selected_menu.extend(self.menu_bar.get_menu_list(menu))
        else:
            if page == "초기화면":
                selected_menu.extend([self.root_first,self.root_second,self.root_third])
                selected_menu += self.menu_bar.get_menu_bar_list()
            else:
                for menu in current_menu.keys():
                    if page == menu:
                        selected_menu.extend([self.back_text])
                        selected_menu.extend(self.menu_bar.get_menu_list(menu))
        return selected_menu
        
    def add_menu_item(self,menu,name,cost):
        """관리자가 메뉴를 추가하는 함수"""
        self.menu_bar.add_menu_item(menu,{name:int(cost)})
    def remove_menu_item(self,menu,name):
        """관리자가 메뉴를 제거하는 함수"""
        self.menu_bar.remove_menu_item(menu,name)