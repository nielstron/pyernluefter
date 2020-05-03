# Pyernluefter - a very basic python Bayernluefter bridge
[![Build Status](https://travis-ci.com/nielstron/pyernluefter.svg?branch=master)](https://travis-ci.com/nielstron/pyernluefter)
[![Coverage Status](https://coveralls.io/repos/github/nielstron/pyernluefter/badge.svg?branch=master)](https://coveralls.io/github/nielstron/pyernluefter?branch=master)
[![Package Version](https://img.shields.io/pypi/v/pyernluefter)](https://pypi.org/project/PySyncThru/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyernluefter.svg)](https://pypi.org/project/PySyncThru/)

A package that connects to the Bayernluefter WiFi-Module.

## Usage

```python
import aiohttp
import asyncio
from pyernluefter import Bayernluefter

IP_BAYERNLUEFTER = '192.168.0.25'

async def main():
    async with aiohttp.ClientSession() as session:
        printer = SyncThru(IP_PRINTER, session)
        await printer.update()

        # Is printer online?
        print("Printer online?:", printer.is_online())
        # Show the printer status
        print("Printer status:", printer.device_status())
        if printer.is_online():
            # Show details about the printer
            print("Printer model:", printer.model())
            # Get the details of a cartridge
            print("Toner Cyan details:", printer.toner_status()['cyan'])
            # Get the details about a tray
            print("Tray 1 Capacity:", printer.input_tray_status()[1]['capa'])
        # Print all available details from the printer
        print("All data:\n", printer.raw())
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Troubleshooting

If the general state of your printer stays at 'Unknown',
it might be the case that the language of your printer is not supported.

Even though officially your language is supported it might be that
some states are not exactly matching the expected states stored in the library.
For this case, have a look at the language support issue template for a detailed how-to on adding support for your printer
or open a general issue.

Current supported languages are: English, Russian, German, French, Italian
