#!/usr/bin/env/python3
import rospy
import os
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties
#import sys, tty, select, termios
from geometry_msgs.msg import Twist


rospy.init_node("vel_controller", anonymous = True)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size="1")

f = 20.0
f = 50.0
T = 1/f
rate = rospy.Rate(f)
vel = Twist()

while True:
    print("---------------------------------------------------------------")
    print("Command  : Result            |   j   : Dance 1")
    print("w        : Drive forward     |   2   : Drive forward faster")
    print("a        : Rotate left       |   q   : Forward, veer left")
    print("d        : Rotate right      |   e   : Forward, veer right")
    print("s        : Stop moving       |   x   : Drive backwards")
    print("r        : Reset the robot   |   k   : Dance 2")
    print("\nCtrl + c + enter to quit.")
    print("(Remember to shift down gears - going from 2 to s will flip the robot!)")
    buff = raw_input("command:")
    
    # Forward -----------------------------
    key_F = False
    if (buff == "w"): key_F = True
    if (key_F):
        vel.linear.x = 2
        vel.linear.y = 2
        pub.publish(vel)

    if (buff == "2"):
        vel.linear.x = 4
        vel.linear.y = 4
        pub.publish(vel)

    # Veer left
    if (buff == "q"):
        vel.linear.x = 4
        vel.linear.y = 3
        pub.publish(vel)

    # Veer right
    if (buff == "e"):
        vel.linear.x = 3
        vel.linear.y = 4
        pub.publish(vel)

    # Left -----------------------------
    key_L = False
    if (buff == "a"): key_L = True
    if (key_L):
        vel.linear.x = 2
        vel.linear.y = -2
        pub.publish(vel)
    
    # Right -----------------------------
    key_R = False
    if (buff == "d"): key_R = True
    if (key_R):
        vel.linear.x = -2
        vel.linear.y = 2
        pub.publish(vel)
    
    # Backward -----------------------------
    key_S = False
    if (buff == "s"): key_S = True
    if (key_S):
        vel.linear.x = 0
        vel.linear.y = 0
        pub.publish(vel)

    if (buff == "x"):
        vel.linear.x = -2
        vel.linear.y = -2
        pub.publish(vel)


    # Reset -----------------------------
    if (buff == "r"):
        os.system("./reset_robo.sh")

    # Quit -----------------------------
    if (buff == "quit"):
        break

    # Silly -----------------------------
    if (buff == "j"):
        vel.linear.x = 10
        vel.linear.y = 10
        pub.publish(vel)
        

    if (buff == "k"):
        vel.linear.x = 20
        vel.linear.y = -20
        pub.publish(vel)

    rate.sleep()

print("Exiting! Bye bye!")