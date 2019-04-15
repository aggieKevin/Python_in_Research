# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 23:04:08 2018

@author: hejia


import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url='http://advance.lexis.com.ezproxy.library.tamu.edu/api/search?q=burden%20of%20proof&collection=cases&qlang=bool&context=1516831'
uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()
page_soup=soup(page_html,'html.parser')

h1=page_soup.h1
body=page_soup.body

container=page_soup.find_all ("div",{"class":"item-container"})

my_url='http://advance.lexis.com.ezproxy.library.tamu.edu/api/search?q= “analyst event” or “analyst conference ” and “Conference Call Participants ”&context=1516831'
webbrowser.open(my_url,new=2)
"""


import pandas as pd
import webbrowser

firms=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\control_firms.csv',index_col='permno')
# delete duplicates

# if conm is empty, just use permno to search
#data=firms.loc[86142]
for i in firms.index:
    if type(firms.loc[i]['conm'])==float:
        if type(firms.loc[i]['tic'])!=float:
            firms.loc[i]['conm']=firms.loc[i]['tic']
        else:
            firms.loc[i]['conm']=str(i)
    if type(firms.loc[i]['tic'])==float:
        firms.loc[i]['tic']=str(i)
 
# use api to search       
head='http://advance.lexis.com.ezproxy.library.tamu.edu/api/'
search='search?q= ' 
#keywords='“investor day” or “investor conference” or “investor event” or “analyst day” or “analyst event” or “analyst conference” and “Conference Call Participants” '
#keywords=['investor day','investors day','investor conference','investors conference','investor event','investors event','analyst day','analyst event','analyst conference']
keywords='“investor day”  or “investor conference”  or “investor event”or “analyst day” or “analyst event” or “analyst conference”'

context='&context=1516831'
date='&startdate=1998'
exclude_head=' and not “Briefing.com: Hourly In Play (R)” and not “Earnings Conference Call - Final” and not “Earnings Call - Final” and not “Investrend / Bestcalls” and not “: To Present At” and not “No Headline In Original”'
#exclude_head=' and not “Briefing.com: Hourly In Play (R)” and not “Earnings Conference Call - Final” and not “Investrend / Bestcalls” '
extension=[' CORP',' INC',' LTD',' CO',' -CL A']
# quote: %22

# set where to begin with
count=1125
indexes=firms.index.values
while count<len(indexes):
    company_name=firms.loc[indexes[count]]['conm']
    #tic_name=firms.loc[indexes[count]]['tic']
    if '&' in company_name:
        company_name=company_name.replace('&',' ')
    company='“'+company_name+'”'
    for item in extension:
        if item in company:
            company=company+' or '+ company.replace(item,'')
            break
    
    #company=company + ' or ' + '“' + tic_name+ '”' 
    keyAndCompany=keywords+' and '+company
    exclude=exclude_head+'and not'+ '“' + company_name + ' to present at ”'
        #print(keyAndCompany)
    keyAndCompanyAndEx=keyAndCompany+exclude
    search_url=head+search+keyAndCompanyAndEx+date+context
    print(search_url)
    print('this is company {}'.format(count))
    print('the permno is {}'.format(i))
    print('the firm name is {}'.format(company))
    print('---------------------')
    webbrowser.open(search_url,new=2)
    count+=1
    if (count%1==0): # search for 5 companies each time
        print('do you want to continue: yes or no? ')
        if input()=='no':
            break
 

    
    
#idx=firms.index
#duplicates=idx[idx.duplicated()].unique()
#for d_index in duplicates:
#    records=firms.loc[d_index]
#    new_permno=d_index
    
    
