# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 17:10:47 2019

@author: yzhao
"""

import json

file=r'C:\NLP\Datasets\dividend\Row1ipoaprouvedr2.json'
newfile=r'C:\NLP\Datasets\dividend\Row1ipoaprouved3.json'


with open(file,'r',encoding='utf8') as f:
    data=f.read()
    JsonObj=json.loads(data)

newjson=[]  
for elem in JsonObj:
    newdic={}
    title=elem['title']
    content=elem['text']
    articleid=elem['ID']
    full_text=title+'\n'+content
    newdic['text']=full_text
    newdic['ID']=articleid
    newjson.append(newdic)
    

with open(newfile,'w',encoding='utf8') as w:
    for item in newjson:
        w.write(json.dumps(item))
        w.write('\n')
    