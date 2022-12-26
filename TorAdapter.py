import pcapy
import subprocess
import logging
import argparse
import time

# Set up logging
logging.basicConfig(filename=
logging.

logging

log
'ip_leak_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--adapter', '-a', help='Network adapter to use', required=True)
parser.add_argument('--filter', '-f', help='Filter to apply to packets', required=True)
parser.add_argument('--disconnect', '-d', help='Action to take when an IP leak is detected',
                    choices=['none', 'wifi'], default='wifi')
args = parser.parse_args()

# Open the network adapter
pcap = pcapy.open_live(args.adapter, 65536, True, 0)

# Set the filter
pcap.setfilter(args.filter)

# Check if an IP leak has occurred
def check_ip_leak(packet_data):
    # Check if the packet contains an IP address that is not a TOR address
    if not packet_data.startswith(b'\x17\x03\x03') and b'\x00\x00\x00\x00' not in packet_data:
        # An IP leak has occurred, disconnect from the Wi-Fi network if specified
        if args.disconnect == 'wifi':
            subprocess.run(['nmcli', 'dev', 'wifi', 'disconnect'])
        logging.warning('IP leak detected!')

# Capture and process packets
def process_packet(hdr, data):
    # Check for an IP leak
    check_ip_leak(data)

# Run the tool continuously
while True:
    pcap.loop(0, process_packet)
