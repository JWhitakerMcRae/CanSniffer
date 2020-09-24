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
    os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
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
    # Bring CAN0 up
    can_up(baud=args.baud)
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('\n\rCannot find PiCAN board!')
        sys.exit(os.EX_UNAVAILABLE)
    # Sniff loop
    start_time = time.time()
    running = True
    try:
        while running:
            message = bus.recv()    # wait until a message is received.
            c = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
            s=''
            for i in range(message.dlc ):
                s +=  '{0:x} '.format(message.data[i])
            print(' {}'.format(c+s))
            # Check for end of capture period (if set)
            if args.length:
                if time.time() - start_time >= args.length:
                    print("\n\rReached end of capture period.")
                    running = False
    except KeyboardInterrupt:
        print('\n\rKeyboard interrupt detected.')
    except BaseException as err:
        print("\n\rCaugh unknown exception: {}".format(err))
        can_down()
        sys.exit(os.EX_PROTOCOL)
    can_down()
    sys.exit(os.EX_OK)