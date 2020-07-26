#!/usr/bin/env python3
import shutil
import psutil
import socket

def check_disk_usage(disk):
    du = shutil.disk_usage(disk)
    free = du.free/du.total*100
    return free > 10

def check_no_network():
    """Will attempt to resolve Google's URL and return False if it fails"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True


def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    return usage < 75

if not check_disk_usage("/") or not check_cpu_usage():
    print("Error!")
else:
    print("Everything is ok!")
