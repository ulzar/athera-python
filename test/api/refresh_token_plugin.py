import os
import os.path
import sys
import logging

from athera.auth.generate_jwt import create_client, refresh_token, read_from_env, write_to_env, read_from_file, write_to_file

from nose2.events import Plugin

class RefreshTokenPlugin(Plugin):
    """
    A Nose2 plugin to perform a token refresh before starting a testing session
    """
    TOKEN_PATH="token.json"
    
    def startTestRun(self, event):
        logging.info("Refreshing token...")
        token = {}
        # Have we an old token on disk?
        if os.path.exists(self.TOKEN_PATH):
            token = read_from_file(self.TOKEN_PATH)
        else:
            # fall back to env
            token = read_from_env()

        if not token:
            logging.info("Token not found")
            sys.exit(3)

        client = create_client()
        if not client:
            logging.info("create_client failed")
            sys.exit(4)

        token = refresh_token(client, token)
        if not token:
            logging.info("refresh_token failed")
            sys.exit(5)

        write_to_env(token)
        write_to_file(token, self.TOKEN_PATH)
