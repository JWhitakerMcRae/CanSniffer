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
import argparse
import can
import os
import sys
import time

from common import can_up, can_down, print_can_msg


if __name__ == "__main__":
    print("Starting CAN sniffer ...")

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="CAN sniffer")
    parser.add_argument("-b", "--baud", type=int, help="BAUD rate of CAN bus", default=250000)
    parser.add_argument("-l", "--length", type=int, help="length to run, in seconds (default: infinite)", default=0) 
    args = parser.parse_args()

    # Bring up CAN0 interface
    can_up(baud=args.baud)
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('\n\rCannot find PiCAN board!')
        sys.exit(os.EX_UNAVAILABLE)

    # Sniff loop (infinite or until --length seconds)
    start_time = time.time()
    running = True
    try:
        print(" Timestamp         | ID       | Data ->")
        print("+------------------+----------+------------------------+")
        while running:
            msg = bus.recv()    # wait until a message is received.
            print_can_msg(msg)
            # Check for end of capture period (if set)
            if args.length: # defaults to 0, treated as infinite
                if time.time() - start_time >= args.length:
                    print("\n\rReached end of {} second capture period.".format(args.length))
                    running = False
    except KeyboardInterrupt:
        print("\n\rKeyboard interrupt detected.")
    except BaseException as err:
        print("\n\rCaught unknown exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)

    # Bring down CAN0 interface before exit
    can_down()
    sys.exit(os.EX_OK)
