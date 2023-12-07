import socket
import cv2

UDP_IP = '127.0.0.1'
UDP_PORT = 9505

cap = cv2.VideoCapture(3)


while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        frame = frame.resize((480, 640))
        if frame:
            print(frame)
            cv2.imshow("aaa", frame)

            d = frame.flatten()
            s = d.tostring()

            for i in range(20):
                sock.sendto(bytes([i]) + s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))    
    print(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break