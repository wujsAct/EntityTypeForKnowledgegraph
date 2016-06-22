# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:14:02 2015

@author: wujs
"""

__author__ = 'wujs'
#!/usr/bin/python
import json
import urllib
import codecs
api_key = 'AIzaSyBUmPsISQrS8C0jUzFoS1NGFmTl9AW0E70'
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
'''
how to get the description:
freebase topic api:
https://www.googleapis.com/freebase/v1/topic/m/07q37w?filter=/common/topic/description
'''


def iscvttype(nodes):
    query = [{
        'id': nodes,
        'name':None,
        '/freebase/type_hints/mediator': []
    }]

    params = {
            'query': json.dumps(query),
            'key': api_key
        }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    result = response['result']
    print result
    
    jsonres =  result[0]
    if jsonres.get('/freebase/type_hints/mediator') !=[]:
        if  jsonres['/freebase/type_hints/mediator'][0]:
            return 1
        else:
            return 0

def getSurfaceName(nodes):
    query = [{
        'id': nodes,
        'name':None,
        'type':[]
    }]
    
    params = {
            'query': json.dumps(query),
            'key': api_key
        }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    try:
        result = response['result']
        
        jsonres =  result[0]
        names = 'None'
        types ='None'
        if jsonres.get('name') !=None:
            names = jsonres['name']
        if jsonres.get('type') !=None:
            types = jsonres['type']
        strs = names+'\t'+'\t'.join(types)
        return strs
    except:
        print 'error get the result'
        return 'None'+'\t'+'None'
# f2 = open("C:/Users/wujs/Desktop/ourdata/matlabpro_500/cvtrel_all.txt",'w')
# for k in result['/type/reflect/any_master']:
    # f2.write(str(k))
    # f2.write("\n")
# f2.close()
#f1 = open('C:/Users/wujs/Desktop/ourdata/film/id2type_tj.txt')
#f2 = open('C:/Users/wujs/Desktop/ourdata/film/typeisCVT.txt','w')
#total = 0
#for line in f1.readlines():
#    line = line.strip()
#    ids,types,num = line.split('\t')
#    
#    types = types.replace('<','')
#    types = types.replace('>','')
#    types = types.split('/')[-1]
#    types = '/'+types.replace('.','/')
#    
#    if iscvttype(types) == 1:
#        print types,num
#        total = total + int(num)
#        f2.write(str(types)+'\n')
#f2.close()
#        
#print total
#dir_path="C:/Users/wujs/Desktop/ourdata/food"
#f2 = open(dir_path+"/id2entity.txt")
#f3 = codecs.open(dir_path+"/ent2name.txt",'a','utf-8')
#line = 157
#t= 0
#for items in f2.readlines():
#    t= t+1
#    if t>962:
#        print t
#        items = items.strip()
#        ids,entName = items.split('\t')
#        entN = entName.split('/')[-1].replace('>','')
#        ent = '/'+entN.replace('.','/')
#        surfaceName_types = getSurfaceName(ent)
#        f3.write(ent+'\t'+surfaceName_types+'\n')
#f3.close()
        

