#!/usr/bin/env python

# control a neato using an accelerometer
# This script listens to an imu topic and outputs a cmd_vel

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

DIR_TOPIC = "/dir"
CMD_TOPIC = "/cmd_vel"
SCALE = .2

class Controller():
    def __init__(self):
        rospy.init_node('neato_controller')
        self.cmd_pub = rospy.Publisher(CMD_TOPIC, Twist, queue_size=10)
        dir_sub = rospy.Subscriber(DIR_TOPIC, String, self.dir_cb)
        rospy.on_shutdown(self.stop)
        
        self.count = 0

        self.cmd = Twist()
        self.timeout = 3

    def stop(self):
        self.cmd_pub.publish(Twist())

    def dir_cb(self, msg):
        self.count = 0
        if msg.data == 'right':
            self.cmd.angular.z -= 0.5*SCALE
            if self.cmd.angular.z < -5*SCALE:
                self.cmd.angular.z = -5*SCALE
        elif msg.data == 'left':
            self.cmd.angular.z += 0.5*SCALE
            if self.cmd.angular.z > 5*SCALE:
                self.cmd.angular.z = 5*SCALE
        elif msg.data == 'up':
            self.cmd.linear.x += 0.5*SCALE
            if self.cmd.linear.x > 3*SCALE:
                self.cmd.linear.x = 3*SCALE
        elif msg.data == 'down':
            self.cmd = Twist()
    
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
    controller = Controller()
    controller.run()
