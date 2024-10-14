import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from controller.kiosk_controller import Kiosk_controller

import unittest
from unittest.mock import patch, MagicMock

class TestKioskUI(unittest.TestCase):
    """_summary_
        Kiosk_controller 메인 메뉴를 관장하는 test
    """
    select_page_data = []
    @patch('controller.kiosk_controller.Tk') 
    def test_initialization(self, MockTk):
        root = MockTk.return_value
        app = Kiosk_controller(root)
        self.select_page_data = [
            "커피",
            "음료/티",
            "디저트"
        ]
        self.assertIsNotNone(app)

    @patch('controller.kiosk_controller.Tk')
    def test_select_page_coffee(self, MockTk):
        """
        사용자 입력이 커피일때 경우, 변수 변환 확인
        """
        root = MockTk.return_value
        app = Kiosk_controller(root)
        app.handle_page_selection("커피")
        self.assertEqual(app.selected_page, "커피")

    @patch('controller.kiosk_controller.Tk') 
    def test_select_page_drinkORtea(self, MockTk):
        """
        사용자 입력이 음료/티일때 경우, 변수 변환 확인
        """
        root = MockTk.return_value
        app = Kiosk_controller(root)
        app.handle_page_selection("음료/티")
        self.assertEqual(app.selected_page, "음료/티")

    @patch('controller.kiosk_controller.Tk')  
    def test_select_page_dessert(self, MockTk):
        """
        사용자 입력이 디저트일때 경우, 변수 변환 확인
        """
        root = MockTk.return_value
        app = Kiosk_controller(root)
        app.handle_page_selection("디저트")
        self.assertEqual(app.selected_page, "디저트")     
    
    @patch('controller.kiosk_controller.Tk')
    def test_select_page_all(self, MockTk):
        """
        위 사용자 입력인 디저트, 커피, 음료/티의 모든 경우 변수 변환 확인
        """
        root = MockTk.return_value
        app = Kiosk_controller(root)
        for page_data in self.select_page_data:
            app.handle_page_selection(page_data)
            self.assertEqual(app.selected_page, page_data)  
               
    @patch('controller.kiosk_controller.Tk') 
    @patch('controller.kiosk_controller.Label')
    def test_select_info_all(self,MockLabel, MockTk):
        """
        frame의 UI인 label text가 들어가는지 확인
        """
        root = MockTk.return_value
        app = Kiosk_controller(root)
        app.info_label = MockLabel.return_value
        app.info_label.cget = MagicMock(side_effect=lambda x: x)  

        for page_data in self.select_page_data:
            app.handle_page_selection(page_data)
            app.info_label.cget.return_value = page_data
            self.assertEqual(app.info_label.cget("text"), page_data)

if __name__ == '__main__':
    unittest.main()
