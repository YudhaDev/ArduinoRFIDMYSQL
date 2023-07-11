import cv2
import win32
import win32com.client
import numpy as np

class MediaClass:
    kernel = np.one
    def loadImage(self):
        img = cv2.imread("Resources/builder1.jpg")
        cv2.imshow("Output", img)
        cv2.waitKey(0)
        return

    def loadImagePostFX(self, mode):
        img = cv2.imread("Resources/builder1.jpg")

        imgGreyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGreyscale, (7, 7), 0)
        imgCanny = cv2.Canny(img,200,200)
        imgdialation =

        cv2.imshow("imgGreyscale", imgGreyscale)
        cv2.imshow("imgBlur", imgBlur)
        cv2.imshow("imgCanny", imgCanny)
        cv2.waitKey(0)

        match mode:
            case 0:
                return
            case 1:
                return
            case 2:
                return

    def loadVideo(self):
        vid = cv2.VideoCapture("Resources/nature.mp4")
        while True:
            success, img = vid.read()
            cv2.imshow("Output Video", img)
            if cv2.waitKey(1) and 0xFF == ord("q"):
                return

    def loadWebcam(self):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)
        cam.set(4, 480)

        while True:
            success, img = cam.read()
            cv2.imshow("Ouput Webcam", img)
            if cv2.waitKey(1) and 0xFF == ord("q"):
                return


# wmi = win32com.client.GetObject("winmgmts:")
# for usb in wmi.InstancesOf("Win32_USBHub"):
#     print(usb.DeviceID)

media_object = MediaClass()
media_object.loadImagePostFX(0)
