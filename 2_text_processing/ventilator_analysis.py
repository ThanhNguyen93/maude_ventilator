#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 13:09:19 2020

@author: thanhng
"""


data = pd.read_csv('ventilator_clean.csv')

data.columns

data['product_problem_edit'] = data['product_problem'].copy()

data['product_problem_edit'] = \
    data['product_problem_edit'].replace("['No Audible Alarm']", "['Device Alarm System']")
          
data['product_problem_edit'] = \
data['product_problem_edit'].replace("['Noise, Audible']", "['Device Alarm System']")

    
data['product_problem_edit'] = \
    data['product_problem_edit'].replace("['Failure to Charge']", "['Battery Problem']")


data['brand_name'] = data['brand_name'].replace("['TRILOGY100']", "['TRILOGY 100']")

#check if correctly replace text
for text in data['brand_name']:
    test = re.search(r'TRILOGY100', text)
    if test:
        print(text)





def GET_TOP_20(data, col):
    df = pd.DataFrame(data[col].value_counts()[:20]).reset_index()
    df.columns = ['product_problem', 'count']
    df['percentage'] = df['count']/data.shape[0]
    return df

GET_TOP_20(data, 'brand_name')

GET_TOP_20(data, 'product_problem_edit')

GET_TOP_20('event_type')



####################
death = data[data['event_type'] == 'Death']


GET_TOP_20(death, 'adverse_event_flag')

GET_TOP_20(death, 'product_problem_edit')


#################

injury = data[data['event_type'] == 'Injury']


GET_TOP_20(injury, 'adverse_event_flag')

GET_TOP_20(injury, 'product_problem_edit')


###################
malfunction = data[data['event_type'] == 'Malfunction']

GET_TOP_20(malfunction, 'adverse_event_flag')

GET_TOP_20(malfunction, 'product_problem_edit')


death[death['product_problem'] == "['Device Alarm System']"]['brand_name'].value_counts()

for i in death[death['product_problem'] == "['Device Alarm System']"]['text_clean']:
    print(i, '\n')

###########

def CONVERT_INT_TO_DATE(data):

    data['date_of_event'] = data['date_of_event'].astype(int).astype(str)

    #convert to datetime
    data['event_date'] = pd.to_datetime(data['date_of_event'])
    #extract yr
    data['event_yr'] = pd.DatetimeIndex(data['event_date']).year
    data= data.sort_values('event_date')
    return data

date_df = CONVERT_INT_TO_DATE(data)

date_df['month_of_event'] = pd.DatetimeIndex(date_df['event_date']).month



yr_2020 = date_df[date_df['event_yr'] == 2020]

#########
yr_2020_march = yr_2020[yr_2020['month_of_event'] == 3]

GET_TOP_20(yr_2020_march, 'product_problem_edit')

GET_TOP_20(yr_2020_march, 'brand_name')


GET_TOP_20(yr_2020_march, 'adverse_event_flag')

for i in yr_2020_march[yr_2020_march['event_type'] == 'Death']['text_clean']:
    print(i, '\n')


###########


yr_2020_april = yr_2020[yr_2020['month_of_event'] == 4]

col_lst = ['brand_name', 'product_problem_edit']
for col in col_lst:
    print(GET_TOP_20(yr_2020_april, col), '\n')
    
data.to_csv('ventilator_clean.csv', index = False)


