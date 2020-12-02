#! /usr/bin/env python

import rospy
from std_srvs.srv import Trigger, TriggerResponse
def trigger_response(request):
    return TriggerResponse(
        success = True,
        message = "A blank test message!"
    )
    
rospy.init_node('service_example')
srv = rospy.Service("/service_temp_topic",Trigger,trigger_response)
rospy.spin()