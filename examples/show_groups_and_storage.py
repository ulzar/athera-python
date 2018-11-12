""" 
We're going to show a hierarchical view of a user's groups, and for each group show ALL the storage sources available, including those provided by ancestors.

Based on Mat's October 2018 webinar.
"""

import sys
import common
from athera.api import apps, groups, storage


class RecursivePrinter(object):
    """
    Starting with the provided group_id, print the storage available, then recurse into children and do the same.
    """
    def __init__(self, logger, base_url, group_id, token, depth=1):
        self.logger = logger
        self.base_url = base_url
        self.group_id = group_id
        self.token = token
        self.depth = depth

        # Do an initial API call to look up information about this group using the group_id.
        group_response = groups.get_group(self.base_url, self.group_id, self.token)
        if group_response.status_code != 200:
            self.logger.error("Failed getting group {}".format(self.group_id))
            return None

        self.group = common.convert_response(group_response)
        self.indented_print("[{}] {} with ID: {} {}".format(self.group['type'], self.group['name'], self.group['id'], self.depth))

    def indented_print(self, s, extra=0):
        """
        Provide some indentation based on tree depth
        """
        this_level = self.depth + extra
    
        if extra == 0:
            self.logger.info('    ' * this_level)
            self.logger.info('=== ' * this_level + s)
        else:
            self.logger.info('    ' * (this_level -1) + '--- ' + s)

        
    def print_storage(self):
        """
        Simply query for storage accessible by this group and print it. Backend supplies storage from the parent group(s) too. 
        """
        storage_response = storage.get_drivers(self.base_url, self.group_id, self.token)
        storage_dict = common.convert_response(storage_response)

        # response contains a field called 'drivers'
        drivers = storage_dict['drivers']
        for d in drivers:
            # Each driver has a mount, describing how the storage resource is mounted in Athera sessions
            mount = d['mounts'][0]
            self.indented_print("{} storage mounted at {} with ID: {}".format(d['name'], mount['mountLocation'], d['id']), 1)
        
    def get_children(self):
        """
        For the current group, fetch the children. We could return the whole objects, but we're just returning the IDs.
        """
        children_response = groups.get_group_children(self.base_url, self.group_id, self.token)
        if children_response.status_code != 200:
            self.logger.error("Failed getting children for group {}".format(self.group_id))
            return None

        children = common.convert_response(children_response)
        if 'groups' not in children:            
            self.logger.error("Missing groups data")
            return None
        
        # json data in contained within the 'groups' object, so extract that
        children = children['groups']

        if len(children) == 0:
            # No children. Its a leaf
            return []
        
        # Return just the ids. This is rather inefficient. How could you improve this?
        return [x['id'] for x in children]

    def __call__(self):
        """
        The class is a functor 
        """
        # Print storage at this level of the tree
        self.print_storage()

        # Get the ids of child groups
        child_group_ids = self.get_children()

        # Recursively repeat
        for group_id in child_group_ids:
            RecursivePrinter(self.logger, self.base_url, group_id, self.token, self.depth+1)()


def main():
    logger = common.setup_logging()
    # What are we going to do?
    logger.info(__doc__)

    # Determine some arguments we need for api calls
    base_url = common.get_base_url()
    token = common.get_token_from_env()
    if not token:
        logger.fatal("ATHERA_API_TOKEN not set in env")
        return 1

    # Show the token expiry
    token_helper = common.TokenHelper(token)
    logger.info("Token expires {}".format(token_helper.get_expiry_string()))

    # API calls all need an active group to define the 'Context' of the request. We only care about the top-level groups, orgs. Ask for user input.
    selector = common.GroupSelector(logger, base_url, token)
    group_id = selector.get_org()
    if not group_id:
        return 2

    # Feed the org id into the class which will recursively walk the Context tree
    RecursivePrinter(logger, base_url, group_id, token)()

        

if __name__=="__main__":
    exit_code = main()
    sys.exit(exit_code)
