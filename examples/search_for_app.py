""" 
This example will ask you to select an Org, then a string, searching for all App families which contain that string in their name.

Only App families for which the Org has an active entitlement are shown.

It then prints the contained app versions with their type (interactive/compute) and app id.

These app ids can be used during sessions.start_session and compute.make_job_request.

Tested with Python 2.7.15, 3.7.1.
"""

import sys
import common
from athera.api import apps

from six.moves import input


class AppSearcher(object):
    def __init__(self, logger, base_url, group_id, token):
        self.logger = logger
        self.base_url = base_url
        self.group_id = group_id
        self.token = token


    def search_families(self, target):
        self.logger.info("Searching families for {}".format(target))

        apps_response = apps.get_app_families(self.base_url, self.group_id, self.token)
        apps_dict = common.convert_response(apps_response)
        if not apps_dict or 'families' not in apps_dict:
            return None

        # response contains one field:
        # 'families'

        apps_list = apps_dict['families']
        # Filter the whole list with the supplied search term, case-insensitive
        return list(filter(lambda x:target.lower() in x['name'].lower(), apps_list))


def main():
    logger = common.setup_logging()
    # What are we going to do?
    logger.info(__doc__)

    # Determine some arguments we need for api calls
    base_url = common.get_base_url()
    token = common.get_token_from_env()
    if not token:
        logger.fatal("ATHERA_API_TOKEN not set in env")
        sys.exit(1)

    # API calls all need an active group to define the 'Context' of the request. We only care about the top-level groups, orgs. Ask for user input.
    selector = common.GroupSelector(logger, base_url, token)
    group_id = selector.get_org()
    if not group_id:
        sys.exit(2)

    # Feed this into the class which will query the app_families endpoint
    searcher = AppSearcher(logger, base_url, group_id, token)

    # Fetch the search term
    target = input("-- Enter the app name (or part of) to search for: ")

    # Run the search
    families = searcher.search_families(target)

    # List comprehension to filter bundled. Bundled apps are legacy and should not be used
    result = list(filter(lambda f: 'Bundled' not in f['name'], families))

    if len(result) == 0:
        logger.info("-- No apps found (bundled apps are ignored)")

    # Pretty-print the output
    for f in result:
        logger.info("{:50} {}".format(f['name'], f['id']))
        if 'apps' not in f:
            logger.error("Missing apps data")
            continue

        apps = f['apps']
        interactive_app = apps['interactive'] if 'interactive' in apps else None
        compute_app = apps['compute'] if 'compute' in apps else None
        if interactive_app:
            for k, v in interactive_app.items():
                logger.info("-- interactive {:35} {}".format(k, v))
        if compute_app:
            for k, v in compute_app.items():
                logger.info("-- compute     {:35} {}".format(k, v))
        

if __name__=="__main__":
    main()