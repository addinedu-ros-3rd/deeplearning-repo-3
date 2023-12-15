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
        # self.getFruits()

        # 테이블 컬럼 창 크기에 맞춰주기
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 불일치 로깅
        # self.mismatch()

    def search(self):
        self.table.clearContents()

        # 고객 ID 입력값 변수로 저장
        self.customerId = self.customer_id.text()
        
        inTimeStart = self.in_time_start.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        inTimeEnd = self.in_time_end.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        outTimeStart = self.out_time_start.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        outTimeEnd = self.out_time_end.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        db = DB()
        self.sql = """
        SELECT c.customerID, 
        CASE WHEN e.enterStatus = '1' THEN e.enterenceTime ELSE NULL END AS inTime,
        CASE WHEN e.enterStatus = '0' THEN e.enterenceTime ELSE NULL END AS outTime,
        f.fruitName, s.outQuantity, p.totalAmount
        FROM shoppingBasket s
        LEFT JOIN customer c ON s.customerID = c.customerID
        LEFT JOIN payment p ON s.shoppingID = p.shoppingID
        LEFT JOIN fruits f ON s.fruitID = f.fruitID
        LEFT JOIN enterence e ON e.customerID = c.customerID
        """
        # 날짜 범위 조건 추가
        if inTimeStart and inTimeEnd:
            self.sql += f"WHERE e.enterenceTime BETWEEN '{inTimeStart}' AND '{inTimeEnd}'"
            if outTimeStart and outTimeEnd:
                self.sql += f" AND e.enterenceTime BETWEEN '{outTimeStart}' AND '{outTimeEnd}'"
        else:
            if outTimeStart and outTimeEnd:
                self.sql += f"WHERE e.enterenceTime BETWEEN '{outTimeStart}' AND '{outTimeEnd}'"

        # # 날짜 범위 조건 추가
        # if inTimeStart and inTimeEnd:
        #     self.sql += f"WHERE e.enterenceTime BETWEEN '{inTimeStart}' AND '{inTimeEnd}'"
        
        # customerID가 입력된 경우 해당 ID에 대한 데이터만 조회
        if self.customerId:
            self.sql += f" AND c.customerID = {self.customerId}"

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
            SELECT p.paymentTime, f.fruitName, s.outQuantity
            FROM shoppingBasket s
            LEFT JOIN payment p ON s.shoppingID = p.shoppingID
            LEFT JOIN fruits f ON s.fruitID = f.fruitID
        """

        db.execute(self.sql)
        result = db.fetchAll()
        db.disconnect()

        for row in result:
            resultRow = self.table_2.rowCount()
            self.table_2.insertRow(resultRow)
            for i, v in enumerate(row):
                self.table_2.setItem(resultRow, i, QTableWidgetItem(str(v)))


    def mismatch(self):
        db = DB()
        self.sql = """
            SELECT mismatch, f1.fruitName, f2.fruitName
            FROM mismatchActionStand AS m
            LEFT JOIN fruits AS f1 ON m.standFruitID = f1.fruitID
            LEFT JOIN fruits AS f2 ON m.actionFruitID = f2.fruitID
        """

        db.execute(self.sql)
        result = db.fetchAll()
        db.disconnect()

        for row in result:
            resultRow = self.table_3.rowCount()
            self.table_3.insertRow(resultRow)
            for i, v in enumerate(row):
                self.table_3.setItem(resultRow, i, QTableWidgetItem(str(v)))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())

