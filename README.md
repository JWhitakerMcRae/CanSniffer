# CanSniffer
Sniffer for CAN bus using the PiCAN2 HAT for the Raspberry Pi 3 B+.

## Prerequisites:
1. Raspberry Pi 3 B+ (should also work with other variants)
1. PiCAN2 HAT (by SK Pang Electronics)
1. Boot from SD card running Raspberry Pi OS (formerly called Raspbian)

## Installation:
1. Ensure Python 3 (and Pip 3) is installed:  
	`sudo apt install python3 python3-pip`
1. Ensure git is installed:  
	`sudo apt install git`
1. Add the following to the /boot/config.txt file and reboot:  
	`dtparam=spi=on`  
	`dtoverlay=mcp2515-can0-overlay,oscillator=16000000,interrupt=25`  
	`dtoverlay=spi-bcm2835-overlay`
1. Clone this repo to your device:  
	`git clone https://github.com/JWhitakerMcRae/CanSniffer.git`  
	`cd ~/CanSniffer`
1. Install required pip packages  
	`pip3 install -r requirements.txt`

## Usage:
1. Capture CAN data for attached bus at baud `<value>`, format is `timestamp | arbitration id | dlc | data bytes`:
	`./sniff_can_bus.py --baud=<value>`

**TIP:** Run `./sniff_can_bus.py --help` to see optional parameters.

Created in part using example code (with the same MIT license) found in:  
[https://github.com/skpang/PiCAN-Python-examples](https://github.com/skpang/PiCAN-Python-examples)

There is also a very cool case designed by [GrodanB](https://www.thingiverse.com/grodanb/designs) that you can 3D print for this project:  
[https://www.thingiverse.com/thing:3409057](https://www.thingiverse.com/thing:3409057)
