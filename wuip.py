# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 09:43:24 2019

@author: hejia
"""
import os
from os import listdir
import pandas as pd
import numpy as np
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

from cleanco import cleanco
import string


def convert_name(name_list):   
    converted_names=[]
    
    for name in name_list:
        if type(name)==str:
        #print(name)
            cleaned_name=cleanco(name).clean_name()
            cleaned_name=cleanco(cleaned_name).clean_name()
            name = cleaned_name.translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
            name_split=name.split()
#            name_copy=name_split.copy()
#            for s in name_copy:
#                if len(s)==1:
#                    name_split.remove(s)
            name_single_spapce=" ".join(name_split)
            final_name=name_single_spapce.upper()
                    
            print(final_name)
            converted_names.append(final_name)
        else: converted_names.append(name)
    return converted_names

def perfect_match(name,name_list):
    index=-1
    for i in range(len(name_list)):
        #if fuzz.partial_ratio(name, n)==100:
        if name==name_list[i]:
            index=i
            break
    return index

def word_match_word(string_a,string_b):
# first word match, and a in b or b in a
    all_match=False
    matched_length=0
    head_match=False
    if type(string_a)==str and string_a and type(string_b)==str:
        words_in_a=string_a.split()
        words_in_b=string_b.split()
        if len(words_in_a)>0 and len(words_in_b)>0:
            if words_in_a[0]==words_in_b[0]:
                head_match=True
            matched_length=sum([word in words_in_a for word in words_in_b])
            if matched_length==len(words_in_a) or matched_length==len(words_in_b):
                all_match=True
    
    return all_match,matched_length,head_match



def word_match_list(fun,name,name_list):
# name match a name in name_list using word_match_word standard
    all_m_list=[]
    matched_4=[]   
    matched_3=[]
    matched_2=[]
    head_match_list=[]    
    for i in range(len(name_list)):
        result=fun(name,name_list[i])
        all_m,matched_len,head_m=result
        if all_m==True:
            all_m_list.append(i)
        elif matched_len>=4:
            matched_4.append(i)
        elif matched_len>=3:
            matched_3.append(i)
        else:
            if matched_len>=2:
                matched_2.append(i)
            if head_m==True:
                head_match_list.append(i)
    
    return all_m_list,matched_4,matched_3,matched_2,head_match_list

def word_match_list_and_head(fun,name,name_list):
# name match a name in name_list using word_match_word standard
    all_m_list=[]
    matched_4=[]   
    matched_3=[]
    matched_2=[]   
    for i in range(len(name_list)):
        result=fun(name,name_list[i])
        all_m,matched_len,head_m=result
        if all_m==True and head_m:
            all_m_list.append(i)
        elif matched_len>=4 and head_m:
            matched_4.append(i)
        elif matched_len>=3 and head_m:
            matched_3.append(i)
        elif matched_len>=2 and head_m:
            matched_2.append(i)
    
    return all_m_list,matched_4,matched_3,matched_2

# about fund dataframe
default_path_head=r"C:\Users\hejia\Documents\python\WUIP"
fund_path=os.path.join(default_path_head,'fund_types.csv')
fund_file=pd.read_csv(fund_path,usecols=['mgrno','mgrname','typecode'])
fund_file['cleaned_mgrname']=convert_name(fund_file['mgrname'])
fund_file.to_csv(os.path.join(default_path_head,'fund_cleaned.csv'))


data_path_head=r"C:\Users\hejia\Documents\python\WUIP\data"
mid_all=listdir(data_path_head)
final=set()
i=0
# read the data from all fils and gather all unique company names
for mid in mid_all:
    i+=1
    print('this is step {}'.format(i))
    path=os.path.join (data_path_head,mid)
    path=os.path.join(path,'GeoIPISP.csv')
    data_one_file=pd.read_csv(path,names=['startIP','endIP','name'],encoding = "ISO-8859-1",)['name'].values
    final.update(data_one_file)
final_lst=list(final)  
# about result datafrme
columns=['company','cleaned_company','perfect_match_mgrname','perfect_match_mgrno','all words',
         'four words','three words','two words']
result=pd.DataFrame(columns=columns)
result = result.fillna('')
result['company']=final_lst
result['cleaned_company']=convert_name(result['company'])

# start match
name_list=fund_file['cleaned_mgrname'].values
record=0
for ind in result.index:   
    print(record)
    nameIn=result.loc[ind]['cleaned_company']
    perfect_match_result=perfect_match(nameIn,name_list)# check 1: do perfect match
    if perfect_match_result !=-1:  # if found a perfect match
        result.loc[ind][['perfect_match_mgrname','perfect_match_mgrno']]=fund_file.iloc[perfect_match_result][['mgrname','mgrno']]
    else: # if perfect match is not found
        word_list_result=word_match_list_and_head(word_match_word,nameIn,name_list)# check 2: do word_match_list search
        col_names=['all words','four words','three words','two words']
        z=list(zip(col_names,word_list_result))
        for column_name, lst in z:
            if lst !=[]:
                nameL=[]
                for i in lst:
                    nameL.append((fund_file.iloc[i]['mgrname'],fund_file.iloc[i]['mgrno']))
                result.loc[ind][column_name]=nameL 
                #result.at[ind,column_name]=nameL
    record+=1
result_path=r"C:\Users\hejia\Documents\python\WUIP"   
result.to_csv(os.path.join(default_path_head,'result.csv'))
from subprocess import Popen
p = Popen(os.path.join(default_path_head,'result.csv'), shell=True)  

#df = pd.DataFrame(data={"col1": final_lst})
#df.to_csv(os.path.join(default_path_head,'list.csv'), sep=',',index=False)