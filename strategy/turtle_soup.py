#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 18:31:26 2020
验证海龟汤算法
Turtle Soup' pattern
1. Today must make a new 20-day low-the lower the better.
前期已经形成支撑20日LOW
2 The previous 20-day low must have occurred at least four trading sessions earlier. This is very important.

#必须跌穿前期 20 日低点 ，在前期最低点 5 TICK一下，挂 buy stop order
3 After the market falls below the prior 20-day low, 
place an entry buy stop 5-10 ticks above the previous 20-day low. 
This buy stop is good for today only.

#设置止损
4 If the buy stop is filled, immediately place an initial good-till -cancelled sell stoploss one tick under today's low.

# 如果运动方向有利，对象利润 ，也许后续行情会持续几天
5 As the position becomes profitable, use a trailing stop to prevent giving back profits. Some of these trades will last two to three hours and some will last a few days. Due to the volatility and the noise at these 20-day high and
low points, each market behaves differently.
#反复入场
6 Re-entry Rule: If you are stopped out on either day one or day two of the trade, you may re- enter on a buy Stop at your original entry price level (day one and day two only). By doing this, you should increase your profitability by a small amount.


http://blog.sina.com.cn/s/blog_53b2d1710100jp1p.html

@author: quchaodong
"""
import sys 
sys.path.append("..") 

#import numpy as np
import pandas as pd 
import tongxinda_data  as txd  
import math
import os

code_name = ""

def test( dataFile , start_time  ,nRollWnd ):    

    dt = txd.read_txt_data(dataFile)
    
    #选取一段时间
    dd = dt[dt.index > start_time ]
    #dd = dt.loc['2019-01-01':'2020-2-1']
    #dd[['close','open']].plot(grid=True, figsize=(20, 10))
    
    minx = dd['close'].rolling( nRollWnd ).min()
    rt = pd.DataFrame({   
    'close': dd['close'],
    'minx': minx})
    #print(minx.count() , dd['close'].count())
    #print(minx.head(nRollWnd*2))
    #print(dd.head(nRollWnd*2))

    
    #dd[['close','sam']].plot(grid=True, figsize=(20, 10))
    #rt.plot(grid=True)
    
    handle(rt , nRollWnd)

def isPreLowExist( dt  , period , index):
    #2 The previous 20-day low must have occurred at least four trading sessions earlier. 
    # This is very important.

    # if pre low in 4 trading seesions , give up
    cur_data  =  dt.iloc[index]
    for i in range(0 , 4) :
        row =dt.iloc[ index - i -1 ] 
        if  row['minx'] < cur_data['minx'] :
            return 0
    
    return 1

def handle( dt  , period ):
    
    '''
    direction = 0 不变 1 上升 , -1 下降
    '''
    dt['dir'] = 0;
    dt['buy'] = 0;
    count = dt['close'].count()
    
    for i in range( period, count  ):        
        row =dt.iloc[i]
        if   math.isnan( row['minx']):
            continue
        
        #print( row , row['minx'] , row['close'])
        pre = dt.iloc[i-1]
        
        #前一个 LOW  小于现在 LOW 
        if pre['minx'] < row['minx']:
            dt.iloc[i, 2] =1
            continue
            
        if pre['minx'] > row['minx']:
            dt.iloc[i, 2] = -1
        
        #如果是下降趋势，并且是新低
        if  dt.iloc[i, 2] == -1:
            #判断，前期已经形成支撑20日LOW （至少4个交易日）
            if isPreLowExist(dt, period , i): 
                dt.iloc[i, 3] = row['close']
                continue
            
     
    
    dt.plot(grid=True , title=code_name )#, figsize=(18, 10))
    #print(dt)

    return    

if __name__=="__main__":
    print("main")
    filepath = '/Users/quchaodong/stu/test_invest_data/edata'
    
    
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        fileName = os.path.join('%s/%s' % (filepath, allDir))
        #print(fileName) # .decode('gbk')是解决中文显示乱码问题
        code_name = allDir[:-4]
        test( fileName , '2019-01-01' , 20)
'''
    files = ['/Users/quchaodong/stu/py_research/tmp/edata/SZ#000768.txt' ,
             '/Users/quchaodong/stu/py_research/tmp/edata/SZ#002079.txt']

    for dataFile in files:
        test( dataFile , '2019-01-01' , 20)
'''