"""
A utility to generate a jwt token for use with the Athera API.

ATHERA_API_CLIENT_ID and ATHERA_API_CLIENT_SECRET need to be set in the environment. These are created at:

    https://developer.athera.io/

Run the generate_jwt.sh script to set up the python environment and execute.

Click the provided link to authorize and create a JWT token.
"""
from athera.auth.oauth_client import OAuthClient
import logging
import sys
import os
import json


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - ATHERA - %(levelname)s - %(process)d - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

def refresh_token(client, token):
    refresh_token = token['refresh_token']
    token = client.refresh(access_token=token, refresh_token=refresh_token)
    if token:
        logging.info("Refresh succeeded")
        logging.info("Access token:\n%s\n\n", token['access_token'])
        logging.info("Refresh token:\n%s\n\n", token['refresh_token'])
    else:
        logging.info("Refresh failed")

    return token

def write_to_env(token):
    os.environ["ATHERA_API_TEST_TOKEN"] = token['access_token']
    os.environ["ATHERA_API_TEST_REFRESH_TOKEN"] = token['refresh_token']
    logging.info("Token written to env")

def read_from_env():
    logging.info("Reading token from env")
    return {
        'access_token': os.getenv("ATHERA_API_TEST_TOKEN"),
        'refresh_token': os.getenv("ATHERA_API_TEST_REFRESH_TOKEN")
    }

def write_to_file(token, filename):
    with open(filename, 'w') as f:
        json.dump(token, f)
        logging.info("Token written to file")

def read_from_file(filename):
    logging.info("Reading token from file")
    with open(filename, 'r') as f:
        token = json.load(f)
        return token

def create_client():
    client_id = os.getenv("ATHERA_API_CLIENT_ID")
    client_secret = os.getenv("ATHERA_API_CLIENT_SECRET")

    if not client_id:
        logging.error("ATHERA_API_CLIENT_ID is not set")
        return None
    if not client_secret:
        logging.error("ATHERA_API_CLIENT_SECRET is not set")
        return None
        
    return OAuthClient(
        client_id, 
        client_secret,
        os.getenv("ATHERA_API_IDP_URL", "https://id.athera.io/"), 
        os.getenv("ATHERA_API_IDP_AUDIENCE", "https://public.athera.io")
    )

def main():
    client = create_client()
    if not client:
        sys.exit(2)

    authorize_url = client.authorize()
    logging.info("\n\nPlease open the following URL to complete authentication:\n\n{}\n".format(authorize_url))

    token = client.wait_for_auth()
    if token:
        logging.info("Authentication succeeded: %s", token)
    else:
        logging.info("Authentication failed")
        return

    if 'refresh_token' not in token:
        logging.info("No refresh token found")
        return

    # Demonstrating how to refresh a currently valid token to extend valid period
    refresh_token(client, token)

if __name__ == "__main__":
    setup_logging()
    main()
