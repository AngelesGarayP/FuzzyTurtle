#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x = 0
y = 0
z = 0
theta = 0

def poseCallback(pose_message):
    global x
    global y
    global z
    global theta
    
    x = pose_message.x
    y = pose_message.y
    theta = pose_message.theta

def orientate (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle4/cmd_vel'

    while(True):
        ka = 4.0
        desired_angle_goal = math.atan2(ygoal-y, xgoal-x)
        dtheta = desired_angle_goal-theta        
        aux = 2*math.pi-dtheta
        if dtheta > math.pi:
            dtheta = dtheta - 2*math.pi
        elif dtheta < -math.pi:
            dtheta = dtheta = 2*math.pi
        angular_speed = ka * (dtheta)
        velocity_message.angular.z = angular_speed
        velocity_message.linear.x = 0.0	
        velocity_publisher.publish(velocity_message)
        print(dtheta)
        if (dtheta < 0.03):
            break

def go_to_goal (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle4/cmd_vel'

    while(True):
        kv = 0.5				
        distance = abs(math.sqrt(((xgoal-x)**2)+((ygoal-y)**2)))
        linear_speed = kv * distance

        ka = 3.0
        desired_angle_goal = math.atan2(ygoal-y, xgoal-x)
        dtheta = desired_angle_goal-theta 
        if dtheta > math.pi:
            dtheta = dtheta - 2*math.pi
        elif dtheta < -math.pi:
            dtheta = dtheta = 2*math.pi
        angular_speed = ka * (dtheta)

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        print(dtheta)
        if (distance < 0.01):
            break

if __name__ == '__main__':
    try:

        rospy.init_node('turtlesim_motion_pose', anonymous = True)

        cmd_vel_topic = '/turtle3/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

        position_topic_pub = "/turtle3/pose"
        pose_subscriber = rospy.Publisher(position_topic_pub, Pose, queue_size=10)

        position_topic_sub = "/turtle3/pose"
        pose_subscriber = rospy.Subscriber(position_topic_sub, Pose, poseCallback)

        rospy.Rate(1)
        # time.sleep(2)     

        
        #Frth line
        #Bot R
        time.sleep(3.0)
        orientate(10,5)
        time.sleep(1.0)
        go_to_goal(10,5)
        time.sleep(1.0)	
         #Thrd line
        #Top R
        orientate(5,10)
        time.sleep(1.0)
        go_to_goal(5,10)
        time.sleep(1.0)		
        #Scnd line
        #Top L
        orientate(1,5)
        time.sleep(2.0)
        orientate(1,5)
        time.sleep(1.0)
        go_to_goal(1,5)
        time.sleep(1.0)


        orientate(5,1)
        time.sleep(2.0)
        # orientate(5,2)
        time.sleep(1.0)
        go_to_goal(5,1)
        time.sleep(1.0)

    except rospy.ROSInterruptException:        
        pass
