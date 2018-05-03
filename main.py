from array import array
from builtins import print
from distutils.command.config import config

import numpy as np
import cv2

"""
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
"""


def pointsNear(a, b):
    return np.sqrt((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1])) < 10


def hasPoint(pol, a):
    for p in pol:
        if pointsNear(p, a):
            return True
    return False


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


img = cv2.imread("img.png")
wname = "OpenCV for Dummies"
window = cv2.namedWindow(wname)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 10, 100, apertureSize=3)

"""
lines = cv2.HoughLines(edges, 2, 6*np.pi/180, 80)
for arg in lines:
    rho, theta = arg[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
"""
"""
points = []

lines = cv2.HoughLinesP(edges, 1, 1 * np.pi / 180, 30, minLineLength=50, maxLineGap=10)
for line in lines:
    for x1, y1, x2, y2 in line:
        if not hasPoint(points, (x1, y1)):
            points.append((x1, y1))
        if not hasPoint(points, (x2, y2)):
            points.append((x2, y2))
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

for p in points:
    cv2.circle(img, p, 4, (0,100,255), -1)
"""

_, thresh = cv2.threshold(gray, 127, 255, 0)

im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours[1::2]:
    shape = cv2.approxPolyDP(c, 4, True)
    for p in shape:
        cv2.circle(img, tuple(p[0]), 3, (0, 100, 255), -1)
    hull = cv2.convexHull(c)
    for a, o, b in angles(shape):
        cosab = length(a,o)*length(a,o)+length(b,o)*length(b,o)-length(a,b)*length(a,b)
        ang = np.arccos(cosab / 2 / length(a,o) / length(b,o))/np.pi*180
        if cv2.pointPolygonTest(hull, tuple(o), False) > 0:
            ang += 180
        cv2.putText(img, '%(num)d' % {"num": np.round(ang)}, tuple(o), cv2.FONT_HERSHEY_PLAIN, 1.2, (150,50,0))

#lines = cv2.HoughLinesP(contours[1], 1, 1 * np.pi / 180, 30, minLineLength=50, maxLineGap=10)

cv2.imshow(wname, img)
cv2.waitKey(0)

cv2.destroyWindow(wname)
