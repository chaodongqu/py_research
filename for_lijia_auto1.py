# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:21:00 2018

读取 目录的文件, 
每个交易历史数据文件, 进行计算
输出每个文件的 5日最大最低值


@author: Administrator
"""

import numpy as np
import pandas as pd 
import os  
      

dataPath ="E:\\invest\\new_gxzq_v6\\T0002\\export\\"
#print dataPath
#names=["date","open","high","low","close","vol","vol_m"]



def test_min_max(data):
    #输入dataframe 
    val_cac = data['open']
    n = val_cac.size

    # cur 为前后5日最大值 输出 val +  datetime
    #cur 为前后5日最小值  输出 val -  datetme
    retv=[]
    retd=[]
    retf=[]
    
    for i in range(5,n-6):
        y = val_cac[i-5:i+5]
        if(y.max() == val_cac[i]):
            #print val_cac[i] , val_cac.index[i] , '+'
            retv.append(val_cac[i] )
            retd.append(val_cac.index[i] )
            retf.append(1)
        elif (y.min() == val_cac[i]):
            #print val_cac[i] , val_cac.index[i] , '-'
            retv.append(val_cac[i] )
            retd.append(val_cac.index[i] )
            retf.append(0)
    df = pd.DataFrame( {'v':retv ,'d':retd,'date':retd , 'f':retf})
    df = df.set_index('d')
    return df
      

def deal_path(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        print(root) #当前目录路径  
        print '---'
        
        print '---'
        print(files) #当前路径下所有非目录子文件
        for x in files:
            print root + "\\" + x 
            deal_file(root, x )            
            
    return 

def deal_file(filePath , filename ):
    dataPath = filePath + "\\" + filename
    names=["date","open","high","low","close","vol","vol_m"]
    
    x = pd.read_csv(dataPath,sep=',',skiprows=2,names =names,index_col=0)
    x = x[:-1]
    x.index = pd.to_datetime(x.index)
    
    df = test_min_max(x)
    df.to_csv( filePath + "\\" + filename.replace("txt" , "csv") )
    
    return 

deal_path(dataPath)