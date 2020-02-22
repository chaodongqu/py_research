import numpy as np
import pandas as pd 


def read_txt_data( file_name ):
    cols= ['Date','Open','Close','Low','High',  'Volume','ms']
    #fileName = '/Users/quchaodong/stu/py_research/export/SH#600757.txt'
    x = pd.read_csv( file_name
                    ,skiprows =2 , 
                    skipfooter=1,
                    names=cols,
                    parse_dates =['Date'], engine='python',
                    #header=None,
                    sep='\t',
                    encoding='ISO-8859-1')
    x = x.set_index('Date')
    return x 

# f= "/Users/quchaodong/stu/py_research/tmp/export/SZ#300739.txt"
# dt = read_txt_data(f)

# print(dt.tail(12))