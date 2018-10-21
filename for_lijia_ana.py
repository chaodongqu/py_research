import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

def deal_file( dataPath):
    print (dataPath)
    names=["date","open","high","low","close","vol","vol_m"]
    x = pd.read_csv(dataPath,sep='\t',skiprows=2,names =names,index_col=0,encoding='gbk')
    s = x.iloc[:,0].size
    #前3天数据
    val = x.iloc[s-4:s-1] ;
    return val