"""Connect to a Bayernluefter."""

import aiohttp
import re
import parse

from typing import Any, Dict

import datetime

ENDPOINT = "?export=1"
ENDPOINT_TEMPLATE = "export.txt"



def repl_to_parse(m: re.Match):
    return "{{{}}}".format(m.group(1))


def construct_url(ip_address: str) -> str:
    """Construct the URL with a given IP address."""
    if "http://" not in ip_address and "https://" not in ip_address:
        ip_address = "{}{}".format("http://", ip_address)
    if ip_address[-1] == "/":
        ip_address = ip_address[:-1]
    return ip_address


class Bayernluefter:
    """Interface to communicate with the Bayernluefter."""

    def __init__(self, ip, session) -> None:
        """Initialize the the printer."""
        self.url = construct_url(ip)
        self._session = session
        self.data = {}  # type: Dict[str, Any]
        self.template = None

    async def fetch_template(self):
        """
        Fetches the template for the export values from the Bayernluefter
        """
        url = "{}{}".format(self.url, ENDPOINT_TEMPLATE)

        try:
            async with self._session.get(url) as response:
                bl_template = await response.text()
            self.template = re.sub(r"~(.+)~", repl_to_parse, bl_template)
        except aiohttp.ClientError:
            raise ValueError("Could not reach the Bayernluefter")

    async def update(self) -> None:
        """
        Retrieve the data from the printer.
        Throws ValueError if host does not support SyncThru
        """
        url = "{}{}".format(self.url, ENDPOINT)

        try:
            async with self._session.get(url) as response:
                state = await response.text()
            self.data = parse.parse(self.template, state)
        except aiohttp.ClientError:
            raise ValueError("Could not reach the Bayernluefter")

    def raw(self) -> Dict:
        """Return all details of the Bayernluefter."""
        try:
            return self.data
        except (KeyError, AttributeError):
            return {}
