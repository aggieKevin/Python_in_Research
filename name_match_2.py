# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 11:36:47 2019

@author: hejia
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 18:50:20 2019

@author: hejia
"""

import pandas as pd
import numpy as np
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

from cleanco import cleanco
from fuzzywuzzy import fuzz
import string

def convert_name(name_list):
    
    converted_names=[]
    for name in name_list:
        #print(name)
        name = name.translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
        name_single_spapce=" ".join(name.split())
        upper_name=name_single_spapce.upper()
        cleaned_name=cleanco(upper_name).clean_name()
        cleaned_name=cleanco(cleaned_name).clean_name()
        print(cleaned_name)
        converted_names.append(cleaned_name)
        
    return converted_names
        
#def perfect_match(string_a,string_b):
#    validility=False
#    if string_a==string_b:
#        validility=True
#    return validility 

def perfect_match(name,name_list): # name match a name in name_list 100%
    index=-1
    for i in range(len(name_list)):
        #if fuzz.partial_ratio(name, n)==100:
        if name==name_list[i]:
            index=i
            break
    return index

def fuzzy_match(name,name_list): # fuzzy match
    index=[]
    for i in range(len(name_list)):
        if fuzz.partial_ratio(name, name_list[i])>=90 and fuzz.ratio(name,name_list[i])>=90 :
            index.append(i)
    return index

def word_match_word(string_a,string_b):
# first word match, and a in b or b in a
    validility=False
    words_in_a=string_a.split()
    words_in_b=string_b.split()
    if words_in_a[0]==words_in_b[0]:
        if all([word in words_in_a[1:] for word in words_in_b[1:]]) or all([word in words_in_b[1:] for word in words_in_a[1:]]):
            validility=True
    return validility

def word_match_list(name,name_list):
# name match a name in name_list using word_match_word standard
    index_list=[]
    for i in range(len(name_list)):
        if word_match_word(name,name_list[i])==True:
            index_list.append(i)
    return index_list

def add_match_zip(address,zipcode):
    valitility=0 # not sure
    print('in function, address,', address)
    print('in function, zipcode, ', zipcode)
    if (pd.isnull(zipcode)==False) & (pd.isnull(address)==False):
        if str(zipcode) in str(address):
            valitility=1
            print('valitility is ', valitility) # match
        else:
            valitility=-1 # no match
        
    return valitility
    
def add_match_add(string_a,string_b):
    print('address a is ', string_a)
    print('address b is ',string_b)
    valitility=0 # not sure
    if pd.isnull(string_a)==False & pd.isnull(string_b) == False:        
        words_in_a=str(string_a).split()
        words_in_b=str(string_b).split()
        result=sum([word in words_in_a[0:] for word in words_in_b[0:]])
        if result>=2:
            valitility=1 # match
        else:
            valitility=-1 # not match
    return valitility

def collect_words(string_a,string_b):
    words=set()
    set_a=set(string_a.split())
    set_b=set(string_b.split())
    words=set_a ^ set_b
    return words

file=pd.read_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\crsp_compustat_merge_1950_2018.csv')
#,encoding='latin-1'

crsp_names=file[['permno','comnam_crsp']].dropna()
crsp_names=crsp_names.drop_duplicates()
crsp_names['cleaned_name_crsp']=convert_name(crsp_names['comnam_crsp'].values)

#crsp_sip=file[['permno','comnam_crsp','sic']].dropna()
#crsp_sip=crsp_sip.drop_duplicates()
#a=crsp_sip[crsp_sip['sic'].isin([2833,2834,2835,2836])]

clar_names=pd.read_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\Basic Company Overview.csv',usecols=['companyid','companyname','ancestorynamedisplay']).dropna()
clar_names['cleaned_name_clar']=convert_name(clar_names['companyname'].values)
clar_names['cleaned_name_ancestory']=convert_name(clar_names['ancestorynamedisplay'].values)


clar_names['perfect_match']=''
clar_names['perfect_match_permno']=''
clar_names['ancestory_match']=''
clar_names['ancestory_match_permno']=''

clar_names['possible_match']=''
#clar_names['fuzzy_match_permno']

#d=defaultdict(list)
name_list=crsp_names['cleaned_name_crsp'].values
record=0
for ind in clar_names.index:   
    print(record)
    # check 1: do perfect match
    nameIn=clar_names.loc[ind]['cleaned_name_clar']
    compare_result=perfect_match(nameIn,name_list)
    if compare_result !=-1:  # if found a perfect match
        clar_names.loc[ind][['perfect_match','perfect_match_permno']]=crsp_names.iloc[compare_result][['comnam_crsp','permno']]
    else: # if perfect match is not found
        compare_result_2=perfect_match(clar_names.loc[ind]['cleaned_name_ancestory'],name_list)
        if compare_result_2!=-1: # if found a perfect match in ancestory        
            clar_names.loc[ind][['ancestory_match','ancestory_match_permno']]=crsp_names.iloc[compare_result_2][['comnam_crsp','permno']]
        
        compare_result_3=word_match_list(nameIn,name_list)
        if compare_result_3 !=[]:
            nameL=[]
            for i in compare_result_3:
                nameL.append((crsp_names.iloc[i]['comnam_crsp'],crsp_names.iloc[i]['permno']))  

            clar_names.loc[ind]['possible_match']=nameL
    record+=1

    
clar_names.to_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\clar_names_2.csv')   



address=pd.read_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\compustat_addresses.csv')
#,encoding='latin-1'
address.drop_duplicates(subset=['permno'],inplace=True)
address.set_index('permno',inplace=True)
address.to_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\compustat_addresses.csv') 
com_address=address
resource=pd.read_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\resource.csv',index_col='No')
resource['zip_check']=''
resource['zip_check_name']=''
resource['zip_check_permno']=''

resource['address_check']=''
resource['address_check_name']=''
resource['address_check_permno']=''

resource['double_check']=''
resource['double_check_permno']=''


#resource.to_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\resource4_ALL.csv')
#com_address=pd.read_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\compustat_addresses.csv')

import ast

for i in resource.index:
    print('i is ,', i)
    print('---------------------')
    if pd.isnull(resource.loc[i]['possible_match'])==False:
        matchs=ast.literal_eval(resource.loc[i]['possible_match'])
        add_cla=resource.loc[i]['hqaddress']
        permnos=[match[1] for match in matchs]
        perm_names=[match[0] for match in matchs]
        first_found=False
        location=0
        location2=0
        for j in range(len(permnos)):
            #print('permno is, ',no)
            add_csrp=com_address.loc[permnos[j]]['add1']
            #print('add_csrp is, ',add_csrp)
            z_csrp=com_address.loc[permnos[j]]['addzip']
                
            if add_match_zip(add_cla,z_csrp)==1:
                first_found=True
                resource.at[i,'zip_check']=z_csrp
                resource.at[i,'zip_check_name']=perm_names[j]
                resource.at[i,'zip_check_permno']=permnos[j]
               # redundant_words.update(collect_words(resource.loc[i]['cleaned_name_clar'], perm_names[location]))
                break
            elif add_match_zip(add_cla,z_csrp)==-1:
                resource.at[i,'zip_check']='not match'
                resource.at[i,'zip_check_permno']='not match'
            else:
                resource.at[i,'zip_check']='not sure'
                resource.at[i,'zip_check_permno']='not sure'
            location+=1
        if first_found==False:
            for j in range(len(permnos)):
                add_csrp=com_address.loc[permnos[j]]['add1']
                if add_match_add(add_cla,add_csrp)==1:
                    #resource.loc[i]['check_possible_match']=found_permno
                    resource.at[i,'address_check']=perm_names[j]
                    resource.at[i,'address_check_name']=add_csrp
                    resource.at[i,'address_check_permno']=permnos[j]
                    break
                elif add_match_add(add_cla,add_csrp)==-1:
                    resource.at[i,'address_check']='not match'
                else:
                    resource.at[i,'address_check']='not sure'
        if resource.loc[i]['address_check']=='not sure':
            for j in range(len(permnos)):
                if add_match_add(resource.loc[i]['cleaned_name_clar'], perm_names[j])==1:
                    resource.at[i,'double_check']=perm_names[j]
                    resource.at[i,'double_check_permno']=permnos[j]
                    break
                    
             
resource.to_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\resource_2_8.csv.csv')
                
new_resource=resource
new_resource['final_match_permno']=''
new_resource['final_match_name']=''
cols=['perfect_match_permno','zip_check_permno','address_check_permno','double_check_permno'] 
cols2=['perfect_match','zip_check_name','address_check_name','double_check']
for i in new_resource.index:
    print(i)
    for col in cols:
        if (pd.isnull(new_resource.loc[i][col]) | (new_resource.loc[i][col] in ['no sure','not sure','no match','not match','']))==False:
            print('col is ',col)
            new_resource.at[i,'final_match']=new_resource.loc[i][col]
            location=cols.index(col)
            new_resource.at[i,'final_match_name']=new_resource.loc[i][cols2[location]]
            break
new_resource.to_csv('C:\\Users\\hejia\\Dropbox\\Dr Wu\\final_match.csv')            
            
            
        
        
        
    
    
    




  

