import logging
from core.lib.error import *
from core.lib.command import Command

class DeleteUser(Command):

    # Request Parameter Info 
    req_params = {
        'user_id': ('r', 'str'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        user_mgr = self.locator.getManager('UserManager')

        result = user_mgr.deleteUser(self.params)

        return result
