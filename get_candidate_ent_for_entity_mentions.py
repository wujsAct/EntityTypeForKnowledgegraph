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
  
def getWikipediaRedirect(title):
  url = 'https://en.wikipedia.org/wiki/'+title
  req = getRequest(url)
  pages = urllib2.urlopen(req,timeout=200).read()
  soup = BeautifulSoup(pages,"lxml")
  tags = soup.find_all('span',class_='mw-redirectedfrom')
  tag = tags[0]
  a_item = tag.find_all('a',href=True)
  ntitle = a_item[0]['title']
  redEnt = None
  if ntitle==title:
    redEnt = soup.find_all('h1',class_='firstHeading')[0].text
  return redEnt
  
def get_candidate_entities(searchent):
  data = {'action': 'wbsearchentities', 'search':searchent, 'language':'en','limit':'10','format': 'json'}
  data = urlencode(data)
  #search all related wiki entity
  url = 'https://www.wikidata.org/w/api.php?'+ data
  print url
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
    ent_item['title'] = title
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
        soup = BeautifulSoup(properties,"lxml")
        
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
        soup = BeautifulSoup(pages, "lxml")
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

def getAllCanEnts(searchent):
  candidate_ent=[];candidate_ent1=[];candidate_ent2=[];
  co_occurence_ent=[];co_occurence_ent1=[];co_occurence_ent2=[]
  candidate_ent1,co_occurence_ent1 = get_candidate_entities(searchent)
  print len(candidate_ent1),len(co_occurence_ent1)
  
  if len(candidate_ent1)<=0 or candidate_ent1[0]['title']!=searchent:
    redent = getWikipediaRedirect(searchent)
    if redent:
      candidate_ent2,co_occurence_ent2 = get_candidate_entities(redent)
      print len(candidate_ent2),len(co_occurence_ent2)
  
  candidate_ent = candidate_ent1 + candidate_ent2
  co_occurence_ent = co_occurence_ent1 + co_occurence_ent2
  print len(candidate_ent),len(co_occurence_ent) 

getAllCanEnts('obama')