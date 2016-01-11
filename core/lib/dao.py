import uuid
import logging
from datetime import datetime
from core.lib.error import *

class DAO():
    model = None
    logger = logging.getLogger('core')

    def __init__(self, model):
        self.model = model

    def insert(self, dic): 
        for field in self.model._meta.fields:
            if dic.has_key(field.name):
                if field.unique == True:
                    filter = {field.name: dic[field.name]}
                    vos = self.model.objects.filter(**filter)

                    if vos.count() > 0:
                        raise ERROR_NOT_UNIQUE(value=dic[field.name] ,field=field.name)
            else:
                if field.name not in ['id','created','last_update'] and str(field.default) == 'django.db.models.fields.NOT_PROVIDED':
                    raise ERROR_REQUIRED_FIELD(field=field.name)

                if str(field.default) == 'custom_id':
                    dic[field.name] = self._createCustomID(field.name, field.help_text)

        insert_model = self.model(**dic)
        insert_model.save()

        return insert_model

    def _createCustomID(self, field_name, id_prefix):
        i = 0

        while True:
            custom_id = '%s-%s' %(id_prefix, str(uuid.uuid4())[:8])

            if i == 10:
                raise ERROR_ID_GENERATION_FAILED()

            filter = {field_name: custom_id}
            vos = self.model.objects.filter(**filter)
            if vos.count() == 0:
                break

            i += 1

        return custom_id

    def update(self, value, dic, update_key='uuid'):
        update_key_filter = {update_key: value}

        for d in dic:
            try:
                field = self.model._meta.get_field(d)
            except Exception as e:
                raise ERROR_UNKNOWN_FIELD(field=d)

            if field:
                if field.unique == True:
                    filter = {field.name: dic[field.name]}

                    vos = self.model.objects.filter(**filter).exclude(**update_key_filter)
                    if vos.count() > 0:
                        raise ERROR_NOT_UNIQUE(value=dic[field.name] ,field=field.name)

        for f in self.model._meta.fields:
            if f.name in ['last_update']:
                dic[f.name] = datetime.now() 

        self.model.objects.filter(**update_key_filter).update(**dic)

    def delete(self, value, delete_key='uuid'):
        delete_key_filter = {delete_key: value}

        self.model.objects.filter(**delete_key_filter).delete()

    def getValuefromKey(self, filed, **filter):
        value_list = []

        vos = self.model.objects.filter(**filter)
        for vo in vos:
            value_list.append(vo.__dict__[field])

        return value_list

    def getVOAll(self, key, value):
        vos = self.mode.objects.all()

        return vos

    def getVOfromKey(self, **filter):
        vos = self.model.objects.filter(**filter)

        return vos

    def isExist(self, **filter):
        vos = self.getVOfromKey(**filter)
        if vos.count() == 0:
            return False
        else:
            return True

    def sql(self, sql, params = []):
        try:
            vos = self.model.objects.raw(sql, params)
        except Exception as e:
            raise ERROR_QUERY_FAILED(reason=e)

        return vos

    def select(self, **kwargs):
        filter = {}
        not_filter = {}
        order_by = None
        distinct = None

        if kwargs.has_key('search'):
            for s in kwargs['search']:
                if s.has_key('key') and s.has_key('value') and s.has_key('option'):
                    if s['option'] == 'contain':
                        filter['%s__icontains' %str(s['key'])] = s['value']
                    elif s['option'] == 'lt':
                        filter['%s__lt' %str(s['key'])] = s['value']
                    elif s['option'] == 'lte':
                        filter['%s__lte' %str(s['key'])] = s['value']
                    elif s['option'] == 'gt':
                        filter['%s__gt' %str(s['key'])] = s['value']
                    elif s['option'] == 'gte':
                        filter['%s__gte' %str(s['key'])] = s['value']
                    elif s['option'] == 'eq':
                        filter[str(s['key'])] = s['value']
                    elif s['option'] == 'not':
                        not_filter[str(s['key'])] = s['value']
                    elif s['option'] == 'ncontain':
                        not_filter['%s__icontains' %str(s['key'])] = s['value']
                    elif s['option'] == 'in':
                        if type(s['value']) == type(list()):
                            filter['%s__in' %str(s['key'])] = s['value']

        if kwargs.has_key('sort'):
            sort = kwargs['sort']
            if sort.has_key('field'):
                if sort.has_key('desc') and sort['desc'] == True:
                    order_by = '-%s' %str(sort['field'])
                else:
                    order_by = '%s' %str(sort['field'])

        if kwargs.has_key('distinct'):
            distinct = kwargs['distinct']

        try:
            vos = self.model.objects.filter(**filter)

            if not_filter != {}:
                vos = vos.exclude(**not_filter)

            if order_by:
                vos = vos.order_by(order_by)

            if distinct:
                vos = vos.values(distinct).distinct()

            total_count = vos.count()

            if kwargs.has_key('sort'):
                sort = kwargs['sort']
                if sort.has_key('row_no'):
                    if sort.has_key('list_scale'):
                        vos = vos[(sort['row_no'] - 1):(sort['row_no'] + sort['list_scale'] - 1)]
                    else:
                        vos = vos[(sort['row_no'] - 1):]

            return (vos, total_count)

        except Exception as e:
            raise ERROR_QUERY_FAILED(reason=e)
