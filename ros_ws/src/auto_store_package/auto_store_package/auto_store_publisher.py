import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2


class camPublisher(Node) :
  def __init__(self) :
    super().__init__('cam_publisher')
    self.publisher = self.create_publisher(Image, 'droid_cam', 10)
    time_period = 0.01
    self.timer = self.create_timer(time_period, self.time_callback)
    self.cap = cv2.VideoCapture('http://IP address:4747/video') 
    # IP address 자리에 본인 ip 주소 입력

  # def time_callback(self) :
  #   ret, frame = self.cap.read()
  #   cv2.imwrite('test.jpg', frame)
  #   if ret == True :
  #     fra = bridge.cv2_to_imgmsg(frame)
  #     self.publisher.publish(fra)
  #     cv2.imshow('droidcamframe', frame)
  #     cv2.waitKey(2)
  #   self.get_logger().info('Publishing Droidcam Image')


def main(args=None) :
  rclpy.init(args=args)
  node = camPublisher()
  try :
    rclpy.spin(node)
  except KeyboardInterrupt :
    node.get_logger().info('Publish Stopped')
  finally :
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__' :
  main()