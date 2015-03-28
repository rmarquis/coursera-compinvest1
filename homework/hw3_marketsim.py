import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import datetime as dt
from pylab import *
import sys
import pandas
import csv


def _csv_read_sym_dates(filename):
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    symbols = []
    dates = []
    for row in reader:
        if not(row[3] in symbols):
            symbols.append(row[3])
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        if not(date in dates):
            dates.append(date)
    dates = sorted(dates)
    return symbols, dates


def _read_data(symbols, dates):
    timeofday = dt.timedelta(hours=16)
    dates = dates
    timestamps = du.getNYSEdays(dates[0], dates[-1] + dt.timedelta(days=1), timeofday)

    dataobj = da.DataAccess('Yahoo')
    close = dataobj.get_data(timestamps, symbols, "close", verbose=True)
    close = close.fillna(method='ffill')
    close = close.fillna(method='bfill')
    return close, timestamps


def _share_holdings(filename, symbols, timestamps, close):
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    share_matrix = np.zeros((len(timestamps), len(symbols)))
    share_matrix = pandas.DataFrame(share_matrix, index=timestamps, columns=symbols)
    for row in reader:
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        time_stp = close.index[close.index >= date][0]
        if row[4] == 'Buy':
            share_matrix.ix[time_stp][row[3]] += float(row[5])
        elif row[4] == 'Sell':
            share_matrix.ix[time_stp][row[3]] -= float(row[5])
    return share_matrix

def share_holdings(input_file, symbols, ldt_timestamps, adjusted_closing):    
    reader = csv.reader(open(input_file, 'rU'))     
    share_matrix = np.zeros((len(ldt_timestamps), len(symbols)))
    share_matrix = pandas.DataFrame(share_matrix, index=ldt_timestamps, columns=symbols)
    for row in reader:
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]))
        time_stp = close.index[close.index >= date][0]
        if row[4] == 'Buy':
            share_matrix.ix[time_stp][row[3]] += float(row[5])
        elif row[4] == 'Sell':
            share_matrix.ix[time_stp][row[3]] -= float(row[5])
    return share_matrix


def _share_value_cash(share_matrix, close, i_start_cash):
    ts_cash = pandas.TimeSeries(0.0, close.index)
    ts_cash[0] = i_start_cash
    #print share_matrix.iterrows()
    for row_index, row in share_matrix.iterrows():
        cash = np.dot(row.values.astype(float), close.ix[row_index].values)
        ts_cash[row_index] -= cash
    share_matrix['_CASH'] = ts_cash
    share_matrix = share_matrix.cumsum()
    return share_matrix


def _fund_value(share_matrix, close):
    historic = close
    historic['_CASH'] = 1
    ts_fund = pandas.TimeSeries(0.0, close.index)
    for row_index, row in share_matrix.iterrows():
        ts_fund[row_index] += np.dot(row.values.astype(float), close.ix[row_index].values)
    return ts_fund


def _write_fund(ts_fund, filename):
    writer = csv.writer(open(filename, 'wb'), delimiter=',')
    for row_index in ts_fund.index:
        row_to_enter = [str(row_index.year), str(row_index.month), \
                        str(row_index.day), str(ts_fund[row_index])]
        writer.writerow(row_to_enter)


i_start_cash = float(sys.argv[1])
symbols, dates = _csv_read_sym_dates(sys.argv[2])
close, timestamps = _read_data(symbols, dates)
share_matrix = _share_holdings(sys.argv[2], symbols, timestamps, close)
print share_matrix
share_matrix = _share_value_cash(share_matrix, close, i_start_cash)
ts_fund = _fund_value(share_matrix, close)
_write_fund(ts_fund, sys.argv[3])
