
import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from data import menu_data, order_data

class Info:
    def __init__(self):
        self.menu_bar_obj = menu_data.Data()
        self.order_obj = order_data.Order_Data()
        self.order =self.menu_bar_obj.get_menu_order_list()
        self.order_cost=self.menu_bar_obj.get_menu_item_prices()
        self.total = 0
        
    def generate_order_summary(self):
        """사용자의 주문 리스트 생성 함수"""
        info_str ="현재 주문 리스트\n"
        self.total = 0
        for order in self.order:
            if order[1] > 0:
                cost = self.order_cost[order[0]] * order[1]
                info_str += order[0] + " 1 개당 "+ str(self.order_cost[order[0]]) + "원 : " + str(order[1]) + " 개(잔), 총 " + str(cost) + "원\n"
                self.total += cost
        info_str += "현재 주문 가격: "+ str(self.total) +"원"
        return info_str
    
    def get_order_items_list(self):
        """전체 메뉴바 생성 함수"""
        return [menu[0] for menu in self.order]
    
    def update_order_quantity(self,menu,num):
        """사용자의 메뉴 주문을 업데이트하는 함수"""
        for order in self.order:
            if order[0] == menu:
                order[1] = max(0, order[1] + num)
                return 
            
    def generate_payment_log(self):
        """관리자의 사용자들의 결제 로그를 생성하는 함수"""
        log = "결제 로그\n"
        order_data = self.order_obj.load_order_data()
        sorted_keys = sorted(order_data.keys(), key=int)  # 키를 정렬
        log += "\n".join(["{}: {}".format(key, order_data[key]) for key in sorted_keys])
        return log
    
    def finalize_order(self):
        """사용자의 주문을 결제한 후, 저장하기 위해 데이터를 변경하는 함수"""
        check_can_order = False
        for order in self.order:
            if order[1] > 0:
                check_can_order = True
        if not check_can_order:
            return False
        
        order_dict = {"결제 날짜": str(datetime.datetime.now()),
                      "요일":str(datetime.datetime.today().weekday())}
        for order in self.order:
            if order[1] > 0:
                order_dict[order[0]] = order[1]
        order_dict["총 가격"] = self.total
        self.order_obj.append_order_data(order_dict)
        self.reset_order()
        
        return True
    def reset_order(self):
        """사용자의 주문을 취소하는 함수와 메뉴제거,추가시 리셋함수"""
        self.order=self.menu_bar_obj.get_menu_order_list()
        self.order_cost=self.menu_bar_obj.get_menu_item_prices()
        
