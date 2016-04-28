from threading import Semaphore, Lock, Thread
from time import sleep
from random import random
from timeit import Timer
import time
import sys


#nPhilosophers = 5 #number of philosophers
nPhilosophers=int(input('Enter the number of Philosophers: '))
#nMeals = 5    #number of meals
nMeals=int(input('Enter the number of Meals:'))
i=0
while True:
    i=int(input('Choose the solution: \n 1. Footman Solution\n 2. Tanenbaum Solution\n 3. Leftie Solution\n 4. Exit \n'))

    forks = [Semaphore(1) for i in range(nPhilosophers)]  #defines forks
    sem = [Semaphore(0) for i in range(nPhilosophers)]    #semaphores
    footman = Semaphore(4) 
    mutex = Semaphore(1)
    state = ['thinking'] * nPhilosophers
    #T-states
    countMeals = []

    def left_fork(id):
         return id

    def right_fork(id):
         return (id+1) % nPhilosophers

    def right(id):
         return (id+1) % nPhilosophers

    def left(id):
         return (id+nPhilosophers-1) % nPhilosophers

    #footman logic
    def footmanPhilosopher(id,meal):
        global forks
        global footman
        global count
        while True:
             countMeals[id] += 1
             if countMeals[id] > meal: break
             footman.acquire()
             forks[right_fork(id)].acquire()
             forks[left_fork(id)].acquire()
             #rng.seed(100)
             #eat
             sleep(0.01)
             forks[right_fork(id)].release()
             forks[left_fork(id)].release()
             footman.release()


    def philosophize_lefthand(id,meal):
         global forks
         while True:
                countMeals[id] += 1
                if countMeals[id] > meal: break
                #define the left hand user.
                if(id == nPhilosophers-1):
                    forks[left_fork(id)].acquire()
                    forks[right_fork(id)].acquire()
                else:
                    forks[right_fork(id)].acquire()
                    forks[left_fork(id)].acquire()
                #rng.seed(100)
                sleep(0.01)
                if(id == 3):
                    forks[left_fork(id)].release()
                    forks[right_fork(id)].release()
                else:
                    forks[right_fork(id)].release()
                    forks[left_fork(id)].release()

    def get_fork(id):
        global mutex
        global state
        global sem

        mutex.acquire()
        state[id] = 'hungry'
        test(id)
        mutex.release()
        sem[id].acquire()

    def put_fork(id):
        global mutex
        global state
        global sem

        mutex.acquire()
        state[id] = 'thinking'
        test(right(id))
        test(left(id))
        mutex.release()

    def test(id):
        global state
        if state[id] == 'hungry' and state[left(id)] != 'eating' and state[right(id)] != 'eating':   
            state[id] = 'eating'
            sem[id].release()

    def philosophize_Tanenbaum(id,meal):
        while True:
            countMeals[id] += 1
            if countMeals[id] > meal: break
            #think
            get_fork(id)  
            #rng.seed(100)
            #eat
            sleep(0.01)
            put_fork(id)

    def runLeftie():
        global nPhilosophers
        global nMeals
        thrds = []
        for i in range(nPhilosophers):
            countMeals.append(0)
            phil = Thread(target = philosophize_lefthand,args = (i,nMeals))
            phil.start()
            thrds.append(phil)
        for t in thrds:
            t.join()

    def runFootman():
        global nPhilosophers
        global nMeals
        thrds = []
        for i in range(nPhilosophers):
            countMeals.append(0)
            phil = Thread(target = footmanPhilosopher, args = (i,nMeals))
            phil.start()
            thrds.append(phil)

        for t in thrds:
            t.join()

    def runTanenbaum():
        global nPhilosophers
        global nMeals
        thrds = []
        for i in range(nPhilosophers):
            countMeals.append(0)
            phil = Thread(target = philosophize_Tanenbaum,args = (i,nMeals))
            phil.start()
            thrds.append(phil)
        for t in thrds:
            t.join()


    if i!=4:

        t = time.time()
        if i==1:
            runFootman()
            print("Footman Time:", time.time() - t, "s")

        t = time.time()
        if i==2:
            runTanenbaum()
            print("Tanenbaum Time:", time.time() - t, "s")

        t = time.time()
        if i==3:
            runLeftie()
            print("Leftie Time:", time.time() - t, "s")
            
        if i>4:
            print("Invalid choice..Try again!!\n")
            
    if i==4:
        print("\nGood bye!!\n")
        sys.exit(0)
