'''
(c) 2013 Remy Marquis
Computational Investing @ Georgia Tech
Homework 5

Create a bollingger band analysis tool
'''

import datetime as dt
import math
import QSTK.qstkutil.tsutil as tsu
import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import matplotlib.pyplot as plt
import pandas as pd

def bollinger(dt_start, dt_end, ls_symbols, ndays):

    #rolling statistic

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ['close'])
    df_close = ldf_data[0]

    rolling_mean = pd.rolling_mean(df_close, ndays)
    rolling_std = pd.rolling_std(df_close, ndays)

    upper = rolling_mean + rolling_std
    lower = rolling_mean - rolling_std

    bollinger_val = (df_close - rolling_mean) / (rolling_std)
    print bollinger_val.tail()


    plt.clf()
    plt.subplot(211, axisbg = 'w')
    plt.plot(df_close)
    plt.plot(upper)
    plt.plot(lower)
    ##plt.plot(bollinger_val)
    plt.plot(rolling_mean)
    plt.ylabel('Price')
    plt.xlabel('Time')
    plt.subplot(212, axisbg = 'w')
    plt.plot(bollinger_val)
    plt.ylabel('bollinger_val')
    plt.xlabel('Time')
    plt.savefig("tst.png", format='png')

    return bollinger_val, df_close, rolling_mean, rolling_std

  
if __name__ == '__main__':
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 5, 14)
    ls_symbols = ["AAPL"]
    ndays = 20

    ## Starting up with SP500 2008
    bollval, close, mean, std = bollinger(dt_start, dt_end, ls_symbols, ndays)
    ##print bollval.tail
