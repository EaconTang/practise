# -*- coding: utf-8 -*-
import fcntl
import socket
import struct

import nmap

SAMPLE_PORTS = "21-23"


def get_interface_status(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_addr = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack("256s", ifname[:15])
    )[20:24])
    nm = nmap.PortScanner()
    nm.scan(ip_addr, SAMPLE_PORTS)
    return nm[ip_addr].state()


if __name__ == '__main__':
    print get_interface_status("eth0")
