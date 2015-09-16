from threading import Thread, Semaphore
import time
import random

# Q05:
# a. Complete the implementation of the OneLaneBridge class below using
#    python semaphores.  Your implementation should be able to make prograss if
#    there are any cars that can cross.
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
        self.numcars_north = 0
        self.numcars_south = 0
        #self.numcars_wait_south=0
        #self.numcars_wait_north=0
        #self.laneDirection = 0
        self.sem_north = Semaphore(1)
        self.sem_south = Semaphore(1)
        #self.sem_count= Semaphore(1)
        self.sem_lane = Semaphore(1)
        

    def cross(self,direction):
        """wait for permission to cross the bridge.  direction should be either
        north (0) or south (1)."""
            
        if direction==north:
            with self.sem_north:
                self.numcars_north+=1
                #self.numcars_wait_north+=1
                if self.numcars_north==1:
                    self.sem_lane.acquire()
                #self.numcars_wait_north+=1
        else:
            with self.sem_south:
                self.numcars_south+=1
                #self.numcars_wait_south+=1
                if self.numcars_south==1:
                    self.sem_lane.acquire()
                #self.numcars_wait_south+=1
    


    def finished(self,direction):
        # TODO
        # with self.sem_count:
        #     self.numcars-=1
        #     if self.numcars==0:
        #         self.sem_lane.release()

        if direction==north:
            with self.sem_north:
                self.numcars_north-=1
                #print self.numcars_north+"north"
                if self.numcars_north==0:
                    #if self.numcars_wait_north>0:
                    self.sem_lane.release()
                #self.numcars_wait=0
        
        else:
            with self.sem_south:
                self.numcars_south-=1
                #print self.numcars_south
                if self.numcars_south==0:
                    #if self.numcars_wait_south>0:
                    self.sem_lane.release()
                    #self.numcars_wait=0
        
        


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
