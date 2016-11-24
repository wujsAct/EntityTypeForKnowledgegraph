# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:23:45 2016

@author: DELL
"""
from urllib import urlencode
import urllib2
import json
import time
from bs4 import BeautifulSoup


def get_candidate_entity(searchent = 'German'):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent
    
    #https://www.wikidata.org/w/api.php?action=wbsearchentities&search=abc&language=en&limit=50
    
    data = {'action': 'wbsearchentities', 'search':searchent, 'language':'en','limit':'50','format': 'json'}
    
    data = urlencode(data)
    
    start = time.time()
    #wiki
    url = 'https://www.wikidata.org/w/api.php?'+ data
    req = urllib2.Request(url,headers=header)
    res = json.loads(urllib2.urlopen(req,timeout=200).read())
    end = time.time()
    print end - start
    candidate_ent = []
    co_occurence_ent = []
    for item in res[u'search']:
        print '---------------'
        ids = item[u'id']
        title = item[u'label']
        if 'description' in item:
            description = item[u'description']
        else:
            continue
        ent_item = {}
        ent_item['ids'] = ids
        ent_item['description'] = description
        
        
        
        co_occurence_ent_item=set()
        url = 'https://www.wikidata.org/wiki/'+ids
        try:
            req = urllib2.Request(url,headers=header)
            properties = urllib2.urlopen(req,timeout=200).read()
            print 'properties'
    
            soup = BeautifulSoup(properties)
            
            print 'right here'
            tags = soup.find_all('div',class_='wikibase-snakview-value wikibase-snakview-variation-valuesnak')
            for tag in tags:
                try:
                    hrefs = tag.a['href']
                    title = tag.a.text
                    if '/wiki/' in hrefs:
                        co_occurence_ent_item.add(hrefs+'\t'+title)
                        print hrefs,title
                except:
                    continue
            if len(co_occurence_ent_item)==0:
                continue
            else:
                candidate_ent.append(ent_item)
                co_occurence_ent.append(co_occurence_ent_item)
            
        except:
            print 'can not find url'
            continue
    return candidate_ent,co_occurence_ent

get_candidate_entity()
