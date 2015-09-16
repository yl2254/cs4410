from threading import Thread, Lock, Condition
import time, random

# Q06:
# Complete the implementation of the PrintScheduler monitor below.  Your
# implementation should use python Lock and Condition variables.

def delay():
    """sleep for a random interval"""
    time.sleep(random.randint(0, 2))

class PrintScheduler:
    """A PrintScheduler matches up printer threads with job threads.
    Applications submit jobs by calling submit_job(); Printers indicate their
    availability by calling printer_ready().

    When a job and a printer have been matched up, the corresponding threads
    should be allowed to continue (that is, the submit_job and printer_ready
    functions should return).

    A PrintScheduler will only allow a fixed number of jobs (num_jobs) to be
    queued up.  If a job is submitted and the PrintScheduler is full, it will
    reject the job immediately."""

    def __init__(self, num_jobs):
        self.lock=Lock()
        self.num_jobs=num_jobs
        self.waiting_jobs=0
        self.printerBusy=False
        # predicate: printBusy = True
        self.printerReady=Condition(self.lock)
        #self.waiting_jobs>0
        self.submitJob=Condition(self.lock)

    def printer_ready(self):
        """Indicate that the currently running printer thread is ready to
        print. This function should return when a job has been assigned to
        this printer."""
        with self.lock:
            while self.waiting_jobs==0:
                self.submitJob.wait()
            self.printerReady.notifyAll()
            self.printerBusy=False

        return

    def submit_job(self):
        """Indicate that the currently running application wants to print.
        Immediately raises an exception if the PrintScheduler is full; utherwise
        waits until a printer has been assigned to this job and then returns."""
        with self.lock:
            if self.waiting_jobs>self.num_jobs:
                raise ValueError('PrintScheduler is full')
            self.submitJob.notify()
            self.waiting_jobs+=1
            while self.printerBusy:
                self.printerReady.wait()
            self.waiting_jobs-=1
            self.printerBusy=True
        return 

        

class Printer(Thread):
    def __init__(self, id, scheduler):
        Thread.__init__(self)
        self.scheduler = scheduler
        self.id        = id

    def run(self):
        while True:
            print("Printer #%d: ready to print" % self.id)
            self.scheduler.printer_ready()
            print("Printer #%d: printing" % self.id)
            delay()
            print("Printer #%d: done printing" % self.id)

class Application(Thread):
    def __init__(self, id, scheduler):
        Thread.__init__(self)
        self.id        = id
        self.scheduler = scheduler

    def run(self):
        while True:
            print("Application #%d: wants to print" % self.id)
            try:
                self.scheduler.submit_job()
                print("Application #%d: job printing" % self.id)
            except:
                print("Application #%d: job rejected" % self.id)
            delay()

if __name__ == '__main__':
    NUM_PRINTERS = 2
    NUM_APPS     = 6
    sched = PrintScheduler(3)

    for i in range(NUM_PRINTERS):
        Printer(i,sched).start()
    for i in range(NUM_APPS):
        Application(i,sched).start()


##
## vim: ts=4 sw=4 et ai
##
