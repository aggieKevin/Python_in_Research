# -*- coding: utf-8 -*-
"""
@author: hejia
"""
import pandas as pd
import webbrowser

#import data from table
source=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\linkedin\\001-599new\\1_200_tobedone.csv',index_col='index')
# use api to search       
head='http://www.google.com/search?q='



indexs=source.index
every_time=10
no=1
for i in indexs:
    print('index is ',i)
    broker_name=source.loc[i]['broker']
    analyst_name=source.loc[i]['analyst']
    if '&' in broker_name:
        broker_name=broker_name.replace('&','%26')
    print(broker_name)
    key_words=analyst_name +' '+  broker_name+' linkedin'
    search_url=head+key_words
    webbrowser.open(search_url,new=2)
    if (no%every_time==0): # search for searches_pertime companies each time
        no=1
        x=input('do you wanna continue')
        if x=='no':
            break
    no+=1
    
        


 

    

    
