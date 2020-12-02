#! /usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerRequest

rospy.init_node("serv_client")
rospy.wait_for_service("/service_temp_topic")
sos_serv = rospy.ServiceProxy("/service_temp_topic", Trigger)
sos = TriggerRequest()
#result = sos_serv(sos)

#print(result)