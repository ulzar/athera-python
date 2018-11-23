""" 
This example will show an implementation on how to copy a local folder to athera.
You will be asked to:
    1) select a destination in Athera to copy the data. This is an Athera mount, associated with a Group context.
    2) provide the path of your local directory you would like to upload.

If there is an error, the program will exit with a specific exit code:
 - "1" - Wrong environment variables
 - "2" - Wrong Input
 - "3" - HTTP error during API call
 - "4" - GRPC error during the API call
 - "5" - Unexpected API result
Tested with Python 3.6.4
"""

import sys
import common

from six.moves import input
from athera.sync import client as sync_client

import os

class FolderSyncer(object):
    def __init__(self, logger, base_url, group_id, token):
        self.logger = logger
        self.base_url = base_url
        self.group_id = group_id
        self.token = token
        self.client = sync_client.Client(common.DEFAULT_REGION, token)


    def upload_folder_to_athera(self, mount_id, local_directory_path):
        ''' This method will list every file at the local_directory_path and then for each,
        it will call the api method athera.sync.upload_file for every file in your local directory
        '''
        
        _, destination_folder = os.path.split(local_directory_path)
        if not destination_folder:
            self.logger.error("Make sure the provided 'local_directory_path' does not end with a '/' or a '\\'")
            sys.exit(2)

        destination_folder = destination_folder + "/"
        self.logger.info("Folder = {}".format(destination_folder))
        for filename in os.listdir(local_directory_path):
                    destination_path = destination_folder + filename
                    filepath = os.path.join(local_directory_path, filename)
                    with open(filepath, "rb") as f:
                        _, err = self.client.upload_file(
                            self.group_id,
                            mount_id,
                            f,
                            destination_path=destination_path,
                        )
                        if err != None:
                            self.logger.error(err)
                            sys.exit(4)

        return destination_folder



def main():
    logger = common.setup_logging()
    # What are we going to do?
    logger.info(__doc__)

    # Determine some arguments we need for API calls
    base_url = common.get_base_url()
    token = common.get_token_from_env()
    if not token:
        logger.fatal("ATHERA_API_TOKEN not set in env")
        sys.exit(1)

    # Show the token expiry
    token_helper = common.TokenHelper(token)
    logger.info("Token expires {}".format(token_helper.get_expiry_string()))

    # API calls all need an active group to define the 'Context' of the request. 
    selector = common.GroupSelector(logger, base_url, token)
    group_id = selector.get_org()
    if not group_id:
        sys.exit(3)

    logger.info("Using group_id {}".format(group_id))

    # Select the destination mount to which the source folder will be uploaded
    selector = common.MountSelector(logger, token)
    
    mounts, err = selector.get_mounts(group_id)
    if err != None:
            logger.error("Failed getting mounts: {}".format(err))
            sys.exit(4)
    if len(mounts) < 1:
        logger.info("No mounts found")
        sys.exit(5)
                   
    selected_mount = selector.select_mount(group_id, "Select the mount on which you would like to upload your folder to", mounts)
    logger.info("Selected mount_id {} ({})".format(selected_mount.id, selected_mount.mount_location))

    destination_folder = input("-- Please provide the absolute path of the local source folder\n")

    if not os.path.isdir(destination_folder):
        logger.info("'{}' is not a valid folder path".format(destination_folder))
        sys.exit(2)


    # Feed this into the class which will query the upload_file endpoint
    folder_syncer = FolderSyncer(logger, base_url, group_id, token)

    # Upload the folder
    remote_folder_name = folder_syncer.upload_folder_to_athera(selected_mount.id, destination_folder)

    logger.info("Successfully uploaded {} to Athera at the location: {}".format(destination_folder, selected_mount.mount_location + "/" + remote_folder_name))

    

if __name__=="__main__":
    main()
