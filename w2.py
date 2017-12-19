# -*- coding=utf-8 -*-


"""
file: w2.py
"""
import sys
from PyQt5.QtWidgets import (QLabel, QCheckBox, QPushButton, QVBoxLayout,QHBoxLayout,
 QApplication, QWidget,QLineEdit,QMessageBox,QDesktopWidget,QFormLayout)
import DataBaseRelated
from PyQt5 import QtCore,QtGui
import qdarkstyle
import temproom

class Window(QWidget):
    currentuser=''
    font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
    def __init__(self,username):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('1.png'))
        self.init_ui(username)

    def init_ui(self,username):
        self.l1 = QLabel('房间号')
        self.l2 = QLabel('密钥')
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le2.setEchoMode(QLineEdit.Password)
        self.b1 = QPushButton('进入房间')
        self.b2 = QPushButton('创建新房间')

        self.setFont(self.font)
        self.l1.setFont(self.font)
        self.l2.setFont(self.font)
        self.b1.setFont(self.font)
        self.b2.setFont(self.font)


        layout=QFormLayout()
        layout.addRow(self.l1,self.le1)
        layout.addRow(self.l2,self.le2)
        v_box = QVBoxLayout()

        h_box = QHBoxLayout()
        # h_box2 = QHBoxLayout()

        # h_box1.addWidget(self.l1)
        # h_box1.addWidget(self.le1)
        # v_box.addLayout(h_box1)


        h_box.addStretch()
        h_box.addWidget(self.b1)
        h_box.addWidget(self.b2)
        # v_box.addLayout(h_box2)

        v_box.addLayout(layout)
        v_box.addLayout(h_box)
        self.setLayout(v_box)
        # self.setLayout(v_box)
        self.currentuser=username
        self.setWindowTitle('Temproom-欢迎您,'+self.currentuser)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.b1.clicked.connect(self.btn1_clk)
        self.b2.clicked.connect(self.btn2_clk)

        self.resize(250,120)
        self.center()
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):
        # reply = QMessageBox.question(self, '确认', 'You sure to quit?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #
        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()
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

        elif result == 1:
            event.ignore()

    def btn1_clk(self):
        # try:
        #     roomnumber = int(self.le1.text())
        # except ValueError:
        #     a = QMessageBox(self)
        #     a.setText("请输入纯数字~")
        #     a.setWindowModality(QtCore.Qt.WindowModal)
        #
        #     a.setIcon(QMessageBox.NoIcon)
        #     a.setDefaultButton(QMessageBox.Yes)
        #
        #     if a.exec() == 1024:
        #         self.le1.clear()
        #         #self.le2.clear()


        if str(self.le1.text()).isdigit()==False or str(self.le2.text()).isdigit()==False:
            a = QMessageBox(self)
            a.setText("请输入纯数字~")
            a.setFont(self.font)
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            if a.exec() == 1024:
                self.le1.clear()
                self.le2.clear()
        else:
            roomnumber = int(self.le1.text())
            keyintoroom = int(self.le2.text())

            cur, conn = DataBaseRelated.ini()
            if DataBaseRelated.getinroom(self.currentuser, roomnumber, keyintoroom, cur, conn)==0:
                self.hide()
                self.window3 = temproom.Dialog(self.currentuser,roomnumber)
                self.window3.show()

            elif DataBaseRelated.getinroom(self.currentuser, roomnumber, keyintoroom, cur, conn)==1:
                a = QMessageBox(self)
                a.setText("密钥错误，请核对后再输入")
                a.setFont(self.font)
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    # self.le1.clear()
                    self.le2.clear()

                # buttonReply = QMessageBox.question(self, 'temproom', "房间密钥错误，请核对后输入", QMessageBox.Yes)
                # if buttonReply == QMessageBox.Yes:
                #
                #     self.le2.clear()
                #     self.show()

            elif DataBaseRelated.getinroom(self.currentuser, roomnumber, keyintoroom, cur, conn) ==2:
                a = QMessageBox(self)
                a.setText("没有这个房间~")
                a.setFont(self.font)
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    self.le1.clear()
                    self.le2.clear()

                # buttonReply = QMessageBox.question(self, 'temproom', "不存在此房间，请新建", QMessageBox.Yes)
                # if buttonReply == QMessageBox.Yes:
                #     self.le1.clear()
                #     self.le2.clear()
                #     self.show()

            conn.close()
    def btn2_clk(self):
        roomnumber = str(self.le1.text())
        keyintoroom = str(self.le2.text())

        if roomnumber.isdigit()==False or roomnumber.isdigit()==False:
            a = QMessageBox(self)
            a.setText("请输入纯数字~")
            a.setFont(self.font)
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            if a.exec() == 1024:
                self.le1.clear()
                self.le2.clear()

            # buttonReply = QMessageBox.question(self, 'temproom', "请输入纯数字~", QMessageBox.Yes)
            # if buttonReply == QMessageBox.Yes:
            #     self.le1.clear()
            #     self.le2.clear()

        elif len(roomnumber) < 4 or len(keyintoroom) < 4:
            a = QMessageBox(self)
            a.setText("请输入不小于四位的数字~")
            a.setFont(self.font)
            a.setWindowModality(QtCore.Qt.WindowModal)

            a.setIcon(QMessageBox.NoIcon)
            a.setDefaultButton(QMessageBox.Yes)

            if a.exec() == 1024:
                #self.le1.clear()
                self.le2.clear()

            # buttonReply = QMessageBox.question(self, 'temproom', "请大于四位数~", QMessageBox.Yes)
            # if buttonReply == QMessageBox.Yes:
            #     self.le1.clear()
            #     self.le2.clear()
        else:
            cur, conn = DataBaseRelated.ini()
            roomnumber = int(self.le1.text())
            keyintoroom = int(self.le2.text())
            if not DataBaseRelated.search_room(roomnumber,cur):
                DataBaseRelated.newroom(roomnumber,keyintoroom,self.currentuser,cur,conn)
                self.hide()
                self.window3 = temproom.Dialog(self.currentuser, roomnumber)
                self.window3.show()

            else:
                a = QMessageBox(self)
                a.setText("这个房间被别人用啦~")
                a.setFont(self.font)
                a.setWindowModality(QtCore.Qt.WindowModal)

                a.setIcon(QMessageBox.NoIcon)
                a.setDefaultButton(QMessageBox.Yes)

                if a.exec() == 1024:
                    self.le1.clear()
                    self.le2.clear()

                # buttonReply = QMessageBox.question(self, 'temproom', "房间已被占用，请重新建立", QMessageBox.Yes)
                # if buttonReply == QMessageBox.Yes:
                #     self.le1.clear()
                #     self.le2.clear()
                #     self.show()

            conn.close()

if __name__=='__main__':
    app = QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())
