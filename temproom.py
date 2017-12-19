# -*- coding=utf-8 -*-


"""
file: main.py
"""
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton,QVBoxLayout, QDesktopWidget,QMessageBox)
from PyQt5 import QtCore,QtGui
import sys
import send,record,play,threading
import DataBaseRelated
import qdarkstyle

class Dialog(QDialog):
    number=0
    roomnumber=0
    userlist=[]
    user=[]
    username=''

    font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)

    def __init__(self,username,roomnumber):
        super(Dialog, self).__init__()
        self.setWindowIcon(QtGui.QIcon('1.png'))
        self.l1 = QLabel('当前用户：')
        self.l2 = QLabel('房间号：')
        self.l3 = QLabel(str(username))
        self.l4 = QLabel(str(roomnumber))
        self.b1 = QPushButton('连接服务器')
        self.b2 = QPushButton('下线')

        self.setFont(self.font)
        self.l1.setFont(self.font)
        self.l2.setFont(self.font)
        self.b1.setFont(self.font)
        self.b2.setFont(self.font)


        self.b1.clicked.connect(self.connect)
        self.b2.clicked.connect(self.close)
        self.username=username
        self.roomnumber=roomnumber
        # 调整显示内容
        cur, conn = DataBaseRelated.ini()
        self.number = DataBaseRelated.curretroomusernumber(roomnumber,cur)
        for i in range(self.number):
            result=DataBaseRelated.curretroomusers(roomnumber,cur)
            self.userlist.append(result[i][2])
            self.use = QLabel(str(self.userlist[i]))
            self.user.append(self.use)
        conn.close()







        self.formGroupBox = QGroupBox("本房间内用户")
        layout = QVBoxLayout()
        for i in range(self.number):
            layout.addWidget(self.user[i])
        layout.addStretch()
        self.formGroupBox.setLayout(layout)




        #
        # self.createFormGroupBox()

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
        layout.addWidget(self.b1,7,0,1,1)
        layout.addWidget(self.b2,7,1,1,1)
        # layout.addWidget(self.user,2,0,0,2)

        self.setLayout(layout)
        self.setWindowTitle('Temproom')
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.resize(250,600)
        self.center()

        # self.b1.clicked.connect(self.btn1_clk)
        # self.b2.clicked.connect(self.btn2_clk)

        self.hide()

    def connect(self):
        pass
        # so =send.client_connect()
        # t = threading.Thread(target=self.flow,args=so)
        # t.start()

    def closeEvent(self, event):
        a = QMessageBox(self)
        a.setText("您确定要退出吗？")
        a.setFont(self.font)
        a.setWindowModality(QtCore.Qt.WindowModal)
        b = QtGui.QPixmap('2.png')
        a.setIconPixmap(b)
        #a.setIcon(QMessageBox.NoIcon)
        # a.addButton('确定',QMessageBox.AcceptRole)
        # a.addButton('取消',QMessageBox.RejectRole)
        a.setDefaultButton(a.addButton('确定', QMessageBox.AcceptRole))
        a.setEscapeButton(a.addButton('取消', QMessageBox.RejectRole))

        # reply = QMessageBox.question(self, '确认', '您确定要退出吗？',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        result = a.exec()
        #print(result)
        if result == 0:
            event.accept()
            cur, conn = DataBaseRelated.ini()
            DataBaseRelated.useroffline(self.username, self.roomnumber, cur, conn)
            DataBaseRelated.roomoffline(self.roomnumber, cur, conn)
            conn.close()
        elif result == 1:
            event.ignore()

        # reply = QMessageBox.question(self, '确认', 'You sure to quit?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #
        # if reply == QMessageBox.Yes:
        #     event.accept()
        #     cur, conn = DataBaseRelated.ini()
        #     DataBaseRelated.useroffline(self.username, self.roomnumber, cur, conn)
        #     DataBaseRelated.roomoffline(self.roomnumber, cur, conn)
        #     conn.close()
        # else:
        #     event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # def b2_click(self):
    #     cur, conn = DataBaseRelated.ini()
    #     DataBaseRelated.useroffline(self.username, self.roomnumber, cur, conn)
    #     DataBaseRelated.roomoffline(self.roomnumber, cur, conn)
    #     conn.close()
    # def btn1_clk(self):
    #         pass
    #
    # def btn2_clk(self):
    #         pass


    #
    # def createFormGroupBox(self,):

    def flow(self,s):
        while 1:
            record.record(self.username)
            send.send(s, self.username)
            for i in self.userlist:
                if self.username != i:
                    send.recv(s)
                    t = threading.Thread(target=play.play,args=i)
                    t.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Dialog()


    sys.exit(main.exec_())
