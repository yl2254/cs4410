from threading import Thread, Lock, Condition
from time import sleep

# Q11:
# A service provider is providing computational resources to several competing
# businesses.  In order to provide fairness, the service provider has entered
# into a complicated series of contracts with its clients regarding which client
# jobs may be admitted.
#
# The rules are thus:
#
#   (a) there are no more than N jobs running
#   (b) govcom jobs are always allowed to run (subject to condition a)
#   (c) searchco jobs may not start if they would cause more than 80% of the
#       running jobs to be searchco jobs
#   (d) mysocialnetwork1 jobs may not start if there are any mysocialnetwork2
#       jobs running;
#   (e) nor may mysocialnetwork2 jobs start if there are mysocialnetwork1 jobs
#       (the two social networks hate each other so much they refuse to share
#       the same machine at the same time)
#
# The contracts make no guarantees about starvation.

# Implement the service provider's monitor using python Locks and
# Condition variables

class Provider(object):
    def __init__(self, n):
        pass

    def govco_enter(self):
        pass

    def govco_leave(self):
        pass

    def searchco_enter(self):
        pass

    def searchco_leave(self):
        pass

    def mysocial1_enter(self):
        pass

    def mysocial1_leave(self):
        pass

    def mysocial2_enter(self):
        pass

    def mysocial2_leave(self):
        pass


GOVCO    = 0
SEARCHCO = 1
MYSOC1   = 2
MYSOC2   = 3

class Job(Thread):
    def __init__(self, job_type, provider):
        Thread.__init__(self)
        self.job_type = job_type
        self.provider = provider

    def run(self):
        enters = [self.provider.govco_enter,
                  self.provider.searchco_enter,
                  self.provider.mysocial1_enter,
                  self.provider.mysocial2_enter]
        leaves = [self.provider.govco_leave,
                  self.provider.searchco_leave,
                  self.provider.mysocial1_leave,
                  self.provider.mysocial2_leave]
        names  = ['govco', 'searchco', 'mysocial1', 'mysocial2']

        print("%s job trying to enter" % names[self.job_type])
        enters[self.job_type]()
        print("%s job admitted" % names[self.job_type])
        sleep(0.1)
        print("%s job leaving" % names[self.job_type])
        leaves[self.job_type]()
        print("%s job done" % names[self.job_type])

max_jobs = 15
numbers = [10, 35, 2, 4]
provider = Provider(max_jobs)
for co in [GOVCO, SEARCHCO, MYSOC1, MYSOC2]:
    for i in range(numbers[co]):
        Job(co, provider).start()

##
## vim: ts=4 sw=4 et ai
##
