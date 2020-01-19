# -*- coding: utf-8 -*-
"""
Created on Sat Nov 04 21:54:59 2017

@author: Administrator

#如果当天价格 低于 std +　前日收盘价 , 次日是否修复

"""

import numpy as np
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
 
import tushare as ts


sd = ts.get_k_data('000973', ktype='d', autype='qfq', start='2017-10-01')
s1 = sd.set_index('date')

c_val = s1['close']

c_std = c_val.std()

print len(c_val) , c_std

for i in range(2,len(c_val) -1 ):
        if (c_val[i-1] - c_val[i] ) > c_std :
            print '---',c_val.index[i] , c_val[i-1] , c_val[i]
            buy = c_val[i-1] - c_std
            if c_val[i+1] > buy :
                print 'OK' , c_val[i] , buy, c_val[i+1]
            else:
                print 'error',c_val[i]