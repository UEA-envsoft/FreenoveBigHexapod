from Action import *
import evdev
from Buzzer import *
from subprocess import call
import atexit
from Led import *
import time
import sys
from selectors import DefaultSelector, EVENT_READ
import threading
from ADC import *
from wander import *


class localKeyboard:
    def __init__(self):
        self.action = Action()
        self.buz = Buzzer()
        self.led = Led()
        self.adc = ADC()
        self.headUpDownAngle = 90
        self.headLeftRightAngle = 90
        self.headLRcorrect = 0
        self.headUDcorrect = 0
        self.reset_head()
        self.leftArmAngle = 90    #servo 4
        self.rightArmAngle = 90   #servo 5
        self.leftClawAngle = 90
        self.rightClawAngle = 90
        #self.leftEyeAngle = 90
        #self.rightEyeAngle = 90
        self.led.colorWipe(self.led.strip, Color(0, 0, 0))  # turn off leds
        self.auton = wander(self)

        self.move_point = [325, 635]
        self.action_flag = 1
        self.gait_flag = 1
        self.move_speed = 8

        self.action.servo.setServoAngle(4, self.leftArmAngle)
        self.action.servo.setServoAngle(5, self.rightArmAngle)
        self.action.servo.setServoAngle(3, self.leftClawAngle)
        self.action.servo.setServoAngle(2, self.rightClawAngle)
        #self.action.servo.setServoAngle(7, self.leftEyeAngle)
        #self.action.servo.setServoAngle(6, self.rightEyeAngle)

        self.selector = DefaultSelector()
        # /dev/input/event3   mini keyboard Consumer Control usb-3f980000.usb-1.1.2/input1
        # /dev/input/event2   mini keyboard System Control usb-3f980000.usb-1.1.2/input1
        # /dev/input/event1   mini keyboard Mouse usb-3f980000.usb-1.1.2/input1
        # /dev/input/event0   mini keyboard usb-3f980000.usb-1.1.2/input0
        self.mouse = evdev.InputDevice('/dev/input/event1')
        self.keybd = evdev.InputDevice('/dev/input/event0')
        self.sysctrl = evdev.InputDevice('/dev/input/event2')
        self.conctrl = evdev.InputDevice('/dev/input/event3')

        self.reading_keys = False
        self.reading_bat = False
        self.wandering = False

        atexit.register(self.keybd.ungrab)  # Don't forget to ungrab the keyboard on exit!
        atexit.register(self.mouse.ungrab)
        self.keybd.grab()  # Grab, i.e. prevent the keyboard from emitting original events.#
        self.mouse.grab()
        # This works because InputDevice has a `fileno()` method.
        self.selector.register(self.mouse, EVENT_READ)
        self.selector.register(self.keybd, EVENT_READ)
        self.selector.register(self.sysctrl, EVENT_READ)
        self.selector.register(self.conctrl, EVENT_READ)
        battery_voltage = self.adc.batteryPower()
        print("Load " + str(battery_voltage[0]) + "V")
        print("RaPi " + str(battery_voltage[1]) + "V")
        self.batStat = threading.Thread(target=self.bat_stat_thread)
        self.batStat.start()

    def bat_stat_thread(self):
        self.reading_bat = True
        while self.reading_bat:
            self.get_bat_stat()
            time.sleep(20)

    def read_keys_loop(self):
        self.reading_keys = True
        while self.reading_keys:
            self.read_keys()

    def read_keys(self):
        for key, mask in self.selector.select():
            device = key.fileobj
            for event in device.read():
                if (event.type == evdev.ecodes.EV_KEY or evdev.ecodes.EV_REL):
                    try:
                        name = str(device.name)
                        cat = str(evdev.categorize(event)).split(",")
                        val = "?"
                        try:
                            val = cat[2]
                        except:
                            try:
                                val = str(event.value)
                            except:
                                val = "?"

                        print(name + " " + cat[1] + " " + val)
                    except:
                        try:
                            print(evdev.categorize(event))
                        except:
                            print("Categorize error")
                            print(event)
                    if event.type == evdev.ecodes.EV_KEY:
                        self.key_press(event, device)
                    elif event.type == evdev.ecodes.EV_REL:
                        if event.code == evdev.ecodes.REL_Y:
                            print("REL_Y")
                            print(event.value)
                            if event.value < 0:
                                self.head_down()
                            else:
                                self.head_up()
                        elif event.code == evdev.ecodes.REL_X:
                            print("REL_X")
                            print(event.value)
                            if event.value < 0:
                                self.head_left()
                            else:
                                self.head_right()
                    else:
                        pass

    def key_press(self, ev, dev):

                                    
        # EVENTS CALLED ON PRESS AND ON HOLD
        if ev.value == 1 or ev.value == 2:
            print(evdev.ecodes.bytype[evdev.ecodes.EV_KEY][ev.code])
            if ev.value == 2:
                # flush the buffer
                while dev.read_one() is not None:
                    pass
            #ARMS and CLAWS
            if ev.code == evdev.ecodes.KEY_W:
                self.left_arm_left()
            if ev.code == evdev.ecodes.KEY_E:
                self.left_arm_right()
            if ev.code == evdev.ecodes.KEY_I:
                self.right_arm_left()
            if ev.code == evdev.ecodes.KEY_O:
                self.right_arm_right()
            if ev.code == evdev.ecodes.KEY_D:
                self.left_claw_open()
            if ev.code == evdev.ecodes.KEY_F:
                self.left_claw_close()
            if ev.code == evdev.ecodes.KEY_K:
                self.right_claw_open()
            if ev.code == evdev.ecodes.KEY_L:
                self.right_claw_close()
            #EYE STALKS
#             if ev.code == evdev.ecodes.KEY_Z:
#                 self.left_eye_left()
#             elif ev.code == evdev.ecodes.KEY_X:
#                 self.left_eye_right()
#             elif ev.code == evdev.ecodes.KEY_I:
#                 self.right_eye_left()
#             elif ev.code == evdev.ecodes.KEY_O:
#                 self.right_eye_right()
            #"""
            # HEAD POSITION
            if ev.code == evdev.ecodes.KEY_A:
                self.head_down()
            elif ev.code == evdev.ecodes.KEY_Q:
                self.head_up()
            if ev.code == evdev.ecodes.KEY_CAPSLOCK:
                self.head_left()
            elif ev.code == evdev.ecodes.KEY_S:
                self.head_right()
            #    """
            # MOVEMENT
            elif ev.code == evdev.ecodes.KEY_UP:
                self.forward()
            elif ev.code == evdev.ecodes.KEY_DOWN:
                self.backward()
            elif ev.code == evdev.ecodes.KEY_LEFT:
                self.turn_left()
            elif ev.code == evdev.ecodes.KEY_RIGHT:
                self.turn_right()

            # not interested in any other held keys
            elif ev.value == 2:
                pass

            # CONSUMER CONTROL EVENTS DO NOT HAVE A HELD STATE
            elif ev.code == evdev.ecodes.KEY_PREVIOUSSONG:
                crabLeft = True
                while crabLeft:
                    self.crab_left()
                    # time.sleep(0.1)
                    ev = dev.read_one()
                    while ev is not None:
                        try:
                            if ev.value == 0:
                                crabLeft = False
                        except:
                            pass
                        ev = dev.read_one()
            elif ev.code == evdev.ecodes.KEY_NEXTSONG:
                crabRight = True
                while crabRight:
                    self.crab_right()
                    # time.sleep(0.1)
                    ev = dev.read_one()
                    while ev is not None:
                        try:
                            if ev.value == 0:
                                crabRight = False
                        except:
                            pass
                        ev = dev.read_one()

            # EVENTS THAT SHOULD ONLY BE CALLED ON PRESS AND NOT HOLD

            # AUTONOMOUS FUNCTION
            elif ev.code == evdev.ecodes.KEY_TAB:
                self.wandering = not self.wandering
                if self.wandering:
                    self.beep()
                    time.sleep(0.2)
                    self.beep()
                    print("wander start")
                    # start with a scan
                    self.auton.init_scan()
                    # call wandering from here so that key presses are still monitored
                    # flush backed up key presses
                    while dev.read_one() is not None:
                        pass
                    while self.wandering:
                        self.auton.go()
                        # time.sleep(0.5)
                        # any interaction will stop
                        ev = dev.read_one()
                        while ev is not None:
                            try:
                                if ev.value == 1:
                                    # print(evdev.ecodes.bytype[evdev.ecodes.EV_KEY][ev.code])
                                    self.beep()
                                    self.wandering = False
                            except:
                                pass
                            ev = dev.read_one()
                self.action.control.scanning = False
                self.action.control.scanAngle = 90
                self.head_LRpos(self.action.control.scanAngle)
                self.action.servo.relax()

            elif ev.code == evdev.ecodes.KEY_B:
                self.beep()
            elif ev.code == evdev.ecodes.KEY_R:
                self.action.servo.relax()

            # SPEED SETTING
            elif ev.code == evdev.ecodes.KEY_1:
                self.move_speed = 2  # don't think 1 is catered for
            elif ev.code == evdev.ecodes.KEY_2:
                self.move_speed = 2
            elif ev.code == evdev.ecodes.KEY_3:
                self.move_speed = 3
            elif ev.code == evdev.ecodes.KEY_4:
                self.move_speed = 4
            elif ev.code == evdev.ecodes.KEY_5:
                self.move_speed = 5
            elif ev.code == evdev.ecodes.KEY_6:
                self.move_speed = 6
            elif ev.code == evdev.ecodes.KEY_7:
                self.move_speed = 7
            elif ev.code == evdev.ecodes.KEY_8:
                self.move_speed = 8
            elif ev.code == evdev.ecodes.KEY_9:
                self.move_speed = 9
            elif ev.code == evdev.ecodes.KEY_0:
                self.move_speed = 10

            # ACTIONS
            elif ev.code == evdev.ecodes.KEY_F1:
                self.action.rearUp()
            elif ev.code == evdev.ecodes.KEY_F2:
                self.action.react()

            # PROG FUNCTIONS
            elif ev.code == evdev.ecodes.KEY_LEFTMETA:
                self.close()
            elif ev.code == evdev.ecodes.KEY_RIGHTMETA:
                self.close()
            elif ev.code == evdev.ecodes.KEY_END:
                self.shutdown_pi()
            elif ev.code == evdev.ecodes.KEY_SYSRQ:
                self.reboot_pi()

            else:
                print("UNUSED KEY CODE")
                print(evdev.ecodes.bytype[evdev.ecodes.EV_KEY][ev.code])

        # flush backed up key presses
        while dev.read_one() != None:
            pass

    def turn_right(self):
        self.action_flag = 0
        self.right()

    def crab_right(self):
        self.action_flag = 1
        self.right()
        self.action_flag = 0

    def right(self):
        self.move_point = [425, 635]
        self.move()

    def diag_right(self):
        self.action_flag = 0
        self.move_point = [425, 535]
        self.move()

    def turn_left(self):
        self.action_flag = 0
        self.left()

    def crab_left(self):
        self.action_flag = 1
        self.left()
        self.action_flag = 0

    def left(self):
        self.move_point = [225, 635]
        self.move()

    def diag_left(self):
        self.action_flag = 0
        self.move_point = [225, 535]
        self.move()

    def backward(self):
        self.action_flag = 1
        self.move_point = [325, 735]
        self.move()

    def forward(self):
        self.action_flag = 1
        self.move_point = [325, 535]
        self.move()

    def move(self):
        # print("A F: " + str(self.action_flag))
        try:
            x = self.map((self.move_point[0] - 325), 0, 100, 0, 35)
            y = self.map((635 - self.move_point[1]), 0, 100, 0, 35)
            if self.action_flag == 1:  # move  sideways
                angle = 0
            else:  # rotate sideways
                if x != 0 or y != 0:
                    angle = math.degrees(math.atan2(x, y))

                    if angle < -90 and angle >= -180:
                        angle = angle + 360
                    if angle >= -90 and angle <= 90:
                        angle = self.map(angle, -90, 90, -10, 10)
                    else:
                        angle = self.map(angle, 270, 90, 10, -10)
                else:
                    angle = 0
            speed = self.move_speed
            command = cmd.CMD_MOVE + "#" + str(self.gait_flag) + "#" + str(round(x)) + "#" + str(round(y)) \
                      + "#" + str(speed) + "#" + str(round(angle)) + '\n'
            # print(command)
            # def run(self,data,Z=40,F=64):#example : data=['CMD_MOVE', '1', '0', '25', '10', '0']
            data = command.split("#")
            self.action.control.run(data)
        except Exception as e:
            print(e)

    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow

    def head_up(self):
        self.headUpDownAngle += 1
        if self.headUpDownAngle > 180 + self.headUDcorrect:
            self.headUpDownAngle = 180 + self.headUDcorrect
        self.action.servo.setServoAngle(0, self.headUpDownAngle)
        print("Up/down " + str(self.headUpDownAngle))

    def head_down(self):
        self.headUpDownAngle -= 1
        if self.headUpDownAngle < 80 + self.headUDcorrect: self.headUpDownAngle = 80 + self.headUDcorrect
        self.action.servo.setServoAngle(0, self.headUpDownAngle)
        print("Up/down " + str(self.headUpDownAngle))

    def head_UDpos(self, angle):
        self.headUpDownAngle = angle + self.headUDcorrect
        self.action.servo.setServoAngle(0, self.headUpDownAngle)

    def head_right(self):
        self.headLeftRightAngle -= 1
        if self.headLeftRightAngle < 10 + self.headLRcorrect:
            self.headLeftRightAngle = 10 + self.headLRcorrect
        self.action.servo.setServoAngle(1, self.headLeftRightAngle)
        print("Left/Right " + str(self.headLeftRightAngle))

    def head_LRpos(self, angle):
        # print("Move head to " + str(self.headLeftRightAngle))
        self.headLeftRightAngle = angle + self.headLRcorrect
        self.action.servo.setServoAngle(1, self.headLeftRightAngle)

    def head_left(self):
        self.headLeftRightAngle += 1
        if self.headLeftRightAngle > 170 + self.headLRcorrect:
            self.headLeftRightAngle = 170 + self.headLRcorrect
        self.action.servo.setServoAngle(1, self.headLeftRightAngle)
        print("Left/Right " + str(self.headLeftRightAngle))

    def reset_head(self):
        self.headLeftRightAngle = 90 + self.headLRcorrect
        self.headUpDownAngle = 90 + self.headUDcorrect
        self.action.servo.setServoAngle(1, int(self.headLeftRightAngle))
        self.action.servo.setServoAngle(0, int(self.headUpDownAngle))

    def right_arm_left(self):
        self.rightArmAngle += 1
        if self.rightArmAngle >95: self.rightArmAngle = 95
        self.action.servo.setServoAngle(5, self.rightArmAngle)

    def right_arm_right(self):
        self.rightArmAngle -= 1
        if self.rightArmAngle < 40: self.rightArmAngle = 40
        self.action.servo.setServoAngle(5, self.rightArmAngle)

    def left_arm_left(self):
        self.leftArmAngle += 1
        if self.leftArmAngle >140: self.leftArmAngle = 140
        print("left arm left " + str(self.leftArmAngle ) )
        self.action.servo.setServoAngle(4, self.leftArmAngle)    
    
    def left_arm_right(self):
        self.leftArmAngle -= 1
        if self.leftArmAngle < 85: self.leftArmAngle = 85
        print("left arm right " + str(self.leftArmAngle ) )
        self.action.servo.setServoAngle(4, self.leftArmAngle)
        
    def right_claw_open(self):
        self.leftClawAngle -= 1
        if self.leftClawAngle < 60: self.leftClawAngle = 60
        self.action.servo.setServoAngle(3, self.leftClawAngle)

    def right_claw_close(self):
        self.leftClawAngle += 1
        if self.leftClawAngle > 120: self.leftClawAngle = 120
        self.action.servo.setServoAngle(3, self.leftClawAngle)

    def left_claw_close(self):
        self.rightClawAngle -= 1
        if self.rightClawAngle < 60: self.rightClawAngle = 60
        self.action.servo.setServoAngle(2, self.rightClawAngle)    
    
    def left_claw_open(self):
        self.rightClawAngle += 1
        if self.rightClawAngle > 120: self.rightClawAngle = 120
        self.action.servo.setServoAngle(2, self.rightClawAngle)

#     def left_eye_left(self):
#         self.leftEyeAngle -= 1
#         if self.leftEyeAngle < 45: self.leftEyeAngle = 45
#         self.action.servo.setServoAngle(7, self.leftEyeAngle)    
#     
#     def left_eye_right(self):
#         self.leftEyeAngle += 1
#         if self.leftEyeAngle > 135: self.leftEyeAngle = 135
#         self.action.servo.setServoAngle(7, self.leftEyeAngle)
# 
#     def right_eye_left(self):
#         self.rightEyeAngle -= 1
#         if self.rightEyeAngle < 45: self.rightEyeAngle = 45
#         self.action.servo.setServoAngle(6, self.rightEyeAngle)
#     
#     def right_eye_right(self):
#         self.rightEyeAngle += 1
#         if self.rightEyeAngle > 135: self.rightEyeAngle = 135
#         self.action.servo.setServoAngle(6, self.rightEyeAngle)

    def close(self):
        print("close")
        self.reading_keys = False
        self.reading_bat = False
        self.crabbingthread = False
        self.selector.unregister(self.mouse)
        self.selector.unregister(self.keybd)
        self.selector.unregister(self.conctrl)
        self.selector.unregister(self.sysctrl)
        self.action.servo.relax()
        sys.exit()

    def shutdown_pi(self):
        self.action.servo.relax()
        self.beep()
        time.sleep(0.2)
        self.beep()
        call("sudo nohup shutdown -h now", shell=True)

    def reboot_pi(self):
        self.action.servo.relax()
        self.beep()
        call("sudo nohup reboot", shell=True)

    def beep(self):
        self.buz.run('1')
        time.sleep(0.2)
        self.buz.run('0')

    def get_bat_stat(self):
        battery_voltage = self.adc.batteryPower()
        print("Load " + str(battery_voltage[0]) + "V")
        print("RaPi " + str(battery_voltage[1]) + "V")
        if battery_voltage[0] < 5.5 or battery_voltage[1] < 6:
            if battery_voltage[0] < 5.5: self.action.servo.relax()
            print("Load " + str(battery_voltage[0]) + "V")
            print("RaPi " + str(battery_voltage[1]) + "V")
            for i in range(3):
                self.buz.run("1")
                time.sleep(0.15)
                self.buz.run("0")
                time.sleep(0.1)


if __name__ == '__main__':
    kb = localKeyboard()
    try:
        kb.read_keys_loop()
    except KeyboardInterrupt:
        print("calling close")
        kb.close()