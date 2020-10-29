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

from common import can_up, can_down


SOURCE_ADDR = 0xFD
MFG_CODE = 0x126

DISABLE_LED_COMM_TIMEOUT = True


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
    # Send out Address Claim message
    print("Sending address claim message ...")
    try:
        msg = can.Message(arbitration_id=0x18EEFFFD, data=[0x00,0x00,0xC0,0x24,0x00,0x00,0x00,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
    except BaseException as err:
        print("\n\rFailed to send address claim message! Exception: {}".format(err))
        can_down()
        sys.exit(os.EX_UNAVAILABLE)
    # Send out write configuration message(s)
    print("Sending write configuration message(s) ...")
    try:
        # Button Send On Event = False
        msg = can.Message(arbitration_id=0x18EF80FD, data=[0x13,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
        # Button Transmit Period = 0 (no periodic transmission)
        msg = can.Message(arbitration_id=0x18EF80FD, data=[0x14,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
        # Indicator Status Send On Event = False
        msg = can.Message(arbitration_id=0x18EF80FD, data=[0x18,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
        # Indicator Status Transmit Period = 0 (no periodic transmission)
        msg = can.Message(arbitration_id=0x18EF80FD, data=[0x19,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
        if DISABLE_LED_COMM_TIMEOUT:
            # LED COMM Timeout Period = 0 (don't blink timeout indicator lights if no can traffic)
            msg = can.Message(arbitration_id=0x18EF80FD, data=[0x19,0x00], is_extended_id=False)
            bus.send(msg)
            time.sleep(0.1)
        # Demo Mode = False (disable demo mode abiliity)
        msg = can.Message(arbitration_id=0x18EF80FD, data=[0x27,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
        # AUXIO1 Send On Event = False
        msg = can.Message(arbitration_id=0x18EF80FD, data=[0x2A,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
        # AUXIO1 TX Period = 0 (no periodic transmission)
        msg = can.Message(arbitration_id=0x18EF80FD, data=[0x2B,0x00], is_extended_id=False)
        bus.send(msg)
        time.sleep(0.1)
    except BaseException as err:
        print("\n\rFailed to send write configuration message(s)! Exception: {}".format(err))can_down()
        can_down()
        sys.exit(os.EX_UNAVAILABLE)
    # Bring down CAN0 interface before exit
    can_down()
    sys.exit(os.EX_OK)
