#!/usr/bin/env/python3
import rospy
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties
import sys, tty, select, termios
from geometry_msgs.msg import Twist

# ------------ Curses ------------
#import curses
#stdscr = curses.initscr() # get a window object, representing the screen
#curses.noecho()
# ------------ End ------------



msg_topic = 'gazebo/apply_joint_effort'
joint_l = "rob_0::hinge_l_wheel"
joint_r = "rob_0::hinge_r_wheel"

msg_topic_feedback = "/gazebo/get_joint_properties"

pub_feedback = rospy.ServiceProxy(msg_topic_feedback, GetJointProperties)

rospy.init_node("dd_control", anonymous = True)
pub = rospy.ServiceProxy(msg_topic,ApplyJointEffort)

effort = 1.0
start_time = rospy.Time(0,0)
end_time = rospy.Time(1,0)

f = 0.5
f = 2.0
T = 1/f
end_time = rospy.Time(T,0)
rate = rospy.Rate(f)
'''
roboVel = Twist()
def getCmdVel(msg):
    print(msg.linear.x)
    global roboVel
    roboVel = msg
sub0 = rospy.Subscriber("/cmd_vel",Twist,getCmdVel)'''
while True:
    #key = getKey(1)
    #print("Key is " + key)
    #print roboVel
    # ----------

    #buff = ""
    print("------------------")
    print("Command          : Result")
    print("w                : Drive forward")
    print("a                : Drive left")
    print("d                : Drive right")
    print("s                : Drive backwards")
    print("Ctrl + c + enter to quit.")
    buff = raw_input("command:")
    
    key_L = False
    if (buff == "d" or buff == "w"): key_L = True
    if (key_L): pub(joint_l, effort, start_time, end_time) # 0.01 sec to execute
    
    key_R = False
    if (buff == "a" or buff == "w"): key_R = True
    if (key_R): pub(joint_r, effort, start_time, end_time) # 0.01 sec to execute
    
    key_S = False
    if (buff == "s"): key_S = True
    if (key_S):
        pub(joint_r, -effort, start_time, end_time)
        pub(joint_l, -effort, start_time, end_time)


    val = pub_feedback(joint_l)
    print(val)
    #rate.sleep() # will sleep for 0.1 - 0.01 = 0.099 seconds
    print(T)
    rate.sleep()


