import logging
from routes import Mapper
from core.lib.error import *
from core.conf import router_conf

class Router:
    
    INFO_META = ['module', 'sub_module', 'api_class', 'api_version']

    logger = logging.getLogger('core')
    map = Mapper()

    def __init__(self):
        with self.map.submapper(path_prefix=router_conf.URL_PREFIX, module=router_conf.MODULE) as m:
            for u in router_conf.URLS:
                m.connect(u[1], sub_module=u[0], api_class=u[3], conditions=dict(method=[u[2]]))

    def match(self, request):
        api_request = {}
        api_request[u'meta'] = {}
        api_request[u'params'] = {}

        # RESTful URL Match
        result = self.map.match(request.path, {'REQUEST_METHOD': request.method})

        if result == None:
            # Error : Undefined URL
            raise ERROR_INVALID_REQUEST(url=request.path, method=request.method)

        for k in result.keys():
            if k in self.INFO_META:
                api_request['meta'][unicode(k)] = result[k]
            else:
                api_request['params'][unicode(k)] = result[k]

        return api_request
