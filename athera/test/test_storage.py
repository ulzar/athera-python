from settings import *
from athera.api import storage

import unittest
import uuid
from requests import codes


class StorageTest(unittest.TestCase):
    # User Mounts
    def test_get_user_mounts(self):
        """ Positive test - List the mounts the authenticated user has in this group """
        response = storage.get_user_mounts(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
        )
        self.assertEqual(response.status_code, codes.ok)
        data = response.json()
        mounts = data['mounts'] 
        self.assertNotEqual(len(mounts), 0)
        first_mount = mounts[0]
        self.assertNotEqual(len(first_mount), 0)
        self.assertIn("id", first_mount)

    def test_get_user_mounts_bad_id(self):
        """ Negative test using a random group id """
        response = storage.get_user_mounts(
            environment.ATHERA_API_TEST_BASE_URL,
            str(uuid.uuid4()),
            environment.ATHERA_API_TEST_TOKEN,
        )
        self.assertEqual(response.status_code, codes.forbidden)
        
    def test_get_user_mounts_wrong_id(self):
        """ Negative test to check we handle an existing but inaccessible group in header """
        response = storage.get_user_mounts(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_OTHER_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
        )
        self.assertEqual(response.status_code, codes.forbidden)
        
    # Group Mounts
    def test_get_group_mounts(self):
        """ Positive test """
        response = storage.get_group_mounts(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
        )
        self.assertEqual(response.status_code, codes.ok)
        data = response.json()
        mounts = data['mounts'] 
        self.assertNotEqual(len(mounts), 0)
        first_mount = mounts[0]
        self.assertNotEqual(len(first_mount), 0)
        self.assertIn("id", first_mount)

    def test_get_group_mounts_bad_id(self):
        """
        Negative test using a random group id
        """
        response = storage.get_group_mounts(
            environment.ATHERA_API_TEST_BASE_URL,
            str(uuid.uuid4()),
            environment.ATHERA_API_TEST_TOKEN,
        )
        self.assertEqual(response.status_code, codes.forbidden)
        
    def test_get_group_mounts_wrong_id(self):
        """	Negative test to check we handle an existing but inaccessible group in header """
        response = storage.get_group_mounts(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_OTHER_GROUP_ID,
            environment.ATHERA_API_TEST_TOKEN,
        )
        self.assertEqual(response.status_code, codes.forbidden)
        