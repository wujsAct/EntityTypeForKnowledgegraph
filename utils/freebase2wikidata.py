# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 11:15:37 2016

@author: DELL
"""

import gzip
import codecs
def un_gz2gettype(file_name):
    """ungz zip file"""
    #创建gzip对象
    if 'gz' in file_name:
        fileobj = gzip.open(file_name)
    if 'txt' in file_name:
        fileobj = open(file_name)
    return fileobj
    
filename = 'E:/lunwen/source_code/fb2w.gz'

fileobj = un_gz2gettype(filename)
f1 = codecs.open('E:/lunwen/source_code/mid2qid.txt','w','utf-8')
while 1:
    lines = fileobj.readlines(10000)
    if not lines:
        break
    for line in lines:       
        line = line.strip()
        #print line
        items = line.split('\t')
        #print items
        if len(items) >=3:
            ent1 = items[0]
            mid = '/m/'+ent1.split('ns/m.')[1].replace('>','')
            ent2 = items[2]
            qid = '/m/'+ent2.split('/entity/')[1].replace('> .','')
            f1.write(mid+'\t'+qid+'\n')
f1.close()