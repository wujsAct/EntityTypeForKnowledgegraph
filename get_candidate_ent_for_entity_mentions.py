# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:23:45 2016

@author: DELL
"""
from urllib import urlencode
import urllib2
import json
from bs4 import BeautifulSoup

def getRequest(url):
  User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
  header = {}
  header['User-Agent'] = User_Agent
  req = None
  try:
    req = urllib2.Request(url,headers=header)
  except:
    print 'wrong url..'
    
  return req

def getAhref(tags):
  co_occurence_ent=set()
    
  for tag in tags:
    for ai in tag.find_all('a',href=True):
      if '/wiki/' in ai['href']:
        co_occurence_ent.add(ai['href']+'\t'+ai.text)
  return co_occurence_ent
  
  
    
    
def get_candidate_entity(searchent = 'German'):
  data = {'action': 'wbsearchentities', 'search':searchent, 'language':'en','limit':'50','format': 'json'}
  data = urlencode(data)
  #search all related wiki entity
  url = 'https://www.wikidata.org/w/api.php?'+ data
  req = getRequest(url)
  res = json.loads(urllib2.urlopen(req,timeout=200).read())
  candidate_ent = []
  co_occurence_ent = []
  for item in res[u'search']:
    description = None
    co_occurence_ent_item1 = set();co_occurence_ent_item2=set()
    co_occurence_ent_item = set()
    print '---------------'
    ids = item[u'id']
    title = item[u'label']
    print 'title:',title
    ent_item = {}
    ent_item['ids'] = ids
    #if entity without description, we need to delete it. Not so popular!
    if 'description' in item:
      description = item[u'description']
      #need to search wikipedia to get 
      
      print description
            
      url = 'https://www.wikidata.org/wiki/'+ids
      try:
        req = getRequest(url)
        properties = urllib2.urlopen(req,timeout=200).read()
        print 'properties'
        soup = BeautifulSoup(properties)
        
        print 'right here'
        tags = soup.find_all('div',class_='wikibase-snakview-value wikibase-snakview-variation-valuesnak')
        co_occurence_ent_item1 = getAhref(tags)
      except:
        print 'can not find wikidate page'
    else:
      print 'get into this pages'
      url = 'https://en.wikipedia.org/wiki/'+title
      try:
        print url
        req = getRequest(url)
        pages = urllib2.urlopen(req,timeout=200).read()
        soup = BeautifulSoup(pages)
        tags = soup.find_all('p')
        description = tags[0].text.split('.')[0]
        print 'description:',description
        co_occurence_ent_item2 = getAhref(tags)
      except:
        print 'can not find entity wikipedia pages'
    co_occurence_ent_item = co_occurence_ent_item1 | co_occurence_ent_item2
    if (description !=None) & (len(co_occurence_ent_item)!=0):
      ent_item['description'] = description
      co_occurence_ent.append(co_occurence_ent_item)
      candidate_ent.append(ent_item)
  return candidate_ent,co_occurence_ent


candidate_ent,co_occurence_ent = get_candidate_entity('obama')
print len(candidate_ent)
print len(co_occurence_ent)
