import logging
from core.lib.error import *
from core.plugin import Plugin
from core.lib.system_client import SystemClient
from core.conf import plugin_conf

class EventPlugin(Plugin):

    def preload(self, api_request):
        api_class = api_request['meta']['api_class']
        if plugin_conf.EVENT_INFO.has_key(api_class):
            event = Event()
            event.start(api_request, plugin_conf.EVENT_INFO[api_class])

            api_request['meta']['plugin']['event'] = event

        return api_request

    def success(self, api_request, result):
        if api_request['meta']['plugin'].has_key('event'):
            api_request['meta']['plugin']['event'].success()

        return result

    def error(self, api_request, error):
        if api_request['meta']['plugin'].has_key('event'):
            api_request['meta']['plugin']['event'].error(error)


class Event:
    
    logger = logging.getLogger('core')
    sc = SystemClient(plugin_conf.STORE_HOST)

    def start(self, api_request, event_info):
        if api_request['params'].has_key(event_info[1]):
            self.logger.debug(event_info[0] %(api_request['params'][event_info[1]]))

    def update(self):
        self.logger.debug('Update Event')
        pass

    def success(self):
        self.logger.debug('Success Event')
        pass

    def error(self, error):
        self.logger.debug(error.message['message'])
        pass
