import rospy
from geometry_msgs.msg import Twist
import socket

"""
    TODO: senden funzt nicht?
    strg c funzt nicht
"""

rospy.init_node("gamepad_translater", anonymous=True)

localIP     = "0.0.0.0"
localPort   = 44000
bufferSize  = 128

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

rospy.loginfo("UDP Gamepad Receiver server up and listening")


# Listen for incoming datagrams

def convert_to_twist(throttle, steering):

    twist_msg = Twist()
    twist_msg.linear.x = float(throttle)
    twist_msg.linear.y = 0
    twist_msg.linear.z = 0
    twist_msg.angular.x = 0
    twist_msg.angular.y = 0
    twist_msg.angular.z = float(steering)
    
    return twist_msg

# connect to cmd_vel
vel_publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

try:
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode("utf-8")

        clientMsg = "Message from Client: {} ".format(message)

        throttle, steering = message.split(",")
        
        rospy.loginfo(f"throttle={throttle}, steering={steering}")

        twist_msg = convert_to_twist(throttle, steering)
        vel_publisher.publish(twist_msg)
        rospy.loginfo("Published data")

except KeyboardInterrupt:
    print('interrupted!')
    socket.close()


