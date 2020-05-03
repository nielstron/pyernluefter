"""
Copyright (c) 2020 Niels Mündler

Licensed under MIT. All rights reserved.
"""
import asyncio

import aiohttp

from pyernluefter import Bayernluefter

IP_Bayernluft = '192.168.0.25'


async def main():
    async with aiohttp.ClientSession() as session:
        luefter = Bayernluefter(IP_Bayernluft, session)
        await luefter.update()

        # Show the luefter status
        print("Bayernluft status:", luefter.raw_converted())

        # turn on
        await luefter.power_on()

        # set fan speed
        await luefter.set_speed(5)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
