from status import *
from customer import Customer
from read_rfid import *


def main():
    customer_dict = {}
    
    # 통신 연결
    connected = communication_connection()

    while connected:
        in_RFID_read = read_in_RFID()                       # 입구 RFID 리더로부터 값 수신
        out_RFID_read = read_out_RFID()                     # 출구 RFID 리더로부터 값 수신
        action_info, action_time = receive_from_acttion()   # Action-Cam으로부터 값 수신
        stand_info, stand_time = receive_from_stand()       # Stand-Cam으로부터 값 수신


        # 입구 RFID가 읽혀졌을 때,
        if in_RFID_read:
            customer = get_checkIn_state()                  # DB에서 고객 정보 가져와서 customer 객체에 저장
            customer_dict[customer.id] = customer           # customer dictionay에 출입한 고객 추가
        
        # 출구 RFID가 읽혀졌을 때,
        if out_RFID_read:
            # 고객 check-in 상태였으면
            if customer.checkIn_state == True:
                customer_dict = get_checkOut_state(customer_dict)
            else:
                print("Check-out Error")   # check-in된 고객이 없는데 출구 RFID가 찍힌 상태
                exit()  # 일단 프로그램 종료하게 해둠

        
        # 고객 check-in 상태
        if customer.checkIn_state == True:
            
            # Action-Cam에 사람이 관측된 상태
            if action_info['person'] == True:
                log_action_state(action_time, action_info['action'], action_info['fruit_type'])  # 행동 DB 기록
                customer.start_shopping()                                                        # customer.shopping_state를 True로 변경
                customer.update_action_state(action_info['action'])                              # customer 현재 action update
            
            # Action-Cam에 사람이 관측되지 않은 상태
            else:               
                if customer.shopping_state == True:         # 쇼핑 중이었다가 나간 것
                    customer.stop_shopping()                # customer.shopping_state를 False로 변경
                    if customer.shopping_state == 3:            # holding 상태일 때만
                        consistent = double_check(stand_info)   # Stand-Cam 결과와 double check
                        if consistent == False:                 # 결과가 Stand-Cam과 일치하지 않을 경우, 불일치 logging 
                            log_mismatch(stand_time)
                        # customer 장바구니 update
                        customer.update_shopping_list(action_info['fruit_type'], action_info['fruit_quantity'])

                # 쇼핑 중이 아님
                else:
                    continue
                
        
        # 고객 check-out 상태
        else:
            continue



if __name__ == "__main__":
    main()