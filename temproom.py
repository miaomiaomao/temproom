# -*- coding=utf-8 -*-


"""
file: main.py
"""
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton,QVBoxLayout, QDesktopWidget)
 
import sys
import DataBaseRelated
 
class Dialog(QDialog):
    number=0
    userlist=[]
    user=[]
    def __init__(self,username,roomnumber):
        super(Dialog, self).__init__()
        
        self.l1 = QLabel('当前用户：')
        self.l2 = QLabel('房间号：')
        self.l3 = QLabel(str(username))
        self.l4 = QLabel(str(roomnumber))

        cur, conn = DataBaseRelated.ini()
        self.number=DataBaseRelated.curretroomusernumber(roomnumber,cur)
        for i in range(self.number):
            result=DataBaseRelated.curretroomusers(roomnumber,cur)
            self.userlist.append(result[i][2])
            self.use = QLabel(str(self.userlist[i]))
            self.user.append(self.use)
        conn.close()


        self.createFormGroupBox()

        v_box = QVBoxLayout()
        

        layout = QGridLayout()  
        # layout.addWidget(self.l1,0,0) 
        # layout.addWidget(self.l3,0,1) 
        # layout.addWidget(self.l2,1,0) 
        # layout.addWidget(self.l4,1,1)


        h_box1 = QHBoxLayout()
        h_box2 = QHBoxLayout()

        h_box1.addWidget(self.l1)
        h_box1.addWidget(self.l3)
        v_box.addLayout(h_box1)

        h_box2.addWidget(self.l2)
        h_box2.addWidget(self.l4)
        v_box.addLayout(h_box2)

        layout.addLayout(v_box,0,0,1,1)
        # self.formGroupBox = QGroupBox("房间内用户")
        layout.addWidget(self.formGroupBox,2,0,5,2)
        # layout.addWidget(self.user,2,0,0,2)

        self.setLayout(layout)
        self.setWindowTitle('Temproom')
        self.resize(250,500)
        self.center()

        # self.b1.clicked.connect(self.btn1_clk)
        # self.b2.clicked.connect(self.btn2_clk)

        self.hide()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # def btn1_clk(self):
    #         pass
    #
    # def btn2_clk(self):
    #         pass


 
    def createFormGroupBox(self,):
        self.formGroupBox = QGroupBox("本房间内用户")
        layout = QVBoxLayout()
        for i in range(self.number):
            layout.addWidget(self.user[i])
        layout.addStretch()
        self.formGroupBox.setLayout(layout)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Dialog()


    sys.exit(main.exec_())