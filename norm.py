import pandas as pd 
import re

def isfloat(n):
    try:
        n = float(n)
        return True
    except:
        return False

# ### Height
# h_data = pd.read_csv('refine_data/height_refine.csv')
# h_data = list(set(h_data['height']))
# h_preproc = [re.sub(r'\D', ' ', w) for w in h_data]
# h_preproc = [re.sub(r'\s+', ' ', w) for w in h_preproc]
# h_preproc = [re.sub(r'^\s|\s$', '', w) for w in h_preproc]

# for (hd,hp) in zip(h_data[:10], h_preproc[:10]):
#     num_1 = hp.split(' ')[-1]
#     if len(num_1) == 1: 
#         num_1 = 100 + int(num_1)*10
#     elif len(num_1) == 2:
#         num_1 = 100 + int(num_1)
#     print(hd, ' => ', num_1)

### Weight
w_data = pd.read_csv('refine_data/weight_refine.csv')
w_data = list(set(w_data['weight']))
w_preproc = [re.sub(r'[^\d(\d.),]', ' ', w) for w in w_data]
w_preproc = [re.sub(r'\s+', ' ', w) for w in w_preproc]
w_preproc = [re.sub(r'^\s|\s$', '', w) for w in w_preproc]

for (wd,wp) in zip(w_data, w_preproc):
    num_1, num_2 = '', ''
    if len(wp.split(' ')) == 2:
        num_1, num_2 = wp.split(' ')
    elif len(wp.split(' ')) == 1:
        num_1 = wp.split(' ')[0]
    
    if isfloat(num_1) and isfloat(num_2):
        print(wd, ' => ', float(num_1), ',', float(num_2))
    elif isfloat(num_1):
        print(wd, ' => ', float(num_1))