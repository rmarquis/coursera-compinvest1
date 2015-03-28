import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
from pylab import *
import sys
import pandas
import csv


def _csv_read_fund(filename):
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    vals = []
    dates = []
    for row in reader:
        vals.append(float(row[3]))
        date = dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16)
        dates.append(date)
    ts_fund = pandas.TimeSeries(dict(zip(dates, vals)))
    return ts_fund


def _read_bench(symbol, timestamps):

    dataobj = da.DataAccess('Yahoo')
    close = dataobj.get_data(timestamps, [symbol], "close", verbose=True)
    close = close.fillna(method='ffill')
    close = close.fillna(method='bfill')
    return close[symbol]

ts_fund = _csv_read_fund(sys.argv[1])
benchmark = sys.argv[2]
bench_vals = _read_bench(benchmark, list(ts_fund.index))
# print bench_vals
multiple = ts_fund[0] / bench_vals[0]
bench_vals = bench_vals * multiple

print "Details of the Performance of the portfolio"
print 'Data Range : ', ts_fund.index[0], ' to ', ts_fund.index[-1]
print 'Sharpe Ratio of Fund :', tsu.get_sharpe_ratio(tsu.daily(ts_fund))[0]
print 'Sharpe Ratio of ' + benchmark + ' :', tsu.get_sharpe_ratio(
                                          tsu.daily(bench_vals))[0]
print 'Total Return of Fund : ', (((ts_fund[-1] / ts_fund[0]) - 1) + 1)
print 'Total Return of ' + benchmark + ' :', (((bench_vals[-1]
                                            / bench_vals[0]) - 1) + 1)
print 'Standard Deviation of Fund : ', np.std(tsu.daily(
                                       ts_fund.values))
print 'Standard Deviation of ' + benchmark + ' :', np.std(
                                       tsu.daily(bench_vals.values))

print 'Average Daily Return of Fund : ', np.mean(tsu.daily(
                                       ts_fund.values))
print 'Average Daily Return of ' + benchmark + ' :', np.mean(
                                       tsu.daily(bench_vals.values))

plt.clf()
plt.plot(ts_fund.index, ts_fund.values)
plt.plot(ts_fund.index, bench_vals)
plt.ylabel('Fund Value', size='xx-small')
plt.xlabel('Date', size='xx-small')
plt.legend(['Fund', 'Benchmark'], loc='best')
plt.xticks(size='xx-small')
plt.yticks(size='xx-small')
savefig('chart.pdf', format='pdf')
