from oauth_client import OAuthClient
import logging
import sys
import os

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - ATHERA - %(levelname)s - %(process)d - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

def main():
    client = OAuthClient(
        os.getenv("ATHERA_API_TEST_CLIENT_ID"), 
        os.getenv("ATHERA_API_TEST_CLIENT_SECRET"), 
        idp_url=os.getenv("ATHERA_API_TEST_IDP_URL"), 
    )

    authorize_url = client.authorize()
    logging.info("Please open %s", authorize_url)

    token = client.wait_for_auth()
    if token:
        logging.info("Test succeeded: %s", token)
    else:
        logging.info("Test failed")

    if 'refresh_token' not in token:
        logging.info("No refresh token found")
        return False
    refresh_token = token['refresh_token']
    logging.info("refresh_token: %s", refresh_token)
    token = client.refresh(access_token=token, refresh_token=refresh_token)
    if token:
        logging.info("Refresh succeeded: %s", token)
        logging.info("\n\n%s\n\n", token['access_token'])
        return True
    else:
        logging.info("Refresh failed")
        return False

if __name__ == "__main__":
    setup_logging()
    main()
