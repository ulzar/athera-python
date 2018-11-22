""" 
This example will show you how to use the APIClient.

In this example, we only use get_orgs() method just because the goal is to show you how to instanciate & use the APIClient.
If you provide a refresh_token during the class instanciation, any expired token will be refreshed BEFORE performing the api call.
"""

import os
from athera.api import APIClient
import sys
import common


def main():
    logger = common.setup_logging()
    # What are we going to do?
    logger.info(__doc__)

    # Note: Please provide an expired token (var env 'ATHERA_API_TOKEN').
    token = common.get_token_from_env()
    if not token:
        logger.fatal("ATHERA_API_TOKEN not set in env")
        sys.exit(1)
    
    refresh_token = common.get_refresh_token_from_env()
    if not token:
        logger.fatal("ATHERA_API_REFRESH_TOKEN not set in env")
        sys.exit(1)
    
    # We are not using the group_id because get_orgs() does not need the group_id
    group_id = ''

    # By providing the optional parameter 'refresh_token', it will automatically refresh the token if it is expired.
    api_client = APIClient(token, group_id, refresh_token=refresh_token)
   
    logger.info("First API call 'get_orgs': using token: {}".format(api_client.token))
    res = api_client.get_orgs()
    logger.info("Resp: {}".format(res))
    logger.info("Data: {}".format(res.json()))

    # Note: If ATHERA_API_TOKEN was expired, you will see that api_client.token has been refreshed.
    logger.info("Second API call 'get_orgs': using token: {}".format(api_client.token))
    res = api_client.get_orgs()
    logger.info("Resp: {}".format(res))
    logger.info("Data: {}".format(res.json()))

if __name__=="__main__":
    main()
