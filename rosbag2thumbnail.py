import rosbag
import rospy
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os

import cv2
from cv_bridge import CvBridge, CvBridgeError



path = './'
bag_name = '2011-01-25-06-29-26.bag'
topic = '/wide_stereo/left/image_rect_throttle'

    
file_name = os.path.join(path, bag_name )
print( file_name + ' is being processed')

bag = rosbag.Bag(file_name, 'r')

# read all messages with designated topic
messages = [ (topic,msg,t) for topic,msg,t in bag.read_messages(topics=topic) ]


fig_vertical_count = 4
fig_horizontal_count = 4

# * * * *
# * * * *
# * * * *
# * * * *

fig_count = fig_vertical_count * fig_horizontal_count

f , ax = plt.subplots()
f.set_size_inches(( 4*(fig_horizontal_count), 4*fig_vertical_count))

# f = plt.figure(figsize=(4*(fig_horizontal_count), 4*fig_vertical_count))

# no titile for now
# plt.subplot(fig_vertical_count+1, fig_horizontal_count, 1)
# plt.text(0.5, 0.5, bag_name, fontsize=72, va='center', ha='center')
# plt.axis('off')


for i in range(0, fig_vertical_count):
    for j in range(0, fig_horizontal_count):
        
        # get the i.th msg
        msg_id = (len(messages)-1)*(j+i*fig_horizontal_count)/(fig_count-1)
        
        # the time recorded with rosbag
        delta_t = '%.6f' %((messages[msg_id][2]-messages[0][2]).to_sec())
        
        ax = plt.subplot(fig_vertical_count, fig_horizontal_count, j+(i)*fig_vertical_count+1)
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(messages[ msg_id ][1])
        plt.imshow( cv_image )

        title = 't = {}'.format(delta_t)
        ax.set_title(title, fontsize=18, y=-0.2)
        plt.axis('off')

        
f.savefig(bag_name+'.png')
print(bag_name+'.png' has been generated)
        
bag.close()

  