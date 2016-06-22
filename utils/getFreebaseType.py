# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 15:44:56 2016

@author: DELL
"""

__author__ = 'wujs'
#!/usr/bin/python
import json
import urllib
import codecs

class FreebaseAPI():
    def __init__(self,api_key):
        #'key 5'
        self.api_key = api_key
        self.service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    '''
    how to get the description:
    freebase topic api:
    https://www.googleapis.com/freebase/v1/topic/m/07q37w?filter=/common/topic/description
    '''
    def getTypesbyId(self,nodes):
        query = [{
#            'id': nodes,
#            'name':None,
#            'type':[]
             'id':None,
             'type':[],
          #   'notable_types':[]
        }]
        
        params = {
                'query': json.dumps(query),
                'key': self.api_key
            }
        url = self.service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())
        try:
            result = response['result']
            
            jsonres =  result[0]
            types ='None'
            if jsonres.get('type') !=None:
                types = jsonres['type']
            return types
        except:
            return 'None'
    
    def getTypesbyName(self,nodes):
        query = [{
            'name': nodes,
            'type':[]
        }]
        
        params = {
                'query': json.dumps(query),
                'key': self.api_key
            }
        url = self.service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())
        try:
            result = response['result']
            
            jsonres =  result[0]
            types =None
            if jsonres.get('type') !=None:
                types = jsonres['type']
            return types
        except:
            return None
    def getSurfaceName(self,nodes):
        query = [{
            'id': nodes,
            'name':None,
        }]
        
        params = {
                'query': json.dumps(query),
                'key': self.api_key
            }
        url = self.service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())
        names = 'None'
        try:
            result = response['result']
            jsonres =  result[0]
            
            if jsonres.get('name') !=None:
                names = jsonres['name']
            #strs = nodes+'\t'+'\t'.join(names)
            #return strs
        except:
            print 'error get the result'
        return names
fr = FreebaseAPI('AIzaSyBF4ujqh3s-bPiyGOTQbJO7mk8BOGoGpz8')
print fr.getSurfaceName('/m/01twh4')


