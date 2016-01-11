import logging
from core.conf import global_conf
from core.lib.system_client import SystemClient
from core.lib.error import *

class Auth:
    
    logger = logging.getLogger('core')

    def verify(self, api_request):
        api_request['meta']['user'] = {}

        if api_request['meta']['sub_module'] in global_conf.NO_AUTH_MODULES:
            return api_request

        elif api_request['meta']['sub_module'] in global_conf.SYSTEM_AUTH_MODULES:
            return self._systemAuth(api_request)

        else:
            if global_conf.AUTH_TYPE == 'xauth':
                return self._xAuth(api_request)

            else:
                return self._noAuth(api_request)

    def _systemAuth(self, api_request):
        if not api_request['params'].has_key('system_key'):
            raise ERROR_AUTH_FAILED(reason = 'Required system key.')

        if api_request['params']['system_key'] != global_conf.SYSTEM_KEY:
            raise ERROR_AUTH_FAILED(auth_type = 'System key is invalid.')

        api_request['meta']['user']['user_id'] = 'system'
        api_request['meta']['user']['permissions'] = '*'
        api_request['meta']['user']['timezone'] = global_conf.DEFAULT_TIMEZONE

        return api_request

    def _xAuth(self, api_request):
        if not api_request['meta'].has_key('xtoken'):
            raise ERROR_AUTH_FAILED(reason = 'Required X-Auth-Token.')

        sc = SystemClient(global_conf.AUTH_HOST)

        req_params = {}
        req_params['system_key'] = global_conf.SYSTEM_KEY
        req_params['token'] = api_request['meta']['xtoken']
        response = sc.request('GET', '/core/v1/token/auth', params=req_params)

        if response['status'] == False:
            raise ERROR_AUTH_FAILED(reason = response['message'])

        api_request['meta']['user'] = response['response']

        return api_request

    def _noAuth(self, api_request):
        api_request['meta']['user']['user_id'] = 'anonymous'
        api_request['meta']['user']['permissions'] = 'all'
        api_request['meta']['user']['timezone'] = global_conf.DEFAULT_TIMEZONE

        return api_request
