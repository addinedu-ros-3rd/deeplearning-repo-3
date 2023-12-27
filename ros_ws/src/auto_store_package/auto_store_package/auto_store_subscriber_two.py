import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from auto_store_package_msgs.msg import ImgNData
import numpy as np
import cv2

class ImageSubscriber(Node) :
  def __init__(self) :
    super().__init__('image_sub')

    qos = QoSProfile(depth=10)

    self.image_sub_1 = self.create_subscription(
      ImgNData, # 임포트 된 메시지 타입 
      '/ImgNData_1', # 토픽리스트에서 조회한 토픽 주소
      self.image_callback1, # 정의한 콜백함수
      qos)
    self.image_1 = np.empty(shape=[1])

    self.image_sub_2 = self.create_subscription(
      ImgNData, # 임포트 된 메시지 타입 
      '/ImgNData_2', # 토픽리스트에서 조회한 토픽 주소
      self.image_callback2, # 정의한 콜백함수
      qos)
    self.image_2 = np.empty(shape=[1])

  def image_callback1(self, msg) :
    img = np.reshape(np.array(msg.img_data), (msg.img_height, msg.img_width, msg.img_channel))
    cv2.imshow('ros_img1', img)
    self.get_logger().info('from cam 1 -> ' + msg.fruit_data)
    cv2.waitKey(10)

  def image_callback2(self, msg) :
    img = np.reshape(np.array(msg.img_data), (msg.img_height, msg.img_width, msg.img_channel))
    cv2.imshow('ros_img2', img)
    self.get_logger().info('from cam 2 -> ' + msg.fruit_data)
    cv2.waitKey(10)
     
def main(args=None) :
  rclpy.init(args=args)
  node = ImageSubscriber()
  
  try :
    rclpy.spin(node)
  except KeyboardInterrupt :
    node.get_logger().info('Stopped by Keyboard')
  finally :
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__' :
  main()