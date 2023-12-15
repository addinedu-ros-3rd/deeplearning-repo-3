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
        
        print(customer.shopping_list)
        fruit_type = customer.shopping_list.keys()  # 추가(태상)
        if len(fruit_type) > 0:
            fruit_type = list(fruit_type)[0]
            fruit_counts = customer.shopping_list[fruit_type]  # 추가(태상)

            price_list = self.update_db.get_price_list(fruit_type)         # DB에서 가격표 조회 필요 (현재는 price 하나만 받음)
            # customer.calc_total_price(price_list)           # 구매한 전체 금액 계산
            customer.total_price = fruit_counts * price_list
            self.update_db.make_payment(customer)           # 결제 : 결제 내역 DB 업데이트 포함 
            self.update_db.update_fruit_stock(customer, fruit_type, fruit_counts)    # 과일 재고 update

        self.update_db.log_checkOut_state(checkOut_time, customer.id)
        customer_dict.pop(customer_id)                # customer_dict에서 나가는 customer 제외

        return customer_dict
    

    def double_check(self, differ_dict, action_fruit_type, action_fruit_quantity):
        matching = True

        fruit_dict = {
            1: "Banana",
            0: "Apple",
            2: "Orange",
            5: "None"
        }
        
        if differ_dict[fruit_dict[action_fruit_type]] != int(action_fruit_quantity):
            matching = False

        differ_fruit_type = action_fruit_type
        differ_quantity = int(action_fruit_quantity) - differ_dict[fruit_dict[action_fruit_type]]

        return matching, differ_fruit_type, differ_quantity
    

    def get_difference(self, before_stand_dict, cur_stand_dict, action_data):

        # 각 과일의 합을 저장할 딕셔너리
        before_fruit_total = {}
        cur_fruit_total = {}

        # 이전매대를 순회하면서 각 과일 개수를 합산
        for key in before_stand_dict:
            for fruit, count in before_stand_dict[key].items():
                if fruit in before_fruit_total:
                    before_fruit_total[fruit] += count
                else:
                    before_fruit_total[fruit] = count

        for key in cur_stand_dict:
            for fruit, count in cur_stand_dict[key].items():
                if fruit in cur_fruit_total:
                    cur_fruit_total[fruit] += count
                else:
                    cur_fruit_total[fruit] = count
        

        # 결과를 저장할 빈 딕셔너리
        difference = {}

        # 이전매대와 현재매대의 차이를 계산
        for key in before_fruit_total:
            difference[key] = before_fruit_total[key] - cur_fruit_total[key]

        matching, differ_fruit_type, differ_quantity = self.double_check(difference, action_data['fruit_type'], action_data['fruit_quantity'])   # Stand-Cam 결과와 double check

        return matching, differ_fruit_type, differ_quantity, before_fruit_total, cur_fruit_total
    
    
    def disconnect_db(self):
        self.update_db.disconnect_db()
    



