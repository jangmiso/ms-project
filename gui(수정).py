import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDate, QTime, Qt

from threading import Timer

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from mplwidget import MplWidget

import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import random
import time
import datetime
import cv2
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='miso1004', db = 'ms_project', charset='utf8')
cur = conn.cursor()

font_dirs = ['/usr/share/fonts/truetype/nanum',]
font_files = fm.findSystemFonts(fontpaths=font_dirs)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)

mpl.rcParams['font.family'] = 'NanumGothic'

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        bglabel = QLabel(self)
        pixmap = QPixmap('/home/pi/ms-project/GUI/image/welcome_sc_or.jpg')
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
        pixmap = QPixmap('/home/pi/ms-project/GUI/image/login_sc_or.jpg')
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
            cur.execute("select 비밀번호 from 생도 where 교번={}".format(user))
            result = cur.fetchone()[0]

            if str(result) == str(password):
                main = MainScreen(user)
                widget.addWidget(main)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.error.setText("로그인 정보가 올바르지 않습니다")
                

class MainScreen(QDialog):
        
    def __init__(self, user):
        
        cur.execute("select * from 생도 where 교번={}".format(user))
        cadet = cur.fetchone()
        self.user = user
        self.rank = cadet[1]
        self.sq = cadet[2]
        self.name = cadet[3]
        self.major = cadet[4]

        super(MainScreen, self).__init__()
        loadUi("main3.ui", self)
        
        label_user = QLabel(self)
        label_user.setGeometry(QtCore.QRect(60, 20, 111, 111))
        label_user.resize(110, 110)
        pixmap = QPixmap('/home/pi/ms-project/GUI/image/user (2).png')
        label_user.setPixmap(pixmap)
        label_user.setScaledContents(True)
        
        label_point = QLabel(self)
        label_point.setGeometry(QtCore.QRect(508, 47, 45, 45))
        label_point.resize(45, 45)
        pixmap = QPixmap('/home/pi/ms-project/GUI/image/coin (1).png')
        label_point.setPixmap(pixmap)
        label_point.setScaledContents(True)
        
        self.label_14.setText("{} 생도".format(self.name))
        self.label_15.setText("{}기 {}중대 {}".format(self.rank, self.sq, self.major))
        
        self.show_time()

        #self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.bt_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))
        self.bt_mypage.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.bt_class.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.bt_bestworst.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
        self.bt_change.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_4))
        #self.bt_logout.clicked.connect()
        
        self.lineEdit.setText(self.name)
        self.lineEdit.setReadOnly(True)
        self.comboBox_12.setCurrentText(str(self.sq))
        self.comboBox_13.setCurrentText(str(self.rank))
        self.comboBox_14.setCurrentText(self.major)
        self.pushButton_3.clicked.connect(self.update_data)
        
        #수업듣기
        self.init_properties()
        self.init_connections()
        
        #마이페이지-기간조회
        self.pushButton_view.clicked.connect(self.view_data)
        
        #마이페이지-월별통계
        self.pushButton_4.clicked.connect(self.show_month_graph)
        
        #마이페이지-전체통계
        cur.execute("select 과목.교과명 from 수강,과목 where 수강.과목코드=과목.과목코드 and 교번={}".format(self.user))
        subjects = cur.fetchall()
        for sub in subjects:
            self.comboBox_20.addItem(sub[0])
        self.pushButton_8.clicked.connect(self.show_graph)
        
        #마이페이지-세부내역
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        cur.execute("select 과목.교과명 from 수강,과목 where 수강.과목코드=과목.과목코드 and 교번={}".format(self.user))
        subjects = cur.fetchall()
        for sub in subjects:
            self.comboBox_11.addItem(sub[0])
        self.pushButton_2.clicked.connect(self.load_table)
            
        #명예의 전당
        self.pushButton_best3.clicked.connect(self.view_best3)
        self.pushButton_worst3.clicked.connect(self.view_worst3)
        
        self.label_gold = QtWidgets.QLabel(self.page_3)
        self.label_gold.setGeometry(QtCore.QRect(40, 180, 70, 70))
        self.label_gold.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_gold.setText("")
        self.label_gold.setPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/gold-medal.png"))
        self.label_gold.setScaledContents(True)
        
        self.label_silver = QtWidgets.QLabel(self.page_3)
        self.label_silver.setGeometry(QtCore.QRect(40, 280, 70, 70))
        self.label_silver.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_silver.setText("")
        self.label_silver.setPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/silver-medal.png"))
        self.label_silver.setScaledContents(True)
        self.label_silver.setObjectName("label_silver")
        self.label_bronze = QtWidgets.QLabel(self.page_3)
        self.label_bronze.setGeometry(QtCore.QRect(40, 380, 70, 70))
        self.label_bronze.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_bronze.setText("")
        self.label_bronze.setPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/bronze.png"))
        self.label_bronze.setScaledContents(True)
        self.label_bronze.setObjectName("label_bronze")
        self.label_gold_2 = QtWidgets.QLabel(self.page_3)
        self.label_gold_2.setGeometry(QtCore.QRect(530, 180, 70, 70))
        self.label_gold_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_gold_2.setText("")
        self.label_gold_2.setPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/gold-medal.png"))
        self.label_gold_2.setScaledContents(True)
        self.label_gold_2.setObjectName("label_gold_2")
        self.label_silver_2 = QtWidgets.QLabel(self.page_3)
        self.label_silver_2.setGeometry(QtCore.QRect(530, 280, 70, 70))
        self.label_silver_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_silver_2.setText("")
        self.label_silver_2.setPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/silver-medal.png"))
        self.label_silver_2.setScaledContents(True)
        self.label_silver_2.setObjectName("label_silver_2")
        self.label_bronze_2 = QtWidgets.QLabel(self.page_3)
        self.label_bronze_2.setGeometry(QtCore.QRect(530, 380, 70, 70))
        self.label_bronze_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_bronze_2.setText("")
        self.label_bronze_2.setPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/bronze.png"))
        self.label_bronze_2.setScaledContents(True)
        self.label_bronze_2.setObjectName("label_bronze_2")
    
    
    def init_properties(self):
        self.stream_thread = Stream_thread()
        
    def init_connections(self):
        self.stream_thread.change_pixmap.connect(self.image_label.setPixmap)
        self.start_stop_btn.clicked.connect(self.run_stop_video_streaming)
    
    @QtCore.pyqtSlot(bool)
    def run_stop_video_streaming(self):
        
        if self.start_stop_btn.isChecked():
            self.stream_thread.start()
            self.update_button_style()
        else:
            self.stream_thread.stop()
            self.update_button_style()
    
    def update_button_style(self):
        if self.start_stop_btn.isChecked():
            icon_stop = QtGui.QIcon()
            icon_stop.addPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/stop_video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.start_stop_btn.setIcon(icon_stop)
            self.start_stop_btn.setStyleSheet("border: 2px solid red; border-radius: 7px;")
        else:
            icon_run = QtGui.QIcon()
            icon_run.addPixmap(QtGui.QPixmap("/home/pi/ms-project/GUI/image/run_video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.start_stop_btn.setIcon(icon_run)
            self.start_stop_btn.setStyleSheet("border: none solid blue; border-radius: 7px;")

    
    
    def show_time(self):
        wd = ['월','화','수','목','금','토','일']
        w_day = time.strftime('%w',time.localtime(time.time()))
        self.label_17.setText("{}({})".format(time.strftime('%Y.%m.%d',time.localtime(time.time())), wd[int(w_day)]))
        self.label_21.setText(time.strftime('%H:%M:%S',time.localtime(time.time())))

        # 타이머 설정 (1초마다, 콜백함수)
        timer = Timer(1, self.show_time)
        timer.start()
    
    
    def update_data(self):
        #new_sq = self.comboBox_12.currentText()
        #new_rank = self.comboBox_13.currentText()
        #new_major = self.comboBox_14.currentText()
        new_pw = self.lineEdit_3.text()
        new_pw2 = self.lineEdit_4.text()
        if new_pw == new_pw2:
            cur.execute("update 생도 set 비밀번호='{}' where 교번={}".format(new_pw, self.user))
            conn.commit()
            QMessageBox.information(self, '비밀번호 변경 완료', '비밀번호 변경이 완료되었습니다!')

        else:
            QMessageBox.warning(self, '비밀번호 오류', "비밀번호가 다릅니다")
    
    def show_month_graph(self):
        year = self.comboBox_10.currentText()[:-1]
        month = self.comboBox_9.currentText()[:-1]
        if len(month)==1:
            month='0'+month
        cur.execute("select 과목.교과명, avg(점수.점수) from 점수,수강,과목 where 점수.수강번호=수강.수강번호 and 수강.과목코드=과목.과목코드 and date_format(점수.날짜,'%Y-%m')='{}-{}' and 점수.최종여부=1 and 수강.교번={} group by(과목.교과명)".format(year, month, self.user))
        result = cur.fetchall()
        
        if result==():
            self.MplWidget_2.canvas.axes.clear()
        else:
            subjects=[]
            scores=[]
            for i in result:
                subjects.append(i[0])
                scores.append(i[1])
            
            colors=['C3','C1','yellow','C2','C9','C0','C4','C6','C5','C7']
            self.MplWidget_2.canvas.axes.clear()
            bar = self.MplWidget_2.canvas.axes.bar(subjects, scores, color=colors, width=0.4)
            self.MplWidget_2.canvas.axes.set_ylim([min(scores)-20, 100])
            
            for rect in bar:
                height = rect.get_height()
                self.MplWidget_2.canvas.axes.text(rect.get_x()+rect.get_width()/2.0, height, '%.2f' % height, ha='center', va='bottom', size=12)

            self.MplWidget_2.canvas.draw()
            
            cur.execute("select avg(점수.점수) from 점수,수강,과목 where 점수.수강번호=수강.수강번호 and 수강.과목코드=과목.과목코드 and date_format(점수.날짜,'%Y-%m')='{}-{}' and 점수.최종여부=1 and 수강.교번={}"
                        .format(year, month, self.user))
            avg_score = cur.fetchone()[0]
            self.label_20.setText("{}월 평균 : {:.2f}점".format(month, avg_score))
            
            
    def show_graph(self):
        sub = self.comboBox_20.currentText()
        cur.execute("select date_format(점수.날짜,'%m') as m, avg(점수.점수) from 점수,수강,과목 where 점수.수강번호=수강.수강번호 and 수강.과목코드=과목.과목코드 and 수강.교번={} and 과목.교과명='{}' group by m"
                    .format(self.user, sub))
        result = cur.fetchall()
        
        months=[]
        scores=[]
        for i in result:
            months.append(i[0]+'월')
            scores.append(i[1])
        
            self.MplWidget_5.canvas.axes.clear()
        line_graph = self.MplWidget_5.canvas.axes.plot(months, scores, 'o-')
        self.MplWidget_5.canvas.axes.set_ylim([min(scores)-10, 100])
        
        for i in range(len(months)):
            height = scores[i]
            self.MplWidget_5.canvas.axes.text(months[i], float(height)+0.25, '%.2f' %height, ha='center', va='bottom', size = 12)
            
        self.MplWidget_5.canvas.draw()
    
    
    def view_data(self):
        s_date = self.dateEdit.date().toString('yyyy-MM-dd')
        e_date = self.dateEdit_2.date().toString('yyyy-MM-dd')
        
        cur.execute("select 점수.날짜, 점수.교시, 과목.교과명, 점수.점수 from 점수,수강,과목 where 점수.수강번호=수강.수강번호 and 수강.과목코드=과목.과목코드 and 수강.교번={} and 점수.최종여부=1 and 날짜>='{}' and 날짜<='{}' order by 점수.날짜, 점수.교시"
                    .format(self.user, s_date, e_date))
        data = cur.fetchall()
        
        self.tableWidget_5.setRowCount(len(data))
        for i, line in enumerate(data):
            for j, item in enumerate(line):
                self.tableWidget_5.setItem(i, j, QTableWidgetItem(str(item)))
                self.tableWidget_5.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    
    def load_table(self):
        subject = self.comboBox_11.currentText()
        cur.execute("select 수강.수강번호 from 수강,과목 where 수강.과목코드=과목.과목코드 and 수강.교번={} and 과목.교과명='{}'".format(self.user, subject))
        num_tc = cur.fetchone()[0]
        cur.execute("select 날짜,교시,date_format(시각,'%H:%i'),사유,가감,점수 from 점수 where 수강번호={} and 최종여부=0".format(num_tc))
        contents = cur.fetchall()
        
        self.tableWidget_2.setRowCount(len(contents))
        for i, line in enumerate(contents):
            for j,item  in enumerate(line):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(item)))
                self.tableWidget_2.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
    
    
    def view_best3(self):
        year = self.comboBox.currentText()[:-1]
        mon = self.comboBox_2.currentText()[:-1]
        if len(mon)==1:
            mon='0'+mon
        cur.execute("select 생도.전공, 생도.기수, 생도.중대, 생도.이름, avg(점수.점수) from 점수,수강,과목,생도 where 점수.수강번호=수강.수강번호 and 수강.과목코드=과목.과목코드 and 수강.교번=생도.교번 and date_format(점수.날짜,'%Y-%m')='{}-{}' and 점수.최종여부=1 group by 수강.교번 order by avg(점수.점수) desc".format(year,mon))
        result = cur.fetchall()
        
        if result==():
            self.label_30.setText('')
            self.label_31.setText('조회 결과 없음')
            self.label_32.setText('')
        else:
            self.label_30.setText('{} {}.{}.{}  {:.2f}점'.format(result[0][0],result[0][1],result[0][2],result[0][3],result[0][4]))
            self.label_31.setText('{} {}.{}.{}  {:.2f}점'.format(result[1][0],result[1][1],result[1][2],result[1][3],result[1][4]))
            self.label_32.setText('{} {}.{}.{}  {:.2f}점'.format(result[2][0],result[2][1],result[2][2],result[2][3],result[2][4]))
        
    
    def view_worst3(self):
        year = self.comboBox_4.currentText()[:-1]
        mon = self.comboBox_5.currentText()[:-1]
        if len(mon)==1:
            mon='0'+mon
        cur.execute("select 생도.전공, 생도.기수, 생도.중대, 생도.이름, avg(점수.점수) from 점수,수강,과목,생도 where 점수.수강번호=수강.수강번호 and 수강.과목코드=과목.과목코드 and 수강.교번=생도.교번 and date_format(점수.날짜,'%Y-%m')='{}-{}' and 점수.최종여부=1 group by 수강.교번 order by avg(점수.점수)".format(year,mon))
        result = cur.fetchall()
        
        if result==():
            self.label_33.setText('')
            self.label_34.setText('조회 결과 없음')
            self.label_35.setText('')
        else:
            self.label_33.setText('{} {}.{}.{}  {:.2f}점'.format(result[0][0],result[0][1],result[0][2],result[0][3],result[0][4]))
            self.label_34.setText('{} {}.{}.{}  {:.2f}점'.format(result[1][0],result[1][1],result[1][2],result[1][3],result[1][4]))
            self.label_35.setText('{} {}.{}.{}  {:.2f}점'.format(result[2][0],result[2][1],result[2][2],result[2][3],result[2][4]))
            
        

class Stream_thread(QtCore.QThread):
    change_pixmap = QtCore.pyqtSignal(QtGui.QPixmap)
    
    def run(self):
        cap = cv2.VideoCapture(0)
        self.thread_is_active = True
        while self.thread_is_active:
            ret, frame = cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipped_image = cv2.flip(image, 1)
                qt_image = QtGui.QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0], QtGui.QImage.Format_RGB888)
                pic = qt_image.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                pixmap = QtGui.QPixmap.fromImage(pic)
                self.change_pixmap.emit(pixmap)
                
    def stop(self):
        self.thread_is_active = False
        self.quit()
        
        

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

