import requests
from athera.common import headers, api_debug

route_app_families = "/families"
route_app          = "/apps/{app_id}"

@api_debug
def get_app_families(base_url, group_id, token):
    """
    App Families represent high-level products, eg Nuke. This endpoint only returns app families for which the authenticated user has an active Entitlement.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    """
    url = base_url + route_app_families
    response = requests.get(url, headers=headers(group_id, token))
    return response

@api_debug
def get_app(base_url, group_id, token, app_id):
    """
    Apps are children of App Families and are either 'interactive' or 'compute'. They normally have a minor version like 11.2v3.
    Response: [403 Forbidden] Incorrect or inaccessible group_id
    Response: [404 Not Found] Incorrect app_id
    """
    url = base_url + route_app.format(app_id=app_id)
    response = requests.get(url, headers=headers(group_id, token))
    return response


