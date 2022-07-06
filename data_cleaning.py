import matplotlib.pyplot as plt
import pandas as pd
import re

data = pd.read_csv("raw_data_used.csv")

# Salary Parsing

data = data[data['Salary Estimate'] != '-1']
data['hourly'] = data['Salary Estimate'].apply(
    lambda x: 1 if 'per hour' in x.lower() else 0)
data['employer_provided'] = data['Salary Estimate'].apply(
    lambda x: 1 if 'employer provided salary' in x.lower() else 0)

salary = data['Salary Estimate'].apply(
    lambda x: x.split('(')[0])
minus_kd = salary.apply(lambda x: re.sub("[K$]", "", x))

minus_hour = minus_kd.apply(lambda x: re.sub("per hour", "", x))
minus_hour = minus_kd.apply(lambda x: re.sub("per hour", "", x))
minus_hour = minus_kd.apply(lambda x: re.sub(
    "employer provided salary:", "", x.lower()))
data['min_salary'] = minus_hour.apply(lambda x: int(x.split("-")[0]))
data['max_salary'] = minus_hour.apply(lambda x: int(x.split("-")[1][:2]))
data['average_salary'] = (data.min_salary+data.max_salary)/2

# company name text only
data['company_txt'] = data.apply(
    lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)
# state field
data['job_state'] = data['Location'].apply(lambda x: x.split(',')[1])
data['same_state'] = data.apply(
    lambda x: 1 if x.Location == x.Headquarters else -1, axis=1)
# age of company

data['age_company'] = data['Founded'].apply(lambda x: x if x < 0 else 2022-x)

# parsing of job description (python, sql, aws, excel, etc .. )

data['python'] = data['Job Description'].apply(
    lambda x: 1 if 'python' in x.lower() else 0)
data['sql'] = data['Job Description'].apply(
    lambda x: 1 if 'sql' in x.lower() else 0)
data['spark'] = data['Job Description'].apply(
    lambda x: 1 if 'spark' in x.lower() else 0)
data['aws'] = data['Job Description'].apply(
    lambda x: 1 if 'aws' in x.lower() else 0)
data['excel'] = data['Job Description'].apply(
    lambda x: 1 if 'excel' in x.lower() else 0)


data_out = data.drop(['Unnamed: 0'], axis=1)

data_out.to_csv('data_salaries_cleaned.csv', index=False)

