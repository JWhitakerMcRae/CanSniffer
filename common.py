#!/usr/bin/python3
#
# sniff_can_bus.py
# 
# Script to sniff CAN traffic off the bus and print it to console. BAUD is input
# as a CLI parameter
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 09-24-20 Whitaker McRae
#
#
#
import os
import time


def can_up(baud=500000):
    print("Bringing up CAN0 with BAUD {} ...".format(baud))
    os.system("sudo /sbin/ip link set can0 up type can bitrate {}".format(baud))
    time.sleep(0.1)


def can_down():
    print("Bringing down CAN0 ...")
    os.system("sudo /sbin/ip link set can0 down")
    time.sleep(0.1)


def print_can_msg(msg):
    c = "{:f} | {:08x} | ".format(msg.timestamp, msg.arbitration_id)
    s=""
    for i in range(msg.dlc):
        s +=  "{:02x} ".format(msg.data[i])
    print(" {}".format(c+s))
