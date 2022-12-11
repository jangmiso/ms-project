import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDate, QTime

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from mplwidget import MplWidget
import numpy as np
import random

import sqlite3





class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        bglabel = QLabel(self)
        pixmap = QPixmap('/home/pi/prj/gui/디자인/welcome_sc_or.jpg')
        bglabel.setPixmap(pixmap)
        loadUi("welcomescreen.ui", self)
        self.start.clicked.connect(self.gotologin)
        
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        bglabel2 = QLabel(self)
        pixmap = QPixmap('/home/pi/prj/gui/디자인/login_sc_or.jpg')
        bglabel2.setPixmap(pixmap)
        loadUi("login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
       
    
    def loginfunction(self):
        user = self.idfield.text()
        password = self.passwordfield.text()

        if len(user)==0:
            self.error.setText("아이디를 입력하세요!")
        elif len(password)==0:
            self.error.setText("비밀번호를 입력하세요!")
        else:   
            conn = sqlite3.connect("jibjung.db")
            cur = conn.cursor()

            query = 'SELECT passwd FROM member WHERE id='+user+""
            
            cur.execute(query)
            
            result = cur.fetchone()[0]

            if str(result) == str(password):
                main = MainScreen(password)
                widget.addWidget(main)
                widget.setCurrentIndex(widget.currentIndex()+1)
                


class MainScreen(QDialog):
    def __init__(self,password):
        super(MainScreen, self).__init__()
        loadUi("main3.ui", self)
        
 
        
        label_user = QLabel(self)
        label_user.setGeometry(QtCore.QRect(60, 20, 111, 111))
        label_user.resize(110, 110)
        pixmap = QPixmap('/home/pi/prj/gui/디자인/user (2).png')
        label_user.setPixmap(pixmap)
        label_user.setScaledContents(True)
        
        label_point = QLabel(self)
        label_point.setGeometry(QtCore.QRect(508, 47, 45, 45))
        label_point.resize(45, 45)
        pixmap = QPixmap('/home/pi/prj/gui/디자인/coin (1).png')
        label_point.setPixmap(pixmap)
        label_point.setScaledContents(True)
        
        
        self.pushButton_generate_random_signal.clicked.connect(self.update_graph)

        #self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        
        self.bt_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))
        self.bt_mypage.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.bt_class.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.bt_bestworst.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
        self.bt_change.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_4))
        
        
        self.label_gold = QtWidgets.QLabel(self.page_3)
        self.label_gold.setGeometry(QtCore.QRect(40, 180, 70, 70))
        self.label_gold.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_gold.setText("")
        self.label_gold.setPixmap(QtGui.QPixmap("/home/pi/prj/gui/디자인/gold-medal.png"))
        self.label_gold.setScaledContents(True)
        
        self.label_silver = QtWidgets.QLabel(self.page_3)
        self.label_silver.setGeometry(QtCore.QRect(40, 280, 70, 70))
        self.label_silver.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_silver.setText("")
        self.label_silver.setPixmap(QtGui.QPixmap("/home/pi/prj/gui/디자인/silver-medal.png"))
        self.label_silver.setScaledContents(True)
        self.label_silver.setObjectName("label_silver")
        self.label_bronze = QtWidgets.QLabel(self.page_3)
        self.label_bronze.setGeometry(QtCore.QRect(40, 380, 70, 70))
        self.label_bronze.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_bronze.setText("")
        self.label_bronze.setPixmap(QtGui.QPixmap("/home/pi/prj/gui/디자인/bronze.png"))
        self.label_bronze.setScaledContents(True)
        self.label_bronze.setObjectName("label_bronze")
        self.label_gold_2 = QtWidgets.QLabel(self.page_3)
        self.label_gold_2.setGeometry(QtCore.QRect(530, 180, 70, 70))
        self.label_gold_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_gold_2.setText("")
        self.label_gold_2.setPixmap(QtGui.QPixmap("/home/pi/prj/gui/디자인/gold-medal.png"))
        self.label_gold_2.setScaledContents(True)
        self.label_gold_2.setObjectName("label_gold_2")
        self.label_silver_2 = QtWidgets.QLabel(self.page_3)
        self.label_silver_2.setGeometry(QtCore.QRect(530, 280, 70, 70))
        self.label_silver_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_silver_2.setText("")
        self.label_silver_2.setPixmap(QtGui.QPixmap("/home/pi/prj/gui/디자인/silver-medal.png"))
        self.label_silver_2.setScaledContents(True)
        self.label_silver_2.setObjectName("label_silver_2")
        self.label_bronze_2 = QtWidgets.QLabel(self.page_3)
        self.label_bronze_2.setGeometry(QtCore.QRect(530, 380, 70, 70))
        self.label_bronze_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_bronze_2.setText("")
        self.label_bronze_2.setPixmap(QtGui.QPixmap(":/icon/디자인/bronze.png"))
        self.label_bronze_2.setScaledContents(True)
        self.label_bronze_2.setObjectName("label_bronze_2")
    
    def update_graph(self):

        f = random.randint(1, 20)
        f2=random.randint(10, 30)
        

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot([0,1,2,3,4],[5*f,f2,2*f,3*f2,4*f])
        self.MplWidget.canvas.axes.legend(('point', 'pointt'),loc='upper right')
        #self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()
        
        
        



#main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
