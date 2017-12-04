# -*- coding=utf-8 -*-


"""
file: w1.py
"""
import sys
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout, QApplication, QWidget,QLineEdit,QMessageBox,QDesktopWidget)


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.l1 = QLabel('用户名')
        self.l2 = QLabel('密码')
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.b1 = QPushButton('登录')
        self.b2 = QPushButton('注册')
        #self.setGeometry(200,200,200,200)
        v_box = QVBoxLayout()
        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()
        h_box3 = QHBoxLayout()

        h_box1.addWidget(self.l1)
        h_box1.addWidget(self.le1)
        v_box.addLayout(h_box1)

        h_box2.addWidget(self.l2)
        h_box2.addStretch(1000)
        h_box2.addWidget(self.le2)
        v_box.addLayout(h_box2)

        h_box3.addWidget(self.b1)
        h_box3.addWidget(self.b2)
        v_box.addLayout(h_box3)

        self.setLayout(v_box)
        self.setWindowTitle('用户登录')

        self.b1.clicked.connect(self.btn1_clk)
        self.b2.clicked.connect(self.btn2_clk)

        self.resize(250,150)
        self.center()
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn1_clk(self):
            self.le.clear()

    def btn2_clk(self):
            print(self.le.text())



app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())