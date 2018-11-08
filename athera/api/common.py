"""
Helpers for the Athera API
"""
import os

def headers(group_id, token):
    """
    Generate the headers expected by the Athera API. All queries require the active group, as well as authentication.
    """
    return { 
        "active-group": group_id,
        "Authorization" : "Bearer: {}".format(token) 
    }


def api_debug(func):
    if os.getenv("ATHERA_API_DEBUG"):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            print("Request: {} {} [{}]".format(response.request.method, response.url, response.status_code))
            print("Body: {}".format(response.request.body))
            return response
        return wrapper
    else:
        return func
    