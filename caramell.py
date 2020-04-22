#!/usr/bin/env python3

import socket
import argparse
import typing
import time
from itertools import cycle
from aioify import aioify
import asyncio

from phue import Bridge, Group, Light, PhueRegistrationException

parser = argparse.ArgumentParser(description="Control your lights! Party time 🌈")

parser.add_argument('--ip', dest='ip', help='IP of Bridge')
parser.add_argument('--group', dest='group', help='Group of lights targetted for party mode')
parser.add_argument('--debug', dest='debug', action='store_true', help="Enter color debug mode")

speed: float = 0.2 # Configurable speed
RED: int = 2000
CYAN: int = 39000
PURPLE: int = 55000
YELLOW: int = 10000

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
        print("Go press the button on your Bridge and try again! Quick!")
    
    return bridge


def get_group_lights(group_name: str) -> list:

    group_id = b.get_group_id_by_name(group_name)

    group = b.groups[group_id - 1] # 1-indexing? In Python?? Good lord...

    return group.lights


async def set_group_hue(lights: typing.List[Light], hue: int):
    ops = list(map(lambda x: b.aio_set_light(x.light_id, 'hue', hue, transitiontime=0.1), lights))

    await asyncio.gather(*ops)


def party_time(lights: typing.List[Light]):

    preflight_command = {
        'transitiontime': speed,
        'on': True,
        'bri': 254,
        'saturation': 254,
        'hue': YELLOW
    }

    for light in lights:
        light.on = preflight_command['on']
        light.transitiontime = preflight_command['transitiontime']
        light.bri = preflight_command['bri']
        light.saturation = preflight_command['saturation']
        light.hue = preflight_command['hue']

    hues: typing.Iterable[int] = iter([YELLOW, RED, CYAN, PURPLE])

    for hue in cycle(hues):
        asyncio.run(set_group_hue(lights, hue))
        time.sleep(speed)

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

    b.aio_set_light = aioify(obj=b.set_light)

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
