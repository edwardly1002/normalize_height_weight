from unidecode import unidecode
import pandas as pd
import numpy as np
import re

def normalize(sent): 
    sent = re.sub('\D', '', sent)
    return sent

def preprocess(text):
    text = text.lower()
    text = re.sub(r'khách\s\d+:', '', text)
    text = unidecode(text)
    text = re.sub(r'[^\w\d]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s+|\s+$', '', text)
    return text

def recognizer(sentence, pattern):
    sent = preprocess(sentence)
    match_lst = []
    k = 0
    while True:
        p = re.search(pattern, sent[k:])
        if p is None: break
        idx = p.span()
        # print(p)
        match_lst += [sent[k:][idx[0]:idx[1]]]
        k = k + idx[1]
    return match_lst

### COMMON PATTERN
dd = r'(\d\d|\d)'
ss = r'(\s|)'
### WEIGHT
kilo = r'(kg|ky|ki|can|kj|kilo|kilogam)'
nang = r'((can|)(nang|nag))'
pt_weight_1 = r'\b\d\d{}{}'.format(ss, kilo) ### case 43
pt_weight_2 = r'\d\d\s\d{}{}'.format(ss, kilo) ### case 43.5
pt_weight_3 = r'{}{}\d\d(\s\d|)({}|)'.format(nang, ss, kilo)
pt_weight_4 = r'\d\d{}k{}cao+'.format(ss, ss)
pt_weight = r'{}|{}|{}|{}'.format(pt_weight_1, pt_weight_2, pt_weight_3, pt_weight_4)
### HEIGHT
kilogram = r'(ki|ky|kilogam|kg|k|kilogram)'
pt_height_1 = r'\d\d\d{}cm|\d{}{}{}m\b'.format(ss,ss,dd,ss)
pt_height_2 = r'\d{}m{}{}|\bm{}{}'.format(ss, ss, dd, ss, dd)
pt_height_3 = r'(cao+){}\d[\sm]*{}[m|met]*|(met){}{}'.format(ss,dd, ss,dd)
pt_height_4 = r'(\d{}{}|\d\d\d)(?={}(nang|nag))'.format(ss, dd, ss)
pt_height_5 = r'(\d{}\d\d|\d\d\d)(?={}{})'.format(ss, ss, pt_weight)
pt_height = r'({}|{}|{}|{}|{})'.format(pt_height_1, \
            pt_height_2, pt_height_3, pt_height_4, pt_height_5)
###-------------------------------------------

if __name__ == "__main__":
    weight_df = pd.read_csv('refine_data/weight_refine.csv')
    text = list(weight_df['text'])
    weight_data = list(weight_df['weight'])
    weight_data = [sent for sent in weight_data]

    weight = [' ? '.join(recognizer(t, pt_weight)) for t in text]
    weight = [sent for sent in weight]

    cnt = 0
    for (d,p,i) in [(weight_data[i],weight[i], i) for i in range(len(weight)) \
                                                if weight[i]!=weight_data[i]]:
        # if re.search('cao|Cao',p) is not None: continue  
        if normalize(d) == normalize(p): continue    
        # if re.search('m\d\d\d',d) is not None: continue                                   
        cnt+= 1
        print(text[i])
        print(d, '=>', p)

    print(cnt/len(weight))
    print(re.search(pt_weight, 'E cao 1m54 nang 43 5 kg a'))

    # height_df = pd.read_csv('refine_data/height_refine.csv')
    # text = list(height_df['text'])
    # height_data = list(height_df['height'])
    # height_data = [sent for sent in height_data]

    # height = [' ? '.join(recognizer(t, pt_height)) for t in text]
    # height = [sent for sent in height]

    # cnt = 0
    # for (d,p,i) in [(height_data[i],height[i], i) for i in range(len(height)) \
    #                                             if height[i]!=height_data[i]]:
    #     # if re.search('cao|Cao',p) is not None: continue  
    #     if normalize(d) == normalize(p): continue    
    #     # if re.search('m\d\d\d',d) is not None: continue                                   
    #     cnt+= 1
    #     print(text[i])
    #     print(d, '=>', p)

    # print(cnt/len(height))