"""Connect to a Bayernluefter."""

import aiohttp
import re
import parse
from http import HTTPStatus

from typing import Any, Dict

from .convert import CONVERSION_DICT

ENDPOINT = "?export=1"
ENDPOINT_TEMPLATE = "export.txt"


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
        url = "{}/{}".format(self.url, ENDPOINT_TEMPLATE)

        try:
            async with self._session.get(url) as response:
                if response.status != HTTPStatus.OK:
                    raise ValueError("Server does not support Bayernluefter protocol.")
                bl_template = await response.text(encoding="ascii", errors="ignore")
            self.template = re.sub(r"~(.+)~", repl_to_parse, bl_template)
        except aiohttp.ClientError:
            raise ValueError("Could not reach the Bayernluefter")

    async def update(self) -> None:
        """
        Retrieve the data from the printer.
        Throws ValueError if host does not support SyncThru
        """
        if self.template is None:
            await self.fetch_template()

        url = "{}{}".format(self.url, ENDPOINT)

        try:
            async with self._session.get(url) as response:
                if response.status != HTTPStatus.OK:
                    raise ValueError("Server does not support Bayernluefter protocol.")
                state = await response.text(encoding="ascii", errors="ignore")
            parse_dict = parse.parse(self.template, state).named
            self.data = {
                key[1:]: value
                for key, value in parse_dict.items()
            }
            self.data_converted = {
                key: CONVERSION_DICT.get(key, str)(value) for key, value in self.data.items()
            }
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
