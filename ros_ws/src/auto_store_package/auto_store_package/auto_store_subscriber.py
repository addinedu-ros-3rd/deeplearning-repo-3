import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from cv_bridge import CvBridge
from auto_store_package_msgs.msg import ImgNData

import numpy as np
import cv2
import time
import json

from modules.status import Status
from modules.customer import Customer
from modules.read_rfid import *

# 이미지 메시지 데이터를 어레이 형태로 변환
bridge = CvBridge() 

action_data = None
stand_data = None

key = None

class ImageSubscriber(Node) :
  def __init__(self) :
    super().__init__('image_sub')
    qos = QoSProfile(depth=10)
    self.image_sub = self.create_subscription(
      ImgNData, # 임포트 된 메시지 타입 
      '/ImgNData', # 토픽리스트에서 조회한 토픽 주소
      self.callback, # 정의한 콜백함수
      qos)
    self.image = np.empty(shape=[1])

  def callback(self, msg) :
    global action_data, stand_data, key

    img = np.reshape(np.array(msg.img_data), (msg.img_height, msg.img_width, msg.img_channel))
    cv2.imshow('ros_img', img)
    action_data = json.loads(msg.action_data)
    stand_data = json.loads(msg.stand_data)
    # self.get_logger().info('action_data : ' + msg.action_data)
    # self.get_logger().info('stand_data : ' + msg.stand_data)
    
    key = cv2.waitKey(10)


### main ###  
def main(args=None) :
  global action_data, stand_data

  status = Status()

  try :
    customer = None
    customer_dict = {}
    before_stand_dict = None
    
    # 통신 연결
    # connected = communication_connection()
    rclpy.init(args=args)
    node = ImageSubscriber()

    while rclpy.ok():
      
      # in_RFID_read = read_in_RFID()                       # 입구 RFID 리더로부터 값 수신
      # out_RFID_read = read_out_RFID()                     # 출구 RFID 리더로부터 값 수신
      in_RFID_read = None
      out_RFID_read = None

      # test code
      if key == ord('i'):
        in_RFID_read = "getrfid0"
        # print(in_RFID_read)
      elif key == ord('o'):
        out_RFID_read = "getrfid0"
        # print(out_RFID_read)
      else :
        in_RFID_read = None
        out_RFID_read = None

      rclpy.spin_once(node) # read action_data & stand_data

      now_time = time.strftime("%Y-%m-%d %H:%M:%S")

      # 입구 RFID가 읽혀졌을 때,
      if in_RFID_read:
        # test code
        before_stand_dict = stand_data

        customer = status.get_checkIn_state(now_time, in_RFID_read)                  # DB에서 고객 정보 가져와서 customer 객체에 저장
        customer_dict[customer.id] = customer           # customer dictionay에 출입한 고객 추가
        
        node.get_logger().info(f"Customer - \"{customer.id}\" entered : {customer.pay_id}")

        in_RFID_read = None
        continue

      # 출구 RFID가 읽혀졌을 때,
      if out_RFID_read:
        # 고객 check-in 상태였으면
        if int(customer.checkIn_state) == True:
          customer.update_out_time(now_time)
          customer_dict = status.get_checkOut_state(now_time, out_RFID_read, customer_dict)
        
          node.get_logger().info(f"Customer - \"{customer.id}\" exited : {customer.pay_id}")

        else:
          print("Check-out Error")   # check-in된 고객이 없는데 출구 RFID가 찍힌 상태
          exit()  # 일단 프로그램 종료하게 해둠

        out_RFID_read = None
        continue
      
      
      # 고객 check-in 상태
      if (customer is not None) and (int(customer.checkIn_state) == True):

        # Action-Cam에 사람이 관측된 상태
        if int(action_data['person']) == True:
          status.update_db.log_action_state(now_time, action_data['action'], action_data['fruit_type'])  # 행동 DB 기록
          customer.start_shopping()                                                        # customer.shopping_state를 True로 변경
          customer.update_action_state(int(action_data['action']))                              # customer 현재 action update
        
        # Action-Cam에 사람이 관측되지 않은 상태
        else:               
          if int(customer.shopping_state) == True:         # 쇼핑 중이었다가 나간 것
            customer.stop_shopping()                # customer.shopping_state를 False로 변경
            if int(customer.action_state) in [1,3]:            # holding 상태일 때만
              matching, differ_fruit_Name, differ_quantity, before_fruit_total, cur_fruit_total \
                  = status.get_difference(before_stand_dict, stand_data, action_data)
              print(matching, differ_fruit_Name, differ_quantity, before_fruit_total, cur_fruit_total)
              if matching == False:                 # 결과가 Stand-Cam과 일치하지 않을 경우, 불일치 logging 
                status.update_db.log_mismatch(now_time, differ_fruit_Name, differ_quantity, before_fruit_total, cur_fruit_total)
              else:
                # customer 장바구니 update
                customer.update_shopping_list(action_data['fruit_type'], action_data['fruit_quantity'])
                # status.update_db.update_fruit_stock(customer, action_data['fruit_type'], action_data['fruit_quantity'])

          # 쇼핑 중이 아님
          # else:
          #     continue
      
        continue
        
      # 고객 check-out 상태
      else:
          continue
      
  # except Exception as e:
  #   node.get_logger().info(str(type(e)) + ',' + str(e))
  # # except KeyboardInterrupt :
  # #   # node.get_logger().info('Stopped by Keyboard')

  finally :
    status.disconnect_db()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
  main()