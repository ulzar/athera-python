"""
A collection of functions and helpers common to multiple examples
"""

import os
import json
import logging

from six.moves import input

from athera.api import groups


def setup_logging():
    """
    Python needs too many lines of code to get a sensible log output
    """
    logger = logging.getLogger('athera-python')
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


def get_token_from_env():
    """
    See README.md for details on creating a token
    """
    return os.getenv("ATHERA_API_TOKEN")


def get_base_url():
    """ 
    Provided as an argument to api calls to aid future expansion
    """
    return "https://api.athera.io/api/v1/"
    

def convert_response(response):
    """
    json -> dict
    """
    return response.json()



class GroupSelector(object):
    """
    List the groups available to the authenticated user, and ask for selection.
    Return the id of that selection
    """
    def __init__(self, logger, base_url, token):
        super(GroupSelector, self).__init__()
        self.logger = logger
        self.base_url = base_url
        self.token = token
    
    def get_org(self):
        self.logger.info("Getting orgs for user")
        orgs_response = groups.get_orgs(self.base_url, self.token)
        if orgs_response.status_code != 200:
            self.logger.error("Failed getting orgs")
            return None

        orgs = convert_response(orgs_response)
        if 'groups' not in orgs:            
            self.logger.error("Missing groups data")
            return None
        
        # json data in contained within the 'groups' object, so extract that
        orgs = orgs['groups']

        choices = [x['name'] for x in orgs]
        org_index, org_name = SelectionHelper(self.logger, choices, "Select an Org")()
        self.logger.info("Selected {}".format(org_name))
        
        return orgs[org_index]['id']


class SelectionHelper(object):
    """
    Ask user to make a selection from a list of choices.

    Returns the selected index and choice text.

    Class is a functor.
    """
    def __init__(self, logger, choices, question):
        super(SelectionHelper, self).__init__()
        self.logger = logger
        self.choices = choices
        self.question = question
        

    def __call__(self):
        for i in range(len(self.choices)):
            self.logger.info("{} {}".format(i, self.choices[i]))   
        
        selection = ""
        while len(selection) < 1:
            i = input(self.question + ": ")
            try:
                selection = self.choices[int(i)]
            except IndexError:
                # out of range
                pass
            except ValueError:
                # non-numeric input
                pass
            
        return int(i), selection
