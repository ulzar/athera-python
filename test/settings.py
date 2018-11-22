import os
import sys

# Allow imports from project root
current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))

if root_dir not in sys.path:
    sys.path.append(root_dir)

compute_arguments    = ("--help",)

keys = (
    "ATHERA_API_TEST_INTERACTIVE_APP_ID",
    "ATHERA_API_TEST_COMPUTE_APP_ID",
    "ATHERA_API_TEST_COMPUTE_FILE_PATH",
    "ATHERA_API_TEST_TOKEN",
    "ATHERA_API_TEST_REFRESH_TOKEN",
    "ATHERA_API_TEST_BASE_URL",
    "ATHERA_API_TEST_SYNC_URL",
    "ATHERA_API_TEST_REGION",
    "ATHERA_API_TEST_DONWLOAD_FILE_PATH",

    "ATHERA_API_TEST_GROUP_ID",
    "ATHERA_API_TEST_OTHER_GROUP_ID",
    "ATHERA_API_TEST_USER_ID",
    "ATHERA_API_TEST_OTHER_USER_ID",
    "ATHERA_API_TEST_SESSION_ID",
    "ATHERA_API_TEST_OTHER_SESSION_ID",

    "ATHERA_API_TEST_JOB_ID",
    "ATHERA_API_TEST_PART_ID",
    "ATHERA_API_TEST_OTHER_JOB_ID",
    "ATHERA_API_TEST_OTHER_PART_ID",
    "ATHERA_API_TEST_OTHER_JOB_GROUP_ID",

    "ATHERA_API_TEST_USER_MOUNT_ID",
    "ATHERA_API_TEST_OTHER_USER_MOUNT_ID",
    "ATHERA_API_TEST_GROUP_MOUNT_ID",
    "ATHERA_API_TEST_OTHER_GROUP_MOUNT_ID",
    "ATHERA_API_TEST_ORG_DRIVER_ID",
    "ATHERA_API_TEST_HOME_DRIVER_ID",
    "ATHERA_API_TEST_GROUP_MOUNT_LOCATION",
    "ATHERA_API_TEST_GCS_BUCKET_ID",
    "ATHERA_API_TEST_GCS_CLIENT_SECRET",
    "ATHERA_API_TEST_LOCAL_ASSETS_FOLDER",
    "ATHERA_API_TEST_REMOTE_ASSETS_MOUNT_ID",
    "ATHERA_API_TEST_REMOTE_ASSETS_FOLDER",
)

class Environment(object):
    def __init__(self, keys):
        for k in keys:
            # Expect an exception if not set
            v = os.environ[k]
            self.__setattr__(k, v)

    def __getattr__(self, name):
        return self[name]

environment = Environment(keys)
