#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 10:25:16 2020
分析获利情况  华泰账户
@author: quchaodong
"""

#import numpy as np
import pandas as pd 
import datetime

#import matplotlib.pyplot as plt


class StockProfile:
    code=''
    name=''
    start_buy_date=''
    end_date=''
    max_pay=0
    
    buy = 0;
    vol_hold = 0;
    days = 0;
    
    def __init__(self, code , name ):
        self.code = code
        self.name = name
        self.start_buy_date = ''
        self.end_date = ''
        self.name = name
        self.buy = 0;
        self.vol_hold = 0;
        self.days = 0;
        

    def info(self ):
        d1 = datetime.datetime.strptime(self.start_buy_date, '%Y%m%d')
        d2 = datetime.datetime.strptime(self.end_date, '%Y%m%d')
        self.days = (d2 - d1).days



        print( '\t',self.code , 
              '\t' ,self.name , 
              '\t' ,self.start_buy_date,
              '\t' ,self.end_date,
              '\t' , self.buy,
              '\t' ,self.days,
              '');
    
    def OnHandle(self , row):
        flag = row['flag']
        money = row['money']        
        vol = row['vol']  
        #print (str(row['date1'] ))
        if(self.buy == 0 ):
            self.start_buy_date = str(row['date1'])
        
        if( flag.find('证券买入') == 0 ):
            self.buy = self.buy - money
            self.vol_hold = self.vol_hold + vol
            #print(self.vol_hold , ' \t buy ' , vol)
        elif(  flag.find('证券卖出') == 0  ):
            self.buy = self.buy + money
            # 注意 华泰导出数据，卖出vol 用负数表示
            self.vol_hold =self.vol_hold + vol
            #print(self.vol_hold , ' \t sell ' , vol)
        else :
            return 0
            
        if self.vol_hold ==0 :
            # 本次利润计算结束
            #print ('after saled out, earn :\t',  self.buy );
            #self.buy = 0;
            #self.vol_hold = 0;   
            #print ('start new ' )
            self.end_date= str(row['date1'])
            return 1 
        
        elif self.vol_hold < 0 :
            # erro data
            print ('can not caculate  ' , self.code)
            self.buy = 0;
            self.vol_hold = 0;    
        
        return 0;


def getCodeData( oneCodeData):
    a1 = oneCodeData.sort_values(['date1','num'])
    return a1

allProfiles = [];
# 计算收益
def cacCodeRet( code, codeDetail ):
    
    _name = codeDetail['name'].iloc[0]
    sp = StockProfile(code , _name );
   
    
    for index, row in codeDetail.iterrows():
        ret = sp.OnHandle(row)
        if( 1 == ret ):
            #print('----');
            allProfiles.append(sp)
            
            # 新建对象
            sp = StockProfile(code , _name);
            
        
    return ;


def stand_data( fileName):
    #exlc转化后格式读取
    data = pd.read_excel(fileName )    
    colMap =  {
                "成交日期": "date1",        
                "证券代码": "code",
                "证券名称":"name",
                "操作":"flag",
                 "成交均价":"price",
                "成交数量":"vol",
                "成交金额":"money",
                "合同编号":"num"}


    dt = data.rename(columns=colMap  ) 
    usedCol = list(colMap.values())
    
    return dt[usedCol]


def stand_raw_data( fileName):
    #华泰导出数据，原始数据
    col_zh =[
            "成交日期",        
            "证券代码",
            "证券名称",
            "操作",
             "成交均价",
            "成交数量",
            "成交金额",
            "合同编号"
            ]

    x = pd.read_csv( fileName,                   
                    sep='\t',usecols=col_zh, 
                    encoding='gbk')
    
    colMap =  {
            "成交日期": "date1",        
            "证券代码": "code",
            "证券名称":"name",
            "操作":"flag",
             "成交均价":"price",
            "成交数量":"vol",
            "成交金额":"money",
            "合同编号":"num"}


    dt = x.rename(columns=colMap  ) 
    
    return dt[ (dt.flag=='证券卖出') | (dt.flag=='证券买入')]

def wash_org_data( fileName  ) :
    #dt = stand_data( fileName)
    dt = stand_raw_data( fileName)
    g= dt.groupby('code')

    return  g;

#多个文件
def wash_multi_org_data( files  ) :
    #dt = stand_data( fileName)
    index =0;
    dt ={}

    for fileName in files:     
        print(fileName)
        index = index + 1 
        if index == 1 :
            dt = stand_raw_data( fileName)
        else:            
            dt1 = stand_raw_data( fileName)
            dt = dt.append(dt1)
            
    
    g= dt.groupby('code')

    return  g;


def ana_single_file( fileName):
    
    allProfiles.clear();
    
    g= wash_org_data(fileName)


    #计算每个股票/每次 收益 
    for name, group in g:
        x = getCodeData ( group)
        #print(x)
        cacCodeRet(name , x)
        
    
    print('')
    
    for s in allProfiles:
        #print(s)
        s.info()
  
    
    return

def ana_mult_file( files):
    allProfiles.clear()
    
    g= wash_multi_org_data(files)


    #计算每个股票/每次 收益 
    for name, group in g:
        x = getCodeData ( group)
        #print(x)
        cacCodeRet(name , x)
        
    
    print('')
    
    for s in allProfiles:
        #print(s)
        s.info()
  
    
    return

# 
print("---- single  file ")
fileName='/Users/quchaodong/stu/py_research/tmp/ht/his_ht2020.xls'
#fileName='/Users/quchaodong/stu/py_research/tmp/ht/1his_ht2020.xls'
#ana_single_file(fileName)
    
print("---- multi files ")
'''
files = { '/Users/quchaodong/stu/py_research/tmp/ht/his_ht1910.xls' ,
          '/Users/quchaodong/stu/py_research/tmp/ht/his_ht1911.xls',
          '/Users/quchaodong/stu/py_research/tmp/ht/his_ht1912.xls',
          '/Users/quchaodong/stu/py_research/tmp/ht/his_ht2001.xls',
          '/Users/quchaodong/stu/py_research/tmp/ht/his_ht2002.xls',
         }
'''
files =[]
for i in range(1,13):
    files.append( '/Users/quchaodong/stu/py_research/tmp/ht/his_ht19' +"{:0>2d}".format(i)+'.xls' )
for i in range(1,3):
    files.append( '/Users/quchaodong/stu/py_research/tmp/ht/his_ht20' +"{:0>2d}".format(i)+'.xls' )
 

ana_mult_file(files)
    