from threading import Thread, Lock, Condition
import time
import random

# Q04:
# a. Complete the implementation of the OneLaneBridge monitor below using
#    python locks and condition variables.  Your implementation should be able
#    to make progress if there are any cars that can cross.
#
# b. What fairness properties does your implementation have?  Under what
#    conditions (if any) can a thread starve?
#

north = 0
south = 1

class OneLaneBridge(object):
    """
    A one-lane bridge allows multiple cars to pass in either direction, but at any
    point in time, all cars on the bridge must be going in the same direction.

    Cars wishing to cross should call the cross function, once they have crossed
    they should call finished()
    """

    def __init__(self):
        # TODO
        #self.numcars_N = 0
        self.numcars = 0
        self.laneLock = Lock()
        self.laneDirection = 0
        #self.laneNorthwait = Condition(self.laneLock)
        #self.laneSouthwait = Condition(self.laneLock)
        self.laneWait= Condition(self.laneLock)

    def cross(self,direction):
        """wait for permission to cross the bridge.  direction should be either
        north (0) or south (1)."""
        # TODO
        # with self.laneLock: #acquire the monitor lock
        #     while self.numcars>0 and direction!=self.laneDirection:
        #         if direction==0:
        #             self.laneNorthwait.wait() # wait until notify()
        #         else:
        #             self.laneSouthwait.wait() # wait until notify()
        #     self.numcars+=1
        #     self.laneDirection=direction
        with self.laneLock:
            #print self.numcars, self.laneDirection, direction
            while (self.numcars>0) and (direction!=self.laneDirection):
                self.laneWait.wait()
        
            self.numcars+=1
            self.laneDirection=direction

    def finished(self,direction):
        # TODO
        with self.laneLock: #acquire the monitor lock
            
            self.numcars-=1
            if self.numcars==0:
                self.laneWait.notifyAll()
                # if self.laneDirection==0:
                #     self.laneSouthwait.notifyAll()  #why notify all will work instead of notify???
                # else:
                #     self.laneNorthwait.notifyAll()
        


class Car(Thread):
    def __init__(self, bridge, car_id):
        Thread.__init__(self)
        self.direction = random.randrange(2)

        self.wait_time = random.uniform(0.1,0.5)
        self.bridge    = bridge
        self.car_id    = car_id

    def run(self):
        # drive to the bridge
        time.sleep(self.wait_time)
        print "Car %d: Trying to cross %s" % (self.car_id, "south" if self.direction else "north")
        # request permission to cross
        self.bridge.cross(self.direction)
        #print self.numcars, self.laneDirection, direction
        print "Car %d: Crossing" % self.car_id
        # drive across
        time.sleep(0.01)
        print "Car %d: Crossed" % self.car_id
        # signal that we have finished crossing
        self.bridge.finished(self.direction)
        print "Car %d: Finished crossing" % self.car_id


if __name__ == "__main__":

    judd_falls = OneLaneBridge()
    for i in range(100):
        Car(judd_falls, i).start()


##
## vim: ts=4 sw=4 et ai
##
