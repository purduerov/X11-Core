#! /usr/bin/python
import threading
from threading import Thread, Lock
from std_msgs.msg import String
from time import sleep
import copy
import rospy
import random


# These will be initialized later
pub1 = None
pub2 = None
kill = False

# Create a lock that controls who has the ball
beach_lock = Lock()


""" Simple class that will be passed back and forth
betweeen threads. For learning purposes only"""
class BeachBall:
  def __init__(self):
    self.hits = 1
    self.court_side = "No one has the ball"

# Initialize the beach ball
ball = BeachBall()


# Function 1 will be run by thread1
def function1(args):
  while not kill:
    print("hello1 from thread1")

    # Get the lock so thread2 does not steal the ball
    beach_lock.acquire()
    ball.court_side = "thread 1 has the ball"
    # Deep copy the ball so that we can release the
    # lock. 
    myball = copy.deepcopy(ball)
    beach_lock.release() # let thread2 have the ball

    # ONLY PUBLISH THE DEEP COPIED VALUE
    pub1.publish(
      String(myball.court_side))

    # Force the threads to run at different rates
    # so that if someone remove the locks, the ball
    # will get stolen
    # (For demo purposes only)
    sleep(random.randint(50,200)/ 100.0)
    

# Function2 will be called by thread2
def function2(args):
  while not kill:
    print("hello2 from thread2")

    # Get the lock so thread1 does not steal the ball
    beach_lock.acquire()
    ball.court_side = "Thread 2 got the ball"

    # Deep copy the ball so that we can release the
    # lock. 
    myball = copy.deepcopy(ball)
    beach_lock.release() # let thread1 get the ball

    
    # ONLY PUBLISH THE DEEP COPIED VALUE
    pub2.publish(
      String(myball.court_side))

    # Force the threads to run at different rates
    # so that if someone remove the locks, the ball
    # will get stolen
    # (For demo purposes only)
    sleep(random.randint(50,200)/ 100.0)





if __name__ == "__main__":
  print('Initializing')
  rospy.init_node("threadripper")
  # initialize the publishers PRIOR to running the
  # threads
  # use 'rotopic echo /t1' to view thread1's output
  # use 'rostopic echo/t2' to view thread2's output
  pub1 = rospy.Publisher("/t1", String, queue_size=2)
  pub2 = rospy.Publisher("/t2", String, queue_size=2)

  print('Launching threads')

  # Creat the threads, pass in a useless argument
  t1 = Thread(target=function1, args=(10,))
  t2 = Thread(target=function2, args=(10,))

  # Let the games begin!
  t1.start()
  t2.start()

  # Wait for a CTRL-C or a roslaunch kill (IMPORTANT)
  while not rospy.is_shutdown():
    pass

  # Tell the threads to die
  kill = True


  # wait for the threads to terminate
  t1.join()
  t2.join()

  # hooray, we done boys
  print("Threads finished, done")

