	def getEventName(self, model, value):
		key = 'id'

		dao = self.locator.getDAO(model)
		vos = dao.getVOfromKey(key, value)

		if vos.count() > 0:
			return vos[0].name
		else:
			raise ERROR_INVALID_PARAMETER(key=key, value=value)


	def insertEvent(self, event_type, message, **kwargs):
		self.event_message = message

		if kwargs.has_key('total_count'):
			self.total_count = kwargs['total_count']
		else:
			self.total_count = 1

		self.fail_count = 0

		self.logger.info('Processing: %s' %(self.event_message))

		dic = {}
		dic['description'] = message
		dic['event_type'] = event_type
		dic['status'] = 'processing'
		dic['username'] = self.account_info['username']
		dic['total_count'] = self.total_count

		if kwargs.has_key('target'):
			dic['target'] = utils.list2DB([kwargs['target']])

		self.event_id = self.event_dao.insert(dic)

		self.locator.event_id = self.event_id


	def setAsync(self, job_id):
		self.is_async = True

		if self.event_id:
			dic = {}
			dic['job_id'] = job_id

			self.event_dao.update(self.event_id, dic)


	def successEvent(self):
		if self.event_id and self.is_async == False:
			dic = {}
			if self.fail_count == 0:
				self.logger.info('Success: %s' %(self.event_message))

				dic['status'] = 'success'
				dic['result'] = ''
			else:
				self.logger.error('Failure: command failed. (%s/%s)' %(str(self.fail_count), str(self.total_count)))

				dic['status'] = 'failure'
				dic['result'] = 'Command failed. (%s/%s)' %(str(self.fail_count), str(self.total_count)) 

				dic['fail_count'] = self.fail_count
				dic['finished'] = datetime.now() 

			self.event_dao.update(self.event_id, dic)


	def errorEvent(self, message):
		self.logger.error('Failure: %s' %(message))

		if self.event_id:
			dic = {}
			dic['status'] = 'failure'
			dic['result'] = message
			dic['fail_count'] = self.total_count
			dic['finished'] = datetime.now()

			self.event_dao.update(self.event_id, dic)


	def updateEvent(self, **kwargs):
		if self.event_id:
			if kwargs.has_key('message'):
				self.logger.info('Processing: %s' %(kwargs['message']))

				dic = {}
				dic['result'] = 'message'

				self.event_dao.update(self.event_id, dic)

			if kwargs.has_key('target'):
				event = self.event_dao.getVOfromID(self.event_id)	

				targets = utils.db2List(event.target)
				targets.append(kwargs['target'])

				dic = {}
				dic['target'] = utils.list2DB(targets)

				self.event_dao.update(self.event_id, dic)
