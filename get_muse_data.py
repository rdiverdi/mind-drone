"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
import time
from memeCallibrate import calibrate

# first resolve an EEG stream on the lab network
print("looking for an Accel stream...")
streams = resolve_stream('type')

accel_stream = None
eeg_stream = None
for stream in streams:
    if stream.type() == 'Accelerometer' and accel_stream == None:
        accel_stream = stream
    if stream.type() == 'EEG' and eeg_stream == None:
        eeg_stream = stream

if accel_stream == None:
    print 'no accelerometer stream'
if eeg_stream == None:
    print 'no eeg stream'

#print accel_stream.nominal_srate()
print eeg_stream.nominal_srate()

print 'streams found'

# create a new inlet to read from the stream
#accel_inlet = StreamInlet(accel_stream)

eeg_inlet = StreamInlet(eeg_stream)

#CALIBRATE
threshes = calibrate(eeg_inlet)
thresh_pub = rospy.Publisher('/thresh', Quaternion, queue_size = 1, latch = True)
thresh_msg.x = threshes[0]
thresh_msg.y = threshes[1]
thresh_msg.z = threshes[2]
thresh_msg.w = threshes[3]
time.sleep(1000)
thresh_pub.publish(thresh_msg)

#accel_pub = rospy.Publisher('/accel', Imu, queue_size = 10)
eeg_pub = rospy.Publisher('/eeg', Quaternion, queue_size = 100)

rospy.init_node('muse_com')
r = rospy.Rate(220) #20 Hz

#accel_msg = Imu()
thresh_msg = Quaternion()
eeg_msg = Quaternion()

t_old = 0

while not rospy.is_shutdown():
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    #accel_sample, timestamp = accel_inlet.pull_sample()
    #print(timestamp, sample)

    eeg_sample, eeg_tstamp = eeg_inlet.pull_sample()
    #print eeg_sample
    

    #print eeg_tstamp-t_old
    t_old = eeg_tstamp

    """
    for i, val in enumerate(eeg_sample):
        print i, ':  ', int(val)
    print '\n'
    """


    eeg_msg.x = eeg_sample[0]
    eeg_msg.y = eeg_sample[1]
    eeg_msg.z = eeg_sample[2]
    eeg_msg.w = eeg_sample[3]

    #accel_msg.linear_acceleration.x = accel_sample[0]/100.
    #accel_msg.linear_acceleration.y = accel_sample[2]/-100.
    #accel_msg.linear_acceleration.z = accel_sample[1]/100.

    #accel_pub.publish(accel_msg)
    eeg_pub.publish(eeg_msg)
    r.sleep()
