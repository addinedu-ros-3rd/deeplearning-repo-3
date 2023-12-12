import time
from customer import Customer
from update_db import *

# Checking communication connection
def communication_connection():
    connected = True
    return connected


def get_checkIn_state():
    checkIn_time = time.strftime("%Y%m%d-%H%M%S")
    customer_id, pay_id = get_customer_info()        # DB에서 고객 정보 가져
    log_checkIn_state(checkIn_time, customer_id)     # DB에 출입 테이블에 기록
    
    customer = Customer()
    customer.id = customer_id
    customer.pay_id = pay_id
    customer.in_time = checkIn_time

    return customer


def get_checkOut_state(customer_dict):
    checkOut_time = time.strftime("%Y%m%d-%H%M%S")
    customer_id, _ = get_customer_info()
    customer = customer_dict[customer_id]

    customer.update_out_time(checkOut_time)
    customer.checkIn_state = False                  # 고객의 check-in 상태 False 로 변경
    fruit_type = customer.shopping_list.keys()[0]  # 추가(태상)
    fruit_values = customer.shopping_list.values()[0]  # 추가(태상)

    price_list = get_price_list(fruit_type)         # DB에서 가격표 조회 필요
    customer.calc_total_price(price_list)           # 구매한 전체 금액 계산
    make_payment(customer)           # 결제 : 결제 내역 DB 업데이트 포함 
    log_checkOut_state(checkOut_time, customer.id)
    update_fruit_stock(fruit_type, fruit_values)    # 과일 재고 update

    customer_dict.pop(customer_dict)                # customer_dict에서 나가는 customer 제외

    return customer_dict


# Receiving information from Action-Cam
# action_info includes presence of a person, action type, fruit type and fruit quantity
def receive_from_acttion():
    action_time = time.strftime("%Y%m%d-%H%M%S")
    action_info = None # dictionay type
    return action_info, action_time


# Receiving information from Stand-Cam
def receive_from_stand():
    stand_time = time.strftime("%Y%m%d-%H%M%S")
    stand_info = None
    return stand_info, stand_time


def double_check(stand_info):
    matching = None
    return matching



