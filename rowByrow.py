# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 20:13:20 2018

@author: hejia
"""

import pandas as pd

pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

def separate (names):
    return [ analyst.strip()for analyst in names.strip('*').split('*') ]

firms=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\testFirms.csv',index_col='NO',encoding='latin-1')
index_sequence=firms.index
for i in index_sequence:
    print('index number is ,',i)
    names=firms.loc[i]['analyst']
    
    if type(names)==str: # mean analysts attended the meeting
        # copy this row
        print('names: ')
        row=firms.loc[i].copy()
        print('row is: ',row)
        names_after_sep=separate(names)
        
        # delete the origial row
        firms.drop(index=i,inplace=True)
        for name in names_after_sep:
            # create a new row for each analyst
            row['analyst']=name
            firms=firms.append(row)
firms.sort_index(inplace=True)            
firms.to_csv('C:\\Users\\hejia\\Documents\\python\\test_firm_result.csv')        
        
