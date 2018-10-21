# -*- coding: utf-8 -*-
"""
"""

import re
from urllib import request
import  winsound 

def get_stock_price( s_code):
    resp = request.urlopen('http://qt.gtimg.cn' , data = b'q='+ bytes( s_code , encoding = "utf8"))
    return resp.read().decode('gb2312')

#返回：股票名称，当前价格，涨价格，涨幅度
def get_vals(str):
    matchObj = re.match( r'[^~]+~([^~]+)~[^~]+~([^~]+)~([^~]+)~([^~]+)~', str, re.M|re.I)     

    if matchObj:
        #rint("found")
        return(matchObj.group(1) ,
               float(matchObj.group(2)) ,
               float(matchObj.group(3)),
               float(matchObj.group(4)) )
        
    else:
        print("not found")
        
#600050 -->s_sh600050
#002268 --> s_sz002268
def stand_code( code):
    if code.startswith('60'):
        return 's_sh'+code
    else:
        return 's_sz'+code

def alarm_sound( str ):
    winsound.PlaySound("*", winsound.SND_ALIAS)
    
def monitor_stock( stock_condition):
    (code ,p_type , compare_type,val) = stock_condition
    
    scode = stand_code(code)
    code_info = get_stock_price(scode)
    x = get_vals(code_info)
    
    #股票当前信息，名称，价格，涨值，涨幅
    (s_name, price,inc,inc_perc)=x
    print(x)
    
    if(  p_type  == 'price'  ):
        print('price')
        if( '>' == compare_type) :
            print(">")
            if( price > val) :
                alarm_sound("Alarm me ")
                
        elif( '<' == compare_type):
            print("<")     
            if( price < val) :
                alarm_sound("Alarm me ")
                
    elif( 'percent' == p_type):
        print('percent')
        if( '>' == compare_type) :
            print(">")
            if( inc_perc > val) :
                alarm_sound("Alarm me ")
                
        elif( '<' == compare_type):
            print("<")
            if( inc_perc < val) :
                alarm_sound("Alarm me ")
##input: code,price,>,5.13
######   code,percent,>,1.0
monitors=[]
monitors.append(('600050','price','>' ,5.0 ) )
for x in monitors:
    print (x)    
    monitor_stock(x)
