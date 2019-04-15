# -*- coding: utf-8 -*-
"""
@author: hejia
"""
import pandas as pd
import webbrowser

#import data from table
firms=pd.read_csv('C:\\Users\\hejia\\Documents\\python\\control_firms.csv',index_col='permno')

for i in firms.index:
    # if company name is empty, try to use tic
    if type(firms.loc[i]['conm'])==float:
        if type(firms.loc[i]['tic'])!=float:
            firms.loc[i]['conm']=firms.loc[i]['tic']
        else:
            # if tic is empty too, then use permno
            firms.loc[i]['conm']=str(i)
    if type(firms.loc[i]['tic'])==float:
        firms.loc[i]['tic']=str(i)
 
# use api to search       
head='http://advance.lexis.com.ezproxy.library.tamu.edu/api/'

# the following rows together creat the URL for search
search='search?q= ' 
#keywords='“investor day” or “investor conference” or “investor event” or “analyst day” or “analyst event” or “analyst conference” and “Conference Call Participants” '
keywords='“investor day”  or “investor conference”  or “investor event”or “analyst day” or “analyst event” or “analyst conference”'

context='&context=1516831'
date='&startdate=1998'
exclude_head=' and not “Briefing.com: Hourly In Play (R)” and not “Earnings Conference Call - Final” and not “Investrend / Bestcalls” '

# company name may include these exentions
extension=[' CORP',' INC',' LTD',' CO',' -CL A']

# set where to begin with
count=0

# set how many companies to search one time
searches_pertime=20
# get the index values
indexes=firms.index.values

while count<len(indexes): # when not at the end of the index list
    company_name=firms.loc[indexes[count]]['conm']
    tic_name=firms.loc[indexes[count]]['tic']
    # URL cannot recognize &, so replace with empty space
    if '&' in company_name:
        company_name=company_name.replace('&',' ')
    #exact match
    company='“'+company_name+'”'
    # if the company name has the any of the extensions, create a copy name without it
    for item in extension:
        if (item in company_name) and item[-1]==company_name[-1]:
            company_name=company_name.replace(item,'')
            company=company+' or '+ '“'+company_name+'”'
            break
    
    company=company + ' or ' + '“' + tic_name+ '”' 
    keyAndCompany=keywords+' and '+company
        #print(keyAndCompany)
    keyAndCompanyAndEx=keyAndCompany+exclude_head
    search_url=head+search+keyAndCompanyAndEx+date+context
    print(search_url)
    print('this is company {}'.format(count))
    print('the permno is {}'.format(i))
    print('the firm name is {}'.format(company))
    print('----------------------------------------------------------')
    webbrowser.open(search_url,new=2)
    count+=1
    if (count%searches_pertime==0): # search for searches_pertime companies each time
        print('Do you want to continue searching: yes or no? ')
        if input()=='no':
            break
 

    

    
