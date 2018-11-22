from settings import environment
from athera.api import APIClient
import unittest
import uuid
from requests import codes
import os

class APIClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # environment.ATHERA_API_TEST_TOKEN is not refreshed by the refresh_token plugin and thus contains an expired token.
        cls.token = environment.ATHERA_API_TEST_TOKEN
        if not cls.token:
            raise ValueError("ATHERA_API_TEST_TOKEN environment variable must be set")

    def test_get_orgs_with_expired_token(self):
        """ Negative test  
        We are using an expired token.
        We Expect 401 - UNAUTHORIZED
        """
        # We want to use an expired token
        api_client = APIClient(self.token, environment.ATHERA_API_TEST_GROUP_ID)

        response = api_client.get_orgs()
        self.assertEqual(response.status_code, codes.unauthorized)

    def test_get_orgs_with_expired_token_with_refresh_token(self):
        """ Negative test  
        We provided the refresh_token whilst instanciating the Client class so we expect the token to be automatically refreshed.
        Even though the provided token is expired, we are expected status code 200.
        """
        refresh_token = os.getenv("ATHERA_API_TEST_REFRESH_TOKEN")
        api_client = APIClient(self.token, environment.ATHERA_API_TEST_GROUP_ID, refresh_token=refresh_token)

        # First call. attribute 'token' of api_client contains an expired token. 
        response = api_client.get_orgs()
        self.assertEqual(response.status_code, codes.ok)
        refreshed_token = api_client.token  # sync_client.token should contain the new refreshed token
        self.assertNotEqual(refreshed_token, self.token)

        # Second call. attribute 'token' of api_client contains a refreshed token

        response = api_client.get_orgs()
        self.assertEqual(response.status_code, codes.ok)
        self.assertEqual(refreshed_token, self.token)  # the refreshed_token should be valid for this second call so we don't expect it to be refreshed again.

