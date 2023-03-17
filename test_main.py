import sys
from unittest import TestCase

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from main import Window


class TestPush(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.window1 = Window('Тестер', '1')
        self.window2 = Window('Кладовщик', 'Федоров Федор Федорович')

    def test_push_order(self):
        btn_add = self.window1.ui.btn_add_order
        self.window1.ui.lbl_name.setText('Тестер')
        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_wh(self):
        btn_add = self.window2.ui.btn_add_wh
        self.window2.ui.edit_type.setText('test')
        self.window2.ui.edit_name.setText('test')
        self.window2.ui.edit_count.setValue(99)
        self.window2.ui.edit_cost.setValue(99)
        self.window2.ui.lbl_name_2.setText('Федоров Федор Федорович')

        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)
