#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.info import Info

class UserInfo(Info):

    def __init__(self, id, options):
        super(self.__class__, self).__init__(id)
        self.fetchByID(options)

    def __repr__(self):
        return '<UserInfo: %s>' %self.id 

    def fetchByID(self, options):
        """
        Besed on ID
        Fetch needed data from vo
        """
        user_dao = self.locator.getDAO('user')

        users = user_dao.getVOfromKey(user_id=self.id)

        if users.count() > 0:
            user = users[0]
            self.output['user_id'] = user.user_id

            if not self.isMinimal(options):
                self.output['name'] = user.name
                self.output['state'] = user.state
                self.output['email'] = user.email
                self.output['language'] = user.language
                self.output['timezone'] = user.timezone
                self.output['created'] = user.created

        else:
            self.logger.error("User ID is not founded : %s" % self.id)
