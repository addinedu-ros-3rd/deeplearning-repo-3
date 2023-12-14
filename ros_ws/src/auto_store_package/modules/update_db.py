from modules.DB import DB
from modules.Logger import Logger
from modules.read_rfid import *


class Update_DB():
    def __init__(self) -> None:
        self.db = DB()
        self.log = Logger('log.log')
        # ser = serial.Serial("/dev/ttyACM0", 9600)  # rfid와 시리얼 통신 필요

    # 고객 table에서 고객 정보 가져오기
    def get_customer_info(self, rfid):
        try:
            query = "select customerID from customer where personality=%s"
            self.db.execute(query, (rfid,))

            customer_ID = self.db.fetchone()

            return customer_ID
        
        except Exception as e:
            print(f"get_customer_info() is error")
            return None 


    # 출입 table : check-in 상태 logging
    def log_checkIn_state(self, checkIn_time, customer_info):
        try:
            query = "insert into enterence (customerID, enterenceTime, enterStatus) values (%s, %s, %s)"
            self.db.execute(query, (customer_info, checkIn_time, 1))
        except Exception as e:
            self.log.error(f"log_checkIn_state() is error")
        

    # 출입 table : check-out 상태 logging
    def log_checkOut_state(self, checkOut_time, customer_info):
        try:
            query = "insert into enterence (customerID, enterenceTime, enterStatus) values (%s, %s, %s)"
            self.db.execute(query, (customer_info, checkOut_time, 0))
        except Exception as e:
            self.log.error(f"log_checkOut_state() is error")
        


    # 결제 내역 table : logging
    def make_payment(self, customer):
        customer_ID = customer.id
        checkOut_time = customer.out_time
        price = customer.total_price
        try:
            query = """insert into payment (customerID, enterenceTime, totalAmount) values (%s, %s, %s)"""
            self.db.execute(query, (customer_ID, checkOut_time, price))
        except Exception as e:
            self.log.error(f"make_payment() is error")
        


    # 행동 인식 table : logging
    def log_action_state(self, action_time, action_type, fruit_id):
        # print(action_time, action_type, fruit_id)
        try:
            query = """insert into actionRecognition (fruitID, actionTime, actionType) values (%s, %s, %s)"""
            self.db.execute(query, (fruit_id, action_time, action_type))
            
        except Exception as e:
            self.log.error(f"log_action_state() is error")
            print(f"log_action_state() is error {type(e)} - {e}")


    # # 불일치 table : logging
    # def log_mismatch(self, customer, mismatch_time):
    #     try:
    #         query = "insert into mismatchActionStand (standFruitID, actionFruitID, mismatch) values (%s, %s, %s)"
    #         self.db.execute(query, (fruit_id, action_time, action_type))
    #     except Exception as e:
    #         self.log.error(f"make_payment() is error")
        


    # 과일 table : 재고 update
    def update_fruit_stock(self, fruit_type, fruit_out_counts):
        try:
            query = "select stockStand from fruits where fruitID=%s"
            self.db.execute(query, (fruit_type,))

            fruit_stock_counts = self.db.fetchone()

            query = "update fruits set stockStand=%s where fruitID=%s"
            self.db.execute(query, ((fruit_stock_counts-fruit_out_counts), fruit_type))

        except Exception as e:
            self.log.error(f"update_fruit_stock() is error")
        
        

    # 과일 table : 과일 가격 조회
    def get_price_list(self, fruit_type):
        try:
            query = "select price from fruits where fruitID=%s"
            self.db.execute(query, (fruit_type,))

            price = self.db.fetchone()
            return price
        
        except Exception as e:
            self.log.error(f"get_price_list() is error")
            return None

    def disconnect_db(self):
        self.db.disconnect()
        