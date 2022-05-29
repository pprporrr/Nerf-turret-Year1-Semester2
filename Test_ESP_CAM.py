import cv2
import urllib.request
import numpy as np

def nothing(x):
    pass

def camera():
    url='http://192.168.1.167/cam-lo.jpg'
    """cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg"""
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
    while True:
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        frame=cv2.imdecode(imgnp,-1)
        #_, frame = cap.read()
        cv2.imshow("live transmission", frame)
        key=cv2.waitKey(5)
        if key==ord('q'):
            break
        
camera()

cv2.destroyAllWindows()