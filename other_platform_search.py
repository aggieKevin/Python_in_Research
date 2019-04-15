# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 22:29:53 2019

@author: hejia
"""

import pandas as pd

source=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\linkedin\\Analyst_Linkedin_remaining.csv',index_col='index')

col_names=['this_index','broker','anndate','merger','analyst','title', 'company','dates employed','city','otherLink','Notes']
collection=pd.DataFrame(columns = col_names)


with open('linkedin_remaining.txt','r') as f:
    content=f.readlines()
content=[x.strip() for x in content]
record=-1

analyst_start=False
record_start=False

# new_index now break line with content
for i in range(len(content)): 
    if 'new_analyst_begin' in content[i]:
        analyst_start=True        
        index_no=int(content[i+1].strip().split()[0])
        link=content[i+2]
    elif 'new_analyst_end' in content[i]:
        rerord_start=False
        analyst_start=False
               
    elif content[i]== '' or content[i]== ' 'or content[i].strip()== 'CAREER':
        if analyst_start==True:
            record_start=True
            record+=1
            line=1
            collection.at[record,'this_index']=index_no
            collection.at[record,'broker']=source.loc[index_no]['broker']
            collection.at[record,'anndate']=source.loc[index_no]['anndate']
            collection.at[record,'merger']=source.loc[index_no]['merger']
            collection.at[record,'analyst']=source.loc[index_no]['analyst']
            collection.at[record,'otherLink']=link
            collection.at[record,'Notes']=''
            collection.at[record,'city']=''
            
    else :
        if record_start==True:
            if line==1: # company name
                collection.at[record,'company']=content[i]
            elif line==2: # city
                collection.at[record,'city']=content[i].replace('Location','')
            elif line==3: # time
                collection.at[record,'dates employed']=content[i]
                #collection.at[record,'company']=content[i].replace('Company Name','')
            elif line==4: # title
                collection.at[record,'title']=content[i]
            elif line>=5: # notes
                collection.at[record,'Notes']=collection.at[record,'Notes']+' '+content[i]
            line+=1
        
collection.to_csv('C:\\Users\\hejia\\Documents\\python\\linkedin\\collection2.csv')  

from subprocess import Popen
p = Popen('collection2.csv', shell=True)           
            
            
            
            
        
        
    
        
        
        
        
    
        