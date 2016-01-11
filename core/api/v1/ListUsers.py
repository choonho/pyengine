import logging
from core.lib.error import *
from core.lib.command import Command

class ListUsers(Command):

    # Request Parameter Info
    req_params = {
        'user_id': ('o', 'str'),
        'state': ('o', 'str'),
        'search': ('o', 'list'),
        'sort': ('o', 'dic'),
        'minimal': ('o', 'bool'),
    }
    
    def __init__(self, api_request):
        super(self.__class__, self).__init__(api_request)

    def execute(self):
        search = self.makeSearch('user_id', 'state')
        sort = self.makeSort('id')
        minimal = self.makeMinimal()

        user_mgr = self.locator.getManager('UserManager')

        (user_infos, total_count) = user_mgr.listUsers(search, sort, minimal)

        response = {}
        response['total_count'] = total_count
        response['results'] = []

        for user_info in user_infos:
            response['results'].append(user_info.result(self.user_meta['timezone']))

        return response
