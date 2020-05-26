#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:15:36 2020

@author: thanhng
"""

from maude_mining import *

import maude_mining as mn


url = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "ventilator"' 
        '+device.brand_name: "ventilator"'
        '+device.openfda.device_name: "ventilator"'                                                                                                                       
         '+AND+date_of_event:[1900-01-01+TO+2020-04-30]'
         '&sort=date_of_event:desc' 
         '&limit=100'
         )
        

url_count = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&count=date_of_event'
         '&search=date_of_event:[2020-04-01+TO+2020-04-30]'
         '&sort=date_of_event:desc'     
         '&limit=100'
         )


url_device_count=('https://api.fda.gov/device/event.json?'
                  'search=device.generic_name:ventilator'
                  '&count=event_type.exact')

url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "SARS-COV-2"' 
        '+device.brand_name: "SARS-COV-2"'
        '+device.openfda.device_name: "SARS-COV-2"' 
         '&sort=date_of_event:desc'
         '&limit=100'
         )

url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "coronavirus"' 
        '+device.brand_name: "coronavirus"'
        '+device.openfda.device_name: "coronavirus"' 
         '&sort=date_of_event:desc'
         '&limit=100'
         )        

response = requests.get(url).json()

#check search results
response['meta']

response['results']

data = mn.MAUDE_DB(response)


data.to_csv('coronavirus.csv', index = False)



list_of_data = []








start = 100
for i in range(890):
    skip = start*i  
    
    url = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "ventilator"' 
        '+device.brand_name: "ventilator"'
        '+device.openfda.device_name: "ventilator"'                                                                                                                       
         '+ AND+date_of_event:[1900-01-01+TO+2010-01-01]'
         '&sort=date_of_event:desc'     
         '&limit=100')
    update_url = url+'&skip='+str(skip)
    response = requests.get(update_url).json()
    data = mn.MAUDE_DB(response)
    list_of_data.append(data)


combine_df = pd.concat(list_of_data)

len(set(combine_df['mdr_report_key']))

combine_df['date_of_event']

combine_df.columns

combine_df=combine_df.drop_duplicates(subset=['mdr_report_key']).reset_index(drop=True)


combine_df.to_csv('ventilator_total.csv', index = False)


combine_df['brand_name'].value_counts()[:50]





###clean 'covid' text

combine_df.iloc[101]

for index in range(combine_df.shape[0]):
    text = combine_df.loc['event_description', index]
    print(index, text)
    
   # text = end_result[ 'manufacturer_narrative'][index][0]
   

    result = re.search(r'([^.]*?covid[^.]*\.)', text,  flags=re.IGNORECASE)
    if result:
        print(result.group(0), '\n')
        

pd.DataFrame(end_result['device_name'].value_counts())


end_result[end_result['device_name'] == "['Disinfectant, Medical Devices']"]





