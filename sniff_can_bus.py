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
import time
import sys


def can_up(baud=500000):
    print("Bringing up CAN0 with BAUD {} ...".format(baud))
    os.system("sudo /sbin/ip link set can0 up type can bitrate {}".format(baud))
    time.sleep(0.1)


def can_down():
    print("Bringing down CAN0 ...")
    os.system("sudo /sbin/ip link set can0 down")
    time.sleep(0.1)


if __name__ == "__main__":
    print("Starting CAN sniffer ...")
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="CAN sniffer")
    parser.add_argument("-b", "--baud", type=int, help="BAUD rate of CAN bus")
    parser.add_argument("-l", "--length", type=int, help="length to run, in seconds (default: infinite)", default=0) 
    args = parser.parse_args()
    # Bring up CAN0 interface
    can_up(baud=args.baud)
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
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
            message = bus.recv()    # wait until a message is received.
            c = "{:f} | {:08x} | ".format(message.timestamp, message.arbitration_id)
            s=""
            for i in range(message.dlc ):
                s +=  "{:02x} ".format(message.data[i])
            print(" {}".format(c+s))
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
