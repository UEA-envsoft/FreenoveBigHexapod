from HexaPosToolui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from Control import *
from Servo import *
from Buzzer import *
from Control import *
from ADS7830 import *


class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.control = Control()
        self.servo = Servo()
        self.adc = ADS7830()
        self.buzzer = Buzzer()
        self.pushButtonSetPos.clicked.connect(self.setPosition)
        self.pushButtonRelax.clicked.connect(self.servo.relax)
        self.xyz2angle.clicked.connect(self.coord2angle)
        self.angle2xyz.clicked.connect(self.angle2coord)
        self.angle=[[90,157,116],[90,157,116],[90,157,116],[90,23,64],[90,23,64],[90,23,64]]
        self.calcAngle=[[90, -67, 116],[90, -67, 116],[90, -67, 116],[90, -67, 116],[90, -67, 116],[90, -67, 116]]
        self.co_ordsStr = "[[140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0]]"
        self.co_ords = [[140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0]]

        # Leg 1
        self.txtbx_servo_15.setText(str(int(self.angle[0][0])))
        self.txtbx_servo_14.setText(str(int(self.angle[0][1])))
        self.txtbx_servo_13.setText(str(int(self.angle[0][2])))
        # Leg 2
        self.txtbx_servo_12.setText(str(int(self.angle[1][0])))
        self.txtbx_servo_11.setText(str(int(self.angle[1][1])))
        self.txtbx_servo_10.setText(str(int(self.angle[1][2])))
        # Leg 3
        self.txtbx_servo_9.setText(str(int(self.angle[2][0])))
        self.txtbx_servo_8.setText(str(int(self.angle[2][1])))
        self.txtbx_servo_31.setText(str(int(self.angle[2][2])))
        # Leg 4
        self.txtbx_servo_22.setText(str(int(self.angle[3][0])))
        self.txtbx_servo_23.setText(str(int(self.angle[3][1])))
        self.txtbx_servo_27.setText(str(int(self.angle[3][2])))
        # Leg 5
        self.txtbx_servo_19.setText(str(int(self.angle[4][0])))
        self.txtbx_servo_20.setText(str(int(self.angle[4][1])))
        self.txtbx_servo_21.setText(str(int(self.angle[4][2])))
        # Leg 6
        self.txtbx_servo_16.setText(str(int(self.angle[5][0])))
        self.txtbx_servo_17.setText(str(int(self.angle[5][1])))
        self.txtbx_servo_18.setText(str(int(self.angle[5][2])))

        self.co_ordSet.setText(self.co_ordsStr)
        self.progress_Power1.setValue(50)
        self.progress_Power2.setValue(60)

        self.batStat = QTimer(self)
        self.batStat.timeout.connect(self.getBatStat)
        self.batStat.start(1000)

    def setPosition(self):
        #Leg 1
        self.angle[0][0] = int(self.txtbx_servo_15.text())
        self.angle[0][1] = int(self.txtbx_servo_14.text())
        self.angle[0][2] = int(self.txtbx_servo_13.text())
        #Leg 2
        self.angle[1][0] = int(self.txtbx_servo_12.text())
        self.angle[1][1] = int(self.txtbx_servo_11.text())
        self.angle[1][2] = int(self.txtbx_servo_10.text())
        #Leg 3
        self.angle[2][0] = int(self.txtbx_servo_9.text())
        self.angle[2][1] = int(self.txtbx_servo_8.text())
        self.angle[2][2] = int(self.txtbx_servo_31.text())
        #Leg 4
        self.angle[3][0] = int(self.txtbx_servo_22.text())
        self.angle[3][1] = int(self.txtbx_servo_23.text())
        self.angle[3][2] = int(self.txtbx_servo_27.text())
        #Leg 5
        self.angle[4][0] = int(self.txtbx_servo_19.text())
        self.angle[4][1] = int(self.txtbx_servo_20.text())
        self.angle[4][2] = int(self.txtbx_servo_21.text())
        #Leg 6
        self.angle[5][0] = int(self.txtbx_servo_16.text())
        self.angle[5][1] = int(self.txtbx_servo_17.text())
        self.angle[5][2] = int(self.txtbx_servo_18.text())

        for i in range(3):
            self.angle[i][0] = self.control.restriction(self.angle[i][0] + self.control.calibration_angle[i][0], 0, 180)
            self.angle[i][1] = self.control.restriction(self.angle[i][1] - self.control.calibration_angle[i][1], 0, 180)
            self.angle[i][2] = self.control.restriction(self.angle[i][2] + self.control.calibration_angle[i][2], 0, 180)
            self.angle[i+3][0] = self.control.restriction(self.angle[i+3][0] + self.control.calibration_angle[i+3][0], 0, 180)
            self.angle[i+3][1] = self.control.restriction(self.angle[i+3][1] + self.control.calibration_angle[i+3][1], 0, 180)
            self.angle[i+3][2] = self.control.restriction(self.angle[i+3][2] - self.control.calibration_angle[i+3][2], 0, 180)

        # leg1
        self.servo.setServoAngle(15, self.angle[0][0])
        self.servo.setServoAngle(14, self.angle[0][1])
        self.servo.setServoAngle(13, self.angle[0][2])

        # leg2
        self.servo.setServoAngle(12, self.angle[1][0])
        self.servo.setServoAngle(11, self.angle[1][1])
        self.servo.setServoAngle(10, self.angle[1][2])

        # leg3
        self.servo.setServoAngle(9, self.angle[2][0])
        self.servo.setServoAngle(8, self.angle[2][1])
        self.servo.setServoAngle(31, self.angle[2][2])

        # leg6
        self.servo.setServoAngle(16, self.angle[5][0])
        self.servo.setServoAngle(17, self.angle[5][1])
        self.servo.setServoAngle(18, self.angle[5][2])

        # leg5
        self.servo.setServoAngle(19, self.angle[4][0])
        self.servo.setServoAngle(20, self.angle[4][1])
        self.servo.setServoAngle(21, self.angle[4][2])

        # leg4
        self.servo.setServoAngle(22, self.angle[3][0])
        self.servo.setServoAngle(23, self.angle[3][1])
        self.servo.setServoAngle(27, self.angle[3][2])


    def coord2angle(self):
        # "[[140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0]]"
        coord = self.co_ordSet.text()
        # lose any white space
        coord = coord.replace(" ", "")
        coord = coord.replace("],[", ":")
        coord = coord.replace("]]", "")
        coord = coord.replace("[[", "")
        # "-100,-100,-100:-100,-100,-100:-100,-100,-100:-100,-100,-100"
        xyzs = coord.split(":")

        for i in range(3):
            self.co_ords[i] = xyzs[i].split(",")
            self.calcAngle[i][0],self.calcAngle[i][1],self.calcAngle[i][2]=self.control.coordinateToAngle(-int(float(self.co_ords[i][2])), int(float(self.co_ords[i][0])), int(float(self.co_ords[i][1])))
            self.angle[i][0] = self.control.restriction(self.calcAngle[i][0], 0, 180)
            self.angle[i][1] = self.control.restriction(90 - (self.calcAngle[i][1]), 0, 180)
            self.angle[i][2] = self.control.restriction(self.calcAngle[i][2], 0, 180)

            self.co_ords[i+3] = xyzs[i+3].split(",")
            self.calcAngle[i+3][0], self.calcAngle[i+3][1], self.calcAngle[i+3][2] = self.control.coordinateToAngle( -int(float(self.co_ords[i+3][2])), int(float(self.co_ords[i+3][0])), int(float(self.co_ords[i+3][1])))
            self.angle[i + 3][0] = self.control.restriction(self.calcAngle[i + 3][0], 0, 180)
            self.angle[i + 3][1] = self.control.restriction(90 + self.calcAngle[i + 3][1] , 0, 180)
            self.angle[i + 3][2] = self.control.restriction(180 - (self.calcAngle[i + 3][2]), 0, 180)

        # Leg 1
        self.txtbx_servo_15.setText(str(int(self.angle[0][0])))
        self.txtbx_servo_14.setText(str(int(self.angle[0][1])))
        self.txtbx_servo_13.setText(str(int(self.angle[0][2])))
        # Leg 2
        self.txtbx_servo_12.setText(str(int(self.angle[1][0])))
        self.txtbx_servo_11.setText(str(int(self.angle[1][1])))
        self.txtbx_servo_10.setText(str(int(self.angle[1][2])))
        # Leg 3
        self.txtbx_servo_9.setText(str(int(self.angle[2][0])))
        self.txtbx_servo_8.setText(str(int(self.angle[2][1])))
        self.txtbx_servo_31.setText(str(int(self.angle[2][2])))
        # Leg 4
        self.txtbx_servo_22.setText(str(int(self.angle[3][0])))
        self.txtbx_servo_23.setText(str(int(self.angle[3][1])))
        self.txtbx_servo_27.setText(str(int(self.angle[3][2])))
        # Leg 5
        self.txtbx_servo_19.setText(str(int(self.angle[4][0])))
        self.txtbx_servo_20.setText(str(int(self.angle[4][1])))
        self.txtbx_servo_21.setText(str(int(self.angle[4][2])))
        # Leg 6
        self.txtbx_servo_16.setText(str(int(self.angle[5][0])))
        self.txtbx_servo_17.setText(str(int(self.angle[5][1])))
        self.txtbx_servo_18.setText(str(int(self.angle[5][2])))

    def angle2coord(self):
        # Leg 1
        self.angle[0][0] = int(self.txtbx_servo_15.text())
        self.angle[0][1] = int(self.txtbx_servo_14.text())
        self.angle[0][2] = int(self.txtbx_servo_13.text())
        # Leg 2
        self.angle[1][0] = int(self.txtbx_servo_12.text())
        self.angle[1][1] = int(self.txtbx_servo_11.text())
        self.angle[1][2] = int(self.txtbx_servo_10.text())
        # Leg 3
        self.angle[2][0] = int(self.txtbx_servo_9.text())
        self.angle[2][1] = int(self.txtbx_servo_8.text())
        self.angle[2][2] = int(self.txtbx_servo_31.text())
        # Leg 4
        self.angle[3][0] = int(self.txtbx_servo_22.text())
        self.angle[3][1] = int(self.txtbx_servo_23.text())
        self.angle[3][2] = int(self.txtbx_servo_27.text())
        # Leg 5
        self.angle[4][0] = int(self.txtbx_servo_19.text())
        self.angle[4][1] = int(self.txtbx_servo_20.text())
        self.angle[4][2] = int(self.txtbx_servo_21.text())
        # Leg 6
        self.angle[5][0] = int(self.txtbx_servo_16.text())
        self.angle[5][1] = int(self.txtbx_servo_17.text())
        self.angle[5][2] = int(self.txtbx_servo_18.text())

        for i in range(3):

            self.calcAngle[i][0] = self.angle[i][0]
            self.calcAngle[i][1] = 90 - self.angle[i][1]
            self.calcAngle[i][2] = self.angle[i][2]

            self.calcAngle[i + 3][0] = self.angle[i + 3][0]
            self.calcAngle[i + 3][1] = self.angle[i + 3][1] - 90
            self.calcAngle[i + 3][2] = 180 - self.angle[i + 3][2]


        self.co_ordsStr = "[["
        for i in range(6):
            self.co_ords[i][2], self.co_ords[i][0], self.co_ords[i][1] = self.control.angleToCoordinate(self.calcAngle[i][0], self.calcAngle[i][1], self.calcAngle[i][2])
            self.co_ordsStr = self.co_ordsStr + str(int(self.co_ords[i][0])) + "," + str(int(self.co_ords[i][1])) + "," + str(0-int(self.co_ords[i][2]))
            if i < 5:
                self.co_ordsStr = self.co_ordsStr + "],["
            else:
                self.co_ordsStr = self.co_ordsStr + "]]"
        self.co_ordSet.setText(self.co_ordsStr)

    def getBatStat(self):
        batteryVoltage = self.adc.batteryPower()
        self.progress_Power1.setFormat(str(batteryVoltage[0])+"V")
        self.progress_Power2.setFormat(str(batteryVoltage[1]) + "V")
        self.progress_Power1.setValue(self.control.restriction(round((batteryVoltage[0] - 5.00) / 3.40 * 100), 0, 100))
        self.progress_Power2.setValue(self.control.restriction(round((batteryVoltage[1] - 7.00) / 1.40 * 100), 0, 100))
        if batteryVoltage[0] < 5.5 or batteryVoltage[1] < 6:
            for i in range(3):
                self.buzzer.run("1")
                time.sleep(0.15)
                self.buzzer.run("0")
                time.sleep(0.1)


    # def closeEvent(self,event):
    #     try:
    #         stop_thread(self.batStat)
    #     except:
    #         pass
    #     QCoreApplication.instance().quit()
    #     os._exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
