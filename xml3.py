# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 11:44:26 2019

@author: hejia
"""
import pandas as pd
import xml.etree.ElementTree as ET
col_names=['investmentVehicle_ID',
 'FundShareClass_ID',
 'Fund_ID',
 'Fund',
 'HistoricalPerformance',
 'OperationHistory',
 'BestFitIndex']

collection=pd.DataFrame(columns = col_names)
tree=ET.parse('xml_data.xml')
root=tree.getroot()

for child1 in root:
    print('----------------------')
    print(child1.tag,child1.attrib)
    print('begin of child2')
    for child2 in child1:
        print(child2.tag,child2.attrib)
        print('begin of child 3')
        for child3 in child2:            
            print(child3.tag,child3.attrib)
            print('begin of child 4')
            for child4 in child3:
                print(child4.tag,child4.attrib)
                print('begin of child 5')
                for child5 in child4:
                    print(child5.tag,child5.attrib)
    

record=0       
for investment in root.iter('InvestmentVehicle'):
    print(investment)
    #d={}
    #id_information=investment.attrib
    #d['investmentVehicle_ID']=list(id_information.values)[0]
    
for investment in root.iter('InvestmentVehicle'):    
    investment_vehicle_ID=investment.get('_Id')   
    print(investment_vehicle_ID)
    fund_share_class=investment.find('FundShareClass').text
    print(fund_share_class)
    fund_share_id=investment.find('FundShareClass').get('_Id')
    print(fund_share_class)
    share_share_id=investment.find('FundShareClass').get('_FundId')
    print(share_share_id)
    fund=investment.find('Fund').text
    print(fund)
    history_performance=investment.find('HistoricalPerformance').text
    print(history_performance)
    operation_history=investment.find('OperationHistory').text
    try:
        best_fit_index=investment.find('BestFitIndex').text
    except:
        best_fit_index=''
    
    
    
    

