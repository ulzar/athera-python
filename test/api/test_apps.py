from settings import environment
from athera.api import apps

import unittest
import uuid
from requests import codes
import os

class AppsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token = os.getenv("ATHERA_API_TEST_TOKEN")
        if not cls.token:
            raise ValueError("ATHERA_API_TEST_TOKEN environment variable must be set")

    def test_get_app_families(self):
        """ Positive test """
        response = apps.get_app_families(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            self.token,
        )
        self.assertEqual(response.status_code, codes.ok)
        data = response.json()
        families = data['families'] 
        self.assertNotEqual(len(families), 0)
        first_family = families[0]
        self.assertNotEqual(len(first_family), 0)
        self.assertIn("id", first_family)

    def test_get_app_families_bad_id(self):
        """ Negative test using a random group id """
        response = apps.get_app_families(
            environment.ATHERA_API_TEST_BASE_URL,
            str(uuid.uuid4()), 
            self.token,
        )
        self.assertEqual(response.status_code, codes.forbidden)
        
    def test_get_app_families_wrong_id(self):
        """ Negative test to check we handle an existing but inaccessible group in header """
        response = apps.get_app_families(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_OTHER_GROUP_ID,
            self.token,
        )
        self.assertEqual(response.status_code, codes.forbidden, "Expected error code FORBIDDEN (403) when providing a wrong family id, Got {}".format(response.status_code))
        

    def test_get_app(self):
        """ Positive test """
        response = apps.get_app(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            self.token,
            environment.ATHERA_API_TEST_INTERACTIVE_APP_ID,
        )
        self.assertEqual(response.status_code, codes.ok)
        app = response.json()
        self.assertIn("id", app)
        self.assertEqual(environment.ATHERA_API_TEST_INTERACTIVE_APP_ID, app['id'])

    def test_get_app_bad_id(self):
        """ Negative test using a random app """
        response = apps.get_app(
            environment.ATHERA_API_TEST_BASE_URL,
            environment.ATHERA_API_TEST_GROUP_ID,
            self.token,
            str(uuid.uuid4()),
        )
        self.assertEqual(response.status_code, codes.not_found)
        