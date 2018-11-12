""" 
This example will ask for a group, and a Nuke script path in the user's dropbox, then launch a Nuke compute job.

The file must exist in the user's dropbox, and the dropbox must be connected to Athera.
"""

import sys
import time
import common
import uuid
from athera.api import apps, compute, compute_arguments, storage

from six.moves import input

NUKE_COMPUTE_APP_ID="4d6c2992-5bb6-47d8-9464-5f30be969980"
NUKE_SCRIPT_WRITE_NODE="Write1"

# Change the following to the filename of a Nuke script in the root of your dropbox
NUKE_SCRIPT_PATH_WITHIN_DROPBOX="myscript.nk"


def validate_app(logger, base_url, group_id, token, app_id):
    """
    Perform a lookup of the supplied app_id. 

    Return None if not found
    """
    app_response = apps.get_app(base_url, group_id, token, app_id)
    if not app_response:
        return None

    app_dict = common.convert_response(app_response)
    if not app_dict:
        return None

    logger.info("App: {}".format(app_dict))
    return app_dict

def check_dropbox_connected(logger, base_url, group_id, token):
    """
    Get all the user and group storage available for the supplied context (dictated by group_id).

    Iterate through the storage paths looking for a 'Dropbox' type.
    """
    storage_response = storage.get_drivers(base_url, group_id, token)
    storage_dict = common.convert_response(storage_response)

    # response contains a field called 'drivers'
    drivers = storage_dict['drivers']
    dropbox = None
    for d in drivers:
        logger.info("Driver: {:50} {}".format(d['name'], d['id']))
        if d['type'] == "Dropbox":
            dropbox = d
    return dropbox
    
def launch(logger, base_url, group_id, token):
    """
    Run a compute job in the supplied group_id context.

    Compute jobs need 'arguments' to go into the 'payload'. The payload is POSTED to the API to describe the job required.
    """
    # The JWT token contains a user id in its metadata. Lets extract it
    token_helper = common.TokenHelper(token)
    user_id = token_helper.get_user_id()
    logger.info("User ID {}".format(user_id))

    # Use the provided helper functions to create the app specific arguments.
    # These are template parameters which will be swapped for things like start frame, end frame, on multi-part jobs.
    args = compute_arguments.get_nuke_arguments(NUKE_SCRIPT_WRITE_NODE)

    # Make a random job name
    name = "example_" + str(time.time())

    region = common.select_region(logger, "Select a Region to run the compute job in")

    # Next, use the payload helper to build the job request body
    payload = compute.make_job_request(user_id, group_id, NUKE_COMPUTE_APP_ID, "/data/dropbox/{}".format(NUKE_SCRIPT_PATH_WITHIN_DROPBOX), 
        name, 1, 100, 1, region, args)

    # Now its time to actually launch it    
    compute_response = compute.create_job(base_url, group_id, token, payload)
    if compute_response.status_code == 200:
        compute_dict = common.convert_response(compute_response) 
        logger.error("Create job succeeded: {}".format(compute_dict['id']))
        return compute_dict['id']
    else:
        logger.error("Create job failed [{}] {}".format(compute_response.status_code, compute_response.text))
        return None
        


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

    # API calls all need an active group to define the 'Context' of the request. In this case, ask the user for a group, starting with Orgs and walking the context tree
    selector = common.GroupSelector(logger, base_url, token)
    org_id = selector.get_org()
    if not org_id:
        logger.fatal("Failed to get Org")
        sys.exit(2)
    
    leaf_group_id = selector.get_leaf_group(org_id)
    if not leaf_group_id:
        logger.fatal("Failed to get leaf group")
        sys.exit(3)

    # Check provided app ID is valid and available for the selected org - The response is based on active entitlements, so we provide the Org ID, not the child group ID.
    if not validate_app(logger, base_url, org_id, token, NUKE_COMPUTE_APP_ID):
        logger.fatal("Validate app failed")
        sys.exit(4)

    # Check the user has a dropbox mount
    dropbox_driver = check_dropbox_connected(logger, base_url, leaf_group_id, token)
    if not dropbox_driver:
        logger.fatal("Dropbox not connected?")
        sys.exit(5)

    logger.info("Found a dropbox driver with id {}".format(dropbox_driver['id']))
    
    # Ready to go!
    # We're launching the compute job in the leaf group's context, not the ancestor Org.
    job_id = launch(logger, base_url, leaf_group_id, token)

    # Exercise for the reader: Use the compute.get_job function to query for progress of the new job (using job_id)


if __name__=="__main__":
    main()

