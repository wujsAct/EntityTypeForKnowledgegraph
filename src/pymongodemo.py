# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 21:27:49 2015

@author: wujs
"""
import pymongo
###mongodb 的基本操作，这样以后就可以轻松的使用了哈

#建立一个连接
def get_db():
    
    mongoclient= pymongo.MongoClient(host='192.168.0.7',port=50000)
    #fb15kdb = mongoclient.freebase_yelp_r50_cluster
    fb15kdb = mongoclient.freebase_yelp_r20_cluster_part1
    return fb15kdb

def get_collection(db,collName):
    # 选择集合（mongo中collection和database都是延时创建的）
    coll = db[collName]
    #print coll
    return coll

#此处的dict是一个字典的形式
def insert_one_doc(db,coll,items):
    #插入一个document
    #post_id = coll.insert(items)
    #print post_id
    coll.insert(items)
    
