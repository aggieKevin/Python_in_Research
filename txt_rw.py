# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 22:29:53 2019

@author: hejia
"""

import pandas as pd

source=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\linkedin\\linkedin_search.csv',index_col='index')

col_names=['this_index','broker','anndate','merger','analyst','title', 'company','dates employed','city','linkedin pages','Notes']
collection=pd.DataFrame(columns = col_names)


with open('linkedin.txt','r') as f:
    content=f.readlines()
content=[x.strip() for x in content]
record=-1

# new_index now break line with content
for i in range(len(content)): 
    if 'new_index' in content[i]:
        record+=1
        index_no=int(content[i].strip().split()[1])
        collection.at[record,'this_index']=index_no
        collection.at[record,'broker']=source.loc[index_no]['broker']
        collection.at[record,'anndate']=source.loc[index_no]['anndate']
        collection.at[record,'merger']=source.loc[index_no]['merger']
        collection.at[record,'analyst']=source.loc[index_no]['analyst']
        link=''# reset link
        creat_empty=True
    elif 'linkedin.com' in content[i]:
        link=content[i]
               
    elif content[i]== '' or content[i].strip()== 'Experience':
        if 'new_index' not in content[i+1]:
            record+=1
            line=1
            collection.at[record,'this_index']=index_no
            collection.at[record,'broker']=source.loc[index_no]['broker']
            collection.at[record,'anndate']=source.loc[index_no]['anndate']
            collection.at[record,'merger']=source.loc[index_no]['merger']
            collection.at[record,'analyst']=source.loc[index_no]['analyst']
            collection.at[record,'linkedin pages']=link
            collection.at[record,'Notes']=''
            collection.at[record,'city']=''
            
    else :
        if line==1: # company name
            pass
        elif line==2: # title
            collection.at[record,'title']=content[i].replace('Title','')
        elif line==3: # company name
            collection.at[record,'company']=content[i].replace('Company Name','')
        elif line==4: # date 
            collection.at[record,'dates employed']=content[i].replace('Dates Employed','')
        elif line==5: # duration
            pass
        elif line>=6: # city
            if 'Location' in content[i]:
                collection.at[record,'city']=content[i].replace('Location','')
            else:
                print(content[i])
                print(collection.at[record,'Notes'])
                collection.at[record,'Notes']=collection.at[record,'Notes']+' '+content[i]
        line+=1
        
collection.to_csv('C:\\Users\\hejia\\Documents\\python\\linkedin\\collection.csv')  

from subprocess import Popen
p = Popen('collection.csv', shell=True)           
            
            
            
            
        
        
    
        
        
        
        
    
        