import re
import numpy as np
import pandas as pd

# data_dir = './data/'
# data_files = ['337.xlsx', '338.xlsx', '339.xlsx', '340.xlsx', '341.xlsx', '342.xlsx', '342.xlsx', '344.xlsx', \
#               '404.xlsx', '405.xlsx', '406.xlsx', '407.xlsx', '408.xlsx', '409.xlsx', '462.xlsx', '463.xlsx', \
#               '464.xlsx', '465_1.xlsx', '465_2.xlsx', '466.xlsx', '546.xlsx']

# ### Get all dataframes
# dataframes = [pd.read_excel(data_dir + f) for f in data_files]
# dataframes = [df[['text', 'height customer', 'weight customer']] for df in dataframes ]
# dataframes = [df.dropna() for df in dataframes]

# ### Get height data
# height_data = [df[['text','height customer']].dropna() for df in dataframes]
# height_text = [list(df['text']) for df in height_data]
# height_text = [i for lst in height_text for i in lst]
# height_data = [list(df['height customer']) for df in height_data]
# height_data = [i for lst in height_data for i in lst]

# height_df = pd.DataFrame({'text': height_text, 'height': height_data})

# ### Get weight data
# weight_data = [df[['text','weight customer']].dropna() for df in dataframes]
# weight_text = [list(df['text']) for df in weight_data]
# weight_text = [i for lst in weight_text for i in lst]
# weight_data = [list(df['weight customer']) for df in weight_data]
# weight_data = [i for lst in weight_data for i in lst]

# weight_df = pd.DataFrame({'text': weight_text, 'weight': weight_data})

# height_df.to_csv('refine_data/height.csv')
# weight_df.to_csv('refine_data/weight.csv')


### Refine data
def refine(df, text_col, data_col):
    result = {text_col: [], data_col: []}
    text = list(df[text_col])
    data = list(df[data_col])
    for i in range(len(df)):
        if re.search('http://|https://', text[i]) is not None: continue
        result[text_col] += [text[i] for w in data[i].split('|/|') if len(w) <= 12]
        result[data_col] += [w for w in data[i].split('|/|') if len(w) <= 12]
    return pd.DataFrame(result)

### Height
height_df = pd.read_csv('refine_data/height.csv')
height_df = refine(height_df, 'text', 'height')
height_df.to_csv('refine_data/height_refine.csv')

### Weight 
weight_df = pd.read_csv('refine_data/weight.csv')
weight_df = refine(weight_df, 'text', 'weight')
weight_df.to_csv('refine_data/weight_refine.csv')