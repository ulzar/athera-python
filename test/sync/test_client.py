import unittest
from athera.sync.client import Client
import os
import logging

class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = os.getenv("ATHERA_API_TEST_TOKEN")
        url = os.getenv("ATHERA_SYNC_URL", "localhost:9001")
        cls.client = Client(url)

    def test_get_mounts(self):
        """ Test we can get groups for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        groups = self.client.get_groups(self.token)
        logging.debug(groups)

