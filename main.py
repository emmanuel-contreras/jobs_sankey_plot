#%% Load imports and data
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 20:09:19 2022

@author: Emmanuel
"""

import pandas as pd
from pathlib import Path
import numpy as np
from itertools import permutations


import plotly.graph_objects as go
# https://stackoverflow.com/questions/35315726/plotly-how-to-display-charts-in-spyder
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot


path_csv = Path(r"./job_applications - Sheet1.csv")

df = pd.read_csv(path_csv)

# visulize DF
df.head(10)

#%% Generate permutation of values and dictionary to store counts

# List of potential statuses that matches CSV 
label = ['applied', 'rejected', 'no-response', 'recruiter',
         'first-interview', 'second-interview','ignored-them', 'on-demad-interview', 
         'stupidly-long-online-assessment', 'hired', 'ghosted',
         'ignored-application'] 
dict_label = {idx: pos for pos, idx in enumerate(label) }

# generate permutations of statuses 
list_permutations = [list(l) for l in list(permutations(label, 2))]    
dict_permutations = {'_'.join(l): idx for idx, l in enumerate(list_permutations)}

# dictionary of permutations to count links
dict_values = {key: 0 for key in dict_permutations}

# Parse application statuses row by row 
for index, values in df['Status'].items():
    
    # data cleanup, remove any spaces
    entries = [s.strip() for s in values.split(',')]
    
    # no respose
    if len(entries) == 1: # applied but no response
        dict_values[f"{entries[0]}_no-response"] += 1
    
    # list is more than 1 item
    else: 
        for pos, entry in enumerate(entries):
            if pos == 0: # skip first entry
                continue              
            dict_values[f"{entries[pos-1]}_{entry}"] += 1


#%% GENERATE PLOT 


# deconstruct dictionary into source, target and values/counts

source = []
target = []
value = []
for index, v in dict_values.items():
    pass
    s, t = index.split('_')
    source.append(dict_label[s])
    target.append(dict_label[t])
    value.append(v)
    
color = ['green', 'red', 'black', 'cyan', 'magenta', 'blue']
color = color + color


dict_key_label = {v:k for k,v in dict_label.items()}

dict_values_with_values = {k:v for k,v in dict_values.items() if v != 0}
dict_labels = {}
for k,v in dict_values_with_values.items():
    pass
    k_target = k.split('_')[1]
    if k_target not in dict_labels.keys():
        dict_labels[k_target] = v
    else:
        dict_labels[k_target] += v

plot_label = []
for l in label:
    pass
    if l in dict_labels.keys():
        temp_label = f"{l} ({dict_labels[l]})"
        plot_label.append(temp_label)
    else:
        plot_label.append(f"{l} ({len(df)})")

## Generate Sankey plot
# https://plotly.com/python/sankey-diagram
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = plot_label,
      # label = label,
      color = color #"blue"
    ),
    link = dict(
      source = source, #  [0, 1, 0, 2, 3, 3], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = target, # [2, 3, 3, 4, 4, 5],
      value = value
  ))])

fig.update_layout(title_text="Job Applications", font_size=10)
fig.show()

plot(fig)