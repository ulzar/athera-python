import unittest
from athera.sync.client import Client
import os
import logging
import sys


from settings import environment, compute_arguments


class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = os.getenv("ATHERA_API_TEST_TOKEN")
        print("token is: {}".format(cls.token))
        url = os.getenv("ATHERA_SYNC_URL", "localhost:9001")
        cls.client = Client(url, cls.token)

    def test_get_mounts(self):
        """ Test we can get groups for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        mounts, err = self.client.get_mounts(
            environment.ATHERA_API_TEST_GROUP_ID,
        )
        print("mounts: {}".format(mounts))


    def test_get_files(self):
        """ Test we can get files for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        filesGenerator = self.client.get_files(
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_GROUP_MOUNT_ID,
            path=""
            )

        for files, err in filesGenerator:
            if err is not None:
                print("Error: {}".format(err))
                break
            print("Files: {}".format(files))

    def test_download_file(self):
        """ Test we can get files for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        with open("titeuf.nk", "w+") as f:
            err = self.client.download_to_file(
                environment.ATHERA_API_TEST_GROUP_ID,
                environment.ATHERA_API_TEST_GROUP_MOUNT_ID,
                f,
                path="titeuf.nk",
                chunk_size=1024
            )
            self.assertIsNone(err, "Got unexpected error: {}".format(err))

    def test_upload_file(self):
        """ Test we can get files for the authenticated user.
        Will only work with Python 2. Python 3 will segfault - TODO check this still applies
        """
        with open("assets/hello.txt", "r") as f:
            response, err = self.client.upload_to_file(
                environment.ATHERA_API_TEST_GROUP_ID,
                environment.ATHERA_API_TEST_GROUP_MOUNT_ID,
                f,
                destination_path="hello_upload.txt",
                chunk_size=5,
            )
            print("Got response: {}".format(response))
            print("Got err: {}".format(err))
        print("Finished Uploading file")

