import cv2
import numpy as np

cap = cv2.VideoCapture("./data/test_sample1.MOV")

canny_low_threshold = 100
canny_high_threshold = 200

while cap.isOpened():
    ret, image =  cap.read()

    if ret:
        # Load image, convert to grayscale, Otsu's threshold
        result = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (6,6), 1)
        canny = cv2.Canny(blur, canny_low_threshold, canny_high_threshold)

        cv2.imshow("canny", canny)
        

        # _, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

        # lines = cv2.HoughLinesP(thr, rho=1, theta=np.pi / 180, threshold=128, minLineLength=300, maxLineGap=30)
        # lines = lines.squeeze()

        # for x1, y1, x2, y2 in lines:
        #     cv2.line(result, (x1, y1), (x2, y2), color=(0, 0, 255)

        # contours, hier = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # for i, contour in enumerate(contours):
        #     # if hier[0][i][2] == -1:
        #     #     continue

        #     approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        #     if len(approx) == 4:
        #         x, y, w, h = cv2.boundingRect(contour)

        #         area = w * h    
        #         aspectRatio = float(w) / h

        #         if 0.5 <= aspectRatio <= 5 and area > 300:
        #             cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow('Result', result)

        key = cv2.waitKey(30)

        if key == 0x1B:
            break
        elif key == ord("q"):
            canny_low_threshold += 10
            print("canny_low_threshold : ", canny_low_threshold)
        elif key == ord("a"):
            canny_low_threshold -= 10
            print("canny_low_threshold : ", canny_low_threshold)
        elif key == ord("w"):
            canny_high_threshold += 10
            print("canny_high_threshold : ", canny_high_threshold)
        elif key == ord("s"):
            canny_high_threshold -= 10
            print("canny_high_threshold : ", canny_high_threshold)
    
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

cv2.destroyAllWindows()