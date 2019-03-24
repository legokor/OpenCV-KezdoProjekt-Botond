import angledrawer
import cv2


cap = cv2.VideoCapture(0)
wname = "OpenCV for Dummies"
window = cv2.namedWindow(wname)

while True:
    ret, img = cap.read()

    img = angledrawer.draw(img)

    cv2.imshow(wname, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyWindow(wname)
