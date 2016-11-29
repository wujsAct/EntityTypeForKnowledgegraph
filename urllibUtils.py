# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:23:45 2016
we can add all the urllib method into this class
@author: wujs
"""
from urllib import urlencode
import urllib2
import json
from bs4 import BeautifulSoup


class urllibUtils():
  def __init__(self):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent
    self.header = header
  
  def getRequest(self,url):
    req = None
    try:
      req = urllib2.Request(url,headers=self.header)
    except:
      pass
      #print 'wrong url..'   
    return req

  def getAhref(self,tags):
    co_occurence_ent=set()
    for tag in tags:
      for ai in tag.find_all('a',href=True):
        if '/wiki/' in ai['href']:
          co_occurence_ent.add(ai['href']+'\t'+ai.text)
    return co_occurence_ent
  
  #»ñÈ¡wikipediaÖÐ
  def getWikipediaRedirect(self,title):
    url = 'https://en.wikipedia.org/wiki/'+title
    req = self.getRequest(url)
    #print 'url:',url
    pages = urllib2.urlopen(req,timeout=200).read()
    soup = BeautifulSoup(pages,"lxml")
    tags = soup.find_all('span',class_='mw-redirectedfrom')
    redEnt = []
    if len(tags)>=1:
      tag = tags[0]
      a_item = tag.find_all('a',href=True)
      if a_item >=1:
        if 'title' in a_item[0]:
          ntitle = a_item[0]['title']
          if ntitle==title:
            firehead = soup.find_all('h1',class_='firstHeading')
            if len(firhead)>=1:
              redEnt.append(firhead[0].text)
    else:
      tags = soup.find_all('div',class_='mw-content-ltr')
      if len(tags)>=1:
        tag = tags[0]
        a_item = tag.find_all('a',href=True)
        redEnt=[]
        for ids in a_item:
          if 'title' in ids:
            ntitle = ids['title']
            if 'disambiguation' not in ntitle:
              redEnt.append(ntitle)
        
    return redEnt
    
    
  def get_candidate_entities(self,searchent):
    data = {'action': 'wbsearchentities', 'search':searchent, 'language':'en','limit':'10','format': 'json'}
    data = urlencode(data)
    #search all related wiki entity
    url = 'https://www.wikidata.org/w/api.php?'+ data
    #print url
    req = self.getRequest(url)
    res = json.loads(urllib2.urlopen(req,timeout=200).read())
    #print res
    candidate_ent = []
    co_occurence_ent = []
    if u'search' in res:
      for item in res[u'search']:
        description = None
        co_occurence_ent_item1 = set();co_occurence_ent_item2=set()
        co_occurence_ent_item = set()
        #print '---------------'
        ids = item[u'id']
        if u'label' in item:
          title = item[u'label']
        else:
          title = searchent
        #print 'title:',title
        ent_item = {}
        ent_item['ids'] = ids
        ent_item['title'] = title
        #if entity without description, we need to delete it. Not so popular!
        if 'description' in item:
          description = item[u'description']
          #need to search wikipedia to get 
          
          #print description
                
          url = 'https://www.wikidata.org/wiki/'+ids
          try:
            req = self.getRequest(url)
            properties = urllib2.urlopen(req,timeout=200).read()
            #print 'properties'
            soup = BeautifulSoup(properties,"lxml")
            
            #print 'right here'
            tags = soup.find_all('div',class_='wikibase-snakview-value wikibase-snakview-variation-valuesnak')
            co_occurence_ent_item1 = self.getAhref(tags)
          except:
            pass
            #print 'can not find wikidate page'
        else:
          #print 'get into this pages'
          url = 'https://en.wikipedia.org/wiki/'+title
          try:
            #print url
            req = self.getRequest(url)
            pages = urllib2.urlopen(req,timeout=200).read()
            soup = BeautifulSoup(pages, "lxml")
            tags = soup.find_all('p')
            #print tags[0].text
            if len(tags)>=1:
              description = tags[0].text.split('.')[0]
              #print 'description:',description
              co_occurence_ent_item2 = self.getAhref(tags)
          except:
            pass
            #print 'can not find entity wikipedia pages'
        co_occurence_ent_item = co_occurence_ent_item1 | co_occurence_ent_item2
        if (description !=None) & (len(co_occurence_ent_item)!=0):
          ent_item['description'] = description
          co_occurence_ent.append(co_occurence_ent_item)
          candidate_ent.append(ent_item)
    return candidate_ent,co_occurence_ent
    
  def parseEntCandFromWikiSearch(self,searchent):
    data = {'search':searchent,'limit':'20','offset':'0','profile':'default', 'title':'Special:Search','fulltext': '1'}
    data = urlencode(data)
    #search all related wiki entity
    url = 'https://en.wikipedia.org/w/index.php?'+ data
    #print url
    req = self.getRequest(url)
    pages = urllib2.urlopen(req,timeout=200).read()
    soup = BeautifulSoup(pages,"lxml")
    tags = soup.find_all('div',class_='mw-search-result-heading')
    candidate_ent=[];co_occurence_ent=[]
    if len(tags)>=1:
      for tag in tags:
        a_item = tag.find_all('a',href=True)
        if 'title' in a_item:
          ntitle = ids['title']
          if (searchent in ntitle) or (ntitle in searchent):
            candidate_ent_i,co_occurence_ent_i = self.get_candidate_entities(ntitle)
            candidate_ent = candidate_ent + candidate_ent_i
            co_occurence_ent = co_occurence_ent + co_occurence_ent_i
    else:
      print 'can not find in wikipedia search!'
    return candidate_ent,co_occurence_ent
