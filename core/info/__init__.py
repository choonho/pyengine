import logging
import pytz
import uuid
from datetime import datetime
from core.lib.error import *
from core.lib.locator import Locator
from core.conf import global_conf

class Info(object):

    logger = logging.getLogger('core')
    locator = Locator()

    def __init__(self, id=None):
        self.id = id  
        self.output = {}

    def isMinimal(self, options):
        if options.has_key('minimal') and options['minimal'] == True:
            return True
        else:
            return False

    def _recursionInfo(self, key, value, tz): 
        # UUID Type to String
        if type(value) == uuid.UUID:
            return str(value)

        # Time Conversion
        elif key in global_conf.DATETIME_FIELDS: 
            if value != None:
                value = value.replace(tzinfo=pytz.utc).astimezone(tz)
                return value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return ''

        # Instance
        elif isinstance(value, Info) == True:
            return value.result(tz)

        # List
        elif type(value) == type(list()):
            # Default
            list_output = []
            for v in value:
                if type(v) == type(dict()):
                    dic_output = {}
                    for k in v:
                        dic_output[k] = self._recursionInfo(k, v[k], tz)

                    list_output.append(dic_output)

                elif isinstance(v, Info) == True:
                    list_output.append(v.result(tz))

                else:
                    list_output.append(v)

            return list_output

        # Dictionary
        elif type(value) == type(dict()):
            output = {}
            for k in value:
                output[k] = self._recursionInfo(k, value[k], tz)

            return output

        # No Change
        else:
            return value

    def result(self, timezone=global_conf.DEFAULT_TIMEZONE): 
        tz = pytz.timezone(timezone)

        to_string = {}
        for k in self.output:
            to_string[k] = self._recursionInfo(k, self.output[k], tz)

        return to_string
