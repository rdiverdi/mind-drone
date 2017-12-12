#!/usr/bin/env python

# Translate EEG data into eye movement directions
# This script listens to an eeg topic and a thresh topic and outputs a dir

import rospy
import time
from geometry_msgs.msg import Quaternion
from std_msgs.msg import String
from memeCallibrate import calibrate

THRESH_TOPIC = "/thresh"
EEG_TOPIC = "/eeg"
DIR_TOPIC = "/dir"
SCALE = 1

class DirNotifier():
    def __init__(self):
        rospy.init_node('direction_notifier')
        thresh_sub = rospy.Subscriber(THRESH_TOPIC, Quaternion, self.thresh_parse)
        eeg_sub = rospy.Subscriber(EEG_TOPIC, Quaternion, self.eeg_parse)
        self.dir_pub = rospy.Publisher(DIR_TOPIC, String, queue_size=10)
        rospy.on_shutdown(self.stop)
        
        self.iter_count = 0
        self.xs = []
        self.ys = []
        self.zs = []
        self.ws = []
        self.len_lim = 20
        
        self.x_thresh = None
        self.y_thresh = None
        self.z_thresh = None
        self.w_thresh = None

        self.dir = ""
        self.timeout = 1

    def stop(self):
        self.dir_pub.publish("")

    def thresh_parse(self, msg):
        self.x_thresh = msg.x
        self.y_thresh = msg.y
        self.z_thresh = msg.z
        self.w_thresh = msg.w
        print("Got threshold")

    def eeg_parse(self, msg):
        self.iter_count = 0
        self.xs.append(msg.x)
        self.ys.append(msg.y)
        self.zs.append(msg.z)
        self.ws.append(msg.w)
        if len(self.xs) > self.len_lim:
            self.xs = self.xs[1:]
            self.ys = self.ys[1:]
            self.zs = self.zs[1:]
            self.ws = self.ws[1:]
    
    def run(self):
        rate = 10
        r = rospy.Rate(rate)
        print("Running...")
        while not rospy.is_shutdown():
            if True:
                if self.x_thresh and (len(self.xs) >= self.len_lim):
                    signal = False
                    if min(self.ws) < self.x_thresh:
                        self.dir_pub.publish("up")
                        print("up")
                        signal = True
                    if max(self.ys) > self.y_thresh:
                        self.dir_pub.publish("left")
                        print("left")
                        signal = True
                    if max(self.zs) > self.z_thresh:
                        self.dir_pub.publish("right")
                        print("right")
                        signal = True
                    if max(self.ws) > self.w_thresh:
                        self.dir_pub.publish("down")
                        print("down")
                        signal = True
                    if signal:
                        time.sleep(1)

            # else:
                #self.stop()
            self.iter_count += 1
            r.sleep()

if __name__ == '__main__':
    controller = DirNotifier()
    controller.run()