# dylan rodriquez
# listener for kasa by tp link
# if change in initial states then starts discomode
# then continues listening
import asyncio
import random
from kasa import Discover, SmartBulb
from random import choice
from time import sleep

def asyncOn(dev):
    asyncio.run(dev.turn_on())
    asyncio.run(dev.update())

def asyncOff(dev):
    asyncio.run(dev.turn_off())
    asyncio.run(dev.update())


def setState(devices, states):
    for dev in states:
        curdev = states[dev]
        if curdev:
            asyncOn(devices[dev])
        else:
            asyncOff(devices[dev])

def discomode(devicedic):
    for i in range(5):
        rand = {x: bool(random.getrandbits(1)) for x in devicedic}
        print(rand)
        setState(devicedic, rand)
        sleep(.2)



if __name__ == "__main__":
    print('finding devices')

    devices = asyncio.run(Discover.discover())
    devicedic = {}
    for addr, dev in devices.items():
        asyncio.run(dev.update())
        devicedic[dev.alias] = dev 

    print('found devices')

    def listen(initialstates):
        changed = False
        while(not changed):
            sleep(.5)
            curst = {x:devicedic[x].is_on for x in devicedic}
            [asyncio.run(devicedic[x].update()) for x in devicedic]
            if not (initialstates == curst):
                changed = True

    initialstates = {x:devicedic[x].is_on for x in devicedic}
    i = 0
    while True:
        listen(initialstates)
        discomode(devicedic)
        setState(devicedic, initialstates)
        i+=1

