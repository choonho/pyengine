import logging
from core.lib.error import *
from core.lib.locator import Locator

class Manager(object):
    """
    Manager class is basic Interface
    Every XXXManager has to inherit Manager
    """

    logger = logging.getLogger('core')
    locator = Locator()
