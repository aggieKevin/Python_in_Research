# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:46:44 2019

@author: hejia
"""

import os
from os import listdir
import pandas as pd
import numpy as np
import ast
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

default_path_head=r"C:\Users\hejia\Documents\python\WUIP"
file_path=os.path.join(default_path_head,'final_result_maxmind.csv')
source=pd.read_csv(file_path)
com_list=source['company'].tolist()

cols=['file','startIP','endIP','company']
df_result=pd.DataFrame(columns=cols)

data_path_head=r"C:\Users\hejia\Documents\python\WUIP\data"
mid_all=listdir(data_path_head)
final=set()
i=0
for mid in mid_all: # loop over different files
    print('file is, ',mid)
    i+=1
    print('this is step {}'.format(i))
    path=os.path.join (data_path_head,mid)
    path=os.path.join(path,'GeoIPISP.csv')
    data_one_file=pd.read_csv(path,names=['startIP','endIP','name'],encoding = "ISO-8859-1")
    for ind in data_one_file.index: # go through each row in one file
        print('ind is, ',ind)
        if data_one_file.loc[ind]['name'] in com_list:
            name1=data_one_file.loc[ind]['name']
            startIP1=data_one_file.loc[ind]['startIP']
            endIP1=data_one_file.loc[ind]['endIP']
            file1=mid
            ser=pd.Series([file1,startIP1,endIP1,name1],index=cols)
            df_result=df_result.append(ser,ignore_index=True)
            
result_path=os.path.join(default_path_head,'final_collection_maxmind.csv')
df_result.to_csv(result_path)    


