#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
import csv

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

def cf3Callback(pose_message):
    global cf3x
    global cf3y
    global cf3z
    global cf3theta
    global cf3lin
    global cf3ang
    
    cf3x = pose_message.x
    cf3y = pose_message.y
    cf3theta = pose_message.theta
    cf3lin = pose_message.linear_velocity
    cf3ang = pose_message.angular_velocity

wrap = 1
def chase():
    global wrap

    while True:

        target_x = cf3x
        target_y=cf3y
        print("Target x:", target_x)
        print("Target y:", target_y)
        orientate(target_x,target_y)
        time.sleep(1)
        # go_to_goal(target_x,target_y)
        time.sleep(0.5)
        # if wrap == 2:    
        #     break
        if cf3x == 4.99 and cf3y ==1.0:
            # wrap = wrap + 1
            print('stop')
            rospy.signal_shutdown("done")
            break

def getLin(distA, linD):
    distA =int(distA)
    linD=int(linD)
    with open('/home/juls/catkin_ws/src/tmara_move/scripts/linear_x.csv') as linvels:
        csv_reader = csv.reader(linvels)
        for index,row in enumerate(csv_reader):
            if index == distA+1:
                print('linvel')
                return (float(row[linD+1]))

###################################### ANGULAR

def getAng(distA, linD):
    distA =int(distA)
    linD=int(linD)
    # distA =int(linD)
    # linD=int(distA)
    with open('/home/juls/catkin_ws/src/tmara_move/scripts/angular_x.csv') as angvels:
        csv_reader = csv.reader(angvels)
        for index,row in enumerate(csv_reader):
            if index == distA:
                rad=math.radians(float(row[linD]))
                print("angvel-->",rad)
                return (float(rad))

###################################### ANGULAR



# def chase():


#     while True:

#         target_x = cf3x
#         target_y=cf3y
#         print("Target x:", target_x)
#         print("Target y:", target_y)
#         orientate(target_x,target_y)
#         go_to_goal(target_x,target_y)



def orientate (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle4/cmd_vel'

    while(True):
        ka = 4.0
        angular_speed= None
        distance = abs(math.sqrt(((xgoal-x)**2)+((ygoal-y)**2)))
        desired_angle_goal = math.atan2(ygoal-y, xgoal-x)
        dtheta = desired_angle_goal-theta 
        # dtheta = desired_angle_goal- cf3theta        
        # aux = 2*math.pi-dtheta
        if dtheta > math.pi:
            dtheta = dtheta -2*math.pi
        elif dtheta < -math.pi:
            dtheta = 2*math.pi
        # print('dtheta:', dtheta)
        angular_speed = dtheta
        # angular_speed = getAng(math.degrees(dtheta),distance)
        # if angular_speed == None:
        #     angular_speed=ka * (dtheta)
        print(type(angular_speed))
        # time.sleep(5)
        # angular_speed = float(getAng(math.degrees(distance),dtheta))
        velocity_message.angular.z = angular_speed
        velocity_message.linear.x = 0.0	
        velocity_publisher.publish(velocity_message)

        if (dtheta < 0.05):
            break

def go_to_goal (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    # cmd_vel_topic = '/turtle4/cmd_vel'

    while(True):
        kv = 0.8				
        distance = abs(math.sqrt(((xgoal-x)**2)+((ygoal-y)**2)))
        #linear_speed = kv * distance

        ka = 3.0
        desired_angle_goal = math.atan2(ygoal-y, xgoal-x)
        dtheta = desired_angle_goal-theta 
        # # dtheta = desired_angle_goal-cf3theta
        if dtheta > math.pi:
            dtheta = dtheta - 2*math.pi
        elif dtheta < -math.pi:
            dtheta = 2*math.pi
        # angular_speed = ka * (dtheta)
        print("This is theta>",dtheta)
        angular_speed = getAng(math.degrees(dtheta),distance)
        if angular_speed == None:
            angular_speed=ka * (dtheta)
        print(type(angular_speed))
        # time.sleep(5)
        # angular_speed = getAng(distance,math.degrees(dtheta))
        linear_speed = getLin(distance,dtheta)

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        # print(dtheta)
        if (distance < 0.1):
            break

if __name__ == '__main__':
    try:

        rospy.init_node('turtlesim_motion_pose', anonymous = True)

        cmd_vel_topic = '/turtle2/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

        position_topic_pub = "/turtle2/pose"
        pose_subscriber = rospy.Publisher(position_topic_pub, Pose, queue_size=10)

        position_topic_sub = "/turtle2/pose"
        pose_subscriber = rospy.Subscriber(position_topic_sub, Pose, poseCallback)
        
        cf3_position_topic = "/turtle3/pose"
        pose_subscriber = rospy.Subscriber(cf3_position_topic, Pose, cf3Callback)
        
        # time.sleep(2)     

        
        #Frth line
        #Bot R
        time.sleep(3.0)
        chase()


    except rospy.ROSInterruptException:        
        pass
