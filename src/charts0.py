#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:37:31 2019

@author: dudulala
"""

import pandas as pd
import seaborn as sns
#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
from matplotlib import pyplot
np.random.seed(1) # For reproducibility
plt.style.use('seaborn')



data_price_or = pd.read_csv("data/result_price.csv",index_col = False)
data_price = data_price_or.iloc[:,1:]
data_info_or = pd.read_csv("data/result.csv",index_col = False)
data_info = data_info_or.iloc[:,1:]
    
def avg_price():
    avg = []
    for i in range (len(data_price.iloc[:,0])):
        avg_price = (data_price.iloc[i,1]+data_price.iloc[i,2])/2
        avg.append(avg_price)
            
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2.- 0.2, 1.03*height, '%s' % int(height))
        
        
    name_list = ['Pudong', 'Yangpu', 'Xuhui', 'Jingan', 'Hongkou', 'Huangpu', 'Changning']
    num_list = avg
    cm = ['r','orange','gold','yellowgreen','darkcyan','cornflowerblue','mediumpurple']
    autolabel(plt.bar(range(len(num_list)), num_list, color=cm, tick_label=name_list))
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f RMB/m^2'))
    plt.text(-0.5,87000 ,"1 USD=7.05 RMB ", size = 13, alpha = 0.6)
    plt.ylim(45000,91000)
    plt.title("Overall house prices in seven districts in Shanghai in November and December")
    plt.show()
    
    
area_name = data_price.iloc[:,0]

mean_price = []
max_price = []
min_price = []
for i in area_name:
    area = []
    for j in range(len(data_info.iloc[:,0])):
        if data_info.iloc[j,0]==i:
            area.append(data_info.iloc[j,2])
    mean_price.append(np.mean(area))
    max_price.append(np.max(area))
    min_price.append(np.min(area))
    
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.- 0.2, 1.03*height, '%s' % int(height))


def Average_price():
    name_list = ['Pudong', 'Yangpu', 'Xuhui', 'Jingan', 'Hongkou', 'Huangpu', 'Changning']
    num_list = mean_price
    cm = ['r','orange','gold','yellowgreen','darkcyan','cornflowerblue','mediumpurple']
    autolabel(plt.bar(range(len(num_list)), num_list, color=cm, tick_label=name_list))
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f RMB/m^2'))
    plt.text(-0.5,87000 ,"1 USD=7.05 RMB ", size = 13, alpha = 0.6)
    plt.ylim(60000,96000)
    plt.title("Average price of the hottest 150 communities in each of the seven areas of Shanghai")
    plt.show()
    
def Min_price():
    name_list = ['Pudong', 'Yangpu', 'Xuhui', 'Jingan', 'Hongkou', 'Huangpu', 'Changning']
    num_list = min_price
    cm = ['r','orange','gold','yellowgreen','darkcyan','cornflowerblue','mediumpurple']
    autolabel(plt.bar(range(len(num_list)), num_list, color=cm, tick_label=name_list))
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f RMB/m^2'))
    plt.text(-0.5,46000 ,"1 USD=7.05 RMB ", size = 13, alpha = 0.6)
    plt.ylim(20000,48000)
    plt.title("Min price of the hottest 150 communities in each of the seven areas of Shanghai")
    plt.show()
  
def Max_price():
    name_list = ['Pudong', 'Yangpu', 'Xuhui', 'Jingan', 'Hongkou', 'Huangpu', 'Changning']
    num_list = max_price
    cm = ['r','orange','gold','yellowgreen','darkcyan','cornflowerblue','mediumpurple']
    autolabel(plt.bar(range(len(num_list)), num_list, color=cm, tick_label=name_list))
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f RMB/m^2'))
    plt.text(-0.5,300000 ,"1 USD=7.05 RMB ", size = 13, alpha = 0.6)
    plt.ylim(90000,315000)
    plt.title("Max price of the hottest 150 communities in each of the seven areas of Shanghai")
    plt.show()
    
def Variable_distribution():
    sns.distplot(data_info.iloc[0:,2])
    
def heatmap():
    sns.set(style = "whitegrid")
    x = data_info.iloc[:,4] #longitude
    y = data_info.iloc[:,5] #latitude
    z = data_info.iloc[0:,2]#point size
    cm = plt.get_cmap('jet')
    fig,ax = plt.subplots(figsize = (15,10))
    
    bubble = ax.scatter(x, y , s =(z/10000)*(z/20000), c = z, cmap = cm, linewidth = 0.5, alpha = 0.5)
    ax.grid()
    fig.colorbar(bubble)
    ax.set_xlabel('longitude', fontsize = 15)
    ax.set_ylabel('latitude', fontsize = 15)
    plt.text(121.36,31.33 ,"1 USD=7.05 RMB ", size = 13, alpha = 0.6)
    plt.ylim(31.10,31.35)
    plt.xlim(121.35,121.65)
    plt.show()
