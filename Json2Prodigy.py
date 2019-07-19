# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 10:43:39 2019

@author: yzhao
"""

'Json2Prodigy'
'This program is to transform the Json file from Brat to the format prodigy'

import json
import spacy
import re

nlp=spacy.load('en_core_web_sm')

filename='selectbratjson25032019.jsonl'

with open(filename,'r',encoding='utf8') as f:
    doc=f.readlines()

event=[]
spans=[]
newdic={}
for annotation in doc:
    dic=json.loads(annotation)
    text=dic['text']
    text=re.sub(r'#','\n',text)
    lis_tokens= nlp(text)
    tokens=[]
    startnumer=[]
    endnumber=[]
    for token in range (0, len(lis_tokens)):
        tokens.append({"text":lis_tokens[token].text, "start": lis_tokens[token].idx, "end": (lis_tokens[token].idx+len(lis_tokens[token].text)), "id":token})
        for element in tokens:
            startnumer.append(element['start'])
            endnumber.append(element['end'])  
    for item in dic['events']:
        if len(dic['events']):
            #event.append(item[0])
            span={}
            span['start']=int(item['event_start'])
            span['end']=int(item['event_end'])
            span['label']=item['event_label']    
            if span['start'] in startnumer:
                pass
            else:
                newstart=min(startnumer,key=lambda x:abs(x-span['start']))
                span['start']=newstart
            if span['end'] in endnumber:
                pass
            else:
                newend=min(endnumber,key=lambda x:abs(x-span['end']))
                span['end']=newend
            spans.append(span)
    if len(dic['events']):
        newdic['text']=text
        newdic['spans']=spans
        newdic['tokens']=tokens
        with open('prodigy25032019.jsonl','a+',encoding='utf8') as f:
            jsonObj=json.dumps(newdic)
            f.write(jsonObj)
            f.write('\n')
        
    spans=[]
    event=[]

    
   