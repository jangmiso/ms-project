import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap



class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        bglabel = QLabel(self)
        pixmap = QPixmap('/home/pi/prj/gui/디자인/welcome_sc2.jpg')
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
        pixmap = QPixmap('/home/pi/prj/gui/디자인/login_sc.jpg')
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
