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
