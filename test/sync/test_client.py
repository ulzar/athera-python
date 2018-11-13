import unittest
from athera.sync.client import Client
import os
import logging
import sys
import uuid


from settings import environment, compute_arguments


class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environment.ATHERA_API_TEST_TOKEN
        url = environment.ATHERA_API_TEST_SYNC_URL
        if url == "":
            url = "localhost:9001"
        cls.client = Client(url, cls.token)

    def test_get_mounts(self):
        """ Test we can get groups for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        mounts, err = self.client.get_mounts(
            environment.ATHERA_API_TEST_GROUP_ID,
        )
        self.assertIsNone(err, "Got unexpected error: {}".format(err))
        self.assertIsNotNone(mounts, "Expected response not to be None")
        self.assertGreaterEqual(len(mounts), 1, "Expected to get at least 1 mount")


    def test_get_files(self):
        """ Test we can get files for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        filesGenerator = self.client.get_files(
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_GROUP_MOUNT_ID,
            path=""
            )

        for _, err in filesGenerator:
            self.assertIsNone(err, "Got unexpected error: {}".format(err))

    def test_download_file(self):
        """ Test we can get files for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        donwload_path = "downloaded_file.txt"
        with open(donwload_path, "wb+") as f:
            err = self.client.download_to_file(
                environment.ATHERA_API_TEST_GROUP_ID,
                environment.ATHERA_API_TEST_GROUP_MOUNT_ID,
                f,
                path=environment.ATHERA_API_TEST_DONWLOAD_FILE_PATH,
                chunk_size=5
            )
            self.assertIsNone(err, "Got unexpected error: {}".format(err))
        stats = os.stat(donwload_path) 
        self.assertEqual(
            stats.st_size, 
            30, 
            "Expected downloaded file ({}) to contains 30 bytes; It contains instead {} bytes".format(environment.ATHERA_API_TEST_DONWLOAD_FILE_PATH, stats.st_size))

    def test_upload_file(self):
        """ Test we can get files for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        updload_file_name = "uploads/upload_file_" + str(uuid.uuid4()) + ".txt"
        with open(environment.ATHERA_API_TEST_FILE_TO_UPLOAD, "rb") as f:
            response, err = self.client.upload_to_file(
                environment.ATHERA_API_TEST_GROUP_ID,
                environment.ATHERA_API_TEST_GROUP_MOUNT_ID,
                f,
                destination_path=updload_file_name,
                chunk_size=5,
            )
            self.assertIsNone(err, "Got unexpected error: {}".format(err))

