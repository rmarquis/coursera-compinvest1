'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 24, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Example tutorial code.
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    '''Main Function'''
    # List of symbols
    ls_symbols = ["AAPL", "GOOG", "IBM", "MSFT"]

    # Start and End date of the charts
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 6, 15)

    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Copying close price into separate dataframe to find rets
    df_close = d_data['close']
    df_mean = pd.rolling_mean(d_data['close'], 20)
    df_std = pd.rolling_std(d_data['close'], 20)

    df_bollinger = (df_close - df_mean) / (df_std)
    print df_bollinger.tail()
    # Plotting the prices with x-axis=timestamps
    plt.clf()
    plt.subplot(211)
    plt.plot(ldt_timestamps, df_close['GOOG'], label='Google')
    plt.legend()
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.xticks(size='xx-small')
    plt.xlim(ldt_timestamps[0], ldt_timestamps[-1])
    plt.subplot(212)
    plt.plot(ldt_timestamps, df_bollinger['GOOG'], label='Google-Bollinger')
    plt.axhline(1.0, color='r')
    plt.axhline(-1.0, color='r')
    plt.legend()
    plt.ylabel('Bollinger')
    plt.xlabel('Date')
    plt.xticks(size='xx-small')
    plt.xlim(ldt_timestamps[0], ldt_timestamps[-1])
    plt.savefig('homework5.pdf', format='pdf')


if __name__ == '__main__':
    main()
