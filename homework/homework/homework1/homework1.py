'''
(c) 2013 Remy Marquis
Computational Investing @ Georgia Tech
Homework 1

Write a Python function that can simulate and assess the performance of a 4 stock portfolio.
'''

# Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def simulate(dt_start, dt_end, ls_symbols, ls_allocation):
    '''
    Simulate function
    '''

    # Get closing prices (hours=16)
    dt_timeofday = dt.timedelta(hours=16)
    # Get a list of trading days.
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Open Yahoo data set and read (adjusted) closing price
    ls_keys = ['close']
    c_dataobj = da.DataAccess('Yahoo')
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Compute portfolio value
    tmp = d_data['close'].values.copy()
    d_normal = tmp / tmp[0,:]
    alloc = np.array(ls_allocation).reshape(4,1)
    portVal = np.dot(d_normal, alloc)

    # Compute daily returns
    dailyVal = portVal.copy()
    tsu.returnize0(dailyVal)

    # Compute statistics
    daily_ret = np.mean(dailyVal)
    vol = np.std(dailyVal)
    sharpe = np.sqrt(252) * daily_ret / vol
    cum_ret = portVal[portVal.shape[0] -1][0]

    # return
    return vol, daily_ret, sharpe, cum_ret

def print_simulate( dt_start, dt_end, ls_symbols, ls_allocation ):
    '''
    Print results
    '''
    # print
    vol, daily_ret, sharpe, cum_ret  = simulate( dt_start, dt_end, ls_symbols, ls_allocation )
    print "Start Date: ", dt_start
    print "End Date: ", dt_end
    print "Symbols: ", ls_symbols
    print "Optimal Allocations: ", ls_allocation
    print "Sharpe Ratio: ", sharpe
    print "Volatility (stdev): ", vol
    print "Average Daily Return: ", daily_ret
    print "Cumulative Return: ", cum_ret


def optimal_allocation_4( dt_start, dt_end, ls_symbols ):

        max_sharpe = -1
        max_alloc = [0.0, 0.0, 0.0, 0.0]
        for i in range(0,11):
            for j in range(0,11-i):
                for k in range(0,11-i-j):
                    for l in range (0,11-i-j-k):
                        if (i + j + l + k) == 10:
                            alloc = [float(i)/10, float(j)/10, float(k)/10, float(l)/10]
                            vol, daily_ret, sharpe, cum_ret = simulate( dt_start, dt_end, ls_symbols, alloc )
                            if sharpe > max_sharpe:
                                max_sharpe = sharpe
                                max_alloc = alloc

        return max_alloc


def main():
    '''
    Main function
    '''
    # vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, ['GOOG','AAPL','GLD','XOM'], [0.2,0.3,0.4,0.1])
    #ls_symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    #ls_symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    #ls_symbols = ['BRCM', 'TXN', 'AMD', 'ADI']
    ls_symbols = ['C', 'GS', 'IBM', 'HNZ']
    #ls_allocations = [0.4, 0.4, 0.0, 0.2]
    ls_allocations = [0.4, 0.4, 0.0, 0.2]
    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)
    # sanity check
    #rint_simulate(dt_start, dt_end, ls_symbols, ls_allocations)

    max_alloc = optimal_allocation_4( dt_start, dt_end, ls_symbols )
    print "---"
    #print max_alloc
    print_simulate( dt_start, dt_end, ls_symbols, max_alloc )

    


if __name__ == '__main__':
    main()