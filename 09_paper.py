import sys
import cv2
import numpy as np


def drawROI(img, quads):
    cpy = img.copy()
    quads = quads.astype(np.int16)
    edges = quads[:4]
    centers = quads[4:]

    c1 = (192, 192, 255)
    c2 = (128, 128, 255)

    for i in range(4):
        cv2.circle(cpy, tuple(edges[i]), 25, c1, -1, cv2.LINE_AA)
        cv2.circle(cpy, tuple(centers[i]), 25, c1, -1, cv2.LINE_AA)
        cv2.line(cpy, tuple(edges[i-1]), tuple(edges[i]), c2, 2, cv2.LINE_AA)

    disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

    return disp


def onMouse(event, x, y, flags, params):
    global srcQuad, dragSrc, ptOld, src
    edges = srcQuad[:4]
    centers = srcQuad[4:]

    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(8):
            if cv2.norm(srcQuad[i] - (x, y)) < 25:
                dragSrc[i] = True
                ptOld = (x, y)
                break


    if event == cv2.EVENT_LBUTTONUP:
        for i in range(8):
            dragSrc[i] = False

    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(8):
            if dragSrc[i]:
                dx = x - ptOld[0]
                dy = y - ptOld[1]

                if i < 4:
                    srcQuad[i] += (dx, dy)

                # 원래 기울기로 계산해야됨
                elif i == 4 or i == 6 : 
                    srcQuad[i] += (0, dy)
                    edges[i-4] += (0, dy)
                    edges[i-4-1] += (0, dy)
                else :
                    srcQuad[i] += (dx, 0)
                    edges[i-4] += (dx, 0)
                    edges[i-4-1] += (dx, 0)
                
                for j in range(4):
                    centers[j] = [(edges[j-1][0] + edges[j][0]) / 2 , (edges[j-1][1] + edges[j][1]) / 2]

                cpy = drawROI(src, srcQuad)
                cv2.imshow('img', cpy)
                ptOld = (x, y)
                break

if __name__ == "__main__":
    src = cv2.imread("./data/scanned.jpg")

    if src is None:
        print("Image Not Found")
        sys.exit()

    h, w = src.shape[:2]
    dw = 500
    dh = round(dw * 297 / 210)  # A4 크기 : 210x297mm
    margin = 30

    srcQuad = [[margin, margin], [margin, h-margin], [w-margin, h-margin], [w-margin, margin]]
    for i in range(4):
        srcQuad.append([(srcQuad[i-1][0] + srcQuad[i][0]) / 2 , (srcQuad[i-1][1] + srcQuad[i][1]) / 2])
    srcQuad = np.array(srcQuad, np.float32)
    dstQuad = np.array([[0, 0], [0, dh-1], [dw-1, dh-1], [dw-1, 0]], np.float32)
    dragSrc = [False] * 8

    disp = drawROI(src, srcQuad)

    cv2.imshow('img', disp)
    cv2.setMouseCallback('img', onMouse)

    while True:
        key = cv2.waitKey()
        if key == 13:
            break
        elif key == 27:
            cv2.destroyWindow('img')
            sys.exit()

    pers = cv2.getPerspectiveTransform(srcQuad[:4], dstQuad)
    dst = cv2.warpPerspective(src, pers, (dw, dh), flags=cv2.INTER_CUBIC)

    cv2.imshow('dst', dst)

    while True:
        if cv2.waitKey() == 27:
            break

    cv2.destroyAllWindows()

