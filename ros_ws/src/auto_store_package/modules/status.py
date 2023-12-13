import time
from modules.customer import Customer
from modules.update_db import Update_DB

class Status():
    def __init__(self) -> None:
        self.update_db = Update_DB()

    # Checking communication connection
    def communication_connection(self):
        connected = True
        return connected


    def get_checkIn_state(self, checkIn_time, pay_id):
        customer_id = self.update_db.get_customer_info(pay_id)        # DB에서 고객 정보 가져
        self.update_db.log_checkIn_state(checkIn_time, customer_id)     # DB에 출입 테이블에 기록
        
        customer = Customer(customer_id, pay_id, checkIn_time)
        # customer.id = customer_id
        # customer.pay_id = pay_id
        # customer.in_time = checkIn_time
        customer.checkIn_state = True

        return customer


    def get_checkOut_state(self, checkOut_time, pay_id, customer_dict):
        customer_id = self.update_db.get_customer_info(pay_id)
        customer = customer_dict[customer_id]

        customer.update_out_time(checkOut_time)
        customer.checkIn_state = False                  # 고객의 check-in 상태 False 로 변경
        fruit_type = list(customer.shopping_list.keys())[0]  # 추가(태상)
        fruit_counts = customer.shopping_list[fruit_type]  # 추가(태상)

        price_list = self.update_db.get_price_list(fruit_type)         # DB에서 가격표 조회 필요 (현재는 price 하나만 받음)
        # customer.calc_total_price(price_list)           # 구매한 전체 금액 계산
        customer.total_price = fruit_counts * price_list
        self.update_db.make_payment(customer)           # 결제 : 결제 내역 DB 업데이트 포함 
        self.update_db.log_checkOut_state(checkOut_time, customer.id)
        self.update_db.update_fruit_stock(fruit_type, fruit_counts)    # 과일 재고 update

        customer_dict.pop(customer_id)                # customer_dict에서 나가는 customer 제외

        return customer_dict


    # # Receiving information from Action-Cam
    # # action_info includes presence of a person, action type, fruit type and fruit quantity
    # def receive_from_action(self):
    #     action_time = time.strftime("%Y%m%d-%H%M%S")
    #     action_info = None # dictionay type
    #     return action_info, action_time


    # # Receiving information from Stand-Cam
    # def receive_from_stand(self):
    #     stand_time = time.strftime("%Y%m%d-%H%M%S")
    #     stand_info = None
    #     return stand_info, stand_time


    def double_check(self, stand_info):
        matching = None
        return matching
    
    def disconnect_db(self):
        self.update_db.disconnect_db()
    



