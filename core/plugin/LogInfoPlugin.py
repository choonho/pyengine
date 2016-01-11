from core.lib.error import *
from core.plugin import Plugin
from core.conf import plugin_conf

class LogInfoPlugin(Plugin):

    def preload(self, api_request):
        if not api_request['meta']['api_class'] in plugin_conf.NO_PRINT_API:
            self.logger.info("%s (Request)==> %s" %(api_request['meta']['api_class'], str(api_request['params'])))

        return api_request

    def success(self, api_request, result):
        if not api_request['meta']['api_class'] in plugin_conf.NO_PRINT_API:
            self.logger.info("%s (Response)==> %s" %(api_request['meta']['api_class'], str(result)))

        return result
