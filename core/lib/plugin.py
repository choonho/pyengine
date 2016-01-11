import traceback, logging
from core.lib.error import *
from core.conf import plugin_conf

class Plugin:
    logger = logging.getLogger('core')

    plugins = []

    def __init__(self):
        for p in plugin_conf.PLUGINS: 
            p_module = __import__('core.plugin.%s' %p, fromlist=[p])

            self.plugins.append(getattr(p_module, p)())

    def preload(self, api_request):
        api_request['meta']['plugin'] = {}

        for p in self.plugins:
            api_request = p.preload(api_request)

        return api_request

    def success(self, api_request, result):
        for p in self.plugins:
            result = p.success(api_request, result)

        return result

    def error(self, api_request, error):
        for p in self.plugins:
            p.error(api_request, error)
