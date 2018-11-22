import os
import logging
import grpc
from athera.auth.oauth_client import OAuthClient, create_oauth_client
from athera.auth.decorators import decorate_all_functions, refresh_token_on_expiry

import io 

from athera.api import apps as api_apps
from athera.api import compute as api_compute
from athera.api import groups as api_groups
from athera.api import sessions as api_sessions
from athera.api import storage as api_storage

@decorate_all_functions(refresh_token_on_expiry)
class APIClient(object):
    """
    Client which encapsulates every api calls.
    This reduces the number of arguments to provide and by default default_group_id for every request.
    You can override the default_group_id by setting the optional argument 'group_id' in the methods.

    Refresh Token feature:
    If you want the token to be automatically refreshed when expired, please set the optional parameter 'refresh_token'.
    When set, before every request we do the following:
        - Is attribute token expired?
            - If so, get a new 'refreshed' token & update the class attribute 'token' with the new refreshed access_token
        - Execute the method you called      
    """

    def __init__(self, token, group_id, refresh_token=None):
        """ 
        'token':  JSON Web Token. See athera.auth.generate_jwt.py on how to generate a JWT.
        'group_id': The defqult group_id to use for the api calls
        'refresh_token': the refresh_token which will be use to refresh the token if expired
        """
        
        self.url = "https://api.athera.io/api/v1"
        self.token = token
        self.group_id = group_id
        
        if refresh_token:
            self.oauth_client = create_oauth_client()
            self.refresh_token =  refresh_token
            if not self.oauth_client :
                raise ValueError("""Could not create oauth client. Make sure that the following environment variables are properly set:
- ATHERA_API_CLIENT_ID
- ATHERA_API_CLIENT_SECRET""")

    # Apps
    def get_app_families(self, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_apps.get_app_families(self.url, group_id, self.token)
    
    def get_app(self, app_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_apps.get_app(self.url, group_id, self.token, app_id)
    
    # Compute
    def get_jobs(self, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_compute.get_jobs(self.url, group_id, self.token)
    
    def get_job(self, job_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_compute.get_job(self.url, group_id, self.token, job_id)

    def create_job(self, payload, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_compute.create_job(self.url, group_id, self.token, payload)

    def stop_job(self, job_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_compute.stop_job(self.url, group_id, self.token, job_id)

    def get_parts(self, job_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_compute.get_parts(self.url, group_id, self.token, job_id)

    def get_part(self, job_id, part_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_compute.get_part(self.url, group_id, self.token, job_id, part_id)

    # Groups
    def get_orgs(self):
        return api_groups.get_orgs(self.url, self.token)

    def get_group(self, group_id):
        return api_groups.get_group(self.url, group_id, self.token, group_id)

    def get_group_children(self, group_id):
        return api_groups.get_group_children(self.url, group_id, self.token, group_id)
    
    def get_group_users(self, job_id, group_id):
        return api_groups.get_group_users(self.url, group_id, self.token, group_id)

    # Sessions
    def get_user_sessions(self, user_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_sessions.get_user_sessions(self.url, group_id, self.token, user_id)

    def get_session(self, session_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_sessions.get_session(self.url, group_id, self.token, session_id)

    def start_session(self, payload, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_sessions.start_session(self.url, group_id, self.token, payload)

    def stop_session(self, session_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_sessions.stop_session(self.url, group_id, self.token, session_id)

    # Storage
    def get_drivers(self, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_storage.get_drivers(self.url, group_id, self.token)

    def get_driver(self, driver_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_storage.get_driver(self.url, group_id, self.token, driver_id)

    def delete_driver(self, driver_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_storage.delete_driver(self.url, group_id, self.token, driver_id)

    def create_driver(self, storage_driver_request, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_storage.create_driver(self.url, group_id, self.token, storage_driver_request)

    def rescan_driver(self, driver_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_storage.rescan_driver(self.url, group_id, self.token, driver_id)
    
    def dropcache_driver(self, driver_id, group_id=None):
        if not group_id:
            group_id =  self.group_id
        return api_storage.dropcache_driver(self.url, group_id, self.token, driver_id)
        