# -*- coding: utf-8 -*-
"""
@author: UMEAIMAN
"""

import pandas as pd 

df = pd.read_csv('C:/Users/AIMAN/data science learn/Glassdoor-Scraper-Final-main/glassdoor_jobs.csv')


### features to change
# salary column
# job desc- extract features
# size of company
# old os the firm- new vari

#  drop columns index and records with no salary 
df = df[df['Salary Estimate']!='-1']
#df = df.iloc[:,1:]

# salary is per hour or not
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['Employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided' in x.lower() else 0)

df['salary'] = df['Salary Estimate'].apply(lambda x: x.split("(")[0].replace('K','').replace('$','').replace("Employer Provided Salary:","").replace("Per Hour",""))

df['min_salary'] = df['salary'].apply(lambda x: x.split("-")[0]).astype('float')
df['max_salary'] = df['salary'].apply(lambda x: x.split("-")[1]).astype('float')

#where salary is hourly- conver to yearly 
df['min_salary'] = df['min_salary'] + round(df['hourly']*df['min_salary']*1.919, 0)
df['max_salary'] = df['max_salary'] + round(df['hourly']*df['max_salary']*1.919, 0)


# job description
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['r'] = df['Job Description'].apply(lambda x: 1 if ' r ' in x.lower() else 0)
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['pipeline'] = df['Job Description'].apply(lambda x: 1 if 'pipeline' in x.lower() else 0)
df['ml'] = df['Job Description'].apply(lambda x: 1 if 'machine learning' in x.lower() else 0)
df['tableau'] = df['Job Description'].apply(lambda x: 1 if ' tableau ' in x.lower() else 0)
df['bi'] = df['Job Description'].apply(lambda x: 1 if 'power bi ' in x.lower() else 0)

# size of company
def company_type(ip):
    if '10000' in ip.lower():
        return 'L'
    elif '1000' in ip.lower() or '1001' in ip.lower():
        return 'M'
    elif 'unknown' in ip.lower() or '-1' in ip.lower():
        return '-1'
    else:
        return 'S'
        
df['employees'] = df['Size'].apply(lambda x: company_type(x))

# old the firm
df['age'] = df['Founded'].apply(lambda x: 2023- x if x>1 else -1)


df.to_csv('cleaned_data.csv',index = False)
