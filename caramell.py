#!/usr/bin/env python3

import socket
import argparse
import typing
import time
from phue import Bridge, Group, Light, PhueRegistrationException

parser = argparse.ArgumentParser(description="Control your lights! Party time 🌈")

parser.add_argument('--ip', dest='ip', help='IP of Bridge')
parser.add_argument('--group', dest='group', help='Group of lights targetted for party mode')
parser.add_argument('--debug', dest='debug', action='store_true', help="Enter color debug mode")

def connect(ip: str) -> Bridge:
    if not ip:
        raise ValueError("must include ip of Bridge!")

    try:
        socket.inet_aton(ip)
    except socket.error:
        raise ValueError("must include ip of Bridge!")

    try:
        bridge = Bridge(ip)
    except PhueRegistrationException:
        print("Go press the button on your Bridge!")
    
    return bridge


def get_group_lights(group_name: str) -> list:

    group_id = b.get_group_id_by_name(group_name)

    group = b.groups[group_id - 1]

    return group.lights

def party_time(lights: typing.List[Light]):

    for light in lights:
        light.transitiontime=0.1
    loop = True

    RED = 2000
    CYAN   = 39000
    PURPLE = 55000
    YELLOW = 10000

    hues = [YELLOW, RED, CYAN, PURPLE]

    i = 0

    while loop:
        for light in lights:
            
            light.hue = hues[i % len(hues)]
        i+=1
        time.sleep(0.1)

def debug_color(lights: typing.List[Light]):
    print("Entering debug mode")

    while True:
        try:
            val = int(input("HSV: "))
            for light in lights:
                light.hue = val
        except ValueError:
            pass


if __name__ == "__main__":
    args = parser.parse_args()
    global b
    b = connect(args.ip)

    b.get_group_id_by_name

    if args.group:
        lights: typing.List[Light] = get_group_lights(group_name=args.group)
    elif args.lights:
        lights = args.lights
    else:
        raise ValueError("No lights or groups targetted!")


    if args.debug:
        debug_color(lights)
    else:
        party_time(lights)
