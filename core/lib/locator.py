import traceback, logging
from core.lib.dao import DAO
from core.lib.error import *
from core import models

class Locator():
    logger = logging.getLogger('core')
    dao_instance = {}

    def getManager(self, name):
        try:
            manager_module = __import__('core.manager.%s' %name, fromlist=[name])
            return getattr(manager_module, name)()

        except:
            self.logger.error(traceback.format_exc())
            raise ERROR_LOCATOR(category='manager', name=name)


    def getDAO(self, name):
        if not self.dao_instance.has_key(name):
            try:
                self.dao_instance[name] = DAO(models.__dict__[name])

            except:
                self.logger.error(traceback.format_exc())
                raise ERROR_LOCATOR(category='dao', name=name)

        return self.dao_instance[name]


    def getInfo(self, name, info_id, **kwargs):
        try:
            info_module = __import__('core.info.%s' %name, fromlist=[name])
            return getattr(info_module, name)(info_id, kwargs)

        except:
            self.logger.error(traceback.format_exc())
            raise ERROR_LOCATOR(category='info', name=name)
