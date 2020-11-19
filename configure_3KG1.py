#!/usr/bin/python3
#
# configure_3KG1.py
# 
# Script to conifgure the Grayhill 3KG1 control panel to work with the HiViz
# FireTech BG2 system.
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 11-12-20 Whitaker McRae
#
#
#
import can
import os
import sys
import time

from common import can_up, can_down, print_can_msg


if __name__ == "__main__":
    print("Configuring Grayhill 3KG1 control panel ...")

    # Bring up CAN0 interface at 250kbps
    can_up(baud=250000)
    try:
        bus = can.interface.Bus(channel="can0", bustype="socketcan_native")
    except OSError:
        print("\n\rCannot find PiCAN board!")
        can_down()
        sys.exit(os.EX_UNAVAILABLE)

    # Send out transmission rate update to 150m
    print("Sending transmission rate update to 150ms ...")
    try:
        msg = can.Message(arbitration_id=0x18EF8021, data=[0xE3,0x0F,0x00,0xFF,0xFF,0xFF,0x55,0xAA], is_extended_id=True)
        print_can_msg(msg)
        bus.send(msg)
        time.sleep(0.1)
    except BaseException as err:
        print("\n\rFailed to send transmisison rate update message! Exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)

    print("Successfully configured Grayhill 3KG1 control panel!")
    sys.exit(os.EX_OK)
