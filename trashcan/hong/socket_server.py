import socket
import numpy
import cv2

UDP_IP = "192.168.0.37"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 875520 for x in range(875520//46080 + 2)]

# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))

while True:
    picture = b''

    data, addr = sock.recvfrom(875520 + 1) # 순번 1byte + 640 * 480 * 3 = 46080bytes
    s[data[0]] = data[1:875520+1]

    if data[0] == 19:
        for i in range(20):
            picture += s[i]

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        # frame = frame.reshape(480, 640, 3)
        cv2.imshow("frame", frame)
        # out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break