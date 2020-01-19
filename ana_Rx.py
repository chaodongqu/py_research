#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 10:25:16 2020

@author: quchaodong
"""

#import numpy as np
import pandas as pd 
#import matplotlib.pyplot as plt


class StockProfile:
    code=''
    start_buy_date=''
    end_date=''
    max_pay=0
    
    buy = 0;
    vol_hold = 0;
    
    def __init__(self, code):
        self.code = code

    def info(self ):
        print( self.code , 
              '\t' ,self.start_buy_date,
              '\t' , self.buy);
    
    def OnHandle(self , row):
        flag = row['flag']
        money = row['money']        
        vol = row['vol']  
        
        if(self.buy == 0 ):
            self.start_buy_date = row['date1']
        
        if( flag.find('证券买入') == 0 ):
            self.buy = self.buy - money
            self.vol_hold = self.vol_hold + vol
            #print(buy , ' -' , money)
        elif(  flag.find('证券卖出') == 0  ):
            self.buy = self.buy + money
            self.vol_hold =self.vol_hold - vol
            #print(buy , ' + ' , money)
        else :
            return 0
            
        if self.vol_hold ==0 :
            # 本次利润计算结束
            #print ('after saled out, earn :\t',  self.buy );
            #self.buy = 0;
            #self.vol_hold = 0;   
            #print ('start new ')
            return 1 
        
        elif self.vol_hold < 0 :
            # erro data
            print ('start new <0 ')
            self.buy = 0;
            self.vol_hold = 0;    
        
        return 0;


def getCodeData(name , oneCodeData):
    a1 = oneCodeData.sort_values(['date1'])
    return a1

allProfiles = [];
# 计算收益
def cacCodeRet( code, codeDetail):
    
    sp = StockProfile(code);
    
    for index, row in codeDetail.iterrows():
        ret = sp.OnHandle(row)
        if( 1 == ret ):
            #print('----');
            allProfiles.append(sp)
            
            # 新建对象
            sp = StockProfile(code);
            
        
    return ;

fileName='/Users/quchaodong/stu/tmp/20191230.xls'
fileName='/Users/quchaodong/stu/tmp/data2-12.xls'
data = pd.read_excel(fileName )
#print(data.head())

colMap =  {
            "成交日期": "date1",        
            "成交时间": "time1",
            "证券代码": "code",
            "证券名称":"name",
            "买卖标志":"flag",
             "成交价格":"price",
            "成交数量":"vol",
            "成交金额":"money"}

dt = data.rename(columns=colMap  ) 
usedCol = list(colMap.values()) 
print( usedCol )

g= dt[usedCol].groupby('code')
allCodeDetail={}

for name, group in g:
    x = getCodeData (name , group)
    allCodeDetail[name] = x
    
#print(allCodeDetail[21])
for x in allCodeDetail:
    cacCodeRet( x , allCodeDetail[x])

print('')

for s in allProfiles:
    #print(s)
    s.info()
  
    
    
    