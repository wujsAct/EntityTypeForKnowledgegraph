# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 20:37:34 2016

@author: DELL
"""
import numpy as np
from scipy.sparse import dok_matrix
import featureGeneration as fg
import random

def DCD(X,y,w,tmax):
    #norm is the regulazation type L1 vs L2
    C =1
    #norm = 1
    norm = 1
    if norm ==2:
        U = 1e5
        Dii = 0.5/C
    else:
        U = C
        Dii = 0
    #矩阵每一列表示一个特征！
    t = np.shape(X)
    print 't',t
    d = t[0]
    n = t[1]
    alpha =np.zeros((len(y),1))
    #w = np.zeros((d,1))
    Qii = sum(X**2) +Dii
    
   # tmax =  1000
    tol = 1e-3
    verbose = 1
    w.shape=(1,d)
    for t in range(1,tmax):
        err = 0
        for i in range(0,n):
            tempXi = X[:,i]
            g = np.dot(w[0],tempXi)*y[i]-1+Dii*alpha[i][0] #linear
            if alpha[i] < tol:
                g = min(g,0)
            if alpha[i] > U:
                g = max(g,0)
            
            if np.abs(g) > err:
                err = np.abs(g) 
            if np.abs(g)>tol:
                alpha_new = min(max(alpha[i]-g / Qii[i],0),U)
                w = w + ((alpha_new - alpha[i]) * y[i]) * X[:, i]
                alpha[i] = alpha_new
        if verbose:
            #if i % 100 ==0:
            print 'Iter %3d: %.4f\n' %(t,err)
        if err< tol:
            break
    return w


def initx(entFeatureDim,typeNum):
    x = np.zeros((entFeatureDim,typeNum))
    return x

def DCDmodel(fgmodel):
    # fa <entityNum,entFeatureDim>
    fa = fgmodel.getEntFeature()
    #data <entityNum,TypeNum>
    datas = fgmodel.getEntityTypeFeatures()
    #print datas
    #negEntSet = fgmodel.getNegEntitySet(datas)
    #negTypeSet = fgmodel.getNegTypeSet(datas)
    w = initx(typeNum,entFeatureDim)
    
    
    for iter in range(20):
        print 'total iter',iter
        X = []
        for i in range(typeNum):
            X.append([])
        y=[]
        for  i in range(typeNum):
            y.append([])
    
        for j in range(typeNum):
            #print 'typeNum',j
            for i in range(entityNum):
                if(datas[i,j]==1):
                    #print 'ent',i
                    temps = fgmodel.getNegSet(i,j,'NegEntitySetColl','NegEntitySet')
                    if temps !=None:
                            temps = temps.split('\t')
                            lists = range(len(temps)-1)
                            #nums=len(lists)/2
                            #print 'neg ent',nums
                            slices = random.sample(lists,2)
                            for kr in slices:
                                k = int(temps[kr])
                                tempX = dok_matrix(fa[k,:].toarray()-fa[i,:].toarray())
                                X[j].append(tempX)
                                y[j].append(1)
                    temps = fgmodel.getNegSet(i,j,'NegTypeSetColl','NegTypeSet')
                    if temps!=None:
                        temps = temps.strip('\t')
                        tempList = map(int,temps.split('\t')) 
                        lists = range(len(tempList)-1)
                        #nums = len(lists)/2
                        #print 'neg type',nums
                        slices = random.sample(lists,1)
                        #print slices
                        for kr in slices:
                            #print kr
                            k = int(tempList[kr])
                            tempX = dok_matrix(fa[i,:].toarray())
                            X[j].append(-tempX)
                            y[j].append(1)
                            X[k].append(tempX)
                            y[k].append(1)
                            #此处存在一个很大的误差呢！但是我无法去考虑呢!
        for i in range(typeNum):
            Xi = X[i]
            sub_entNum = len(Xi)
            X_rel = dok_matrix((sub_entNum, entFeatureDim)) 
            print 'type',i,':\t',sub_entNum
            j=0
            for each in Xi:
                #print j
                X_rel[j] = each
                j = j + 1
            
            Xi= (X_rel.T).toarray()
            print 'np.shape(Xi)',np.shape(Xi)
            yi =y[i]
            #print yi
#            if i != 2 and i!=3:
#                tmax = 5000
#            else:
#                tmax = 5000
            tmax = 1000
            w1 = DCD(Xi,yi,w[i,:],tmax)
            w1.shape=(1,entFeatureDim)
            w[i,:] = w1
    return w
                        
entityNum=fg.featureGeneration.knowentNo
typeNum=fg.featureGeneration.typeNum
entFeatureDim=fg.featureGeneration.lnkmodel.entfeatureDim
fgmodel = fg.featureGeneration()
w = DCDmodel(fgmodel)
#datas = fgmodel.getEntityTypeFeatures()
#negEntSet = fgmodel.getNegEntitySet(datas)
#negTypeSet = fgmodel.getNegTypeSet(datas)
dir_path = fg.linkmodel.linkmodel1.dir_path
f1 = open(dir_path+'/w_1_DCD.txt','w')
#f2 = open('sum_gradient','w')
wsize = w.shape
print wsize
for i in range(wsize[0]):
    for j in range(wsize[1]):
        f1.write(str(w[i,j])+"\t")
    f1.write('\n')