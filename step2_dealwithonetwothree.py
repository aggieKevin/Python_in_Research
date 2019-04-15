# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 23:35:00 2019

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
import ast


def convert_name(name):   
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

    else:
        final_name=name
    return final_name

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

'''
abbr_path_head=r"C:\Users\hejia\Documents\python\WUIP"
abbr_path=os.path.join(abbr_path_head,'abbr_table.csv')
abbr_table=pd.read_csv(abbr_path).values
abbr_dic=dict(abbr_table)

default_path_head=r"C:\Users\hejia\Documents\python\WUIP"
fund_path=os.path.join(default_path_head,'fund_types.csv')
fund_file=pd.read_csv(fund_path,usecols=['mgrno','mgrname','typecode'])
fund_file['cleaned_mgrname']=''
fund_file['full_cleaned_mgnrname']=''
for ind in fund_file.index:
    fund_file.at[ind,'cleaned_mgrname']=convert_name(fund_file.loc[ind]['mgrname'])
    cleaned_name=fund_file.loc[ind]['cleaned_mgrname']
    words_list=cleaned_name.split()
    for word in words_list:
        if word in abbr_dic:
            cleaned_name=cleaned_name.replace(word,abbr_dic[word])
            print('cleaned name is, ',cleaned_name)
            fund_file.at[ind,'full_cleaned_mgnrname']=cleaned_name               
fund_file.to_csv(os.path.join(default_path_head,'fund_cleaned.csv'))
'''

default_path_head=r"C:\Users\hejia\Documents\python\WUIP"
fund_path=os.path.join(default_path_head,'fund_cleaned.csv')
fund_file=pd.read_csv(fund_path,index_col='mgrno')

default_path_head=r"C:\Users\hejia\Documents\python\WUIP"
file_path=os.path.join(default_path_head,'all_words_remove_space_0and1.csv')
source=pd.read_csv(file_path,index_col='ind')
source['all_match']=''
source['three words']=''
#source_index=source.loc[source['spaces']==1].index
source_index=source.index
for ind in source_index:
    print(ind)
    if  type(source.loc[ind]['two words'])==str:
        options=source.loc[ind]['two words']
        options_array=ast.literal_eval(options)
        for option in options_array:
            all_list=[]
            three_match=[]
            name,no=option
            cleaned_name=fund_file.loc[no]['full_cleaned_mgnrname']   
            if cleaned_name==source.loc[ind]['cleaned_company']:
                source.at[ind,'perfect_match_mgrname']=name
                source.at[ind,'perfect_match_mgrno']=no
                source.at[ind,'two words']=''
                break
            else:
                result=word_match_word(cleaned_name,source.loc[ind]['cleaned_company'])
                all_match,matched_length,head_match=result
                if all_match==True:
                    all_list.append((name,no))
                if matched_length==3:
                    three_match.append((name,no))
        if len(all_list)>0:
            source.at[ind,'all_match']=all_list
            source.at[ind,'two words']=''
        if len(three_match)>0:
            source.at[ind,'three words']=three_match
            source.at[ind,'two words']=''
                    
                    
                




'''
for ind in source_index:
    print(ind)
    if type(source.loc[ind]['all words'])==str:
        options=source.loc[ind]['all words']
        options_array=ast.literal_eval(options)
        perfect_result=[]
        possible_result=[]
        for option in options_array:
            name,no=option
            cleaned_name=convert_name(name)
            #if source.at[ind,'cleaned_company'] in cleaned_name
            if all([word in cleaned_name for word in source.at[ind,'cleaned_company']] )==True:
                perfect_result.append((name,no))
            else:
                possible_result.append((name,no))
        if len(perfect_result)>0:            
            source.at[ind,'perfect_match_mgrname']=perfect_result
        if len(possible_result)>0:
            source.at[ind,'possible_match']=possible_result
        source.at[ind,'all words']=''
        
         

for ind in source_index:
    print(ind)
    if source['spaces'].loc[ind]==0:# means len(cleaned_company)==1
        if type(source.loc[ind]['perfect_match_mgrname'])!=str and type(source.loc[ind]['all words'])==str:# means no pefect found, and all words match exists
            options=source.loc[ind]['all words']
            options_array=ast.literal_eval(options)
            if len(options_array)==1: # only one match
                source.at[ind,'perfect_match_mgrname']=options_array[0][0]
                source.at[ind,'perfect_match_mgrno']=options_array[0][1]
            else:
                source.at[ind,'possible_match']=options
            source.at[ind,'all words']=''
'''            
                
            
        
'''
source['three replaced']=''
source_index=source.index
for ind in source_index:
    print(ind)
    three=source['three words'].loc[ind]
    if type(three)==str:
        if type(source['cleaned_company'].loc[ind])==str:
            cleaned_com=(source['cleaned_company'].loc[ind]).replace('MGMT','MANAGEMENT')

        three_array=ast.literal_eval(three)
        for e in three_array:
            name=e[0]
            print('name is,', name)
            no=e[1]
            print('no is , ', no)
            if type(name)==str:
                processed_name=convert_name(name).replace('MGMT','MANAGEMENT')
                print('converted name is, ', processed_name)
                print('clean_name is, ',cleaned_com)
            source.at[ind,'three replaced']=processed_name
            if processed_name== cleaned_com:
                print('found here, ',ind)
                source.at[ind,'perfect_match_mgrname']=name
                source.at[ind,'perfect_match_mgrno']=no

'''
result_path=r"C:\Users\hejia\Documents\python\WUIP"   
source.to_csv(os.path.join(default_path_head,'all_words_remove_space_two_words.csv'))
from subprocess import Popen
Popen(os.path.join(default_path_head,'all_words_remove_space_two_words.csv'), shell=True)    
p=os.path.join(defaut_path_head,'aa.txt')