# -*- coding=utf-8 -*-


"""
file: w2.py
"""
import sys
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout, QApplication, QWidget,QLineEdit,QMessageBox,QDesktopWidget)


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.l1 = QLabel('房间号')
        self.l2 = QLabel('密钥')
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.b1 = QPushButton('进入')
        
        v_box = QVBoxLayout()
        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()

        h_box1.addWidget(self.l1)
        h_box1.addWidget(self.le1)
        v_box.addLayout(h_box1)

        h_box2.addWidget(self.l2)
        h_box2.addStretch()
        h_box2.addWidget(self.le2)
        v_box.addLayout(h_box2)

        v_box.addWidget(self.b1)

        self.setLayout(v_box)
        self.setWindowTitle('进入房间')

        self.b1.clicked.connect(self.btn1_clk)

        self.center()
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn1_clk(self):
            self.le.clear()




app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())