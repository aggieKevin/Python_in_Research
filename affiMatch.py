# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 23:09:43 2018

@author: hejia
"""

import pandas as pd

pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

def affi_affi(affiA,affiB):
    wordsA=[x.strip() for x in affiA.strip().split()]
    wordsB=[x.strip() for x in affiB.strip().split()]
    matchingWords=0
    for i in range(min(len(wordsA),len(wordsB))):
        if wordsA[i].lower()==wordsB[i].lower():
            matchingWords+=1
        else:
            break
    return matchingWords

def string_list(affi,affi_list):
    maxMatch=0
    location=-1 # mean not found
    for i in range(len(affi_list)):
        match=affi_affi(affi,affi_list[i])
        if match>maxMatch:
            maxMatch=match
            location=i
    print('max match is, ',maxMatch)
    return location
                     
institutionNames_df=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\InstitutionNames.csv',encoding='latin-1')
institutionNames=institutionNames_df['mgrname'].values

#separte with space for both
# compare one by one
# the one with most matches is the one.

toMatch=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\secondPartTreated.csv',index_col='no',encoding='latin-1')
institutionNames_index=institutionNames_df.index
toMatch_index=toMatch.index

for i in toMatch_index:
    affiliation=toMatch.loc[i]['affiliation']
    foundLocation=string_list(affiliation,institutionNames)
    if foundLocation!=-1:
        toMatch['name1'][i]=institutionNames_df.iloc[foundLocation]['mgrname']
        toMatch['no1'][i]=institutionNames_df.iloc[foundLocation]['mgrno']
    
toMatch.to_csv('C:\\Users\\hejia\\Documents\\python\\secondPart.csv')        

