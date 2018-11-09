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
    formatter = logging.Formatter('%(message)s')
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
    try:
        return response.json()
    except:
        return None



class GroupSelector(object):
    """
    List the groups available to the authenticated user, and ask for numeric selection.
    
    Return the id of that selection.
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

        orgs_dict = convert_response(orgs_response)
        if not orgs_dict or 'groups' not in orgs_dict:            
            self.logger.error("Missing groups data")
            return None
        
        # json data in contained within the 'groups' object, so extract that. A 'pagination' object also exists.
        orgs = orgs_dict['groups']

        # This is technically impossible
        if len(orgs) == 0:
            self.logger.error("No orgs found!")
            return None

        # We have found multiple options so begin the selection process.
        choices = [x['name'] for x in orgs]
        org_index, org_name = SelectionHelper(self.logger, choices, "Select an Org")()
        self.logger.info("Selected {}".format(org_name))
        
        return orgs[org_index]['id']


class SelectionHelper(object):
    """
    Ask user to make a selection from a list of choices, by entering the number of the choice.

    Returns the selected index and choice text.

    Also early returns if the list of choices has a length of 1.

    Class is a functor.
    """
    def __init__(self, logger, choices, question):
        super(SelectionHelper, self).__init__()
        self.logger = logger
        self.choices = choices
        self.question = question
        

    def __call__(self):
        # If there is just a single choice, simply use that.
        if len(self.choices) == 1:
            return 0, self.choices[0]

        # Multple choices available - list them with number indices (one-based for humans)
        self.logger.info("-- {}".format(self.question))
        for i in range(len(self.choices)):
            self.logger.info("{}) {}".format(i + 1, self.choices[i]))   
        
        selection = ""
        while len(selection) < 1:
            i = input("-- ")
            try:
                if int(i) == 0:
                    self.logger.warning("Please enter a number from 1 to {}".format(len(self.choices)))
                    continue
                selection = self.choices[int(i)-1]
            except IndexError:
                # out of range
                self.logger.warning("Invalid choice. Please choose again.")
            except ValueError:
                # non-numeric input
                self.logger.warning("Please enter a number from 1 to {}".format(len(self.choices)))
            
        return int(i)-1, selection
