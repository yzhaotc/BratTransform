# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 15:00:55 2019

@author: yzhao
"""

'''This script is to transform the Brat annotation to Json format in order to using in the event model training'''

import json
import os
from optparse import OptionParser
import pandas as pd


'The list of label of entity'
entity_list=["PERSON" ,"GPE", "LOC","FAC", "ORG","COMPANY", "PRODUCT", "COMMODITY","CURRENCY","INDEX", "TOPIC","ECO_IND", "EVENT"]


parser=OptionParser()
parser.add_option("-I", dest="Inpath",help="Input Path of Brat annotation")
parser.add_option("-O", dest="Outpath",help="Output Path of the Json file ")
options, arguments = parser.parse_args()


path=options.Inpath
outpath=options.Outpath

path=r'C:\NLP\operation\Prodigy2Brat\18072019'
outpath='18072019.jsonl'

'Read the name in the folder'
namelist=os.listdir(path)
numberlist=[]
jsonObj={}
for name in namelist:
    filename,filetype=name.split('.')
    numberlist.append(filename)
numberlist=list(set(numberlist))

for number in numberlist:
    elementlist=[]
    span=[]
    eventlist=[]
    relationlist=[]
    attributelist=[]
    print(number)
    textname=path+'\\'+number+'.txt'
    annoname=path+'\\'+number+'.ann'
    with open(textname,'r',encoding="utf8") as t:
        text=t.read()
#        text.replace("\xc2\xa0"," ")
    with open(annoname,'r',encoding='utf8') as a:
        annotation=a.readlines()
    for element in annotation:
        elementlist.append(element.split())
    for item in elementlist:
        dic_span={}
        dic_event={}
        dic_ralation={}
        dic_attribute={}
        'Generate the span for Entity'        
        if 'T' in item[0] and item[1] in entity_list:
            dic_span['id']=item[0]
            dic_span['label']=item[1]
            dic_span['start']=int(item[2])
            dic_span['end']=int(item[3])
            dic_text=''
            for m in range(4,len(item)):
                dic_text=dic_text+item[m]+' '
            dic_span['text']=dic_text
            span.append(dic_span)
        'Generate Event'    
        if 'E' in item[0]:
            event=[]
            relation=[]
            dic_event['event_ID']=item[0]
            event_label,event_order=item[1].split(':')
            dic_event['event_label']=event_label
            for xiang in elementlist:
                if xiang[0]==event_order:
                    dic_event['event_start']=int(xiang[2])
                    dic_event['event_end']=int(xiang[3])
                    event_text=''
                    for m in range(4,len(xiang)):
                        event_text=event_text+xiang[m]+' '
                    dic_event['event_text']=event_text
            eventlist.append(dic_event)
            dic_event={}
            for i in range(2,len(item)):
                Arg_relation,Arg_order=item[i].split(':')
                Argname='Arg'+str(i-1)
                dic_ralation['label']=Arg_relation
                dic_ralation['R_EventID']=item[0]
                dic_ralation['R_ArgId']=Arg_order
#                for itemitem in elementlist:
#                    if itemitem[0]==Arg_order:
#                        dic_ralation[Argname+'_start']=int(itemitem[2])
#                        dic_ralation[Argname+'_end']=int(itemitem[3])
#                        dic_ralation[Argname+'_text']=itemitem[4]
#                        dic_ralation[Argname+'_label']=itemitem[1]
                relationlist.append(dic_ralation)
                dic_ralation={}
        
        if 'A' in item[0]:
            dic_attribute['attribute_ID']=item[0]
            dic_attribute['attribute_type']=item[1]
            dic_attribute['master_ID']=item[2]
            dic_attribute['attribute_text']=item[3]
            attributelist.append(dic_attribute)
            dic_attribute={}
#            eventlist.append(event)
#            relationlist.append(relation)
    

    df_eventlist=pd.DataFrame(eventlist)
    for attribute in attributelist:
        master_id=attribute['master_ID']
        attribute_text=attribute['attribute_text']
        old_eventtest=df_eventlist[df_eventlist['event_ID']==master_id]['event_label'].values[0]
        new_eventtest=old_eventtest+'_'+attribute_text
        df_eventlist.loc[df_eventlist['event_ID']==master_id,'event_label']=new_eventtest
    
    
    eventlist=df_eventlist.to_dict('records')


    jsonObj['text']=text
    jsonObj['spans']=span
    jsonObj['events']=eventlist
    jsonObj['relation']=relationlist
    with open(outpath,'a+',encoding='utf8') as w:
        obj=json.dumps(jsonObj, ensure_ascii=False).encode('utf8')
        w.write(obj.decode('utf8'))
        w.write('\n')



#        if 'E' in item[0]:
#            event=[]
#            dic_event['event_ID']=item[0]
#            event_label,event_order=item[1].split(':')
#            dic_event['event_label']=event_label
#            for xiang in elementlist:
#                if xiang[0]==event_order:
#                    dic_event['event_start']=int(xiang[2])
#                    dic_event['event_end']=int(xiang[3])
#                    event_text=''
#                    for m in range(4,len(xiang)):
#                        event_text=event_text+xiang[m]+' '
#                    dic_event['event_text']=event_text
#            event.append(dic_event)
#            for i in range(2,len(item)):
#                Arg_relation,Arg_order=item[i].split(':')
#                Argname='Arg'+str(i-1)
#                dic_ralation[Argname+'_relation']=Arg_relation
#                for itemitem in elementlist:
#                    if itemitem[0]==Arg_order:
#                        dic_ralation[Argname+'_start']=int(itemitem[2])
#                        dic_ralation[Argname+'_end']=int(itemitem[3])
#                        dic_ralation[Argname+'_text']=itemitem[4]
#                        dic_ralation[Argname+'_label']=itemitem[1]
#                event.append(dic_ralation)
#                dic_ralation={}
#            eventlist.append(event)
                
                


            
            
            
        
    
        
    
        
    
    