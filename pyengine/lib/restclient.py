#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import httplib
import urllib
import json  
from dicttoxml import dicttoxml
import xmltodict

class RestClient():

    CONTENT_TYPE = {
        "json": "application/json", 
        "xml": "application/xml", 
        "post": "application/x-www-form-urlencoded"
    }

    ACCEPT = {
        "json": "application/json", 
        "xml": "application/xml",
        "text": "text/plain"
    }

    def __init__(self, ip, **keywords): 
        # Default Server Settings
        self.ip = ip
        self.port = "80"
        self.url = "/"

        # Default XML Root : root
        self.xml_root = 'root'

        # Default Content Type : json
        self.content_type = "json"
        self.headers = {}
        self.headers['Content-type'] = self.CONTENT_TYPE['json']
        self.headers['Accept'] = self.ACCEPT['json']

        # Set Extra Arguments
        for key in keywords.keys(): 
            if key == "url":
                self.url = keywords[key]

            if key == "port":
                self.port = keywords[key] 

            if key == "content_type":
                if self.CONTENT_TYPE.has_key(keywords[key]):
                    self.content_type = keywords[key]
                    self.headers['Content-type'] = self.CONTENT_TYPE[keywords[key]]

            if key == "accept":
                if self.ACCEPT.has_key(keywords[key]):
                    self.headers['Accept'] = self.ACCEPT[keywords[key]]

            if key == 'token':
                self.headers['Authorization'] = 'Token %s' %(str(keywords[key]))

            if key == 'xtoken':
                self.headers['X-Auth-Token'] = '%s' %(str(keywords[key]))

            if key == 'xml_root':
                self.xml_root = keywords[key]

    def updateSettings(self, **keywords):
        for key in keywords.keys(): 
            if key == "ip":
                self.ip = keywords[key]

            if key == "port":
                self.port = keywords[key] 

            if key == "url":
                self.url = keywords[key]

            if key == "content_type":
                if self.CONTENT_TYPE.has_key(keywords[key]):
                    self.content_type = keywords[key]
                    self.headers['Content-type'] = self.CONTENT_TYPE[keywords[key]]

            if key == "accept":
                if self.ACCEPT.has_key(keywords[key]):
                    self.headers['Accept'] = self.ACCEPT[keywords[key]]

            if key == 'token':
                self.headers['Authorization'] = 'Token %s' %(str(keywords[key]))

            if key == 'xtoken':
                self.headers['X-Auth-Token'] = '%s' %(str(keywords[key]))

            if key == 'xml_root':
                self.xml_root = keywords[key]

    def request(self, method='GET', **kwargs):
        (url, params) = self._parseRequest(**kwargs)

        try:
            if method in ['POST', 'PUT']:
                encoded_params = self._encodeParams(params)
            else:
                encoded_params = self._urlEncode(params)

            conn = httplib.HTTPConnection(self.ip, self.port)

            if method in ['POST', 'PUT']:
                conn.request(method, url, encoded_params, self.headers)
            else:
                conn.request(method, '%s?%s' %(url, encoded_params), "", self.headers)

            res = conn.getresponse()
            content_type = self._getContentType(res.getheaders())
            received_data = res.read()

            decoded_data = self._decodeData(received_data, content_type)

            return (res.status, decoded_data)

        except Exception as e:
            print e
            return False, e

    def _getContentType(self, header_list):
        for item in header_list:
            if item[0].upper() == 'CONTENT-TYPE':
                return item[1].split(';')

        return "text/plain"

    def _parseRequest(self, **kwargs):
        if kwargs.has_key('url'):
            url = kwargs['url']
        else:
            url = self.url

        if kwargs.has_key('params'):
            params = kwargs['params']
        else:
            params = {}

        return (url, params)

    def _encodeParams(self, params):
        if self.content_type == "json":
            encoded_params = self._jsonEncode(params)
        elif self.content_type == "xml":
            encoded_params = self._xmlEncode(params)
        else:
            encoded_params = self._urlEncode(params)

        return encoded_params

    def _decodeData(self, data, content_type):
        if "application/json" in content_type:
            decoded_data = self._jsonDecode(data)
        elif "application/xml" in content_type:
            decoded_data = self._xmlDecode(data)
        else:
            decoded_data = data

        return decoded_data

    def _urlEncode(self, req_params):
        params = urllib.urlencode(req_params)
        return params

    def _xmlEncode(self, req_params): 
        try:
            req_xml = dicttoxml(req_params, attr_type=False, custom_root=self.xml_root) 
            return req_xml

        except Exception as e:
            print e
            return False
            
    def _xmlDecode(self, res_xml): 
        try:
            res_params = xmltodict.parse(res_xml.strip())
            return res_params

        except Exception as e:
            print e
            return False

    def _jsonEncode(self, req_params): 
        try:
            req_json = json.dumps(req_params , sort_keys=True)            
            return req_json

        except Exception as e:
            print e
            return False

    def _jsonDecode(self, res_json):
        try:
            res_params = json.loads(res_json)
            return res_params

        except Exception as e:
            print e
            return False

if __name__ == "__main__":
    pass
