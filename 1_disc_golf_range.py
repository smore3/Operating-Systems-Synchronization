from threading import Semaphore, Lock, Thread
from time import sleep
from random import random
from timeit import Timer

#stash = 20
#DiscsPerBucket = 5
#Frolfer=3
stash=int(input('Enter the Stash size: '))
Frolfer = int(input('Enter the number of Frolfers: '))
DiscsPerBucket = int(input('Enter the number of Discs per bucket'))

mutex=Semaphore(1)    #Mutex for acquiring the stash
turnstile=Semaphore(1)#Semaphore for blocking the frolfers from throwing when the cart is refilling stash
barrier=Semaphore(0)  #Semaphore used for stopping the frolfers from accessing the stash
DiscsOnField=0
count=0
#cartOnField = Lightswitch()
#stashEmpty = Semaphore(1) 

def frolfer(n):
    global stash
    global numDisc
    global DiscsPerBucket
    global DiscsOnField
    global count 

    while True:
       
       print('\n Frolfer %d calling for bucket' % n)
       
       if stash < DiscsPerBucket:
          #barrier.acquire()
          #stash -= DiscsPerBucket
           
          threads_cart= Thread(target=cart, args=[])
          threads_cart.start()
          barrier.acquire()
       
       stash-=DiscsPerBucket
       print('\n frolfer %d got %d discs Stash= %d' % (n,DiscsPerBucket,stash))
       mutex.release()
       for i in range(DiscsPerBucket):
           sleep(random())
           turnstile.acquire()
           turnstile.release()
           mutex.acquire()
           DiscsOnField +=1
           mutex.release()
           
           print('\n frolfer %d threw disc %d. Number of Discs on field = %d' %(n,i,DiscsOnField))     
           
def cart():
          global stash
          global DiscsOnField
          turnstile.acquire()
          sleep(random())
          stash += DiscsOnField

          print('\n ###################################### \n Cart entering field. Stash is now = %d \n ##################################### \n' % stash)
          
          DiscsOnField=0
          turnstile.release()
          barrier.release()


    
###Starting the threads
          
for i in range(Frolfer):
       threads_frolfers = Thread(target=frolfer, args=[i])
       threads_frolfers.start()
     
