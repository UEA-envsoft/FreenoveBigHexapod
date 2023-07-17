from Servo import *
import time


class Claws:
    def __init__(self):
        self.servo = Servo()
        self.leftArmAngle = 90
        self.leftWristAngle = 90
        self.leftClawAngle = 60
        self.rightArmAngle = 90
        self.rightWristAngle = 90
        self.rightClawAngle = 60

    def leftClawArm(self, angle):
        # arm servos have a range from 40 to 140
        if angle < 40: angle = 40
        if angle > 140: angle = 140
        self.leftArmAngle = angle
        self.leftWristAngle = (-1.12 * angle) + 180.8
        self.servo.setServoAngle(4, self.leftArmAngle)
        self.servo.setServoAngle(6, self.leftWristAngle)

    def rightClawArm(self, angle):
        # arm servos have a range from 40 to 140
        if angle < 40: angle = 40
        if angle > 140: angle = 140
        # positioning  correction ( servo can handllle 144)
        angle = angle + 4
        self.rightArmAngle = angle
        self.rightWristAngle = (-1.1 * angle) + 198
        self.servo.setServoAngle(5, self.rightArmAngle)
        self.servo.setServoAngle(7, self.rightWristAngle)

    def moveArms(self, leftAngle, rightAngle, steps=5, sleep=0.01):
        if leftAngle == 0: leftAngle = self.leftArmAngle
        if rightAngle == 0: rightAngle = self.rightArmAngle
        # calculate incremental change for each step
        leftIncr = (leftAngle - self.leftArmAngle) / steps
        leftIncrAngle = self.leftArmAngle
        rightIncr = (rightAngle - self.rightArmAngle) / steps
        rightIncrAngle = self.rightArmAngle
        for i in range(steps):  # For each step ....
            leftIncrAngle += leftIncr
            self.leftClawArm(leftIncrAngle)
            rightIncrAngle += rightIncr
            self.rightClawArm(rightIncrAngle)
            time.sleep(sleep)

    def leftClaw(self, angle):
        # arm servos have a range from 60 to 120
        if angle < 60: angle = 60
        if angle > 120: angle = 120
        self.leftClawAngle = angle
        self.servo.setServoAngle(2, self.leftClawAngle)

    def rightClaw(self, angle):
        # arm servos have a range from 60 to 120
        if angle < 60: angle = 60
        if angle > 120: angle = 120
        self.rightClawAngle = angle
        self.servo.setServoAngle(3, self.rightClawAngle)

    def moveClaws(self, leftAngle, rightAngle, steps=5, sleep=0.01):
        if leftAngle == 0: leftAngle = self.leftClawAngle
        if rightAngle == 0: rightAngle = self.rightClawAngle
        # calculate incremental change for each step
        leftIncr = (leftAngle - self.leftClawAngle) / steps
        leftIncrAngle = self.leftClawAngle
        rightIncr = (rightAngle - self.rightClawAngle) / steps
        rightIncrAngle = self.rightClawAngle
        for i in range(steps):  # For each step ....
            leftIncrAngle += leftIncr
            self.leftClaw(leftIncrAngle)
            rightIncrAngle += rightIncr
            self.rightClaw(rightIncrAngle)
            time.sleep(sleep)

    def testClaws(self):
        # for j in range(100):
        #     self.leftClawArm(j + 40)
        #     self.rightClawArm(j + 40)
        #     time.sleep(0.04)
        # for j in range(100, 0, -1):
        #     self.leftClawArm(j + 40)
        #     self.rightClawArm(j + 40)
        #     time.sleep(0.04)
        self.moveClaws(90,90,30)
        self.moveArms(140,140,100)
        self.moveClaws(60,60,30,0.04)
        time.sleep(0.5)
        self.moveClaws(120,120,30,0.04)
        time.sleep(0.5)
        self.moveArms(40,40,100)
        self.moveClaws(90,90,5)
        time.sleep(0.5)
        self.moveArms(90,90,50)
