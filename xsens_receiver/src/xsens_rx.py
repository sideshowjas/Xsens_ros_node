#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib
#roslib.load_manifest('learning_tf')
import tf
#from std_msgs.msg import String
#from idress_msgs.msg import xsens_mvn 
#from idress_msgs.msg import xsens_sensor

from xsens_receiver.msg import xsens_data
import socket
import struct
import signal
import sys

#UDP_IP = "192.168.1.101"
UDP_IP = "192.168.5.206"
UDP_PORT = 9764

if __name__ == '__main__':
#    mymsg = xsens_mvn()
    #mymsg.xsensor=xsens_sensor(17)


    mymsg = xsens_data()
    pub = rospy.Publisher('xsens_data', xsens_data, queue_size=10)

    rospy.init_node('Xsens_RX', anonymous=True)
    rate = rospy.Rate(1000) # 10hz
    sock = socket.socket(socket.AF_INET,
    					 socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    #br = tf.TransformBroadcaster()
    print "xsens topic active"
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #print "received message:", len(data)," ","\n",
        if len(data) == 760:
            #mymsg.ID = data[0:6] #MXTP01
            ID = struct.unpack('!I',data[6:10])[0] #ID
            UDP_counter = struct.unpack('!B',data[10])[0] #datagram counter
            item_number = struct.unpack('!B',data[11])[0] #number of item
            # print struct.unpack('!B',data[11])[0] #number of item
            time_code = struct.unpack('!I',data[12:16])[0] #time code
            character_ID = struct.unpack('!B',data[16])[0] #character ID
            # 7 chars reserved [17:24]
            #segement = ["s","head",""]
            try:
                timeNow=rospy.Time.now()
                for i in range(0,23):
                    strstep = i*32
                    mymsg.segment_ID = struct.unpack('!I',data[strstep+24:strstep+28])[0] #segment ID
                    mymsg.x_pos = struct.unpack('!f',data[strstep+28:strstep+32])[0] #x pos
                    mymsg.y_pos = struct.unpack('!f',data[strstep+32:strstep+36])[0] #y pos
                    mymsg.z_pos = struct.unpack('!f',data[strstep+36:strstep+40])[0] #z pos
                    mymsg.q1_rot = struct.unpack('!f',data[strstep+40:strstep+44])[0] #q1 rot (re)
                    mymsg.q2_rot = struct.unpack('!f',data[strstep+44:strstep+48])[0] #q2 rot (i)
                    mymsg.q3_rot = struct.unpack('!f',data[strstep+48:strstep+52])[0] #q3 rot (j)
                    mymsg.q4_rot = struct.unpack('!f',data[strstep+52:strstep+56])[0] #q4 rot (k)
                    
                    
                    print mymsg
                    #hello_str = "hello world %s" % rospy.get_time()
                    pub.publish(mymsg)
                    #br.sendTransform((x_pos, y_pos, z_pos),
#                    tf.transformations.quaternion_from_euler(1,0,0),
                    #tf.transformations.quaternion_from_euler(q3_rot,q2_rot, q1_rot),
                    #(q2_rot, q3_rot, q4_rot, q1_rot),
                    #timeNow,str(segment_ID),"world")
                    #timeNow,str(segment_ID),"xsens_parent")
                rate.sleep()
            except rospy.ROSInterruptException:
                pass
#            except KeyboardInterupt:
#                sys.exit()

