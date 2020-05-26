#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:29:58 2020

@author: thanhng
"""

import os, requests
import pandas as pd
from urllib.parse import urljoin, urlparse
import re, json
from collections import Counter

def COMBINE_TEXT_COL(x): return '; '.join(x[x.notnull()].astype(str))

def GET_EVENT_TEXT(result_dict):
    result_df = []
    if result_dict.get('mdr_text') == []:
        result_df.append(
                {'Description of Event or Problem': 'none', 
                 'Additional Manufacturer Narrative': 'none'})
        return pd.DataFrame(result_df)

    if result_dict.get('mdr_text') !=[]:    
        for i in range(len(result_dict.get('mdr_text'))): 
            text_title = [sub['text_type_code'] for sub in result_dict.get('mdr_text')] 
            list_text = [sub['text'] for sub in result_dict.get('mdr_text')]            
            result_df.append(
                    {'text_title': text_title[i], 
                     'text_content': list_text[i]
                            })
        df_trans = pd.DataFrame(result_df).transpose()
        headers = df_trans.iloc[0]
        df_trans  = pd.DataFrame(df_trans.values[1:], columns=headers)
        combine_text_df = df_trans.groupby(level=0, axis=1).apply(lambda x: x.apply(COMBINE_TEXT_COL, axis=1))
        return combine_text_df
    
    
def GET_TEXT_COLUMNS(result_dict):
    text_df = GET_EVENT_TEXT(result_dict)
    manu_narrative = 'none'
    event_description = 'none'   
     
    if len(text_df.columns) <2:
        if text_df.columns == 'Additional Manufacturer Narrative':
            manu_narrative = text_df['Additional Manufacturer Narrative'].values        
        if text_df.columns == 'Description of Event or Problem':
            event_description = text_df['Description of Event or Problem'].values       
        
    if len(text_df.columns) >= 2:
        manu_narrative = text_df['Additional Manufacturer Narrative'].values
        event_description = text_df['Description of Event or Problem'].values    
    return manu_narrative, event_description


def GET_PRODUCT_PROBLEMS(result_dict):
    product_problem = ''
    if 'product_problems' in result_dict.keys():
        product_problem = result_dict['product_problems']
    return product_problem
   
def MAUDE_DB(response):
   res_df = []
   for i in range(len(response['results'])): 
        result_dict = response['results'][i]        
                  
        mdr_report_key = result_dict.get('report_number')
        manu_narrative, event_description = GET_TEXT_COLUMNS(result_dict)   
        product_problem = GET_PRODUCT_PROBLEMS(result_dict)
    
        brand_name = [dev.get('brand_name') for dev in result_dict.get('device')]
        generic_name = [dev.get('generic_name') for dev in result_dict.get('device')]
        manufacture_d_name = [dev.get('manufacturer_d_name') for dev in result_dict.get('device')]
        device_code = [dev.get( 'device_report_product_code') for dev in result_dict.get('device')]
        
        date_received = result_dict.get('date_received') 
        date_of_event = result_dict.get('date_of_event')
        occupation = result_dict.get('reporter_occupation_code')  
        event_type = result_dict.get('event_type')
        adverse_event_flag = result_dict['adverse_event_flag']
    
        device_lst = [sub['openfda'] for sub in result_dict.get('device')]   
        device_name = [dev.get('device_name') for dev in device_lst]
        device_class = [dev.get('device_class') for dev in device_lst]
        
        res_df.append({'mdr_report_key': mdr_report_key,
                       'brand_name': brand_name,
                       'generic_name': generic_name, 
                       'device_name': device_name,
                       'product_problem': product_problem,
                       'adverse_event_flag': adverse_event_flag,
                       'event_type': event_type,
                       'manufacturer_d_name': manufacture_d_name,
                       'device_class': device_class,
                       'date_received': date_received, 
                       'date_of_event': date_of_event, 
                       'reporter_occupation_code': occupation, 
                       'device_report_pr oduct_code': device_code, 
                       'event_description': event_description,
                       'manufacturer_narrative': manu_narrative
                       })
   end_result = pd.DataFrame(res_df)
   return end_result



def MAUDE_QUERY_COUNT_BY_DATE(response):
    count_df = []
    for i in range(len(response['results'])):
        event = response['results'][i]
        date = event.get('time')
        count = event.get('count')
        count_df.append({
                        'date': date, 
                        'count': count})
    return pd.DataFrame(count_df)
