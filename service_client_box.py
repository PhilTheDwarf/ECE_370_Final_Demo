#! /usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerRequest
from nav_msgs.srv import GetMap, GetMapRequest
import time as t

rospy.init_node("serv_client")
rospy.wait_for_service("/box")
serv0 = rospy.ServiceProxy("/box", Trigger)
#sos = TriggerRequest()
trigReq = TriggerRequest()
while True:
    tick = t.time()
    result = serv0(trigReq)
    tock = t.time()
    print(tock - tick)
    print(result)
    rospy.sleep(0.02)