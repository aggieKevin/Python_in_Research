# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 01:16:08 2019

@author: hejia
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 22:29:53 2019

@author: hejia
"""

import pandas as pd

source=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\linkedin\\001-599new\\all.csv',index_col='index')

col_names=['this_index','broker','anndate','merger','analyst','title', 'company','dates employed','city','otherLink','Notes']
collection=pd.DataFrame(columns = col_names)


with open('C:\\Users\\hejia\\Documents\\python\\linkedin\\001-599new\\401_599.txt','r') as f:
    content=f.readlines()
content=[x.strip() for x in content]
record=-1

analyst_start=False
record_start=False

# new_index now break line with content
for i in range(len(content)): 
    #print('content i is, ', content[i])
    if 'aaa' in content[i]:
        analyst_start=True        
        index_no=int(content[i+1].strip().split()[0])
        link=content[i+2]
        if 'brokercheck' in link:
            website='broker'
        elif 'linkedin' in link:
            website='linkedin'
        elif 'relationshipscience' in link or 'relsci' in link:
            website='relationshipscience'
        print('website is, ',website)
        print('index_no is,',index_no)
    elif 'bbb' in content[i]:
        record_start=False
        analyst_start=False              
    #elif content[i]== '' or content[i]== ' 'or content[i].strip()== 'CAREER' or content[i].strip()== 'CAREER':
    elif content[i] in ['',' ','CAREER','Experience']:
        if analyst_start==True:
            print('new rocord')
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
        if record_start==True and website=='relationshipscience':
            if line==1: # company name
                collection.at[record,'company']=content[i]
            elif line==2: # city
                collection.at[record,'city']=content[i].replace('location','').replace('Location','')

            elif line==3: # time
                collection.at[record,'dates employed']=content[i]
                #collection.at[record,'company']=content[i].replace('Company Name','')
            elif line==4: # title
                collection.at[record,'title']=content[i]
            elif line>=5: # notes
                collection.at[record,'Notes']=collection.at[record,'Notes']+' '+content[i]
            line+=1        
        elif record_start==True and website=='linkedin':
            print('come to linkedin')
            if line==1: # company name
                collection.at[record,'Notes']=''
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
                    collection.at[record,'Notes']=collection.at[record,'Notes']+content[i]
            line+=1
        elif record_start==True and website=='broker':
            print('come to broker')
            collection.at[record,'Notes']=''
            collection.at[record,'title']=''
            collection.at[record,'city']=''
            if line==1:
                collection.at[record,'company']=content[i]
            elif line==2:    
                collection.at[record,'dates employed']=content[i]
            line+=1
        
collection.to_csv('C:\\Users\\hejia\\Documents\\python\\linkedin\\001-599new\\401_599.csv')  

from subprocess import Popen
p = Popen('C:\\Users\\hejia\\Documents\\python\\linkedin\\001-599new\\401_599.csv', shell=True)           
            
            
            
            
        
        
    
        
        
        
        
    
        