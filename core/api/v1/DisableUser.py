import logging
from core.lib.error import *
from core.lib.command import Command

class DisableUser(Command):

    # Request Parameter Info 
    req_params = {
        'user_id': ('r', 'str'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        user_mgr = self.locator.getManager('UserManager')

        user_info = user_mgr.disableUser(self.params)

        return user_info.result(self.user_meta['timezone'])
