#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install sodapy


# In[2]:


# importing libraries
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sodapy import Socrata


# In[4]:


# importing data
#get request using Socrata
client = Socrata("data.cdc.gov", None)
results = client.get("9mfq-cb36", limit=60000)
# putting data into a dataframe
results_df = pd.DataFrame.from_records(results)
results_df


# In[5]:


results_df.shape


# In[6]:


results_df.info()


# In[7]:


results_df.isnull().sum()


# In[8]:


# dropping the null values
results_df.dropna(subset=['conf_cases', 'conf_death'], inplace=True)


# In[9]:


results_df.dtypes


# In[10]:


results_df['submission_date'] = pd.to_datetime(results_df['submission_date'])
results_df['year'] = results_df['submission_date'].dt.year
results_df = results_df[results_df['year'] == 2020]
warnings.filterwarnings("ignore")
results_df.head()


# In[11]:


results_df['state'].value_counts()	


# In[12]:


#testing to plot data on a graph
plt.figure(figsize=(50,15))
ax = sns.countplot(x="state", data=results_df,
                   linewidth=5,
                   edgecolor=sns.color_palette("dark", 24))
#plt.figure(figsize = (30,8))
#plt.bar(list(results_df['state']), list(results_df['conf_cases']), color ='maroon')


# In[13]:


#parsing data to just include confirmed deaths and cases
df = results_df.drop(columns=['consent_deaths', 'consent_cases', 'created_at','pnew_death','new_death','prob_death', 'pnew_case', 'prob_cases', 'tot_cases', 'new_case','tot_death'])
df.head()


# In[14]:


df.sort_values(['state'])


# In[15]:


df_cases = df.groupby('state').agg({'conf_cases': 'first'}).reset_index()
df_cases


# In[16]:


df = results_df.drop(columns=['submission_date', 'year'])
df_deaths = df.groupby('state').agg({'conf_death': 'first'})
df_deaths


# In[20]:


df.to_csv('output.csv', encoding = 'utf-8-sig') 
df_deaths.to_csv('statewise_deaths.csv', encoding = 'utf-8-sig')
df_cases.to_csv('statewise_cases.csv', encoding = 'utf-8-sig')


# In[ ]:




