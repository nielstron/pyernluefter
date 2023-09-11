#!/usr/bin/env python
# -*- coding: utf-8 -*-

# general requirements
import unittest
from .test_structure.server_control import Server
from .test_structure.bayernluefter_mock_server import BayernLuftHandler, BayernLuftServer

# For the server in this case
import time

# For the tests
import aiohttp
import asyncio
from pyernluefter import Bayernluefter
from .web_raw.web_state import RAW_V1, PROCESSED_V1, RAW_V2, PROCESSED_V2

ADDRESS = 'localhost'


class BayernluefterWebTestRev1(unittest.TestCase):

    server = None
    server_control = None
    port = 0
    url = 'http://localhost:80'
    bayernluefter = None

    def setUp(self):
        # Create an arbitrary subclass of TCP Server as the server to be started
        # Here, it is an Simple HTTP file serving server
        handler = BayernLuftHandler

        max_retries = 10
        r = 0
        while not self.server:
            try:
                # Connect to any open port
                self.server = BayernLuftServer("rev1", (ADDRESS, 0), handler)
            except OSError:
                if r < max_retries:
                    r += 1
                else:
                    raise
                time.sleep(1)

        self.server_control = Server(self.server)
        self.port = self.server_control.get_port()
        self.url = "{}:{}".format(ADDRESS, self.port)
        # Start test server before running any tests
        self.server_control.start_server()

        async def fetch():
            async with aiohttp.ClientSession() as session:
                self.bayernluefter = Bayernluefter(self.url, session)
                await self.bayernluefter.update()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch())

    def test_raw(self):
        self.assertEqual(self.bayernluefter.raw(), RAW_V1)

    def test_raw_converted(self):
        self.assertEqual(self.bayernluefter.raw_converted(), PROCESSED_V1)

    def tearDown(self):
        self.server_control.stop_server()
        pass

class BayernluefterWebTestRev2(unittest.TestCase):

    server = None
    server_control = None
    port = 0
    url = 'http://localhost:80'
    bayernluefter = None

    def setUp(self):
        # Create an arbitrary subclass of TCP Server as the server to be started
        # Here, it is an Simple HTTP file serving server
        handler = BayernLuftHandler

        max_retries = 10
        r = 0
        while not self.server:
            try:
                # Connect to any open port
                self.server = BayernLuftServer("rev2", (ADDRESS, 0), handler)
            except OSError:
                if r < max_retries:
                    r += 1
                else:
                    raise
                time.sleep(1)

        self.server_control = Server(self.server)
        self.port = self.server_control.get_port()
        self.url = "{}:{}".format(ADDRESS, self.port)
        # Start test server before running any tests
        self.server_control.start_server()

        async def fetch():
            async with aiohttp.ClientSession() as session:
                self.bayernluefter = Bayernluefter(self.url, session)
                await self.bayernluefter.update()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch())

    def test_raw(self):
        self.assertEqual(self.bayernluefter.raw(), RAW_V2)

    def test_raw_converted(self):
        self.assertEqual(self.bayernluefter.raw_converted(), PROCESSED_V2)

    def tearDown(self):
        self.server_control.stop_server()
        pass


class NonSyncthruWebTest(unittest.TestCase):

    server = None
    server_control = None
    port = 0
    url = 'http://localhost:80'
    syncthru = None

    def test_no_syncthru(self):
        """Test that an error is thrown when no syncthru is supported"""
        # Create an arbitrary subclass of TCP Server as the server to be started
        # Here, it is an Simple HTTP file serving server
        handler = BayernLuftHandler

        max_retries = 10
        r = 0
        while not self.server:
            try:
                # Connect to any open port
                self.server = BayernLuftServer("rev1", (ADDRESS, 0), handler)
            except OSError:
                if r < max_retries:
                    r += 1
                else:
                    raise
                time.sleep(1)

        self.server_control = Server(self.server)
        self.port = self.server_control.get_port()
        self.url = "{}:{}".format(ADDRESS, self.port)
        # Start test server before running any tests
        self.server_control.start_server()

        # Block server to make sure we get "no support"
        self.server.set_blocked()

        try:
            async def fetch():
                async with aiohttp.ClientSession() as session:
                    self.bayernluefter = Bayernluefter(self.url, session)
                    await self.bayernluefter.update()

            loop = asyncio.get_event_loop()
            loop.run_until_complete(fetch())
            self.fail("No error thrown when noticing that the host does not support Syncthru")
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
