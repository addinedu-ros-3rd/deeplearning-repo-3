from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
import datetime
import cv2
import time
import re
import time
from  Database import DB
from ImageReceiver import ImageReceiver

from_class = uic.loadUiType("UI.ui")[0]

class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("UI Manager")

        # 입장 퇴장 시간 초기화
        self.minInTime = self.in_time_start.dateTime()
        self.maxInTime = self.in_time_end.dateTime()
        self.minOutTime = self.out_time_start.dateTime()
        self.maxOutTime = self.out_time_end.dateTime()
        
        # 검색, 리셋 버튼 함수 연결
        self.reset_btn.clicked.connect(self.reset)
        self.search_btn.clicked.connect(self.search)

        # 과일이 팔린 개수 로깅
        self.getFruits()

        # 테이블 컬럼 창 크기에 맞춰주기
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        
        self.pixmap = QPixmap()
        
        # self.player = ImageReceiver(filename=file[0], framerate=20)
        self.player = ImageReceiver()
        self.player.daemon = True
        self.player.running = True
        self.player.update.connect(self.updatePlayer)
        self.player.start()
        

        # 불일치 로깅
        self.mismatch()

        # 매대 재고 가져오기
        self.getStock()

    def updatePlayer(self, frame):
        self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # print(frame)
        self.plotImg()

    
    def plotImg(self):
        h, w, c = self.image.shape

        qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)

        self.label.setPixmap(self.pixmap)
    
    
    
    def search(self):
        self.table.clearContents()
        self.getFruits()
        self.mismatch()
        self.getStock()
        # 고객 ID 입력값 변수로 저장
        self.customerId = self.customer_id.text()
        
        inTimeStart = self.in_time_start.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        inTimeEnd = self.in_time_end.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        outTimeStart = self.out_time_start.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        outTimeEnd = self.out_time_end.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        db = DB()
        self.sql = """
            SELECT e.customerID,
            CASE WHEN e.enterStatus = '1' THEN e.enterenceTime ELSE NULL END AS inTime,
            CASE WHEN e.enterStatus = '0' THEN e.enterenceTime ELSE NULL END AS outTime,
            f.fruitName, po.outQuantity, po.outQuantity * f.price AS totalPrice
            FROM enterence e
            LEFT JOIN productOut po ON po.customerID = e.customerID
            LEFT JOIN fruits f ON po.fruitID = f.fruitID
        """
        if self.customerId:
            self.sql += f" WHERE e.customerID = {self.customerId}"

        # 날짜 범위 조건 추가
        if inTimeStart and inTimeEnd:
            self.sql += f" AND e.enterenceTime BETWEEN '{inTimeStart}' AND '{inTimeEnd}'"
            if outTimeStart and outTimeEnd:
                self.sql += f" AND e.enterenceTime BETWEEN '{outTimeStart}' AND '{outTimeEnd}'"
        else:
            if outTimeStart and outTimeEnd:
                self.sql += f" AND e.enterenceTime BETWEEN '{outTimeStart}' AND '{outTimeEnd}'"
            
        self.table.setRowCount(0)

        db.execute(self.sql)
        result = db.fetchAll()
        print(result)

        db.disconnect()
        for row in result:
            resultRow = self.table.rowCount()
            self.table.insertRow(resultRow)
            for i, v in enumerate(row):
                self.table.setItem(resultRow, i, QTableWidgetItem(str(v)))

            
    def reset(self):

        self.table.clearContents()
        

    def getFruits(self):
        db=DB()
        
        self.sql = """
            SELECT po.outDate, f.fruitName, po.outQuantity
            FROM productOut po
            JOIN fruits f ON po.fruitID = f.fruitID
        """

        db.execute(self.sql)
        result = db.fetchAll()
        db.disconnect()
        self.table_2.setRowCount(0)

        for row in result:
            resultRow = self.table_2.rowCount()
            self.table_2.insertRow(resultRow)
            for i, v in enumerate(row):
                self.table_2.setItem(resultRow, i, QTableWidgetItem(str(v)))


    def mismatch(self):
        db = DB()
        self.sql = """
            SELECT m.mismatchTime, f.fruitName, po.outQuantity
            FROM mismatchActionStand AS m
            LEFT JOIN
            fruits f ON m.fruitName = f.fruitName
            LEFT JOIN
            productOut po ON m.fruitName = f.fruitName
        """

        db.execute(self.sql)
        result = db.fetchAll()
        db.disconnect()
        self.table_3.setRowCount(0)

        for row in result:
            resultRow = self.table_3.rowCount()
            self.table_3.insertRow(resultRow)
            for i, v in enumerate(row):
                self.table_3.setItem(resultRow, i, QTableWidgetItem(str(v)))

    def getStock(self):
        db = DB()
        self.sql = """
            select fruitName, stockStand
            from fruits
        """
        db.execute(self.sql)
        result = db.fetchAll()
        db.disconnect()
        result_list = []
        for row in result:
            result_list.append(row)

        self.apple.setText(str(result_list[0][1]))
        self.banana.setText(str(result_list[1][1]))
        self.orange.setText(str(result_list[2][1]))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())

