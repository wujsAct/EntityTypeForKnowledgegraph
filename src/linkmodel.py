# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:38:44 2015

@author: DELL
"""

import numpy as np
from scipy.sparse import csr_matrix
class linkmodel:
    entityNum =988;typeNum=8;relNum=200*2;
    entfeatureDim =relNum+300
    k = 0
    dir_path = 'data/newdata'+str(k)+'/typePropagation_yelp_r200_max'
    print dir_path
 
    untypeEntity = np.loadtxt(dir_path+'/entity_missingtype'+str(k)+'.txt',dtype='int')-1
        
    #the number of missing type entity
    missent = len(untypeEntity)
    print missent
    knowentNo = entityNum-missent
    knowtypeEntity=np.ones((knowentNo,1),dtype="int")
    
    k = 0
    for i in range(entityNum):
        if i not in untypeEntity:
            knowtypeEntity[k,0]=i
            k = k +1
    t = np.zeros((missent*typeNum,1),dtype='int')  
    unkownX = np.ones((missent*typeNum,1))
    data = np.loadtxt(dir_path+'/entityid2typeid.txt',dtype='int')-1  
        
    def getuntypeent(self):
        untypeEntity = self.untypeEntity
        typeNum = self.typeNum            
        t = self.t
        untypeEntNum = len(untypeEntity)
        untypeEnt =  np.zeros((untypeEntNum*typeNum,1),dtype='int')
        for i in range(untypeEntNum):
            untypeEnt[i*typeNum:(i+1)*typeNum,0] = untypeEntity[i]
            for j in range(typeNum):
                t[i*typeNum+j,0] = j
        return untypeEnt
        
    def getX(self):
        data = self.data
        entityNum = self.entityNum
        typeNum = self.typeNum
        
        untypeEnt = self.getuntypeent()
        unkownX = self.unkownX
        t = self.t
        
        row = np.concatenate((data[:,0],untypeEnt[:,0]))
        col = np.concatenate((data[:,1],t[:,0]))
        print row
        temp = np.ones((np.shape(data)[0],1),dtype='int')
        value = np.concatenate((temp[:,0],unkownX[:,0]))
        
    
        X = csr_matrix((value,(row,col)),shape=(entityNum,typeNum))
        
        return X
        
    def getY(self):
        print 'getY'
        dir_path = self.dir_path
        entityNum = self.entityNum
        dim = self.entfeatureDim
        print dim
        #relNum = self.relNum
        #typeNum = self.typeNum
        knowy = np.loadtxt(dir_path+'/Y.txt')
        Y = csr_matrix((knowy[:,2],(map(int,(knowy[:,0]-1)),
                     map(int,(knowy[:,1]-1)))),
                     shape=(entityNum,dim))        
        
        
        
        #knowy = np.loadtxt(dir_path+'/knowY.txt')
        
        #Y = spmatrix(np.log(knowy[:,2]+1),map(int,(knowy[:,0]).tolist())-1,
        #             map(int,(knowy[:,1]).tolist())-1,
        #             size=(entityNum,typeNum*relNum))
        return Y


   
linkmodel1 = linkmodel()
X = linkmodel1.getX()
Y = linkmodel1.getY()
t = 1

    
    
    
    
        
        
    
    
      