# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 23:44:48 2019

@author: hejia
"""

import pandas as pd
import numpy as np
import re
pd.set_option('display.max_rows',100)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)
regex=r"\d{4}"

def separate_time(string): 
    can_separate=False
    begin=''
    end=''
#    if np.isnan(string)==True:# if string is empty
    if type(string)==float:
        can_separate=False
    else: # if string is not empty
        string=string.lower()
        string=string.replace('current','2019')
        string=string.replace('present','2019')            
        arr=[i.strip() for i in string.strip().split('-')]
        
        if len(arr)==1: # when arr has one value, which means no '-'
            if 'prior' in arr[0]: # if prior in arr[0]
                can_separate=False
            else:
                year=re.findall(regex,arr[0]) # when prior not in arr, see whether year in arr[0]
                if year!=[]: # year is in  
                    year=int(year[0])
                    begin,end=year,year
                    can_separate=True
        elif len(arr)==2: # when '-' exists in string, like 2017-2019 or prior - 2019
            first=re.findall(regex,arr[0])
            second=re.findall(regex,arr[1])
            can_separate=True
            if first!=[] and second!=[]:
                begin,end=int(first[0]),int(second[0])          
            elif 'prior' in arr[0] and second!=[]:
                begin,end=int(second[0]),int(second[0])
            elif 'prior' in arr[1] and first!=[]:
                begin,end=int(first[0]),int(first[0])
            else:
                print('special')
                can_separate=False
    return can_separate,begin,end
'''           
string='Jul 2000 – Aug 2012 1234'
regex=r"\d{4}"
x=re.findall(regex,string)    
'''    

fund_file=pd.read_csv(r'C:\Users\hejia\Documents\python\_RA_Jia_copy_local\Linkedin\Fund_types.csv',encoding = "ISO-8859-1",index_col='mgrno')
link_file=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\Analyst_1_599_with_match.csv',encoding = "ISO-8859-1")
link_file['begin_year']=''
link_file['end_year']=''
ind=link_file.index
link_file['position']=link_file.index.tolist()
analysts_no=np.sort(list(set(link_file['index'])))


for i in analysts_no:
    time_list=[]
    df=link_file.loc[link_file['index']==i]
    initial_position=df['position'].iloc[0] # the intial position value   
    for j in df.index:
        result=separate_time(df.loc[j]['time period'])
        if result[0]==True:
            df.at[j,'begin_year']=result[1]
            link_file.at[j,'begin_year']=result[1]
            df.at[j,'end_year']=result[2]
            link_file.at[j,'end_year']=result[2]
            time_list.append(result[1])
    time_list.sort()
    for k in df.index:
        if df.loc[k]['begin_year']!='':
            ranking=time_list.index(df.loc[k]['begin_year'])
            print(ranking)
            df.at[k,'position']=initial_position+ranking
            link_file.at[k,'position']=initial_position+ranking
    for l in df.index:
        if link_file.loc[l,'time period'] !=link_file.loc[l,'time period backup']:
            link_file.at[l,'begin_year']=''
            link_file.at[l,'end_year']=''
    print(df)
link_file.to_csv('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\sorted_separted.csv')
from subprocess import Popen
p = Popen('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\sorted_separted.csv', shell=True)    

# step 2    
link_file.set_index('position',inplace=True)
link_file.sort_index(inplace=True)

link_file.to_csv('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\sorted_separted22.csv')
from subprocess import Popen
p = Popen('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\sorted_separted22.csv', shell=True)    

# step 3 separate possible match

import ast                     
link_file2=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\sorted_separted2.csv')
link_file2['possible_mgr_no']=''
link_file2['possible_fund_type']=''
link_file2['possible_match_flag']=''
ind=link_file2.index
error=[]
for i in ind:
    
    if type(link_file2['mgr_possible_match'].loc[i])==str and link_file2['mgr_possible_match'].loc[i]!='0':
        link_file2.at[i,'possible_match_flag']=1
        row=link_file2.loc[i].copy()# copy content from that row
        try:
            possible=ast.literal_eval(link_file2['mgr_possible_match'].loc[i]) # content in mgr_possible
            link_file2.drop(index=i,inplace=True)
            for c in possible:
                print(c)
                try:
                    name,no=c
                    print('no is: ',no)
                    row['mgr_possible_match']=name
                    row['possible_mgr_no']=no
                    link_file2=link_file2.append(row)
                except:
                    error.append(i)
        except:
            error.append(i)
link_file2.sort_index(inplace=True)             
link_file2.to_csv('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\sorted_separted3.csv')
from subprocess import Popen
p = Popen('C:\\Users\\hejia\\Documents\\python\\_RA_Jia_copy_local\\Linkedin\\sorted_separted3.csv', shell=True)    



