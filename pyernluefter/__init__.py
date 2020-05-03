"""Connect to a Bayernluefter."""

import aiohttp
import re
import parse
from http import HTTPStatus

from typing import Any, Dict

from .convert import CONVERSION_DICT

ENDPOINT_EXPORT = "?export=1"
ENDPOINT_TEMPLATE = "/export.txt"
ENDPOINT_POWER_ON = "?power=on"
ENDPOINT_POWER_OFF = "?power=off"
ENDPOINT_BUTTON_POWER = "?button=power"
ENDPOINT_BUTTON_TIMER = "?button=timer"
ENDPOINT_SPEED = "?speed={}"


def repl_to_parse(m: re.Match):
    # prepend a v s.t. no variable begins with an underscore
    return "{{v{}}}".format(m.group(1))


def construct_url(ip_address: str) -> str:
    """Construct the URL with a given IP address."""
    if "http://" not in ip_address and "https://" not in ip_address:
        ip_address = "{}{}".format("http://", ip_address)
    ip_address = ip_address.rstrip("/")
    return ip_address


class Bayernluefter:
    """Interface to communicate with the Bayernluefter."""

    def __init__(self, ip, session: aiohttp.ClientSession) -> None:
        """Initialize the the printer."""
        self.url = construct_url(ip)
        self._session = session
        self.data = {}  # type: Dict[str, Any]
        self.data_converted = {}  # type: Dict[str, Any]
        self.template = None

    async def fetch_template(self):
        """
        Fetches the template for the export values from the Bayernluefter
        """

        bl_template = await self._request_bl(ENDPOINT_TEMPLATE)
        self.template = re.sub(r"~(.+)~", repl_to_parse, bl_template)

    async def update(self) -> None:
        """
        Retrieve the data from the printer.
        Throws ValueError if host does not support SyncThru
        """
        if self.template is None:
            await self.fetch_template()

        state = await  self._request_bl(ENDPOINT_EXPORT)
        parse_dict = parse.parse(self.template, state).named
        self.data = {
            key[1:]: value
            for key, value in parse_dict.items()
        }
        self.data_converted = {
            key: CONVERSION_DICT.get(key, str)(value) for key, value in self.data.items()
        }

    async def _request_bl(self, target):
        url = "{}{}".format(self.url, target)
        try:
            async with self._session.get(url) as response:
                if response.status != HTTPStatus.OK:
                    raise ValueError("Server does not support Bayernluefter protocol.")
                return await response.text(encoding="ascii", errors="ignore")
        except aiohttp.ClientError:
            raise ValueError("Could not reach the Bayernluefter")

    def raw(self) -> Dict:
        """Return all details of the Bayernluefter."""
        try:
            return self.data
        except (KeyError, AttributeError):
            return {}

    def raw_converted(self) -> Dict:
        """Return all details of the Bayernluefter, converted"""
        try:
            return self.data_converted
        except (KeyError, AttributeError):
            return {}

    async def power_on(self):
        await self._request_bl(ENDPOINT_POWER_ON)

    async def power_off(self):
        await self._request_bl(ENDPOINT_POWER_OFF)

    async def power_toggle(self):
        await self._request_bl(ENDPOINT_BUTTON_POWER)

    async def timer_toggle(self):
        await self._request_bl(ENDPOINT_BUTTON_TIMER)

    async def reset_speed(self):
        await self._request_bl(ENDPOINT_SPEED.format(0))

    async def set_speed(self, level:int):
        assert 1 <= level <= 10, "Level must be between 1 and 10"
        await self._request_bl(ENDPOINT_SPEED.format(level))
