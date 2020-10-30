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


if __name__ == "__main__":
    print("Starting Grayhill read buttons script ...")
    # Bring up CAN0 interface at 250kbps
    can_up(baud=250000)
    try:
        bus = can.interface.Bus(channel="can0", bustype="socketcan_native")
    except OSError:
        print("\n\rCannot find PiCAN board!")
        can_down()
        sys.exit(os.EX_UNAVAILABLE)
    # Send out read Key Press Data message (then wait for a response) in a loop
    running = True
    try:
        while running:
            msg = can.Message(arbitration_id=0x18EA00FD, data=[0x00,0x00,0x00], is_extended_id=True)
            print_can_msg(msg)
            bus.send(msg)
            msg = bus.recv()    # wait until a message is received.
            print_can_msg(msg)
    except KeyboardInterrupt:
        print("\n\rKeyboard interrupt detected.")
    except BaseException as err:
        print("\n\rCaught unknown exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)
    # Bring down CAN0 interface before exit
    can_down()
    sys.exit(os.EX_OK)