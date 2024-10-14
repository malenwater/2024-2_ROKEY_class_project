import json
import os

class Order_Data:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'order.json')
        
    def load_order_data(self):
        """사용자 결제 로그를 리턴하는 함수"""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def append_order_data(self, data):
        """사용자 결제 로그를 저장하는 함수"""
        self.order = self.load_order_data()
        if isinstance(self.order, dict) and not self.order:
            self.order["1"] = data
        else:
            max_key = max(map(int, self.order.keys()))
            self.order[str(max_key + 1)] = data
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.order, file, indent=4, ensure_ascii=False)
