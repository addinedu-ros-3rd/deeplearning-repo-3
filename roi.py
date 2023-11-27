import sys
import cv2
import numpy as np

class Square:
    def __init__(self, h, w):
        dw = 100
        dh = round(dw * 297 / 210)  # A4 크기 : 210x297mm
        margin = 4 * h / 5
        self.srcQuad = [[margin, margin], [margin, h-margin], [w-margin, h-margin], [w-margin, margin]]
        self.srcQuad = np.array(self.srcQuad, np.float32)
        self.dragSrc = [False] * 4
        self.ptOld = None

    def savePoints(self):
        return " ".join(map(str, np.array(self.srcQuad).flatten().tolist())) + "\n"
            
    def loadPoints(self, points):
        self.srcQuad = points
        self.srcQuad = np.array(self.srcQuad, np.float32)

def drawROI(img):
    global squares
    cpy = img.copy()

    for sq in squares:
        quads = sq.srcQuad.astype(np.int16)

        c1 = (192, 192, 255)
        c2 = (128, 128, 255)

        for i in range(4):
            cv2.circle(cpy, tuple(quads[i]), 25, c1, -1, cv2.LINE_AA)
            cv2.line(cpy, tuple(quads[i-1]), tuple(quads[i]), c2, 2, cv2.LINE_AA)

        disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

    return disp


def onMouse(event, x, y, flags, params):
    global src, squares
    # edges = srcQuad[:4]
    # centers = srcQuad[4:]

    if event == cv2.EVENT_LBUTTONDOWN:
        for sq in squares:
            for i in range(4):
                if cv2.norm(sq.srcQuad[i] - (x, y)) < 25:
                    sq.dragSrc[i] = True
                    sq.ptOld = (x, y)
                    break


    if event == cv2.EVENT_LBUTTONUP:
        for sq in squares:
            for i in range(4):
                sq.dragSrc[i] = False

    if event == cv2.EVENT_MOUSEMOVE:
        flag = False
        for sq in squares:
            for i in range(4):
                if sq.dragSrc[i]:
                    flag = True
                    dx = x - sq.ptOld[0]
                    dy = y - sq.ptOld[1]

                    sq.srcQuad[i] += (dx, dy)

                    cpy = drawROI(src)
                    cv2.imshow('img', cpy)
                    sq.ptOld = (x, y)
                    break
            if flag:
                break


if __name__ == "__main__":
    cam = cv2.VideoCapture(1)

    while not cam.isOpened():
        i=0

    _, src = cam.read()

    if src is None:
        print("Image Not Found")
        sys.exit()

    h, w = src.shape[:2]

    squares = [Square(h, w)]

    disp = drawROI(src)

    cv2.imshow('img', disp)
    cv2.setMouseCallback('img', onMouse)

    while True:
        key = cv2.waitKey()
        if key == 13:
            break

        elif key == 27:
            cv2.destroyWindow('img')
            sys.exit()

        elif key == ord("a"):
            squares.append(Square(h, w))
            cpy = drawROI(src)
            cv2.imshow('img', cpy)
            
        elif key == ord("s"):
            with open("save.txt", "w") as f:
                for sq in squares:
                    f.write(sq.savePoints())
            
            cv2.destroyWindow('img')
            sys.exit()

        elif key == ord("l"):
            squares = []
            with open("save.txt", "r") as f:
                for line in f.readlines():
                    a = np.array(list(map(np.float32, line.split())))
                    a = a.reshape((4, 2))
                    sq = Square(h, w)
                    sq.loadPoints(a)
                    squares.append(sq)
            cpy = drawROI(src)
            cv2.imshow('img', cpy)


    cv2.destroyAllWindows()

