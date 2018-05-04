import numpy as np
import cv2


def angles(lst):
    if len(lst) < 3:
        return
    i = iter(lst)
    last = lst[-2]
    this = lst[-1]
    for next in i:
        yield last[0], this[0], next[0]
        last = this
        this = next


def length(a, b):
    return np.sqrt((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]))


def near(a, b):
    return length(a, b) < 20


cap = cv2.VideoCapture(0)
wname = "OpenCV for Dummies"
window = cv2.namedWindow(wname)

while True:
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200, apertureSize=3)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilated = cv2.dilate(edges, kernel)
    _, thresh = cv2.threshold(dilated, 50, 255, 0)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    prev = [[[0, 0]]]
    for c in contours:
        shape = cv2.approxPolyDP(c, 7, True)
        if len(shape) < 2:
            continue
        if len(shape) == len(prev) and near(shape[0][0], prev[0][0]):
            continue
        for p in shape:
            cv2.circle(img, tuple(p[0]), 3, (0, 100, 255), -1)
        hull = cv2.convexHull(c)
        for a, o, b in angles(shape):
            cosab = length(a,o)*length(a,o)+length(b,o)*length(b,o)-length(a,b)*length(a,b)
            ang = np.arccos(cosab / 2 / length(a,o) / length(b,o))/np.pi*180
            if cv2.pointPolygonTest(hull, tuple(o), False) > 0:
                ang += 180
            cv2.putText(img, '%(num)d' % {"num": np.round(ang)}, tuple(o), cv2.FONT_HERSHEY_PLAIN, 1.2, (150,50,0))
        prev = shape

    cv2.imshow(wname, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyWindow(wname)
