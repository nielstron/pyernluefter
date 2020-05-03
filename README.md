# Pyernluefter - a very basic python Bayernluefter bridge
[![Build Status](https://travis-ci.com/nielstron/pyernluefter.svg?branch=master)](https://travis-ci.com/nielstron/pyernluefter)
[![Coverage Status](https://coveralls.io/repos/github/nielstron/pyernluefter/badge.svg?branch=master)](https://coveralls.io/github/nielstron/pyernluefter?branch=master)
[![Package Version](https://img.shields.io/pypi/v/pyernluefter)](https://pypi.org/project/PySyncThru/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyernluefter.svg)](https://pypi.org/project/PySyncThru/)

A package that connects to the Bayernluefter WiFi-Module.
It controls the module via the simple web-based access provided by the Bayernluft software.
Any templates module should be supported as the tool first fetches the uploaded template and then parses
the exported data based on the template.

## Usage

```python
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
```
