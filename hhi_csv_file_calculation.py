# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 06:30:29 2015
@author: Andrew
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_name = "firm_market_size.csv" #enter your .csv file path

df = pd.read_table(file_name, sep=',')

#HHI Calculation Details & Use: http://www.justice.gov/atr/public/guidelines/hhi.html

#get the values of each apps revenue, date, and firm
df2 = df[["date","revenue","firm"]]

#group revenue by date, firm, and sum the revenue for each firm
firm_rev = df2.groupby(["date","firm"]).sum()

#group revenue by date and sum the market size for the day
m_rev = df2.groupby(["date"])["revenue"].sum()

#Herfindahl-Hirschman Index - HHI Function for each date
def hhi(firm_rev, m_rev):
    #reset the indexes
    firm_rev = firm_rev.reset_index()
    m_size = m_rev.reset_index()
    
    #rename the revenue column
    m_size.rename(columns={'date': 'date', 'revenue': 'm_revenue'}, inplace=True)
    
    #perform outer join for the columns
    m_data = pd.merge(firm_rev, m_size, on='date', how='outer')
    
    #Calculate market share of each firm as a new column
    m_data['m_share'] = pd.Series((m_data["revenue"]/m_data["m_revenue"])*100, index=m_data.index)
    
    #Calculate square of market share of each firm as a new column
    m_data['sq_m_share'] = pd.Series(m_data["m_share"]*m_data["m_share"], index=m_data.index)
    
    #return the HHI, or sum of sq_m_share for the given date
    hhi_range = m_data.groupby("date")["sq_m_share"].sum()
    
    #do a little analysis
    
    plt.figure()
    hhi_range.hist(bins=30)
    
    plt.figure()
    hhi_range.plot()
    
    summary_stats = hhi_range.describe()
    print "median " + str(np.median(hhi_range))
    print summary_stats
    
    return m_data, hhi_range

hhi(firm_rev, m_rev)