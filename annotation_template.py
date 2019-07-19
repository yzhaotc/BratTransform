'This script is to make a template for prodigy annotation'
import json
from optparse import OptionParser
import re
import spacy

parser=OptionParser()
parser.add_option('-I',dest=('Inpath'),help='Input Path of the annotation')
parser.add_option('-D',dest=('Indic'),help='Input path of dictionary')
parser.add_option('-O',dest=('Outpath'),help='Output annotation with new list')
parser.add_option('-L',dest=('Label'),help='The label want update')
options,arguments=parser.parse_args()

inputfile=options.Inpath
inputdic=options.Indic
outfile=options.Outpath


#'read the list of dictionary'
#with open(inputdic,'rb',encoding='utf8') as dictionary:
#    list2add=dictionary.readlines()

'download the spacy model to analyse the token'
nlp=spacy.load('en_core_web_sm')

'the part to test'
word_list=[]
text_new_list=[]
tokens_list=[]
text_original_list=[]
docs=[]
spans_original_list=[]
inputfile='template.jsonl'
label='COMPANY'
list2add=['TradingCentral']




'Get the Word list'
with open(inputfile,'rb') as file:
    lines=[line for line in file.readlines()]
    for line in lines:
        doc=json.loads(line)
        if doc['answer']=='accept':
            docs.append(doc)
            text=doc['text']
            spans_original=doc['spans']
            spans_original_list.append(spans_original)
            tokens=doc['tokens']
            tokens_list.append(tokens)
            text_original_list.append(text)
            for span_original in spans_original:
                if span_original['label']==label:
                    token_start=int(span_original['token_start'])
                    token_end=int(span_original['token_end'])
                    word_text=''
                    for i in range(token_start,token_end):
                        word_text=word_text+tokens[i]['text']
                    if word_text!='':
                        print(word_text)
                        word_list.append(word_text)
                    word_list=list(set(word_list))



'Get token ID in the span original'
old_tokentoken=[]
old_tokens_list=[]
for text_original in text_original_list:
    old_tokens=nlp(text_original)
    for old_token in range (0, len(old_tokens)):
        old_tokentoken.append({"text":old_tokens[old_token].text, "start": old_tokens[old_token].idx, "end": (old_tokens[old_token].idx+len(old_tokens[old_token].text)), "index":old_token,"id":old_tokens[old_token].norm})
    old_tokens_list.append(old_tokentoken)
    old_tokentoken=[]


i=0
for old_spans in spans_original_list:
    for old_span in old_spans:
        token_start=int(old_span['token_start'])
        token_end=int(old_span['token_end'])
        old_span['id_start']=old_tokens_list [i][token_start]['id']
        old_span['id_end']=old_tokens_list[i][token_end]['id']
i=i+1
        
'Extrat ID Except input label'
start_ID=[]
end_ID=[]
for old_spans in spans_original_list:
    for old_span in old_spans:
        if old_span['label'] !=label:
            start_ID.append(old_span['id_start'])
            end_ID.append(old_span['id_end'])



'creat a big regular expression'
big_regex = re.compile('|'.join(map(re.escape, word_list)))
#
'Change the word in the text'
for item in list2add:
    for text_original in text_original_list:
#        for word in word_list:
#            text_original=text_original.replace(word,item)
#        text_new=text_original
        text_new = big_regex.sub(item, text_original)
        text_new_list.append(text_new)

        

'Get new token_start,token_end,start,end'
new_tokentoken=[]
new_tokens_list=[]
for new_text in text_new_list:
    new_tokens=nlp(new_text)
    for token in range (0, len(new_tokens)):
        new_tokentoken.append({"text":new_tokens[token].text, "start": new_tokens[token].idx, "end": (new_tokens[token].idx+len(new_tokens[token].text)), "index":token,"id":old_tokens[old_token].norm})
    new_tokens_list.append(new_tokentoken)
    new_tokentoken=[]
        
        


#'Change the annotation file'
#for item in list2add:
#    length_item_token=len(nlp(item))
#    length_item=len(item)
#    for i in range(0,len(tokens_list)):
#        docs[i]['tokens']=new_tokens_list[i]
#        docs[i]['text']=text_new_list[i]
#        for k in range (0,len(docs[i]['spans'])):
#            span=docs[i]['spans'][k]
#            if span['label']==label:
#                span['start']=span['start']
#                dif_length=length_item-(span['end']-span['start'])
#                span['end']=span['start']+length_item
#                span['token_start']=span['token_start']
#                dif_token_length=length_item_token-(span['token_end']-span['token_start']+1)
#                span['token_end']=span['token_start']+length_item_token-1
#                for y in range(k+1,len(docs[i]['spans'])):
#                    spanspan=docs[i]['spans'][y]
#                    spanspan['start']=spanspan['start']+dif_length
#                    spanspan['end']=spanspan['end']+dif_length
#                    spanspan['token_start']=spanspan['token_start']+dif_token_length
#                    spanspan['token_end']=spanspan['token_end']+dif_token_length
#
#
#
#
#'Write new annotation file'
#with open('annotation_template.jsonl','w',encoding='utf8') as f:
#    for dicdic in docs:
#        jsonObj=json.dumps(dicdic)
#        f.write(jsonObj)
#        f.write('\n')
                

    
            
                            
                        
                        
                        
                    

