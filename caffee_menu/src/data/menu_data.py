import json
import os

class Data:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'menu.json')

    def get_menu_data(self):
        """전체 메뉴를 json으로 리턴하는 함수"""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_menu_bar_list_with_first_page(self):
        """메뉴바에 '초기화면'과 '결제하기'가 있는 리스트를 리턴하는 함수"""
        return ["초기화면"] + self.get_menu_bar_list_with_payment()
    
    def get_menu_list_including_first_page_for_admin(self):
        """메뉴바에 '초기화면'이 있는 리스트를 리턴하는 함수"""
        return ["초기화면"] + self.get_menu_bar_list()
    
    def get_menu_bar_list_with_payment(self):
        """메뉴바에 '결제하기'가 있는 리스트를 리턴하는 함수"""
        return ["결제하기"] + self.get_menu_bar_list()
        
    def get_menu_bar_list(self):
        """메뉴바에 '초기화면'과 '결제하기'가 없는 정렬된 리스트를 리턴하는 함수"""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            current_menu = json.load(file)
            return sorted([menu for menu in current_menu.keys() if menu != "초기화면" and menu != "결제하기"  ])
        
    def get_menu_list(self,menu):
        """모든 메뉴의 가격과 메뉴이름을 리스트로 정렬하여 리턴하는 함수"""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            current_menu = json.load(file)
            return sorted(["{} : {}원".format(menu,cost) for menu,cost in current_menu[menu].items()])
        
    def get_menu_order_list(self):
        """사용자의 주문 리스트를 만드는 함수"""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            current_menu = json.load(file)
            result = {}
            for menu_bar, menu in current_menu.items():
                if menu_bar not in ["초기화면", "결제하기"]:
                    if isinstance(menu, dict):
                        for menu_key in menu.keys():
                            result[menu_key] = 0
                    else:
                        result[menu] = 0
            return [[menu, 0] for menu in sorted(result.keys())]
        
    def get_menu_item_prices(self):
        """모든 메뉴의 이름과 가격을 딕셔너리로 리턴하는 함수"""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            current_menu = json.load(file)
            order_cost = {}
            menu_bar_all = [menu_bar for menu_bar in self.get_menu_bar_list()]
            for menu_bar in menu_bar_all:
                for menu,cost in current_menu[menu_bar].items():
                    order_cost[menu] =cost
            return order_cost
        
    def add_menu_item(self, menu_kind, menu):
        """관리자가 메뉴를 추가하는 함수"""
        self.menu_data = self.get_menu_data()
        for menu_kind_key,menu_kind_values in self.menu_data.items():
            if menu_kind_key == menu_kind and menu_kind_key != "초기화면" and menu_kind_key != "결제하기":
                self.menu_data[menu_kind].update(menu)
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.menu_data, file, indent=4, ensure_ascii=False)
                return

    def remove_menu_item(self, menu_kind, menu):
        """관리자가 메뉴를 제거하는 함수"""
        self.menu_data = self.get_menu_data()
        for menu_kind_key,menu_kind_values in self.menu_data.items():
            if menu_kind_key == menu_kind and menu_kind_key != "초기화면" and menu_kind_key != "결제하기":
                del self.menu_data[menu_kind][menu]
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.menu_data, file, indent=4, ensure_ascii=False)
                return
                
                
