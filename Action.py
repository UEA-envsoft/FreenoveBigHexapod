import math
from Control import *
from Servo import *
import time

class Action:
    def __init__(self):
        self.servo=Servo()
        self.control=Control()

    # to move from current position to desired position
    # targetPosition - the new desired position  default = relax
    # steps - the number of intermeidate positions to get from current to desired position
    #                                            default is 30
    # sleep - the pause between each stage       default is 0.01
    def transition(self, targetPosition= [[140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0], [140, 0, 0]], steps=30, sleep=0.01):
        """ the control class uses 'self.leg_point' as the basic position reference
        when setLegAngle is called it calculates angles based on leg_point
        leg_point is the xyz co-ordinates
        """
        xyz = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]] # increment
        for i in range(6):  # For each limb, calculate the incremental change in X Y Z for each step
            xyz[i][0] = (targetPosition[i][0] - self.control.leg_point[i][0]) / steps
            xyz[i][1] = (targetPosition[i][1] - self.control.leg_point[i][1]) / steps
            xyz[i][2] = (targetPosition[i][2] - self.control.leg_point[i][2]) / steps

        # print("Fractional steps: " + str(xyz))
        for j in range(steps):  # For each step ....
            for i in range(6):  # Tell control class about the new position of each limb
                self.control.leg_point[i][0] += xyz[i][0]
                self.control.leg_point[i][1] += xyz[i][1]
                self.control.leg_point[i][2] += xyz[i][2]
            # print("new self.control.point: " + str(self.control.point))
            self.control.setLegAngle()  # move limbs to new position (Servo.setServoAngle handles conversion to int values)
            time.sleep(sleep)


    def rearUp(self):
        #self.expr.suprise()  # requires LED matrix mouth
        #rear legs back
        self.transition([[122,0,-126],[118,0,-79],[199,0,50],[199,0,50],[118,0,-79],[122,0,-126]],10)
        #front up
        self.transition([[103,59,180],[118,0,-79],[199,0,50],[199,0,50],[118,0,-79],[103,-59,180]],10)

    def frontWaggle(self):        
        #left up right down
        self.servo.setServoAngle(18, 172)
        time.sleep(0.2)
        self.servo.setServoAngle(13, 140)
        time.sleep(0.2)
        #right up left down
        self.servo.setServoAngle(18, 40)
        time.sleep(0.2)
        self.servo.setServoAngle(13, 8)
        
    def react(self):
        self.rearUp()
        time.sleep(0.2)
        #self.expr.fangs()
        self.frontWaggle()
        time.sleep(0.2)
        self.frontWaggle()
        time.sleep(0.2)
        self.frontWaggle()
        time.sleep(1)
        self.transition()
        self.servo.relax()
        #self.expr.grin2()
   
# Main program logic follows:
if __name__ == '__main__':
    A = Action()
    A.react()
