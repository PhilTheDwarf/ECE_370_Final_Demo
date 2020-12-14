#!/usr/bin/env/python3
import rospy
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties
import sys, tty, select, termios
from geometry_msgs.msg import Twist

msg_topic = 'gazebo/apply_joint_effort'
msg_topic_feedback = "/gazebo/get_joint_properties"

joint_l = "rob_0::hinge_fl_wheel"
joint_bl = "rob_0::hinge_bl_wheel"
joint_r = "rob_0::hinge_fr_wheel"
joint_br = "rob_0::hinge_br_wheel"

rospy.init_node("dd_control", anonymous = True)
pub = rospy.ServiceProxy(msg_topic,ApplyJointEffort)
pub_feedback = rospy.ServiceProxy(msg_topic_feedback, GetJointProperties)

effort = 1.0
start_time = rospy.Time(0,0)
end_time = rospy.Time(1,0)

f = 0.5
f = 50.0
T = 1/f
end_time = rospy.Time(T,0)
rate = rospy.Rate(f)

roboVel = Twist()
def getCmdVel(msg):
    #print(msg.linear.x)
    global roboVel
    roboVel = msg
sub0 = rospy.Subscriber("/cmd_vel",Twist,getCmdVel)

# rostopic pub /cmd_vel geometry...
# setting x as linear speed and y to angular speed below.

while True:
    # Use a topic to set vd_r and vd_l.
    vd_r = roboVel.linear.x
    vd_l = roboVel.linear.y
    #vd_r = roboVel.linear.x * 

    # Left wheel CTR
    val = pub_feedback(joint_l)
    #vd = 0.0 # The desired velocity, which we will set.
    if (len(val.rate) == 0): continue # tired of it crashing on reset
    va = val.rate[0] # the actual velocity of our wheel*
    e = vd_l - va # The error of our wheels
    Kp = 3
    cl = e * Kp

    val = pub_feedback(joint_bl)
    #vd = 0.0 # The desired velocity, which we will set.
    if (len(val.rate) == 0): continue # tired of it crashing on reset
    va = val.rate[0] # the actual velocity of our wheel*
    e = vd_l - va # The error of our wheels
    Kp = 3
    cbl = e * Kp



    # Right wheel CTR
    val = pub_feedback(joint_r)
    if (len(val.rate) == 0): continue # tired of it crashing on reset
    #vd = 0.0 # The desired velocity, which we will set.
    va = val.rate[0] # the actual velocity of our wheel*
    e = vd_r - va # The error of our wheels
    Kp = 3
    cr = e * Kp

    val = pub_feedback(joint_br)
    if (len(val.rate) == 0): continue # tired of it crashing on reset
    #vd = 0.0 # The desired velocity, which we will set.
    va = val.rate[0] # the actual velocity of our wheel*
    e = vd_r - va # The error of our wheels
    Kp = 3
    cbr = e * Kp

    pub(joint_r, cr, start_time, end_time)
    pub(joint_l, cl, start_time, end_time)
    pub(joint_bl, cbl, start_time, end_time)
    pub(joint_br, cbr, start_time, end_time)

    #rate.sleep() # will sleep for 0.1 - 0.01 = 0.099 seconds
    rate.sleep()


