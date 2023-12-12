import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile

from cv_bridge import CvBridge
from auto_store_package_msgs.msg import ImgNData

import numpy as np
import cv2
import time

from status import *
from customer import Customer
from read_rfid import *

# 이미지 메시지 데이터를 어레이 형태로 변환
bridge = CvBridge() 

action_data = None
stand_data = None

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
    global action_data, stand_data

    img = np.reshape(np.array(msg.img_data), (msg.img_height, msg.img_width, msg.img_channel))
    cv2.imshow('ros_img', img)
    action_data = msg.action_data
    stand_data = msg.stand_data
    # self.get_logger().info('action_data : ' + msg.action_data)
    # self.get_logger().info('stand_data : ' + msg.stand_data)
    cv2.waitKey(10)
     
def main(args=None) :
  global action_data, stand_data

  try :
    customer_dict = {}
    
    # 통신 연결
    # connected = communication_connection()
    rclpy.init(args=args)
    node = ImageSubscriber()

    while rclpy.ok():
      
      # in_RFID_read = read_in_RFID()                       # 입구 RFID 리더로부터 값 수신
      # out_RFID_read = read_out_RFID()                     # 출구 RFID 리더로부터 값 수신
      in_RFID_read = "ff:ff:ff:ff"
      out_RFID_read = None
      
      # action_data, action_time = receive_from_acttion()   # Action-Cam으로부터 값 수신
      # stand_data, stand_time = receive_from_stand()       # Stand-Cam으로부터 값 수신
      
      rclpy.spin_once(node)

      now_time = time.strftime("%Y%m%d-%H%M%S")

      # 입구 RFID가 읽혀졌을 때,
      if in_RFID_read:
          customer = get_checkIn_state(now_time, in_RFID_read)                  # DB에서 고객 정보 가져와서 customer 객체에 저장
          customer_dict[customer.id] = customer           # customer dictionay에 출입한 고객 추가
      
      # 출구 RFID가 읽혀졌을 때,
      if out_RFID_read:
          # 고객 check-in 상태였으면
          if customer.checkIn_state == True:
              customer_dict = get_checkOut_state(now_time, customer_dict)
          else:
              print("Check-out Error")   # check-in된 고객이 없는데 출구 RFID가 찍힌 상태
              exit()  # 일단 프로그램 종료하게 해둠

      
      # 고객 check-in 상태
      if customer.checkIn_state == True:
          
          # Action-Cam에 사람이 관측된 상태
          if action_data['person'] == True:
              log_action_state(now_time, action_data['action'], action_data['fruit_type'])  # 행동 DB 기록
              customer.start_shopping()                                                        # customer.shopping_state를 True로 변경
              customer.update_action_state(action_data['action'])                              # customer 현재 action update
          
          # Action-Cam에 사람이 관측되지 않은 상태
          else:               
              if customer.shopping_state == True:         # 쇼핑 중이었다가 나간 것
                  customer.stop_shopping()                # customer.shopping_state를 False로 변경
                  if customer.shopping_state == 3:            # holding 상태일 때만
                      consistent = double_check(stand_data)   # Stand-Cam 결과와 double check
                      # if consistent == False:                 # 결과가 Stand-Cam과 일치하지 않을 경우, 불일치 logging 
                      #     log_mismatch(now_time)
                      # customer 장바구니 update
                      customer.update_shopping_list(action_data['fruit_type'], action_data['fruit_quantity'])

              # 쇼핑 중이 아님
              else:
                  continue
        
      # 고객 check-out 상태
      else:
          continue
        
  except KeyboardInterrupt :
    node.get_logger().info('Stopped by Keyboard')
  finally :
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__' :
  main()