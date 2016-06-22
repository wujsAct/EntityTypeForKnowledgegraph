# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 17:57:29 2015

@author: wujs
"""
import math
import numpy as np
import linkmodel
from scipy.sparse import dok_matrix
import featureGeneration as fg
lnkmodel = linkmodel.linkmodel

dir_path = lnkmodel.dir_path
f1 = open(dir_path+'/w_1_DCD.txt')
entityNum = lnkmodel.knowentNo
featureNum = lnkmodel.entfeatureDim
typeNum = lnkmodel.typeNum
w = np.zeros((typeNum,featureNum),dtype='float')
fgmodel = fg.featureGeneration()
datas = fgmodel.getUntypeEntFeature()
datas1 = fgmodel.Y
print np.shape(datas)
#yuanshuju = fgmodel.getEntityTypeFeatures()
lineno = 0
nans = 0
for line in f1.readlines():
    line = line.strip()
    t  = line.split('\t')
    for i in range(len(t)):
        if math.isnan(float((t[i]))):
            nans = nans + 1
        w[lineno,i] = float(t[i])
    lineno = lineno+1
    print lineno
print 'nans',nans
print np.shape(w)
print np.shape(datas)
#dir_path = lnkmodel.dir_path
f3 = open(dir_path+'/pretype_DCD','w')
f4 = open('quan0feature_dcd.txt','w')
for i in range(lnkmodel.missent):
    print i
    temps = 0
    for j in range(featureNum):
        temps = temps + datas[i,j]
    if temps==0:
        print 'sum i is zeros',i
        f4.write(i)
    else:
        
        for j in range(typeNum):
            tempdata = datas[i].toarray()[0]
#            print 'data shape',np.shape(tempdata)
#            print 'w shape',np.shape(w[j])
            temp = w[j]
            score = np.dot(tempdata,temp)
#            for j1 in range(featureNum):
#                if datas[i,j1] !=0 and w[j,j1]!=0:
#                    score = score + datas[i,j1] * w[j,j1]
            f3.write(str(score)+"\n")
#    f3.write("\n")
f3.close()
f4.close()

#for i in range(10):
#    for j in range(typeNum):
#        f4.write(str(yuanshuju[i,j])+'\t')
#    f4.write('\n')
#f4.close()
#for i in range(90):
#    print i
#    temps = 0
#    for j in range(featureNum):
#        temps = temps + datas[i,j]
#    if temps==0:
#        print 'sum i is zeros',i
#        f4.write(i)