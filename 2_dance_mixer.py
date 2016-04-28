from threading import Thread, Semaphore
from time import sleep
from collections import deque
from itertools import cycle
from random import random

class Fifo:

    def __init__(self):
        self.queue = deque()
        self.mutex = Semaphore(1)
               
    def acquire(self, mySem):
        self.mutex.acquire()
        self.queue.append(mySem)   
        self.mutex.release()
        mySem.acquire()
        
        
    def release(self):
        self.mutex.acquire()
        sem = self.queue.popleft()  
        self.mutex.release()
        sem.release()
                   
leaderQueue = Fifo()          #Object of class Fifo for leader semaphores
followerQueue = Fifo()        #Object of class Fifo for follower sempahores
nleaders = nfollowers = 0     
leadFollowMutex = Semaphore(1)#Mutex acquired by leaders and follower threads
floorMutex = Semaphore(1)     #Mutex for acquiring the floor when incrementing the count of dancers on the floor
floorMutex2 = Semaphore(1)    #Mutex for acquiring floor when decrementing the count of dancers on floor
fQueue = deque()              #Follower Queue for tracking which thread was poped and appended
lQueue = deque()              #Leader Queue for tracking which thread was poped and appended
mySem = Semaphore(0)          #Semaphore to be sent to object of Fifo class
emptyFloor = Semaphore(0)
bandLeaderBarrier = Semaphore(0)#semaphores acquired by bandleader when it needs to change the music
nDancers = 0
    
def leaders(id):
    global nfollowers
    global nleaders
    global nDancers
    followerId = -1
    count = 0
    while True:
       
        bandLeaderBarrier.acquire()
        bandLeaderBarrier.release()
        #sleep(random())
        leadFollowMutex.acquire()
        if nfollowers > 0:
           nfollowers -= 1
           followerQueue.release()
           followerId = fQueue.popleft(); 
           leadFollowMutex.release()
        else:
           nleaders += 1
           lQueue.append(id)
           leadFollowMutex.release()
           leaderQueue.acquire(mySem)

        print("\nLeader %d entering the floor.\n" % id)
        floorMutex.acquire()
        nDancers += 1
        if nDancers == 1:
            emptyFloor.acquire()
        floorMutex.release()
        if (id != -1) and (followerId != -1):
            print("\nLeader %s and Follower %s are dancing.\n" % (id, followerId))

        sleep(1) #time for dancing
        #line up logic
        print("\nLeader %d getting back in line. \n" % id)
        floorMutex2.acquire()
        nDancers -= 1
        if nDancers == 0:
            emptyFloor.release()
            print('\n Number of dancers on floor are: %d.\n' % nDancers)
        floorMutex2.release()


def followers(id):
    global nfollowers
    global nleaders
    global nDancers,count
    leaderId = -1
    mySem =Semaphore(0)
    
    while True:

        bandLeaderBarrier.acquire()
        bandLeaderBarrier.release()
        sleep(random())
        leadFollowMutex.acquire()
        if  nleaders > 0:
            nleaders -= 1
            leaderQueue.release()
            leaderId = lQueue.popleft()
            leadFollowMutex.release()           
        else:
            nfollowers += 1
            fQueue.append(id)
            leadFollowMutex.release()
            followerQueue.acquire(mySem)

        print("\nFollower %d entering the floor. \n" % id)
        floorMutex.acquire()
        nDancers += 1
        if nDancers == 1:
            emptyFloor.acquire()
        floorMutex.release()
        if (id != -1) and (leaderId != -1):
            print("\nFollower %s and Leader %s are dancing.\n" % (id,leaderId))
        

        sleep(5) #the sleep time for which dancing is done
        #line up
        print("\nFollower %d getting back in line.\n" % id)
        floorMutex2.acquire()
        nDancers -= 1
        if nDancers == 0:
            emptyFloor.release()
            print('\n Number of dancers on floor are: %d.\n' % nDancers)
        floorMutex2.release()
          

if __name__ == '__main__':

    no_of_leaders=int(input('Enter the number of leaders: '))
    no_of_followers=int(input('Enter the number of followers: '))

    ldrthrd = [Thread(target=leaders, args=[i]) for i in range(no_of_leaders)]
    for lt in ldrthrd: lt.start()

    flrthrd = [Thread(target=followers, args=[i]) for i in range(no_of_followers)]
    for ft in flrthrd: ft.start()
    
    
    for music in cycle(['waltz', 'tango', 'foxtrot']):
        print("** Band leader started playing the music %s **" %(music))
        emptyFloor.release()
        bandLeaderBarrier.release()
        sleep(5)
        bandLeaderBarrier.acquire()
        emptyFloor.acquire()
        sleep(random())
#     floorEmpty.release()
        print("** Band leader stopped playing the music %s **" %(music))


