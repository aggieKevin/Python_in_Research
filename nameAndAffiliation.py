# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 20:13:20 2018

@author: hejia
"""

import pandas as pd
import numpy as np

pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

def separateAnalysts (names):
    return [ analyst.strip()for analyst in names.strip('*').split('*') ]
def separateNameAndAffi (nameAndAffi):
    sepWithComma=[phrase.strip() for phrase in nameAndAffi.strip(',').split(',')]
    if len(sepWithComma)==3:
        name=sepWithComma[0]+'-'+sepWithComma[1]
        affi=sepWithComma[2]
    elif '-' in nameAndAffi:
        sepWithHyphen=[x.strip() for x in nameAndAffi.strip().split('-')]
        title=sepWithHyphen[1]
        nameAndAffi2=sepWithHyphen[0].split()
        if len(nameAndAffi2)<=2:
            name=sepWithHyphen[0]+'-'+ title
            affi=np.nan
        else:
            name=nameAndAffi2[0]+' '+ nameAndAffi2[1]+'-'+ title
            affi=' '.join(nameAndAffi2[2:])
    else:
        name=nameAndAffi
        affi=np.nan
            
    return name,affi
        
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
        names_after_sep=separateAnalysts(names)
        
        # delete the origial row
        firms.drop(index=i,inplace=True)
        for name in names_after_sep:
            # create a new row for each analyst
            row['analyst'],row['affiliation']=separateNameAndAffi(name)
       
            firms=firms.append(row)
firms.sort_index(inplace=True)            
firms.to_csv('C:\\Users\\hejia\\Documents\\python\\test_firm_result_1.csv')        
        
