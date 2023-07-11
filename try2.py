import cv2
import win32
import win32com.client
import numpy as np

class MediaClass:
    __kernel = np.ones((5,5), np.uint8) #sebesar matrix 5 x 5 dengan nilai unsigned int (0-255)
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
        imgDialation = cv2.dilate(imgCanny, self.__kernel, iterations= 1)
        imgEroded = cv2.erode(imgDialation, self.__kernel, iterations= 1)

        cv2.imshow("imgGreyscale", imgGreyscale)
        cv2.imshow("imgBlur", imgBlur)
        cv2.imshow("imgCanny", imgCanny)
        cv2.imshow("Dilation", imgDialation)
        cv2.imshow("imgEroded", imgEroded)
        cv2.waitKey(0)

        match mode:
            case 0:
                return
            case 1:
                return
            case 2:
                return

    def resizeAndCrop(self):
        img = cv2.imread("Resources/builder1.jpg")

        imgResize = cv2.resize(img, (400,400))
        cv2.imshow("Resize", imgResize)
        imgCrop = img[0:300, 0:300]
        cv2.imshow("Crop", imgCrop)
        cv2.waitKey(0)

    def editImg(self):
        img = np.zeros((512,512)) # pixel 512 x 512 grescale
        img = np.zeros((512,512,3),np.uint8) # pixel 512 x 512 3 channel RGB/BGR
        img[:] = 230,10,234 # memberikan warna pada seluruh pixel
        cv2.imshow("edit image", img)
        cv2.waitKey(0)


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
media_object.editImg()
