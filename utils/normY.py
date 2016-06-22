# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:19:51 2015

@author: DELL
"""
from cvxopt import spmatrix
import numpy as np

def normY(Y):
    f1 = open(filenormy,'w')
    for i in range(entityNum):
        print 'i',i
        for j in range(relNum):
            yi1 = j*typeNum
            #yi2 = (j+1)*typeNum
            temp = 0
            for i1 in range(typeNum):
                temp = temp + Y[i,yi1+i1]
            if temp !=0:
                for k in range(typeNum):
                    value = Y[i,j*typeNum+k]
                    if value !=0:
                        Y[i,j*typeNum+k] = value/temp
                        f1.write(str(i)+'\t'+str(j*typeNum+k)+'\t'+str(Y[i,j*typeNum+k])+'\n')
    f1.close()
    
    

if __name__ == '__main__':
  #just need to change the variation to get the norm for other datas  
    Yf = 'C:/Users/wujs/Desktop/ourdata/matlabpro_60/knowY.txt'
    entityNum = 12659;relNum = 1118 * 2;typeNum=60;
   # entityNum = 13921;typeNum =50;relNum =1978;
    filenormy = 'C:/Users/wujs/Desktop/ourdata/matlabpro_60/knowY_norm.txt'
    knowy = np.loadtxt(Yf)
    Y = spmatrix(knowy[:,2],map(int,(knowy[:,0]-1).tolist()),
                     map(int,(knowy[:,1]-1).tolist()),
                     size=(entityNum,typeNum*relNum))
    normY(Y)
    
    