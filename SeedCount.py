from PyQt5 import QtWidgets
import numpy as np
import cv2
import time
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.uic  import loadUi
from PyQt5.QtCore import QTimer

denoise = 40
backsub = cv2.createBackgroundSubtractorMOG2()

        
class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        loadUi('program.ui',self)
        self.image=None
        self
        self.btnCameraOpen.clicked.connect(self.startCamera)
        self.btnCameraClose.clicked.connect(self.stopCamera)
        self.conveyer_speed = 3
        
    def startCamera(self):
        self.capture=cv2.VideoCapture("original video.m4v")
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)

        self.timer=QTimer(self)
        print('dayandi ...')
        
        self.timer.timeout.connect(self.update_frame)
        print('cekdi')
        self.timer.start(5)
        self.sayac=0
    def update_frame(self):
        ret, self.image = self.capture.read()
        time.sleep(self.conveyer_speed/100)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        ret,thresh1 = cv2.threshold(self.image,int(denoise),255,cv2.THRESH_BINARY)
        kernel = np.ones((9,9),np.uint8)
        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
        fgmask = backsub.apply(self.image, None, 0.01)
        cv2.rectangle(self.image, (300, 100), (1000, 600), (0, 0, 255), 2)
        contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        try: hierarchy = hierarchy[0]
        except: hierarchy = []
        for contour, hier in zip(contours, hierarchy):
            area = cv2.contourArea(contour)
            M = cv2.moments(contour) 
            (x,y,w,h) = cv2.boundingRect(contour)
            if w > 30 and h > 30:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(self.image,(cx,cy), 5, (0,0,255), -1)
                cv2.drawContours(self.image, contour, -1, (0,255,0), 3) # draw contours of every seeds
                #x,y,w,h = cv2.boundingRect(contour)  

                if y>10 and y<40:
                    self.sayac+=1
                    print(self.sayac)
        cv2.putText(self.image,"Tohum Sayi: "+str(self.sayac), (220, 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 0, 0), 2)

        #self.image=cv2.flip(self.image,1)
        self.displayImage(self.image,1)


    def stopCamera(self):
        self.timer.stop()

    def displayImage(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if (len(img.shape)==3):
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:

                qformat=QImage.Format_RGB888
        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        outImage=outImage.rgbSwapped()

        if window==1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)



if __name__=='__main__':

    app=QtWidgets.QApplication(sys.argv)
    win =myApp()
    win.setGeometry(100,50,800,600)
    win.show()
    sys.exit(app.exec_())
