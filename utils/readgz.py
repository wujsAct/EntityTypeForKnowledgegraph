# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 19:33:21 2015

@author: wujs
"""

#read gz file

import gzip
import codecs
import sys
from getFreebaseType import FreebaseAPI

#return an gzip object so that we can get
def un_gz2gettype(file_name):
    """ungz zip file"""
    #创建gzip对象
    if 'gz' in file_name:
        fileobj = gzip.open(file_name)
    if 'txt' in file_name:
        fileobj = open(file_name)
    return fileobj
    
#def getthing2id(filename):
#    thing2id = {}
#    id2thing = {}
def getEnthasName(fileobj,ent_hasName):
    ent2name={}
    api = FreebaseAPI()
    fr =  codecs.open(dir_path+"ourdata/nyt/"+domains+"/id2entity.txt",'r','utf-8')
    f1 = codecs.open(ent_hasName,'w','utf-8')
    for line in fr.readlines():
        line = line.strip()
        items = line.split('\t')
        ent = items[1]
        mid = '/m/'+ent.split('ns/m.')[1].replace('>','')
        
        name = api.getSurfaceName(mid)
        
        if name!='None':
            ent2name[ent] = name
            print mid,name
    for key in ent2name:
        f1.write(key+'\t'+ent2name[key]+'\n')
    f1.close()                 
def gettype2id(fileobj):
    type2id_dict={}
    id2type_dict={}
    typeid2num_dict={}
    typeNo=1
    
    enttag = '<http://rdf.freebase.com/ns/m.'
    reltag = '<http://rdf.freebase.com/ns/type.object.type>'
    while 1:
        lines = fileobj.readlines(100000)
        if not lines:
            break
        for line in lines:       
            line = line.strip()
            items = line.split()
            if len(items)>=4:
                ent1 = items[0]
                rel = items[1]
                
                if enttag in ent1 and reltag in rel:
                    if type2id_dict.get(items[2]) == None:
                        type2id_dict[items[2]] = typeNo
                        id2type_dict[typeNo] = items[2]
                        typeid2num_dict[typeNo] = 1
                        typeNo = typeNo + 1
                        print typeNo
                    else:
                        typeId = type2id_dict[items[2]]
                        typeid2num_dict[typeId] = typeid2num_dict[typeId]+1
    f1 = open(dir_path+"ourdata/nyt/"+domains+"/id2type_tj.txt",'w')
    for i in range(typeNo-1):
        temp = i+1
        f1.write(str(temp)+'\t'+
        str(id2type_dict[temp])+'\t'+
        str(typeid2num_dict[temp])+'\n')
    f1.close()
    
#传递一个文件对象
def getentity2id(fileobj):
    entdict={}
    id2entdict={}
    entNo=1
    enttag = '<http://rdf.freebase.com/ns/m.'
    while 1:
        lines = fileobj.readlines(100000)
        if not lines:
            break
        for line in lines:
            line = line.strip()
            items = line.split()
            if len(items)>=4:
                ent1 = items[0]
                ent2 = items[2]
                if enttag in ent1 and entdict.get(ent1) ==None:
                    entdict[ent1] = entNo
                    id2entdict[entNo] = ent1   
                    entNo = entNo+1
                    print entNo
                if enttag in ent2 and entdict.get(ent2) == None:
                    entdict[ent2] = entNo
                    id2entdict[entNo] = ent2
                    entNo = entNo +1
                    print entNo
    
    f1 = open(dir_path+"ourdata/"+domains+"/id2entity.txt",'w')
    for i in range(entNo-1):
        temp = i + 1
        f1.write(str(temp)+"\t"+id2entdict[temp]+"\n")
        
    f1.close()

def getrel2id(fileobj):
    rel2id={}
    id2rel={}
    relNo =1
    enttag = '<http://rdf.freebase.com/ns/m.'
    #reltag = '<http://rdf.freebase.com/ns/film.'
    reltag = '<http://rdf.freebase.com/ns/food.'
    while 1:
        lines = fileobj.readlines(100000)
        if not lines:
            break
        for line in lines:
            line = line.strip()
            items = line.split()
            if len(items)>=4:
                ent1 = items[0]
                rel = items[1]
                ent2 = items[2]
                if enttag in ent1 and reltag in rel and enttag in ent2:
                    if rel2id.get(rel)==None:
                        rel2id[rel]=relNo
                        id2rel[relNo] = rel
                        relNo  = relNo + 1
                        print relNo
    
    f1 = open(dir_path+"ourdata/nyt/"+domains+"/id2rel.txt",'w')
    #f1 = open(dir_path+"ourdata/food/id2rel.txt",'w')
    for i in range(relNo-1):
        temp = i + 1
        f1.write(str(temp)+"\t"+id2rel[temp]+"\n")
    f1.close()

#获取这些cvt节点观察一下子！
def getEntisCVT(fileobj):  
    enttag = '<http://rdf.freebase.com/ns/m.'
    reltag = '<http://rdf.freebase.com/ns/type.object.type>'
    #f1 = open(dir_path+'ourdata/film/typeisCVT.txt')
    f1 = open(dir_path+'ourdata/food/typeisCVT.txt')
    typeisCVT =[]
    for line in f1.readlines():
        line = line.strip()
        items = line.split('/')
        strr = '/'+items[1]
        for i in range(2,len(items)):
            strr = strr+'.'+items[i]
        typeisCVT.append('<http://rdf.freebase.com/ns'+strr+'>')
    print typeisCVT
    extractanNode = {}
    while 1:
        lines = fileobj.readlines(100000)
        if not lines or len(extractanNode)==len(typeisCVT):
            break
        for line in lines:
            line = line.strip()
            items = line.split('\t')
            if len(items)>=4:
                ent1 = items[0]
                rel = items[1]
                ent2 = items[2]
                if ent2 in typeisCVT and reltag in rel:
                    if extractanNode.get(ent2) ==None:
                        extractanNode[ent2] = ent1
                        print line
                    print len(extractanNode)
    return extractanNode

def getCVTnodeInfo(fileobj,nodes,i):
    #enttag = '<http://rdf.freebase.com/ns/m.'
    #reltag = '<http://rdf.freebase.com/ns/type.object.type>'
    bufsize=0
    #f1 = open(dir_path+'ourdata/film/cvtnodes/cvtnode'+str(i)+'.txt','w',bufsize)
    f1 = open(dir_path+'ourdata/food/cvtnodes/cvtnode'+str(i)+'.txt','w',bufsize)
    while 1:
        lines = fileobj.readlines(100000)
        if not lines:
            break
        for line in lines:
            line = line.strip()
            items = line.split('\t')
            if len(items)>=4:
                ent1 = items[0]
                #rel = items[1]
                ent2 = items[2]
                if ent1 == nodes or ent2 == nodes:
                    print line                    
                    f1.write(line+'\n')
    f1.close()

def getEnt2Type(ent_hasName,output_file,fileobj):
    ent2name = {}
    fr = FreebaseAPI()
    with codecs.open(ent_hasName,'r','utf-8') as file:
        for line in file:
            line = line.strip()
            ent,name = line.split('\t')
            ent2name[ent] = name
    reltag = '<http://rdf.freebase.com/ns/type.object.type>'
    types = {}
    while 1:
        lines = fileobj.readlines(100000)
        if not lines:
            break
        for line in lines:
            line = line.strip()
            items = line.split('\t')
            ent1 = items[0]
            new_ent1 = '/m/'+ent1.split('m.')[-1].replace('>','')
            #print new_ent1
            rel = items[1]
            if ent2name.get(new_ent1) !=None and reltag in rel:
                typeoi = items[2]
                typei = items[2]
                typei = typei.split('ns/')[-1]
                typei = typei.replace('.','/')
                typei = '/'+typei.replace('>','')
                if types.get(typei)==None:
                    types[typei] = 1
                    print 'typei\t', typeoi,'\t',typei
                else:
                    types[typei] = types[typei] + 1
                temps = ent2name[new_ent1]+'\t'+typei
                ent2name[new_ent1] = temps
                #print new_ent1
    result = codecs.open(output_file,'w','utf-8')
    #result1 = codecs.open('moreresult','w','utf-8')
    moretype = codecs.open('moretypes.txt','w','utf-8')
    non_type = 0
    for key in ent2name:
        value= ent2name.get(key)
        lens = len(value.split('\t'))
       # print key
       # tags = '<http://rdf.freebase.com/ns/'
        names = value.split('\t')[0]
        if lens >= 2:
            result.write(key+'\t'+value+'\n')
        if  lens < 2:
            typess = fr.getTypesbyName(names)
            if typess !=None:
                print 'freebase api by name',typess
                strs = '\t'.join(typess)
                result.write(key+'\t'+names+'\t'+strs+'\n')
            else:
                typess = fr.getTypesbyId(key)
                if typess !=None:
                    print 'freebase api by id', typess
                    strs = '\t'.join(typess)
                    result.write(key+'\t'+names+'\t'+strs+'\n')
                else:
                    print 'can not get the result!'
                    non_type = non_type + 1
            if typess!=None:
                for typei in typess:
                        if types.get(typei)==None:
                            types[typei] = 1
                        else:
                            types[typei] = types[typei] + 1
                        
    print 'no type entity num:', non_type
    types_sorted = sorted(types.items(),key=lambda d:d[1])
    for key in types_sorted:
        moretype.write(key[0]+'\t'+str(key[1])+'\n')
    result.close()
    moretype.close()
    #result1.close()
    
dir_path = 'C:/Users/DELL/Desktop/'
domains = 'food'
ent_hasName = dir_path+'ourdata/nyt/'+domains+'/'+domains+'_enthasName.txt'
output_file = dir_path+'ourdata/nyt/'+domains+'/'+domains+'_enthasName_type.txt'
#g_file = un_gz2gettype(dir_path+'freebase-films.gz')

g_file = un_gz2gettype(dir_path+'ourdata/nyt/'+'freebase-'+domains+'.gz')
#getentity2id(g_file)
getEnthasName(g_file,ent_hasName)
#getEnt2Type(ent_hasName,output_file,g_file)

#gettype2id(g_file)
#getrel2id(g_file)
#entiscvts =  getEntisCVT(g_file)
#f_cvt = open(dir_path+'ourdata/film/entiscvt.txt','w')
#for key in entiscvts:
#    f_cvt.write(key+'\t'+entiscvts[key]+'\n')
#f_cvt.close()
#f1 = open(dir_path+'ourdata/film/entiscvt.txt')
#i=0
#for line in f1.readlines():
#    print i
#    line = line.strip()
#    items = line.split('\t')
#    print line
#    getCVTnodeInfo(g_file,items[1],i)
#    i = i + 1
tt ='111'
tt.strip
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.0100zby9>',1)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.01006ysx>',2)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.0gw7j3k>',3)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.0104gv33>',4)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.0100vq_m>',5)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.0100f487>',6)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.010dsl_0>',7)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.0jxj13b>',8)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.010g4hxk>',9)
#getCVTnodeInfo(g_file,'<http://rdf.freebase.com/ns/m.010fynhp>',10)
 
