# -*- coding: utf-8 -*-
__author__ = 'wujs'
#date:2015/11/11
import numpy as np
import linkmodel
import math

models = linkmodel.linkmodel
dir_path = models.dir_path
#get the entity standard type
def getEntRightType(missentNum,fileaddr=dir_path+"/entity_missingtype_c.txt1", entity2idf=dir_path+"/entity_missingtype.txt1"):
    f1 = open(fileaddr,'r')
    entType_dict={}
    for line in f1.readlines():
        line = line.strip()
        ent,type1 = line.split("\t")
        if entType_dict.get(ent) ==None:
            entType_dict[ent]=type1
        else:
            key = entType_dict.get(ent)
            key_new = key+"_"+type1
            entType_dict[ent]=key_new
    entity2id ={}
    id2entity={}

    f2 = open(entity2idf,'r')
    i=0;
    for line in f2.readlines():
        line = line.strip()
        ent = line
        entity2id[ent]=i
        id2entity[i]=ent
        i = i + 1
    return entType_dict,entity2id,id2entity

#计算precision


#def gettypeMAP(typeNum, entityNum, entType_dict, entity2id,id2entity,fileaddr='E:/lunwen/source_code/ourmodels/entity/data/yelp'+"/results_clustype_pretype.txt"):
def gettypeMAP(typeNum, entityNum, entType_dict, entity2id,id2entity,fileaddr=dir_path+"/pretype"):
#def gettypeMAP(typeNum, entityNum, entType_dict, entity2id,id2entity,fileaddr=dir_path+"/pretype_DCD"):
#def gettypeMAP(typeNum, entityNum, entType_dict, entity2id,id2entity,fileaddr='E:/lunwen/source_code/ourmodels/entity/data/yelp'+"/figer_pretype.txt"):
    #datamat = sio.loadmat(fileaddr)
    real_cluster = np.zeros((typeNum,1))
    pre_cluster = np.zeros((typeNum,1))
    cross_cluster = np.zeros((typeNum,1))
    #data = datamat['Xunk']
    data = np.loadtxt(fileaddr)
    y_true= np.zeros((entityNum, typeNum))

    for key in entType_dict:
        ent_id = entity2id[key]
        for t in entType_dict[key].split("_"):
            type_id = int(t) -1 
            y_true[ent_id,type_id]=1
            real_cluster[type_id] = real_cluster[type_id] + 1

    top =-2
    all_average = 0.0
    has_righttype =0
    for i in range(entityNum):
         y_score={}
         for j in range(typeNum):
            #print data[i*typeNum+j]
            y_score[j]=data[i*typeNum+j]
         #对字典排序
         y_score = sorted(y_score.items(), key=lambda y_score:y_score[1],reverse=True)
         true_pred = 0
         for i1 in range(typeNum):
             trr = float(y_score[i1][1])
#             trr =  float(-y_score[i1][1])
#             print trr
#             if trr >700:
#                 break
#             temp = 1.0/(1+math.exp(trr))
             if trr>=0:
                 top = i1
         top =top+1
         if top >typeNum:
             top = typeNum
         print 'top',top
         if top>0:
             t = np.zeros((top,1))
             for j in range(top):
                 typeid = y_score[j][0]
                 pre_cluster[typeid] = pre_cluster[typeid] + 1
                 
                 if y_true[i][typeid] == 1:
                     cross_cluster[typeid] = cross_cluster[typeid] + 1
                     true_pred = true_pred + 1
                     t[j] = true_pred/float((j+1))
            
             if sum(t)==0:
                 print i,t
                 print y_score
                 print np.nonzero(y_true[i,:])
                 continue
             else:
                 has_righttype = has_righttype + 1
    #             print i,t
    #             print y_score
    #             print y_true[i,:]
                 all_average = all_average + sum(t)/true_pred
    meanap = all_average/has_righttype
    print 'has_righttype',has_righttype
    
    averagep = 0
    averager = 0
    ttt = 0
    for i in range(typeNum):
        if real_cluster[i,0]!=0 and pre_cluster[i,0]!=0:
            ttt = ttt + 1
            print 'rel_cluster',real_cluster[i,0]
            averagep = averagep + cross_cluster[i,0]/pre_cluster[i,0]
            averager = averager + cross_cluster[i,0]/real_cluster[i,0]
            print 'type',i
            p = cross_cluster[i,0]/pre_cluster[i,0]
            r = cross_cluster[i,0]/real_cluster[i,0]
            print 'p:', p
            print 'r',r
            print 'f1',2*p*r/(p+r)
    print averagep/ttt
    print averager/ttt
    print meanap
    return meanap
    
#missentNum=200;typeNum=15
missentNum=460;typeNum=32
#missentNum=100;typeNum=30
#missentNum = 20; typeNum = 10;
#missentNum = 90 ;typeNum =60;
entType_dict,entity2id,id2entity =  getEntRightType(missentNum)       
meanap = gettypeMAP(typeNum, missentNum, entType_dict, entity2id,id2entity)

#null_type_list =[]
###由于抽取出的数据不是每个实体都分配到cluster中了
#total = 0
#for i in range(typeNum):
#    if sum(y_true[:,i])==0:
#        null_type_list.append(i)
#
#
#
#delete_type_size = len(null_type_list)
#y_true_new = np.zeros((missentNum,typeNum-delete_type_size))
#y_score_new = np.zeros((missentNum,typeNum-delete_type_size))
#k=0
#for i in range(typeNum):
#    if i not in null_type_list:
#        y_true_new[:,k] = y_true[:,i]
#        y_score_new[:,k] = y_score[:,i]
#        k=k+1
#
#print average_precision_score(y_true_new,y_score_new,average='weighted')