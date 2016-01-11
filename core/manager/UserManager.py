from django.contrib.auth.hashers import make_password
from pyengine.lib import utils
from core.manager import Manager 
from core.lib.error import *
from core.conf import global_conf

class UserManager(Manager):

    def createUser(self, params):
        user_dao = self.locator.getDAO('user') 

        if user_dao.isExistfromKey('user_id', params['user_id']):
            raise ERROR_EXIST_RESOURCE(key='user_id', value=params['user_id'])

        if not utils.checkIDFormat(params['user_id']):
            raise ERROR_INVALID_ID_FORMAT()

        if not utils.checkPasswordFormat(params['password']):
            raise ERROR_INVALID_PASSWORD_FORMAT()

        dic = {}
        dic['user_id'] = params['user_id']
        dic['password'] = make_password(params['password'])

        if params.has_key('name'):
            dic['name'] = params['name']

        if params.has_key('email'):
            dic['email'] = params['email']

        if params.has_key('language'):
            dic['language'] = params['language']
        else:
            dic['language'] = global_conf.DEFAULT_LANGUAGE

        if params.has_key('timezone'):
            dic['timezone'] = params['timezone']
        else:
            dic['timezone'] = global_conf.DEFAULT_TIMEZONE


        user = user_dao.insert(dic)

        return self.locator.getInfo('UserInfo', user.user_id)

    def updateUser(self, params):
        user_dao = self.locator.getDAO('user') 

        if not user_dao.isExistfromKey('user_id', params['user_id']):
            raise ERROR_INVALID_PARAMETER(key='user_id', value=params['user_id'])

        dic = {}

        if params.has_key('password'):
            if not utils.checkPasswordFormat(params['password']):
                raise ERROR_INVALID_PASSWORD_FORMAT()

            dic['password'] = make_password(params['password'])

        if params.has_key('name'):
            dic['name'] = params['name']

        if params.has_key('state'):
            dic['state'] = params['state']

        if params.has_key('email'):
            dic['email'] = params['email']

        if params.has_key('language'):
            dic['language'] = params['language']

        if params.has_key('timezone'):
            dic['timezone'] = params['timezone']


        user_dao.update(params['user_id'], dic, 'user_id')

        return self.locator.getInfo('UserInfo', params['user_id'])

    def deleteUser(self, params):
        user_dao = self.locator.getDAO('user') 

        users = user_dao.getVOfromKey(user_id=params['user_id'])

        users.delete()

        return {}

    def enableUser(self, params):
        params['state'] = 'enable'

        return self.updateUser(params)

    def disableUser(self, params):
        params['state'] = 'disable'

        return self.updateUser(params)

    def getUser(self, params):
        user_dao = self.locator.getDAO('user')

        if not user_dao.isExistfromKey('user_id', params['user_id']):
            raise ERROR_INVALID_PARAMETER(key='user_id', value=params['user_id'])

        return self.locator.getInfo('UserInfo', params['user_id'])

    def listUsers(self, search, sort, minimal):
        user_dao = self.locator.getDAO('user')

        output = []
        (users, total_count) = user_dao.select(search=search, sort=sort)

        for user in users:
            user_info = self.locator.getInfo('UserInfo', user.user_id, minimal=minimal)
            output.append(user_info)

        return (output, total_count)
