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
    text = re.sub(r'[^\w\d\.,]', ' ', text)
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
        match = sent[k:][idx[0]:idx[1]]
        match = re.sub('mot', '1', match)
        match = re.sub('ruoi', ' 50 ', match)
        match_lst += [match]
        k = k + idx[1]
    return match_lst

### COMMON PATTERN
dd = r'(\d\d|\d)'
ss = r'(\s|)'
dot = r'(\.|,)'
kilo = r'(kg|ky|ki|can|kj|kilo|kilogam|k)'
nang = r'((can|)(nang|nag))'
met = r'(m|met)'

### WEIGHT
pt_weight_1 = r'\b\d\d{}{}'.format(ss, kilo) ### case 43
pt_weight_2 = r'\d\d{}\d{}{}'.format(dot, ss, kilo) ### case 43.5
pt_weight_3 = r'{}{}\d\d(\s\d|)({}|)'.format(nang, ss, kilo)
pt_weight_4 = r'\d\d{}k{}cao+'.format(ss, ss)
pt_weight = r'{}|{}|{}|{}'.format(pt_weight_1, pt_weight_2, pt_weight_3, pt_weight_4)


### HEIGHT
### 150cm, 150 cm 
pt_height_1 = r'(cao+|)1\d\d{}cm'.format(ss)
### 1m5, 1m50, 1 m 5, 1 m 50
pt_height_2 = r'(cao+|)1{}{}{}{}'.format(ss, met, ss, dd)
### 1.5m, 1 . 5m, 1.50m, 1 . 50m
pt_height_3 = r'(cao+|)1{}{}{}{}m'.format(ss, dot, ss, dd)
### 1.50 1,5 1 . 50 1 , 5 (not kg)
pt_height_4 = r'(\b|cao+)1{}{}{}{}(?!{}{})'.format(ss, dot, ss, dd, ss, kilo)
### m50, m5, m 50
pt_height_5 = r'(\b|cao+){}{}{}\b'.format(met, ss, dd)
### cao 150, 150 (nặng ...), 150 (45kg)
pt_height_6 = r'cao+{}1\d\d|1\d\d\s(?=({}|{}))'.format(ss, nang, pt_weight)
### 
pt_height_7 = r'(met|m) ruoi'

pt_height = r'({}|{}|{}|{}|{}|{}|{})'.format(pt_height_1, pt_height_2, \
            pt_height_3, pt_height_4, pt_height_5, pt_height_6, pt_height_7)
###-------------------------------------------

if __name__ == "__main__":
    # weight_df = pd.read_csv('refine_data/weight_refine.csv')
    # text = list(weight_df['text'])
    # weight_data = list(weight_df['weight'])
    # weight_data = [sent for sent in weight_data]

    # weight = [' ? '.join(recognizer(t, pt_weight)) for t in text]
    # weight = [sent for sent in weight]

    # cnt = 0
    # for (d,p,i) in [(weight_data[i],weight[i], i) for i in range(len(weight)) \
    #                                             if weight[i]!=weight_data[i]]:
    #     # if re.search('cao|Cao',p) is not None: continue  
    #     if normalize(d) == normalize(p): continue    
    #     # if re.search('m\d\d\d',d) is not None: continue                                   
    #     cnt+= 1
    #     print(text[i])
    #     print(d, '=>', p)

    # print(cnt/len(weight))
    # print(re.search(pt_weight, 'E cao 1m54 nang 43 5 kg a'))

    height_df = pd.read_csv('refine_data/height_refine.csv')
    text = list(height_df['text'])
    height_data = list(height_df['height'])
    height_data = [sent for sent in height_data]

    height = [' ? '.join(recognizer(t, pt_height)) for t in text]
    height = [sent for sent in height]

    cnt = 0
    for (d,p,i) in [(height_data[i],height[i], i) for i in range(len(height)) \
                                                if height[i]!=height_data[i]]:
        # if re.search('cao|Cao',p) is not None: continue  
        if normalize(d) == normalize(p): continue  
        # if re.search('\d\d\d', d) is None: continue  
        # if re.search('m\d\d\d',d) is not None: continue                                   
        cnt+= 1
        print(text[i])
        print(d, '=>', p)

    print(cnt/len(height))