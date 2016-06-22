# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 08:51:31 2015

@author: wujs
"""

from cvxopt import spmatrix,solvers,matrix
import linkmodel
import numpy as np
## Define QP parameters (directly)
#P = matrix([[1.0,0.0],[0.0,0.0]])
#q = matrix([3.0,4.0])
#G = matrix([[-1.0,0.0,-1.0,2.0,3.0],[0.0,-1.0,-3.0,5.0,4.0]])
#h = matrix([0.0,0.0,-15.0,100.0,80.0])
## Define QP parameters (with NumPy)
#P = matrix(numpy.diag([1,0]), tc='d')
#q = matrix(numpy.array([3,4]), tc='d')
#G = matrix(numpy.array([[-1,0],[0,-1],[-1,-3],[2,5],[3,4]]), tc='d')
#h = matrix(numpy.array([0,0,-15,100,80]), tc='d')
## Construct the QP, invoke solver
#sol = solvers.qp(P,q,G,h)
## Extract optimal value and solution
#sol['x'] # [7.13e-07, 5.00e+00]
#sol['primal objective'] 
class QPmodelAb:
    
    lnkmodel=linkmodel.linkmodel()
    entityNum = lnkmodel.entityNum
    relNum = lnkmodel.relNum
    typeNum = lnkmodel.typeNum
    rel_type = relNum*typeNum  
    dir_path = lnkmodel.dir_path
    resultA_file =  dir_path+"/A.txt"
    resultb_file =  dir_path+"/b.txt"
    X1 = linkmodel.X
    knowtypeEntity = linkmodel.linkmodel1.knowtypeEntity
    X =X1[knowtypeEntity[:,0].tolist(),:]
    Y1 = linkmodel.Y
    Y = Y1[knowtypeEntity[:,0].tolist(),:]
    knowentNo = linkmodel.linkmodel1.knowentNo
    
    
    def trainAbQP(self,HAb,fAb):
        print 'start to train!!!'
        rel_type = self.rel_type
        typeNum = self.typeNum
     #   q = fAb.T
        f1= open(self.resultA_file,'w')
        f2= open(self.resultb_file,'w')
        q = matrix(fAb.T,tc='d')
        sol = solvers.qp(HAb,q)
        result = sol['x']
#        for i in range(len(result)):
#            print i
#            f1.write(str(result[i]+'\n')
#        f1.close()
        tag = 0
        for i in range(rel_type):
            for j in range(typeNum):
                if result[tag] !=0:
                    f1.write(str(i)+'\t'+str(j)+'\t'+str(result[tag])+'\n')
                tag = tag+1
        f1.close()
        print 'tag',tag
        for i in range(rel_type):
            f2.write(str(result[tag])+'\n')
            tag = tag+1
        print 'tag',tag
        f2.close()
        print sol['primal objective']
        
    def getAb_to_A(self):
        rows = []
        cols = []
        value =[]
        rel_type = self.rel_type
        typeNum = self.typeNum
        
    
        ktt = rel_type*typeNum
        ktt1 = rel_type*(typeNum+1)
        for i in range(ktt):
            rows.append(i)
            cols.append(i)
            value.append(1)
        Ab_to_A = spmatrix(value, rows, cols,size=(ktt,ktt1))
        return Ab_to_A
    
    def getAb_to_b(self):
        rows=[]
        cols=[]
        value=[]
        rel_type = self.rel_type
        typeNum = self.typeNum
        ktt = rel_type*typeNum
        ktt1 = rel_type*(typeNum+1)
        for i in range(ktt,ktt1):
            print i-ktt
            rows.append(i-ktt)
            cols.append(i)
            value.append(1)
        Ab_to_b = spmatrix(value, rows, cols,size=(rel_type,ktt1))
        return Ab_to_b
    
    def getHessianAbD1(self):
        f1 = open(self.lnkmodel.dir_path+'/D1.txt','w')
        row = 0
        rel_type = self.rel_type
        typeNum = self.typeNum
        #the first part of hessianAb
        X = self.X
        for k in range(typeNum):
            print k
            for l in range(typeNum):
                tm = X[:,k].T*X[:,l]
                temp =tm[0,0]
                #print 'temp',temp
                if temp!=0:
                    for i in range(rel_type):
                 #       print row
                        row = row+1
                        f1.write(str(k*rel_type+i)+'\t'+str(l*rel_type+i)+'\t'+str(temp)+'\n')
            #D1 = spmatrix(value, row, col,size=(ktt,ktt))
        f1.close()
            
    #def the hessianAb that's P
    #the hessian is very big, so we need to write the storage and then to extract!
    def getHessianAb(self,Ab_to_A,Ab_to_b):
        #entityNum = self.entityNum
        knowentNo = self.knowentNo
        rel_type = self.rel_type
        typeNum = self.typeNum
        ktt = typeNum*rel_type
        ktt1 = rel_type*(typeNum+1)
        print 'get HessianAb'
        D1f= np.loadtxt(self.dir_path+'/D1.txt',dtype='int')
        D1 = spmatrix(D1f[:,2].tolist(),D1f[:,0].tolist(),D1f[:,1].tolist(),size=(ktt,ktt))
        H1 = Ab_to_A.T*D1*Ab_to_A
        print 'H1,H2'
        row = []
        col = []
        value=[]
        X = self.X
        #the second part of hessian
        for i in range(typeNum):
            print i
            temp = sum(X[:,i].V)
            for j in range(rel_type):
                row.append(j)
                col.append(i*rel_type+j)
                value.append(temp)
        D2 = spmatrix(value, row, col,size=(rel_type,ktt))        
        H2 = -2*Ab_to_b.T*D2*Ab_to_A
        
        H3=knowentNo*Ab_to_b.T*Ab_to_b
        Hab = H1 + H2 +H3
        Hab = Hab+Hab.T
        f1 = open(self.lnkmodel.dir_path+'/Hab.txt','w')
        for i in range(ktt1):
            for j in range(ktt1):
                if Hab[i,j]!=0:
                    f1.write(str(i+1)+"\t"+str(j+1)+"\t"+str(Hab[i,j])+'\n')
        f1.close()
        
        
        return Hab
        
    def getfAb(self,Ab_to_A,Ab_to_b):
        print 'getfAb'
        X = self.X
        Y = self.Y
        rel_type = self.rel_type
        typeNum = self.typeNum
#        entityNum = self.entityNum
        knowentNo = self.knowentNo
        ktt = rel_type*typeNum
        row1 = []
        col1 = []
        row2 = []
        col2 = []
        value1=[]
        value2=[]
        for i in range(ktt):
            row1.append(0)
            col1.append(i)
        for i in range(rel_type):
            row2.append(0)
            col2.append(i)
            
           # value.append(0)
        
        #D1 = matrix(0,(1,ktt))
        #print D1[0:220]
        for k in range(typeNum):
            print k
            #for i in range(entityNum):
            for i in range(knowentNo):
                tempd = X[i,k]*Y[i,:]
                if i ==0:
                    temp = tempd
                else:
                    temp = temp + tempd   
            for j in range(rel_type):
                value1.append(temp[0,j])
                
        for i in range(knowentNo):
            if i==0:
                tempf2d = Y[i,:]
            else:
                tempf2d = tempf2d +Y[i,:]     
        for i in range(rel_type):
            value2.append(tempf2d[0,i])
                
        D1 = spmatrix(value1,row1,col1,size=(1,ktt))       
        f1 = -2*D1*Ab_to_A
        
        D2 =  spmatrix(value2,row2,col2,size=(1,rel_type)) 
        
        f2 = 2*D2*Ab_to_b
        
        f = f1+f2
        
#        f1f = open(self.lnkmodel.dir_path+'/fab.txt','w')
#        ktt1 = rel_type*(typeNum+1)
#        for i in range(ktt1):
#            f1f.write(str(f[0,i])+'\n')
#            
#        f1f.close()
        return f
    def yuxiang(self):
        Y = self.Y
        total = 0
        knowentNo = self.knowentNo
        for i in range(knowentNo):
            total = total + Y[i,:]*Y[i,:].T
         
        return total
        
    def printX(self):
        X = self.X
        f1 = open(self.dir_path+'/knowX.txt','w')
        typeNum= self.typeNum
        knowentNo = self.knowentNo
        for i in range(knowentNo):
            for j in range(typeNum):
              if X[i,j] !=0:
                  f1.write(str(i+1)+'\t'+str(j+1)+'\t'+str(X[i,j])+'\n')
                  
            
#relNum = 22; typeNum =10; entityNum =1415
##relNum = 2; typeNum =3; entityNum =5
#rel_type = relNum*typeNum

#X = main.getX()
qpab = QPmodelAb()
Ab_to_A = qpab.getAb_to_A()
Ab_to_b = qpab.getAb_to_b()
#qpab.getHessianAbD1()
HAb= qpab.getHessianAb(Ab_to_A,Ab_to_b)
fAb= qpab.getfAb(Ab_to_A,Ab_to_b)
qpab.trainAbQP(HAb,fAb)
total = qpab.yuxiang()
#qpab.printX()