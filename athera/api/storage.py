import requests
from athera.api.common import headers, api_debug

route_user_mounts  = "/storage/user/mounts"
route_user_mount   = "/storage/user/mounts/{mount_id}"
route_group_mounts = "/storage/group/mounts"
route_group_mount  = "/storage/group/mounts/{mount_id}"

# User mounts
@api_debug
def get_user_mounts(base_url, group_id, token):
    """
    Get all user storage mounts assigned to the authenticated user. User mounts are things like /home and Dropbox, and are mounted into all a users sessions, irrespective of context.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    """
    url = base_url + route_user_mounts
    response = requests.get(url, headers=headers(group_id, token))
    return response

@api_debug
def reindex_user_mount_cache(base_url, group_id, token, mount_id):
    """
    Reindex the cache of a single user storage mount, useful to pull in changes to an external bucket or across regions.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    Response: [404 Not Found] Incorrect mount_id
    """
    url = base_url + route_user_mount.format(mount_id=mount_id)
    response = requests.post(url, headers=headers(group_id, token))
    return response

# Group Mounts
@api_debug
def get_group_mounts(base_url, group_id, token):
    """
    Get all group storage mounts assigned to the provided Group. Group mounts (eg /data/org), and are mounted based on session context.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    """
    url = base_url + route_group_mounts
    response = requests.get(url, headers=headers(group_id, token))
    return response

@api_debug
def reindex_group_mount_cache(base_url, group_id, token, mount_id):
    """
    Reindex the cache of a single group storage mount
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    Response: [404 Not Found] Incorrect mount_id
    """
    url = base_url + route_group_mount.format(mount_id=mount_id)
    response = requests.post(url, headers=headers(group_id, token))
    return response



