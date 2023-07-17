import time
from BorisKb import *


class wander:
    def __init__(self, kb):
        self.kb = kb
        #self.kb.reset_head()
        self.kb.move_speed = 8

    def init_scan(self):
        #start with a scan
        self.kb.head_UDpos(95)
        for i in range(1, 40):
            self.kb.action.control.head_sweep()
            time.sleep(0.05)
            self.kb.action.control.logScanDistance()

    def go(self):
        self.kb.action.control.scanning = True
        try:
            print("Try")
            fwd, midl, farl, midr, farr = self.updateDistances()
            edgeDanger = 40
            aheadClear = 50
            obstDanger = 35
            criticalEdge = 15

            #make some decisions
            #way ahead blocked

            if ((midl < criticalEdge or farl < criticalEdge) and farr > edgeDanger):
                print("Critical Crab Right")
                self.kb.crab_right()
            elif ((midr < criticalEdge or farr < criticalEdge) and farl > edgeDanger):
                print("Critical Crab Left")
                self.kb.crab_left()
            elif farl < edgeDanger - 15 and farr < edgeDanger - 15:
                print("Hemmed in")
                self.kb.backward()
            elif fwd < obstDanger:
                print("Blocked")
                # self.kb.backward()
                self.init_scan()
                fwd, midl, farl, midr, farr = self.updateDistances()
                if fwd > aheadClear:
                    print("Forward")
                    self.kb.forward()
                elif farl > farr:
                    print("Turn Left")
                    while fwd < obstDanger:
                        self.kb.turn_left()
                        fwd, midl, farl, midr, farr = self.updateDistances()
                else:
                    print("Turn Right")
                    while fwd < obstDanger:
                        self.kb.turn_right()
                        fwd, midl, farl, midr, farr = self.updateDistances()
            #edge avoidance
            elif farl < edgeDanger:
                print("Left Edge")
                if fwd > aheadClear:
                    print("Diag Right")
                    self.kb.diag_right()
                else:
                    if farr > edgeDanger:
                        print("Crab Right")
                        self.kb.crab_right()
                    else:
                        print("Turn Right")
                        self.kb.turn_right()
            elif farr < edgeDanger:
                print("Right Edge")
                if fwd > aheadClear:
                    print("Diag Left")
                    self.kb.diag_left()
                else:
                    if farl > edgeDanger:
                        print("Crab Left")
                        self.kb.crab_left()
                    else:
                        self.kb.turn_left
            #shoulod we turn a bit anyway?
            elif midr > fwd:
                print("Diag Right")
                self.kb.diag_right()
            elif midl > fwd:
                print("Diag Left")
                self.kb.diag_left()
            else:
                print("Forward")
                self.kb.forward()
        except:
            e = sys.exc_info()[0]
            print("Except: %s" % e)
            pass

    def updateDistances(self):
        ll = self.kb.action.control.scanFarLeftDist
        l = self.kb.action.control.scanMidLeftDist
        f = self.kb.action.control.scanForwardDist
        r = self.kb.action.control.scanMidRightDist
        rr = self.kb.action.control.scanFarRightDist
        print("L to R: " + str(ll) + " " + str(l) + " " + str(f) + " " + str(r) + " " + str(rr))
        return f, l, ll, r, rr
