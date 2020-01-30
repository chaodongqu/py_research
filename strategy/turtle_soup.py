#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 18:31:26 2020
验证海龟汤算法
Turtle Soup' pattern
1. Today must make a new 20-day low-the lower the better.
前期已经形成支撑20日LOW
2 The previous 20-day low must have occurred at least four trading sessions earlier. This is very important.

#反弹收复前期低点5 TICK
3 After the market falls below the prior 20-day low, place an entry buy stop 5-10 ticks above the previous 20-day
low. This buy stop is good for today only.

#设置止损
4 If the buy stop is filled, immediately place an initial good-till -cancelled sell stoploss one tick under today's low.

# 如果运动方向有利，对象利润 ，也许后续行情会持续几天
5 As the position becomes profitable, use a trailing stop to prevent giving back profits. Some of these trades will last two to three hours and some will last a few days. Due to the volatility and the noise at these 20-day high and
low points, each market behaves differently.
#反复入场
6 Re-entry Rule: If you are stopped out on either day one or day two of the trade, you may re- enter on a buy Stop at your original entry price level (day one and day two only). By doing this, you should increase your profitability by a small amount.

@author: quchaodong
"""
import sys 
sys.path.append("..") 

#import numpy as np
import pandas as pd 
import tongxinda_data  as txd  


def test( dataFile , start_time ):    
    dt = txd.read_txt_data(dataFile)
    
    #选取一段时间
    dd = dt[dt.index > start_time ]
    #dd = dt.loc['2019-01-01':'2020-2-1']
    #dd[['close','open']].plot(grid=True, figsize=(20, 10))
    
    minx = dd['close'].rolling(10).min()
    rt = pd.DataFrame({   
    'close': dd['close'],
    'minx': minx})

    
    #dd[['close','sam']].plot(grid=True, figsize=(20, 10))
    rt.plot(grid=True)
    

if __name__=="__main__":
    print("main")
    dataFile= "/Users/quchaodong/stu/py_research/tmp/edata/SZ#002129.txt"

    test( dataFile , '2019-01-01')
