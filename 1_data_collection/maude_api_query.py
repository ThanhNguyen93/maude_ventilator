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

#return 3
url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "SARS-COV-2"'
        '+device.brand_name: "SARS-COV-2"'
        '+device.openfda.device_name: "SARS-COV-2"'
        '+mdr_text.text: "SARS-COV-2"'
         '&sort=date_of_event:desc'
         '&limit=100'
         )

#return 152
url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "corona"'
        '+device.brand_name: "corona"'
        '+device.openfda.device_name: "corona"'
        '+ mdr_text.text: "corona"'
         '&sort=date_of_event:desc'
         '&limit=100'
        # '&skip=100'
         )
#185
url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "COVID-19"'
        '+device.brand_name: "COVID-19"'
        '+device.openfda.device_name: "COVID-19"'
        '+mdr_text.text: "COVID-19"'
         '&sort=date_of_event:desc'
         '&limit=100'
         '&skip=100'
         )

#return 14
url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "COVID19"'
        '+device.brand_name: "COVID19"'
        '+device.openfda.device_name: "COVID19"'
        '+mdr_text.text: "COVID19"'
         '&sort=date_of_event:desc'
         '&limit=100'
        # '&skip=100'
         )

url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "COBAS SARS-COV-2 TEST"'
        '+device.brand_name: "COBAS SARS-COV-2 TEST"'
        '+device.openfda.device_name: "COBAS SARS-COV-2 TEST"'
        '+mdr_text.text: "COVID19"'
         '&sort=date_of_event:desc'
         '&limit=100'
        # '&skip=100'
         )

url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "2019-novel"'
        '+device.brand_name: "2019-novel"'
        '+device.openfda.device_name: "2019-novel"'
        '+mdr_text.text: "COVID19"'
         '&sort=date_of_event:desc'
         '&limit=100'
        # '&skip=100'
         )

response = requests.get(url_covid_text).json()

#check search results
response['meta']

response['results']


data_novel = mn.MAUDE_DB(response)

data_cobas = mn.MAUDE_DB(response)

data_corona_1 = mn.MAUDE_DB(response)
data_corona = mn.MAUDE_DB(response)


data_sars = mn.MAUDE_DB(response)


data_covid19 = mn.MAUDE_DB(response)


data_covid_19 = mn.MAUDE_DB(response)
data_covid_19_1 = mn.MAUDE_DB(response)


maude_covid = pd.concat([data_corona, data_corona_1, data_sars, data_covid19, data_covid_19, data_covid_19_1])

maude_covid.to_csv('corona_keyword.csv', index = False)


###query api multiple times


start = 100
for i in range(3):
    skip = start*i

    url_covid_text = ('https://api.fda.gov/device/event.json?'
        'api_key=lvmKNeCdZN3OX0QttZL2ovaDsFpLb26J5otfRFRh'
        '&search=device.generic_name: "corona"'
        '+device.brand_name: "corona"'
        '+device.openfda.device_name: "corona"'
        '+ mdr_text.text: "corona"'
         '&sort=date_of_event:desc'
         '&limit=100'
         )
    update_url = url_covid_text+'&skip='+str(skip)
    response = requests.get(update_url).json()
    data = mn.MAUDE_DB(response)
    list_of_data.append(data)


combine_df = pd.concat(list_of_data)

len(set(combine_df['mdr_report_key']))

combine_df=combine_df.drop_duplicates(subset=['mdr_report_key']).reset_index(drop=True)

combine_df.to_csv('ventilator_total.csv', index = False)




###clean 'covid' text

combine_df.iloc[101]

for index in range(combine_df.shape[0]):
    text = combine_df.loc['event_description', index]
    print(index, text)

   # text = end_result[ 'manufacturer_narrative'][index][0]

#extract sentence contain 'covid'
    result = re.search(r'([^.]*?covid[^.]*\.)', text,  flags=re.IGNORECASE)
    if result:
        print(result.group(0), '\n')
