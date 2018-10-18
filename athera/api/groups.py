import requests
from athera.common import headers, api_debug

route_orgs           = "/orgs"
route_group          = "/groups/{group_id}"
route_group_children = "/groups/{group_id}/children"
route_group_users    = "/groups/{group_id}/users"


@api_debug
def get_orgs(base_url, token):
    """
    Get all Orgs (top level groups) belonging to the authenticated user. 
    This endpoint does not require the 'active-group' header to be set.
    """
    url = base_url + route_orgs
    response = requests.get(url, headers={ 
        "Authorization" : "Bearer: {}".format(token) 
    })
    return response

@api_debug
def get_group(base_url, group_id, token, target_group_id=None):
    """
    Get a single Group, which must be within the context of the main group.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    Response: [404 Not Found] Incorrect target group
    """
    # If target_group_id is supplied use that, otherwise use the base group
    target = target_group_id if target_group_id else group_id
    url = base_url + route_group.format(group_id=target)
    response = requests.get(url, headers=headers(group_id, token))
    return response

@api_debug
def get_group_children(base_url, group_id, token, target_group_id=None):
    """
    Get the child groups of a single Group, which must be within the context of the main group.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    Response: [404 Not Found] Incorrect target group
    """
    # If target_group_id is supplied use that, otherwise use the base group
    target = target_group_id if target_group_id else group_id
    url = base_url + route_group_children.format(group_id=target)
    response = requests.get(url, headers=headers(group_id, token))
    return response

@api_debug
def get_group_users(base_url, group_id, token, target_group_id=None):
    """
    Get users who belong to a single Group, which must be within the context of the main group.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    Response: [404 Not Found] Incorrect target group
    """
    target = target_group_id if target_group_id else group_id
    url = base_url + route_group_users.format(group_id=target)
    response = requests.get(url, headers=headers(group_id, token))
    return response
