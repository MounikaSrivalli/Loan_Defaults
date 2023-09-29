''' Importing necessary libraries'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

''' Reading dataset'''
data = pd.read_csv('application_data.csv')

''' Finding the number of rows and columns'''
rows, columns = data.shape
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns',200)

'''cleaning the data'''
# list the null value columns and drop them
emptycol = data.isnull().sum()
emptycol = emptycol[emptycol.values > (0.3*len(emptycol))]
emptycol = list(emptycol[emptycol.values >= 0.3].index)
data.drop(labels=emptycol, axis=1, inplace=True)
# print((data.isnull().sum()/len(data)) *100)

'''list the null value rows and drop them'''
emptyrow = data.isnull().sum(axis=1)
emptyrow = emptyrow[emptyrow.values > (0.3*len(emptyrow))]
emptyrow = list(emptyrow[emptyrow.values >= 0.3].index)
data.drop(labels=emptyrow, axis=0, inplace=True)
# print(len(emptyrow))

'''Removing unwanted columns from the data'''
no_need = ['FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE', 'FLAG_EMAIL', 'DAYS_LAST_PHONE_CHANGE', 'FLAG_DOCUMENT_2',
           'FLAG_DOCUMENT_3', 'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6', 'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9', 'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12', 'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15', 'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18', 'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21']
data.drop(labels=no_need, axis=1, inplace=True)

'''Removing the not available(XNA) columns'''
# print(data.shape)
# print(data[data['CODE_GENDER']=='XNA'].shape)
data.loc[data['CODE_GENDER'] == 'XNA', 'CODE_GENDER'] = 'F'
# print(data['CODE_GENDER'].value_counts())
data = data.drop(data.loc[data['ORGANIZATION_TYPE'] == 'XNA'].index)
data[data['ORGANIZATION_TYPE'] == 'XNA'].index
# print(data[data['ORGANIZATION_TYPE']=='XNA'].shape)
# print(data.isnull().sum())
# data[numeric_columns]=data[numeric_columns].apply(pd.to_numeric)
# print(data.head(5))

'''creating bins for income amount'''
bins = [0, 25000, 50000, 75000, 100000, 125000, 150000, 175000, 200000, 225000, 250000,
        275000, 300000, 325000, 350000, 375000, 400000, 425000, 450000, 475000, 500000, 10000000000]
slot = ['0-25000', '25000-50000', '50000-75000', '75000-100000', '100000-125000', '125000-150000', '150000-175000', '175000-200000',
        '200000-225000', '225000-250000', '250000-275000', '275000-300000', '300000-325000', '325000-350000', '350000-375000',
        '375000-400000', '400000-425000', '425000-450000', '450000-475000', '475000-500000', '500000 and above']
data['AMT_INCOME_RANGE'] = pd.cut(data['AMT_INCOME_TOTAL'], bins, labels=slot)

''' creating bins for credit amount'''
bins = [0, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000,
        550000, 600000, 650000, 700000, 750000, 800000, 850000, 900000, 1000000000]
slots = ['0-150000', '150000-200000',            '200000-250000', '250000-300000', '300000-350000', '350000-400000', '400000-450000',
         '450000-500000', '500000-550000', '550000-600000', '600000-650000', '650000-700000', '700000-750000', '750000-800000','800000-850000', '850000-900000', '900000 and above']
data['AMT_CREDIT_RANGE'] = pd.cut(data['AMT_CREDIT'], bins=bins, labels=slots)

''' dividing dataset into two datasets
target 1 = clients who are facing difficulties to repay
target 0= others '''
target0_df = data.loc[data['TARGET'] == 0]
target1_df = data.loc[data['TARGET'] == 1]
# print(round(len(target0_df)/len(target1_df),2))

''' category wise univariate analysis of target 0 clients '''
def uniplot(df,col,title,hue =None):
    
    sns.set_style('whitegrid')
    sns.set_context('talk')
    plt.rcParams["axes.labelsize"] = 20
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['axes.titlepad'] = 30
    
    
    temp = pd.Series(data = hue)
    fig, ax = plt.subplots()
    width = len(df[col].unique()) + 7 + 4*len(temp.unique())
    fig.set_size_inches(width , 6)
    plt.xticks(rotation=45)
    plt.yscale('log')
    plt.title(title)
    ax = sns.countplot(data = df, x= col, order=df[col].value_counts().index,hue = hue,palette='magma') 
        
    plt.show()

'''plotting of income range based on gender'''
# uniplot(target0_df,col='AMT_INCOME_RANGE',title='Distribution of income range',hue='CODE_GENDER')

''' plotting of income type based on gender'''
# uniplot(target0_df,col='NAME_INCOME_TYPE',title='Distribution of income type',hue='CODE_GENDER')

'''plotting of contract type based on gender'''
# uniplot(target0_df,col='NAME_CONTRACT_TYPE',title='Distribution of contract type',hue='CODE_GENDER')
    
''' plotting of organization type for target 0 clients'''
# sns.set_style('whitegrid')
# sns.set_context('paper')
# plt.figure(figsize=(15,30))
# plt.rcParams["axes.labelsize"] = 20
# plt.rcParams['axes.titlesize'] = 22
# plt.rcParams['axes.titlepad'] = 30
# plt.title("Distribution of Organization type for target - 0")
# plt.xticks(rotation=90)
# plt.xscale('log')
# sns.countplot(data=target0_df,y='ORGANIZATION_TYPE',order=target0_df['ORGANIZATION_TYPE'].value_counts().index,palette='cool')
# plt.show()

'''category wise univariate analysis of target 1 clients
   plotting of income range based on gender'''
uniplot(target1_df,col='AMT_INCOME_RANGE',title='Distribution of income range',hue='CODE_GENDER')

''' plotting of income type based on gender'''
# uniplot(target1_df,col='NAME_INCOME_TYPE',title='Distribution of income type',hue='CODE_GENDER')

''' plotting of contract type based on gender '''
# uniplot(target0_df,col='NAME_CONTRACT_TYPE',title='Distribution of contract type',hue='CODE_GENDER')

'''plotting of organization type for target 1 clients'''
# sns.set_style('whitegrid')
# sns.set_context('paper')
# plt.figure(figsize=(15,30))
# plt.rcParams["axes.labelsize"] = 20
# plt.rcParams['axes.titlesize'] = 22
# plt.rcParams['axes.titlepad'] = 30
# plt.title("Distribution of Organization type for target - 0")
# plt.xticks(rotation=90)
# plt.xscale('log')
# sns.countplot(data=target1_df,y='ORGANIZATION_TYPE',order=target0_df['ORGANIZATION_TYPE'].value_counts().index,palette='cool')
# plt.show()

'''Box plotting for univariate variables'''
def univariate_numerical(data,col,title):
    sns.set_style('whitegrid')
    sns.set_context('talk')
    plt.rcParams["axes.labelsize"] = 20
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['axes.titlepad'] = 30
    
    plt.title(title)
    plt.xscale('log')
    
    sns.boxplot(data =target1_df, x=col,orient='v')
    plt.show()

''' Finding outliers and max clients for credit amount for both target 0 and target 1 datasets'''
# univariate_numerical(data=target0_df,col='AMT_CREDIT',title='Distribution of credit amount')
# univariate_numerical(data=target1_df,col='AMT_CREDIT',title='Distribution of credit amount')

'''Finding outliers and max clients for income amount for both target 0 and target 1 datasets'''
# univariate_numerical(data=target0_df,col='AMT_INCOME_TOTAL',title='Distribution of income amount')
# univariate_numerical(data=target1_df,col='AMT_INCOME_TOTAL',title='Distribution of income amount')

'''Finding outliers and max clients for annuity amount for both target 0 and target 1 datasets'''
# univariate_numerical(data=target0_df,col='AMT_ANNUITY',title='Distribution of annuity amount')
# univariate_numerical(data=target1_df,col='AMT_ANNUITY',title='Distribution of annuity amount')
    
'''Box plotting for bivariate variables of target 0 dataset
   Box plotting for credit amount'''
# plt.figure(figsize=(16,12))
# plt.xticks(rotation=45)
# sns.boxplot(data =target0_df, x='NAME_EDUCATION_TYPE',y='AMT_CREDIT', hue ='NAME_FAMILY_STATUS',orient='v')
# plt.title('Credit amount vs Education Status')
# plt.show()

'''Box plotting for income amount'''
# plt.figure(figsize=(16,12))
# plt.xticks(rotation=45)
# plt.yscale('log')
# sns.boxplot(data =target0_df, x='NAME_EDUCATION_TYPE',y='AMT_INCOME_TOTAL', hue ='NAME_FAMILY_STATUS',orient='v')
# plt.title('Income amount vs Education Status')
# plt.show()

'''Box plotting for bivariate variables of target 1 dataset'''
# Box plotting for credit amount
# plt.figure(figsize=(16,12))
# plt.xticks(rotation=45)
# sns.boxplot(data =target1_df, x='NAME_EDUCATION_TYPE',y='AMT_CREDIT', hue ='NAME_FAMILY_STATUS',orient='v')
# plt.title('Credit amount vs Education Status')
# plt.show()

''' Box plotting for income amount '''
# plt.figure(figsize=(16,12))
# plt.xticks(rotation=45)
# plt.yscale('log')
# sns.boxplot(data =target1_df, x='NAME_EDUCATION_TYPE',y='AMT_INCOME_TOTAL', hue ='NAME_FAMILY_STATUS',orient='v')
# plt.title('Income amount vs Education Status')
# plt.show()


''' Analysing previous data details
 Reading dataset '''
data1 = pd.read_csv("previous_application.csv")

''' cleaning the data
 list the null value columns and drop them '''
emptycol1 = data1.isnull().sum()
emptycol1 = emptycol1[emptycol1.values>(0.3*len(emptycol1))]

''' droping the empty columns '''
emptycol1 = list(emptycol1[emptycol1.values>=0.3].index)
data1.drop(labels=emptycol1,axis=1,inplace=True)

''' Removing the not available(XNA) column values '''
data1 = data1.drop(data1[data1['NAME_CASH_LOAN_PURPOSE']== 'XNA'].index)
data1 = data1.drop(data1[data1['NAME_CASH_LOAN_PURPOSE']== 'XAP'].index)

''' merging the application dataset and with previous dataset '''
new_data=pd.merge(left=data,right=data1,how='inner',on='SK_ID_CURR',suffixes='_x')

''' Renaming the column names after merging is done '''
new_data1 = new_data.rename({'NAME_CONTRACT_TYPE_' : 'NAME_CONTRACT_TYPE','AMT_CREDIT_':'AMT_CREDIT','AMT_ANNUITY_':'AMT_ANNUITY',
                         'WEEKDAY_APPR_PROCESS_START_' : 'WEEKDAY_APPR_PROCESS_START',
                         'HOUR_APPR_PROCESS_START_':'HOUR_APPR_PROCESS_START','NAME_CONTRACT_TYPEx':'NAME_CONTRACT_TYPE_PREV',
                         'AMT_CREDITx':'AMT_CREDIT_PREV','AMT_ANNUITYx':'AMT_ANNUITY_PREV',
                         'WEEKDAY_APPR_PROCESS_STARTx':'WEEKDAY_APPR_PROCESS_START_PREV',
                         'HOUR_APPR_PROCESS_STARTx':'HOUR_APPR_PROCESS_START_PREV'}, axis=1)

''' Removing unwanted columns '''
new_data1.drop(['SK_ID_CURR','WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START','REG_REGION_NOT_LIVE_REGION', 
              'REG_REGION_NOT_WORK_REGION','LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
              'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY','WEEKDAY_APPR_PROCESS_START_PREV',
              'HOUR_APPR_PROCESS_START_PREV', 'FLAG_LAST_APPL_PER_CONTRACT','NFLAG_LAST_APPL_IN_DAY'],axis=1,inplace=True)

''' Univariate analysis based on contract status '''
# sns.set_style('whitegrid')
# sns.set_context('talk')
# plt.figure(figsize=(15,30))
# plt.rcParams["axes.labelsize"] = 20
# plt.rcParams['axes.titlesize'] = 22
# plt.rcParams['axes.titlepad'] = 30
# plt.xticks(rotation=90)
# plt.xscale('log')
# plt.title('Distribution of contract status with purposes')
# sns.countplot(data = new_data1, y= 'NAME_CASH_LOAN_PURPOSE',order=new_data1['NAME_CASH_LOAN_PURPOSE'].value_counts().index,hue = 'NAME_CONTRACT_STATUS',palette='magma') 
# plt.show()

''' Analysis of distribution of Loan purpose with target '''
# sns.set_style('whitegrid')
# sns.set_context('talk')
# plt.figure(figsize=(15,30))
# plt.rcParams["axes.labelsize"] = 20
# plt.rcParams['axes.titlesize'] = 22
# plt.rcParams['axes.titlepad'] = 30
# plt.xticks(rotation=90)
# plt.xscale('log')
# plt.title('Distribution of purposes with target ')
# sns.countplot(data = new_data1, y= 'NAME_CASH_LOAN_PURPOSE',order=new_data1['NAME_CASH_LOAN_PURPOSE'].value_counts().index,hue = 'TARGET',palette='magma') 
# plt.show()

''' Performing bivariate analysis after merge '''
''' Box plot of credit amount vs loan purpose'''
# plt.figure(figsize=(16,12))
# plt.xticks(rotation=90)
# plt.yscale('log')
# sns.boxplot(data =new_data1, x='NAME_CASH_LOAN_PURPOSE',hue='NAME_INCOME_TYPE',y='AMT_CREDIT_PREV',orient='v')
# plt.title('Prev Credit amount vs Loan Purpose')
# plt.show()

''' Box plot of prev credit amount vs housing type'''
# plt.figure(figsize=(16,12))
# plt.xticks(rotation=90)
# sns.barplot(data =new_data1, y='AMT_CREDIT_PREV',hue='TARGET',x='NAME_HOUSING_TYPE')
# plt.title('Prev Credit amount vs Housing type')
# plt.show()
