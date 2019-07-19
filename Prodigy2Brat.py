# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 09:50:12 2019

@author: yzhao
"""

'This script is to transform the format of annotation from Prodigy to the format witch can be used by Brat'

import json
import sys
import os
import re

'Raed the annotation'
#inputname=sys.argv[1]  #the input file to check
#outputname=sys.argv[2] #the output file to save the result

inputname='crypto2pre.jsonl'
ficher_name=inputname.split('.')[0]
if os.path.isdir(ficher_name):
    pass
else:
    os.mkdir(ficher_name)

inputhash=1

with open(inputname,'rb') as file:
    lines=[line for line in file.readlines()]
    for line in lines:
        doc=json.loads(line)
        #        if doc['answer']=='accept':
        text=doc['text']
        text=re.sub(r'\n','#',text)
        spans=doc['spans']
#        inputhash=str(doc['_input_hash'])
        tokenlist=doc['tokens']
        textname=str(inputhash)+'.txt'
        annoname=str(inputhash)+'.ann'
        inputhash=inputhash+1   

        annotationlist=[]
        i=1
        for span in spans:
#            token_start=span['token_start']
#            token_end=span['token_end']
            start=span['start']
            end=span['end']
            label=span['label']
            token=''
#            if token_start==token_end:
#                token=token+tokenlist[token_start]['text']
##                end=tokenlist[token_start]['end']
#            else:
#                while token_start<=token_end:
#                    token=token+tokenlist[token_start]['text']+' '
#                    token_start=token_start+1
#                    end=tokenlist[token_start]['end']
#            token=re.sub(r'\s+','  ',token)
            annotation='T'+str(i)+'\t'+label+' '+str(start)+' '+str(end)+'\t'
            annotationlist.append(annotation)
            i=i+1
            
        with open(ficher_name+'\\'+textname,'w',encoding="utf-8") as textfile:
            textfile.write(text)
        with open(ficher_name+'\\'+annoname,'w',encoding="utf-8") as annofile:
            for item in annotationlist:
                annofile.write(item)
                annofile.write('\n')
        