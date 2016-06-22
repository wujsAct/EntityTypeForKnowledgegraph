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
def AdaGradUpdate(iterNo,w,t,fa_wt_dense,sum_gradient,learn_rate=0.01):
    
    tempse_error= np.linalg.norm(fa_wt_dense)
    #if iterNo%50==0:
        #print 'type',t,'\t','error:',tempse_error
    if tempse_error >1e-12:
        w_t = w[t,:].toarray()[0]
        SumGradT = sum_gradient[t,:].toarray()[0]
        if t==0:
            for i in range(len(w_t)):            
                w[t,i] = w_t[i]-(learn_rate)*fa_wt_dense[i]
        else:
            SumGradT = sum_gradient[t,:].toarray()[0]
            for i in range(len(w_t)):
                if SumGradT[i] == 0:
                    w[t,i] = w_t[i]-(learn_rate)*fa_wt_dense[i]
                else:
                    w[t,i] = w_t[i]-(learn_rate/np.sqrt(SumGradT[i]))*fa_wt_dense[i]
        #update the sum_gradient
        tempSumGradT = SumGradT + [each**2 for each in fa_wt_dense]
        i=range(len(w_t))
        sum_gradient[t,i] = tempSumGradT[i]
    return w,sum_gradient

def LinearAdagrad(fgmodel):
    fa = fgmodel.getEntFeature()
    datas = fgmodel.getEntityTypeFeatures()
    sum_gradient = initx(typeNum,entFeatureDim)
    w = initx(typeNum,entFeatureDim)
    for maxIter in range(1):
        print 'yelp r500 maxIter:',maxIter
        for i in range(entityNum):
            #print i
            if i % 100 ==0:
                print i
            for j in range(typeNum):
                if(datas[i,j]==1):
                    #tempList = negEntSet.get(temp)
                    temps = fgmodel.getNegSet(i,j,'NegEntitySetColl','NegEntitySet')
                    
                   #如果存在negative entity set
                   #此处负例实在太多，我们仅需随机抽取100个去做训练，看下效果
                    if temps !=None:
                        temps = temps.split('\t')
                        lists = range(len(temps)-1)
                        nums=max(1,len(lists)/10)
                        slices = random.sample(lists,nums)
                       
                        for kr in slices:
                            k = int(temps[kr])
                            if (w[j,:]*fa[i,:].T)[0,0] - (w[j,:]*fa[k,:].T)[0,0] -1 <0:
                                w,sum_gradient = AdaGradUpdate(i,w,j,np.array(fa[k,:].todense()-fa[i,:].todense())[0],sum_gradient)
                    #如果存在negative type set
                    temps = fgmodel.getNegSet(i,j,'NegTypeSetColl','NegTypeSet')
                    temps = temps.strip()
                    tempList = map(int,temps.split('\t')) 
                    if tempList !=None:
                        lists = range(len(tempList)-1)
                        nums=max(1,len(lists)/10)
                        slices = random.sample(lists,nums)
                        for k in slices:
                            if (w[j,:]*fa[i,:].T)[0,0] - (w[tempList[k],:]*fa[i,:].T)[0,0] -1 <0:
                                w,sum_gradient = AdaGradUpdate(i,w,j,-np.array(fa[i,:].todense())[0],sum_gradient)
                                w,sum_gradient = AdaGradUpdate(i,w,tempList[k],np.array(fa[i,:].todense())[0],sum_gradient)
    return w,sum_gradient

entityNum=fg.featureGeneration.knowentNo
typeNum=fg.featureGeneration.typeNum
entFeatureDim=fg.featureGeneration.lnkmodel.entfeatureDim
fgmodel = fg.featureGeneration()
w,sum_gradient = LinearAdagrad(fgmodel)
dir_path = fg.linkmodel.linkmodel1.dir_path
f1 = open(dir_path+'/w_1.txt','w')
wsize = w.shape
print wsize
for i in range(wsize[0]):
    for j in range(wsize[1]):
        f1.write(str(w[i,j])+"\t")
    f1.write('\n')