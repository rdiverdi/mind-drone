#!/usr/bin/env python

# control a neato using an accelerometer
# This script listens to an imu topic and outputs a cmd_vel

import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist

IMU_TOPIC = "/accel"
CMD_TOPIC = "turtle1/cmd_vel"
SCALE = 1

class AccelControl ():
    def __init__(self):
        rospy.init_node('accel_controller')
        self.cmd_pub = rospy.Publisher(CMD_TOPIC, Twist, queue_size=10)
        imu_sub = rospy.Subscriber(IMU_TOPIC, Imu, self.imu_cb)
        rospy.on_shutdown(self.stop)
        
        self.count = 0

        self.cmd = Twist()
        self.timeout = 1

    def stop(self):
        self.cmd_pub.publish(Twist())

    def imu_cb(self, msg):
        self.count = 0
        x_accel = msg.linear_acceleration.x
        y_accel = msg.linear_acceleration.y
        self.cmd.linear.x = (x_accel+3)*SCALE/10
        self.cmd.angular.z = y_accel*SCALE/10
    
    def run(self):
        rate = 10
        r = rospy.Rate(rate)
        while not rospy.is_shutdown():
            if self.count < self.timeout*rate:
                self.cmd_pub.publish(self.cmd)
            else:
                self.stop()
            self.count += 1
            r.sleep()

if __name__ == '__main__':
    controller = AccelControl()
    controller.run()
