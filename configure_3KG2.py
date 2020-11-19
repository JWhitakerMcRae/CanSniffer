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
    [0x13,0x00],    # Button Send On Event = False
    [0x14,0x00],    # Button Transmit Period = 0 (no periodic transmission)
    [0x18,0x00],    # Indicator Status Send On Event = False
    [0x19,0x00],    # Indicator Status Transmit Period = 0 (no periodic transmission)
    [0x1A,0x00],    # Diagnostic Blink Period (disable diagnostic blink on boot)
    [0x1B,0x00],    # LED COMM Timeout Period = 0 (don't blink timeout indicator lights if no CAN traffic)
    [0x26,0x00],    # FLEXIO Config (disable Flex IO 1 and Flex IO 2)
    [0x27,0x00],    # Demo Mode = False (disable demo mode abiliity)
    [0x2A,0x00],    # AUXIO1 Send On Event = False
    [0x2B,0x00])    # AUXIO1 TX Period = 0 (no periodic transmission)


if __name__ == "__main__":
    print("Starting Grayhill config script ...")

    # Bring up CAN0 interface at 250kbps
    can_up(baud=250000)
    try:
        bus = can.interface.Bus(channel="can0", bustype="socketcan_native")
    except OSError:
        print("\n\rCannot find PiCAN board!")
        can_down()
        sys.exit(os.EX_UNAVAILABLE)

    # Send out Address Claim message (with Grayhill mfg code)
    print("Sending address claim message (with Grayhill mfg code) ...")
    try:
        msg = can.Message(arbitration_id=0x18EEFFFD, data=[0x00,0x00,0xC0,0x24,0x00,0x00,0x00,0x00], is_extended_id=True)
        print_can_msg(msg)
        bus.send(msg)
        time.sleep(0.1)
    except BaseException as err:
        print("\n\rFailed to send address claim message (with Grayhill mfg code)! Exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)

    # Send out write configuration message(s)
    print("Sending write configuration message(s) ...")
    try:
        for config_payload in config_payloads :
            msg = can.Message(arbitration_id=0x18EF80FD, data=config_payload, is_extended_id=True)
            print_can_msg(msg)
            bus.send(msg)
            time.sleep(0.1)
    except BaseException as err:
        print("\n\rFailed to send write configuration message(s)! Exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)

    # Send out Address Claim message (with non-Grayhill mfg code)
    print("Sending address claim message (with non-Grayhill mfg code) ...")
    try:
        msg = can.Message(arbitration_id=0x18EEFFFD, data=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00], is_extended_id=True)
        print_can_msg(msg)
        bus.send(msg)
        time.sleep(0.1)
    except BaseException as err:
        print("\n\rFailed to send address claim message (with non-Grayhill mfg code)! Exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)

    # Bring down CAN0 interface before exit
    can_down()
    sys.exit(os.EX_OK)
