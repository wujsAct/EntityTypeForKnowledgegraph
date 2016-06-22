# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 20:51:15 2016

@author: wujs
"""

import gensim,logging
import os
import nltk
import string

#如果输入分布在硬盘的多个文件中，文件的每一行是一个句子那么可以逐个文件，逐行输入
class MySentences():
    
    '''
    如果需要对文件中的单词做其他处理, 比如转换为unicode, 
    转换大小写, 删除数字, 抽取命名实体等, 所有这些都可以在MySentence迭代器中进行处理
    '''
    def __init__(self,dirname):
        print 'this is the inital function'
        self.dirname = dirname
#    
#    def CleanLines(self,line):
#        identify = string.maketrans('', '')
#        delEStr = string.punctuation +string.digits  #ASCII 标点符号，数字  
#        cleanLine = line.translate(identify,delEStr) #去掉ASCII 标点符号和空格
#        cleanLine =line.translate(identify,delEStr) #去掉ASCII 标点符号
#        return cleanLine
#    #从句子中抽取命名实体
#    #此处是根据relation去抽取左右的实体，因此具有更好的意义吧！
#    #需要对比用其他方法抽取的命名实体和用这种方法的差别吧！
#    #能不能把一个词组作为一个训练项，还需要看word2vec的论文，明早完成吧！
#    def get_NamedEntity(self):
#        return 0
#        
#    def delete_number(self,line):
#       words= line.split()
#       new_line = ''
#       for word_item in words:
#           #轻松判断是否为数字
#           if word_item.isdigit():
#               continue
#           else:
#               new_line = new_line+'\t'+word_item
#       return new_line
#       
    def genSen(self,context):
        sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')  
        sents = sent_tokenizer.tokenize(context)
        return sents
        
    def __iterss__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname,fname)):
                #need to parse
                line = line.strip()
                #replace '. , !' with '\t'                
                ids,context = line.split('\t')
                context = context.replace(' .',' . ')
                #此处我们需要按照'. !'将多个句子变成一个句子
                sentences = self.genSen(context)
                for sentence in sentences: 
                    #第一步：去掉符号
                    #line = self.CleanLines(sentence)
                    sentence = sentence.strip()
                    #第二步: 删除数字
                    #final_line = self.delete_number(line)
                    yield sentence
                   # yield context.split()

#dir_path = 'C:/Users/wujs/Desktop/ourdata/typePropagation_50k'
#sentences = MySentences(dir_path+'/context')
sentences = MySentences('d://data/')
#for i in sentences.__iterss__():
#    print i
#sentences.__iterss__()
#an empty mode, no training
model = gensim.models.Word2Vec()
model.build_vocab(sentences.__iterss__())
model.train(sentences.__iterss__())





#can be a non-repateable, 1-pass generator
#model.build_vocab()
