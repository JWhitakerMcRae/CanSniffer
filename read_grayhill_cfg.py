#!/usr/bin/python3
#
# grayhill_cfg.py
# 
# Configure a Grayhill controller via CAN.
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 10-29-20 Whitaker McRae
#
#
#
import can
import sys
import time
import os

from common import can_up, can_down, print_can_msg


config_payloads = (
    [0x13],    # Button Send On Event
    [0x14],    # Button Transmit Period
    [0x18],    # Indicator Status Send On Event
    [0x19],    # Indicator Status Transmit Period
    [0x1A],    # Diagnostic Blink Period
    [0x1B],    # LED COMM Timeout Period
    [0x26],    # FLEXIO Config
    [0x27],    # Demo Mode
    [0x2A],    # AUXIO1 Send On Event
    [0x2B])    # AUXIO1 TX Period


if __name__ == "__main__":
    print("Starting Grayhill read config script ...")
    # Bring up CAN0 interface at 250kbps
    can_up(baud=250000)
    try:
        bus = can.interface.Bus(channel="can0", bustype="socketcan_native")
    except OSError:
        print("\n\rCannot find PiCAN board!")
        can_down()
        sys.exit(os.EX_UNAVAILABLE)
    # Send out Address Claim message
    print("Sending address claim message ...")
    try:
        msg = can.Message(arbitration_id=0x18EEFFFD, data=[0x00,0x00,0xC0,0x24,0x00,0x00,0x00,0x00], is_extended_id=True)
        print_can_msg(msg)
        bus.send(msg)
        time.sleep(0.1)
    except BaseException as err:
        print("\n\rFailed to send address claim message! Exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)
    # Send out write configuration message(s)
    print("Sending read configuration message(s) ...")
    try:
        for config_payload in config_payloads :
            msg = can.Message(arbitration_id=0x18EF80FD, data=config_payload, is_extended_id=True)
            print_can_msg(msg)
            bus.send(msg)
            msg = bus.recv()    # wait until a message is received.
            print_can_msg(msg)
    except BaseException as err:
        print("\n\rFailed to send read configuration message(s)! Exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)
    # Bring down CAN0 interface before exit
    can_down()
    sys.exit(os.EX_OK)