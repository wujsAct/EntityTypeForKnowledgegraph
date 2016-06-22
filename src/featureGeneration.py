# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 20:17:01 2015

@author: wujs
"""
import random
import linkmodel
import numpy as np
import pymongodemo

class featureGeneration:
    lnkmodel=linkmodel.linkmodel()
    #entityNum = lnkmodel.entityNum
    relNum = lnkmodel.relNum
    typeNum = lnkmodel.typeNum
    rel_type = lnkmodel.entfeatureDim 
    dir_path = lnkmodel.dir_path
    X1 = linkmodel.X
    knowtypeEntity = linkmodel.linkmodel1.knowtypeEntity
    untypeEntity = linkmodel.linkmodel1.untypeEntity
    missent = linkmodel.linkmodel1.missent
    X =X1[knowtypeEntity[:,0].tolist(),:]
    Y1 = linkmodel.Y
    Y = Y1[knowtypeEntity[:,0].tolist(),:]
    knowentNo = linkmodel.linkmodel1.knowentNo
    entityNum = knowentNo    
    db = pymongodemo.get_db()
    
    #X2 = X1[untypeEntity[:,0].tolist(),:]
    Y2 = Y1[map(int,untypeEntity.tolist()),:]
    #Y2 = Y1[untypeEntity[:,0].tolist(),:]
    
    def getEntityTypeFeatures(self):
#        datas = dok_matrix((self.knowentNo,self.typeNum))
#        X = self.X
#        print 'get ent types'
#        for i in range(self.knowentNo):
#            print i
#            for j in range(self.typeNum):
#                if X[i,j]!=0:
#                    datas[i,j]=1
        return self.X
        
    def getEntFeature(self):
#        datas = dok_matrix((self.knowentNo,self.rel_type),dtype='float')
#        print 'get ent feature'
#        for i in range(self.knowentNo):
#            print i
#            for j in range(self.rel_type):
#                if self.Y[i,j] !=0:
#                    datas[i,j]=self.Y[i,j]
        return self.Y
    def getUntypeEntFeature(self):
#        datas = dok_matrix((self.missent,self.rel_type),dtype='float')
#        
#        for i in range(self.missent):
#            for j in range(self.rel_type):
#                if self.Y2[i,j] !=0:
#                    datas[i,j] = self.Y2[i,j]
        return self.Y2
     
    #转化成数据库的操作
    def insertNegEntSet(self,datas):
        print 'neg entity set\n'
        collName = 'NegEntitySetColl'
        coll = pymongodemo.get_collection(self.db,collName)
        #negEntSet = {}
        entityNum,typeNum = np.shape(datas)
        for i in range(entityNum):
            print 'neg ent set',i
            for j in range(typeNum):
                if datas[i,j]==1:
                    #tempList = []
                    tempList=[]
                    for k in range(entityNum):
                        if datas[k,j]!=1:
                            tempList.append(k)
                            #tempList = tempList + str(k)+'\t'
                    lists = range(len(tempList)-1)
                    slices = random.sample(lists,10)
                    #print slices
                    tempList=''
                    for k in range(10):
                        tempList = tempList + str(slices[k])+'\t'
                    tempList = tempList.strip()
                    #temp = str(i)+"_"+str(j)
                    #negEntSet[temp]=tempList
                    items =  {"entid":i, "typeid":j, "NegEntitySet":tempList}
                    pymongodemo.insert_one_doc(self.db,coll,items)    
                    #print ("%s\t%s") %(temp,tempList)
        print 'finish generate neg entity set'
    #抽取操作也转换成数据库操作了！
    def getNegSet(self,i,j,collName,key):
        #collName = 'NegEntitySetColl'
        coll = pymongodemo.get_collection(self.db,collName)
        items = {}
        items['entid'] = i
        items['typeid']=j
        temp =None
        for eachent in coll.find(items):
              temp  = eachent[key]
        #print temp
        return temp
        
        
#generate the negtive type set: negTypeSet = {}
    def insertNegTypeSet(self,datas):
        print 'net type set\n'
        #negTypeSet = {}
        collName = 'NegTypeSetColl'
        coll = pymongodemo.get_collection(self.db,collName)
        entityNum,typeNum = np.shape(datas)
        print np.shape(datas)
        for i in range(entityNum):
            print 'neg type set',i
            for j in range(typeNum):
                if datas[i,j] == 1:
                    #tempList = []
                    tempList=''
                    for k in range(typeNum):
                        if datas[i,k]!=1:
                            #tempList.append(k)
                            tempList = tempList + str(k)+'\t'
                    #temp = str(i)+"_"+str(j)
                    #negTypeSet[temp]=tempList
                    #print ("%s\t%s") %(temp,tempList)
                    items =  {"entid":i, "typeid":j, "NegTypeSet":tempList}
                    pymongodemo.insert_one_doc(self.db,coll,items)
        print 'finish generate neg type set'
        
fgg = featureGeneration()
datas = fgg.getEntityTypeFeatures()
#print datas
#collName = 'NegEntitySetColl'
#key = 'NegEntitySet'
#fgg.insertNegEntSet(datas)
#fgg.insertNegTypeSet(datas)
#fgg.getNegSet(0,0,collName,key)
  