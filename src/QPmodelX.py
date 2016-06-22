# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:26:47 2015

@author: wujs
"""
from cvxopt import spmatrix,solvers,matrix
import linkmodel
import numpy as np

class QPmodelX:
    
    lnkmodel=linkmodel.linkmodel()
    entityNum = lnkmodel.entityNum
    relNum = lnkmodel.relNum
    typeNum = lnkmodel.typeNum
    rel_type = relNum*typeNum  
    dir_path = lnkmodel.dir_path
    missent = lnkmodel.missent  
    
#    X1 = linkmodel.X
    untypeEntity = lnkmodel.untypeEntity
#    X =X1[map(int,untypeEntity.tolist()),:]
    Y1 = linkmodel.Y
    Y = Y1[map(int,untypeEntity.tolist()),:]
    af = np.loadtxt(dir_path+'/A.txt')
    A = spmatrix(af[:,2],map(int,af[:,0].tolist()),
                 map(int,af[:,1].tolist()),
                 size=(rel_type,typeNum))
    bf = np.loadtxt(dir_path+'/b.txt')
    b = matrix(bf)
    resultX =  dir_path+"/result.txt"    
    
    
    def trainXQP(self,Hx,fx,G,H,A,b):
        sol = solvers.qp(Hx,fx,G,H)
        f = open(self.resultX,'w')
        result = sol['x']
        for i in range(len(result)):
            f.write(str(result[i])+'\n')
        f.close()
        print sol['primal objective']
    
    def getHessianXf(self):
        dir_path = self.dir_path
        f1 = open(dir_path +'/Hx.txt','w')
        A = self.A
        Hf = A.T* A
        typeNum = self.typeNum
        missent = self.missent
        for k in range(missent):
            print k
            for i in range(self.typeNum):
                for j in range(self.typeNum):
                    temp = Hf[i,j]
                    if temp !=0:
                        row = k*typeNum+i
                        col = k*typeNum+j  
                        f1.write(str(row)+'\t'+str(col)+'\t'+str(temp)+'\n')
        f1.close()
    def getHessianX(self):
        dir_path = self.dir_path
        typeNum = self.typeNum
        missent = self.missent
        hxf= np.loadtxt(dir_path+'/Hx.txt')
        Hx = spmatrix(hxf[:,2],map(int,hxf[:,0].tolist()),
                     map(int,hxf[:,1].tolist()),
                     size=(typeNum*missent,typeNum*missent))
        H = Hx+Hx.T
        return H
        
    def getfX(self):
        missent= self.missent
        typeNum = self.typeNum
        Y= self.Y
        A = self.A
        b = self.b
        b = b.T
        fx1 = matrix(0,(missent*typeNum,1),tc='d')
        for i in range(missent):
            fx1[i*typeNum:(i+1)*typeNum,0]= (Y[i,:]*A).T
        
        fx = -2 * fx1
        
        for i in range(missent):
            fx[i*typeNum:(i+1)*typeNum,0] = fx[i*typeNum:(i+1)*typeNum,0] -2*(b*A).T
        
        return fx
    def getGx(self):
        missent= self.missent
        typeNum = self.typeNum
       
        row=[]
        col=[]
        val=[]
        rowNo = 0
        colNo = 0
        h = []
        for i in range(missent*typeNum):
            row.append(rowNo)
            col.append(colNo)
            val.append(-1)
            h.append(0)
            # rowNo = rowNo + 1
            # row.append(rowNo)
            # col.append(colNo)
            # val.append(-1) 
            # h.append(0)
            colNo = colNo + 1
            rowNo = rowNo+1
        G = spmatrix(val,row,col,size=(missent*typeNum,missent*typeNum),tc='d')
        
        H = matrix(h,tc='d')        
        return G,H
        
    def getAx(self):
        missent= self.missent
        typeNum = self.typeNum
        row=[]
        col=[]
        val=[]
        for i in range(missent):
            for j in range(typeNum):
                row.append(i)
                col.append(i*typeNum+j)
                val.append(1)
        A = spmatrix(val,row,col,size=(missent,missent*typeNum),tc='d')
        b = matrix(1,size=(missent,1),tc='d')
        return A,b
qpX = QPmodelX()
#just need to recompute before the model
qpX.getHessianXf()
Hx = qpX.getHessianX()
fx = qpX.getfX()
G,H = qpX.getGx()
A,b = qpX.getAx()
qpX.trainXQP(Hx,fx,G,H,A,b)