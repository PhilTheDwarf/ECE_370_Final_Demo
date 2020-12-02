#! /usr/bin/env python
import rospy
from std_srvs.srv import Trigger, TriggerResponse
import os
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
import numpy as np

name = "pizzabox"
box_i = 0

robotProxy = None

def trigger_response(request): # Done!
    print("Received!")

    rLoc = getRobotLocation()
    x = rLoc[0]
    y = rLoc[1]

    dropBoxBool = False
    boxLoc = getBoxLocation(x, y)
    print("FLAG B: ",boxLoc)
    if (boxLoc != None):
        if not checkBoxLocation(boxLoc[0],boxLoc[1]):
            dropBox(boxLoc[0], boxLoc[1])
            dropBoxBool = True

    return TriggerResponse(
        success = dropBoxBool,
        message = "Test server message!"
    )

box_x = []
box_y = []
def saveBoxVal(x, y):
    global box_x, box_y
    box_x.append(x)
    box_y.append(y)
    return

def checkBoxLocation(x, y):
    global box_x, box_y
    for i in range(len(box_x)):
        xx = box_x[i]
        yy = box_y[i]
        d = np.sqrt((xx-x)**2 + (yy-y)**2)
        if d < 1.01:
            return True # if within  x amount of m
    return False

def dropBox(x, y):
    saveBoxVal(x,y)
    b0 = "./dropBox.sh "
    global box_i
    b1 = name + str(box_i) + " "
    box_i += 1
    b2 = str(x) + " "
    b3 = str(y) + " "
    b4 = "&"
    buff = b0 + b1 + b2 + b3 + b4
    #os.system("./dropBox.sh")
    print(buffer)
    os.system(buff)
    '''
    return TriggerResponse(
        success = dropBoxBool,
        message = "A blank test message!"
    )'''
    
def delBox(bi):
    buff = "rosservice call gazebo/delete_model "+name+str(bi)
    os.system(buff)

def delBoxAll(bi):
    for i in range(bi):
        delBox(i)




def getBoxLocation(x, y): # Done!
    # determine if inside 50m circle ( or in our case, square)
    x0 = 0.0
    y0 = 0.0
    '''
    #R = 50.0
    #dist = ((x - x0)**2 + (y - y0)**2)**0.5
    print("Dist is: ", dist)
    #if(False):
    if (dist < R - 2):
        return
    else:
        theta = np.arctan2(y,x)
        xn = R * np.cos(theta)
        yn = R * np.sin(theta)
        return (xn, yn)
    '''
    x_max = 50 - x0
    y_max = 50 - y0
    offset = 2
    x_dist = x - x0
    y_dist = y - y0
    #If at both x and y boundary, drop a box at x bound and y bound
    if ((x >= x_max - offset) and (y >= y_max - offset)):
        return (x_max, y_max)
    #If at x boundary, drop a box at x bound and current y
    if (x >= x_max - offset):
        return (x_max, y_dist)
    #If at y boundary, drop a box at y bound and current x
    if (y >= y_max - offset):
        return (y_max, x_dist)
    
    return

def getRobotLocation(): # Done!
    global robotProxy
    a = GetModelStateRequest(model_name="rob_0")
    a.model_name = "rob_0"
    s = robotProxy(a)
    #print(a)
    #print(s)
    
    x = s.pose.position.x
    y = s.pose.position.y
    print(x,y)
    print("x = ",str(x),", y = ",str(y))
    return (x,y)
    #return (0, 0)


#delBoxAll(255)
rospy.init_node('service_example')
srv0 = rospy.Service("/box",Trigger,trigger_response)

rospy.wait_for_service("/gazebo/get_model_state")
robotProxy = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)

rospy.spin()