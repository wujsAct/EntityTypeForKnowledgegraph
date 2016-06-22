# -*- coding: utf-8 -*-
"""
修改过后
Created on Mon Dec 21 20:12:45 2015

@author: wujs
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 11:11:28 2015
@author: DELL
"""

"""
The training algorithms for Linear.Adagrad
"""

import numpy as np
from scipy.sparse import dok_matrix
import featureGeneration as fg
import random



def initx(entFeatureDim,typeNum):
    x = dok_matrix((entFeatureDim,typeNum))
    return x


#fa_wt_dense is the row vector
def AdaGradUpdate(w,t,fa_wt_dense,sum_gradient,learn_rate=0.01):
    if np.linalg.norm(fa_wt_dense) >1e-12:
        w_t = w[t,:].toarray()[0]
        #print w_t
        #sizet  = sum_gradient.shape
        SumGradT = sum_gradient[t,:].toarray()[0]
        #SumGradT = 1
        #update the w_t
        #for i in range(len(w_t)):
        if t==0:
            for i in range(len(w_t)):            
                w[t,i] = w_t[i]-(learn_rate)*fa_wt_dense[i]
        else:
            SumGradT = sum_gradient[t,:].toarray()[0]
            for i in range(len(w_t)):
                if SumGradT[i] == 0:
                    w[t,i] = w_t[i]-(learn_rate)*fa_wt_dense[i]
                else:
                #SumGradT = sum_gradient[t-1].toarray()[0]
                    w[t,i] = w_t[i]-(learn_rate/np.sqrt(SumGradT[i]))*fa_wt_dense[i]
        #update the sum_gradient
        tempSumGradT = SumGradT + [each**2 for each in fa_wt_dense]
        i=range(len(w_t))
        #for i in range(len(w_t)):
        #if tempSumGradT[i] !=0:
        sum_gradient[t,i] = tempSumGradT[i]
    return w,sum_gradient

def LinearAdagrad(fgmodel):
    # fa <entityNum,entFeatureDim>
    fa = fgmodel.getEntFeature()
    #data <entityNum,TypeNum>
    datas = fgmodel.getEntityTypeFeatures()
    #print datas
    #negEntSet = fgmodel.getNegEntitySet(datas)
    #negTypeSet = fgmodel.getNegTypeSet(datas)
    sum_gradient = initx(typeNum,entFeatureDim)
    w = initx(typeNum,entFeatureDim)
    for maxIter in range(100):
        print 'maxIter',maxIter
        for i in range(entityNum):
            if i % 100 ==0:
                print i
            for j in range(typeNum):
                #temp = str(i)+"_"+str(j)
                if(datas[i,j]==1):
                    #tempList = negEntSet.get(temp)
                    temps = fgmodel.getNegSet(i,j,'NegEntitySetColl','NegEntitySet')
#                    temps = temps.strip()                    
#                    tempList = map(int,temps.split('\t'))
                    #此时数据库中随机存储了1个反例！
                    
                   #如果存在negative entity set
                   #此处负例实在太多，我们仅需随机抽取100个去做训练，看下效果
                    if temps !=None:
                        temps = temps.split('\t')
                        #lists = range(len(temps)-1)
#                        slices = random.sample(lists, 1)
                        lists = range(len(temps)-1)
#                        nums=len(lists)/3
#                        if nums ==0:
#                            nums= len(lists)
                        slices = random.sample(lists,1)
                       
                        for kr in slices:
                            k = int(temps[kr])
    #                            #ss = 'train negent'+str(k)
    #                            #print ss
    #                            if (w[j,:]*fa[i,:].T)[0,0] - (w[j,:]*fa[tempList[k],:].T)[0,0] -1 <0:
    #                                w,sum_gradient = AdaGradUpdate(w,j,np.array(fa[tempList[k],:].todense()-fa[i,:].todense())[0],sum_gradient)
    #                            #ss = 'train negent'+str(k)
    #                            #print ss
                            if (w[j,:]*fa[i,:].T)[0,0] - (w[j,:]*fa[k,:].T)[0,0] -1 <0:
                                w,sum_gradient = AdaGradUpdate(w,j,np.array(fa[k,:].todense()-fa[i,:].todense())[0],sum_gradient)
                    #如果存在negative type set
                    #tempList = negTypeSet.get(temp)
                    temps = fgmodel.getNegSet(i,j,'NegTypeSetColl','NegTypeSet')
                    temps = temps.strip()
                    tempList = map(int,temps.split('\t')) 
                    if tempList !=None:
                        lists = range(len(tempList)-1)
#                        nums = len(lists)/3
#                        if nums == 0:
#                            nums = len(lists)
                        slices = random.sample(lists,1)
                        for k in slices:
                            #ss = 'train negtype'+str(k)
                            #print ss
                            if (w[j,:]*fa[i,:].T)[0,0] - (w[tempList[k],:]*fa[i,:].T)[0,0] -1 <0:
                                w,sum_gradient = AdaGradUpdate(w,j,-np.array(fa[i,:].todense())[0],sum_gradient)
                                w,sum_gradient = AdaGradUpdate(w,tempList[k],np.array(fa[i,:].todense())[0],sum_gradient)
    return w,sum_gradient

entityNum=fg.featureGeneration.knowentNo
typeNum=fg.featureGeneration.typeNum
entFeatureDim=fg.featureGeneration.lnkmodel.entfeatureDim
fgmodel = fg.featureGeneration()
w,sum_gradient = LinearAdagrad(fgmodel)
#datas = fgmodel.getEntityTypeFeatures()
#negEntSet = fgmodel.getNegEntitySet(datas)
#negTypeSet = fgmodel.getNegTypeSet(datas)
dir_path = fg.linkmodel.linkmodel1.dir_path
f1 = open(dir_path+'/w_1.txt','w')
#f2 = open('sum_gradient','w')
wsize = w.shape
print wsize
for i in range(wsize[0]):
    for j in range(wsize[1]):
        f1.write(str(w[i,j])+"\t")
    f1.write('\n')
#sumgrad = sum_gradient.shape
#print sumgrad
#for i in range(sumgrad[0]):
#    for j in range(sumgrad[1]):
#        f2.write(str(sum_gradient[i,j])+"\t")
#    f2.write('\n')
#f1.close()
#f2.close()
