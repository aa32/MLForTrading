'''
Student Name: Anshuta Awasthi
GT User ID: aawasthi32
GT ID: 903379179
'''



import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt
import datetime as dt
import marketsimcode as ms
import numpy as np
from indicators import bollingerbands, PriceSMA , MACD
from datetime import datetime, timedelta
import marketsimcode as msc


class ManualStrategy(object):

    def testPolicy(self, symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        sym = [symbol]
        lookback =20
        new_sd = sd - timedelta(days=lookback+15)
        dates = pd.date_range(new_sd, ed)
        df = get_data(sym, dates)
        price1, sma1, top_band, bottom_band, bbp = bollingerbands(df,lookback,sd,ed,sym)

        bbp1 = bbp.loc[sd:ed]

        #Calculate Price/SMA

        price2,sma2,crossover = PriceSMA(df,lookback,sd,ed,sym)
        pricebysma = crossover.loc[sd:ed]

        #Calculate Macd_crossover
        price, ema26, ema12, signal, macd, crossover_macd = MACD(df,sd,ed,sym)

        macd1 = macd.loc[sd:ed]
        macd_crossover = crossover_macd.loc[sd:ed]

        df_dates = df[sym].loc[sd:ed]
        d = df_dates.shape[0] -1

        df_trades = df_dates.copy()

        df_trades.ix[:] = 0.0
        holdings = 0


        long =[]
        short =[]


        for i in range (0,d):

            if ((pricebysma.ix[i,0] <0.90 ) and  bbp1.ix[i,0] <0  and holdings == 0):
                df_trades.ix[i, symbol] = 1000
                holdings = holdings + 1000
                long.append(df_trades.index[i])


            elif ((pricebysma.ix[i,0] <0.90 ) and bbp1.ix[i,0] <0  and holdings == -1000):
                df_trades.ix[i, symbol] = 2000
                holdings = holdings + 2000
                long.append(df_trades.index[i])

            elif ((pricebysma.ix[i,0] >1.10 ) and bbp1.ix[i,0] >0  and holdings == 0):
                df_trades.ix[i, symbol] = -1000
                holdings = holdings -1000
                short.append(df_trades.index[i])

            elif ((pricebysma.ix[i,0] >1.10 ) and bbp1.ix[i,0] >0  and holdings ==1000):
                df_trades.ix[i, symbol] = -2000
                holdings = holdings - 2000
                short.append(df_trades.index[i])

            elif (macd_crossover.ix[i-1,0]<0 and macd_crossover.ix[i,0]>0 and holdings == 0):
                df_trades.ix[i, symbol] = 1000
                holdings = holdings + 1000
                long.append(df_trades.index[i])

            elif (macd_crossover.ix[i-1,0]<0 and macd_crossover.ix[i,0]>0 and holdings == -1000):
                df_trades.ix[i, symbol] = 2000
                holdings = holdings + 2000
                long.append(df_trades.index[i])

            elif (macd_crossover.ix[i-1,0]>0 and macd_crossover.ix[i,0]<0 and holdings == 0):
                df_trades.ix[i, symbol] = -1000
                holdings = holdings - 1000
                short.append(df_trades.index[i])


            elif (macd_crossover.ix[i-1,0]>0 and macd_crossover.ix[i,0]<0 and holdings == 1000):
                df_trades.ix[i, symbol] = -2000
                holdings = holdings - 2000
                short.append(df_trades.index[i])


        return long,short,df_trades


def author():
    return 'aawasthi32'

def test_code():
    sym = 'JPM'
    start_dt = dt.datetime(2008, 1, 1)
    end_dt = dt.datetime(2009, 12, 31)
    startval = 100000

    mss = ManualStrategy()
    long,short,df_trades = mss.testPolicy(sym, start_dt, end_dt, startval)

    df_trades_bnch = df_trades.copy()
    df_trades_bnch.ix[:] = 0.0

    portvals = msc.compute_portvals(df_trades, startval, 9.95, 0.005)
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    cum_ret = (portvals[-1] / portvals[0]) - 1

    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()

    # for benchmark

    df_trades_bnch.ix[0, sym] = 1000

    portvals_bnch = msc.compute_portvals(df_trades_bnch, startval, 9.95, 0.005)
    cum_ret_bnch = (portvals_bnch[-1] / portvals_bnch[0]) - 1

    daily_returns_bnch = portvals_bnch / portvals_bnch.shift(1) - 1
    daily_returns_bnch = daily_returns_bnch[1:]
    avg_daily_ret_bnch = daily_returns_bnch.mean()
    std_daily_ret_bnch = daily_returns_bnch.std()

    print
    print "In sample Date Range: {} to {}".format(start_dt, end_dt)
    print


    print "In-Sample Cumulative Return of Portfolio: {}".format(cum_ret)
    print "In-Sample Cumulative Return of Benchmark : {}".format(cum_ret_bnch)
    print
    print "In-Sample Standard Deviation of Portfolio: {}".format(std_daily_ret)
    print "In-Sample Standard Deviation of Benchmark : {}".format(std_daily_ret_bnch)
    print
    print "In-Sample Average Daily Return of Portfolio: {}".format(avg_daily_ret)
    print "In-Sample Average Daily Return of Benchmark : {}".format(avg_daily_ret_bnch)
    print
    print "In-Sample Final Portfolio Value of Portfolio: {}".format(portvals[-1])
    print "In-Sample Final Portfolio value of Benchmark :{}".format(portvals_bnch[-1])

    print

    print '**************************************************************************'
    print

    portval_norm_fund = portvals / portvals.ix[0,]
    bnch_norm_fund = portvals_bnch / portvals_bnch.ix[0,]

    plt.figure(figsize=(16, 9))

    plt.plot(portval_norm_fund, color='Red', label='Portfolio')
    plt.plot(bnch_norm_fund, color='Green', label='Benchmark')
    for l in long:
        plt.axvline(x=l, color='blue')
    for s in short:
        plt.axvline(x=s, color='black')
    plt.legend(fontsize =18)
    plt.title('Manual Strategy In Sample Portfolio Vs Benchmark' ,fontsize = 20)
    plt.xlim(start_dt, end_dt)
    plt.xticks(rotation=25)
    plt.ylabel('Value' , fontsize =15)
    plt.xlabel('Dates', fontsize =15)

    plt.savefig('Part3.png')

    #out of sample


    sd = dt.datetime(2010, 1, 1)
    ed= dt.datetime(2011, 12, 31)


    mss2 = ManualStrategy()
    long2, short2, df_trades2 = mss2.testPolicy(sym, sd, ed, startval)

    df_trades_bnch2 = df_trades2.copy()
    df_trades_bnch2.ix[:] = 0.0

    portvals2 = msc.compute_portvals(df_trades2, startval, 9.95, 0.005)
    cum_ret2 = (portvals2[-1] / portvals2[0]) - 1

    daily_returns2 = portvals2 / portvals2.shift(1) - 1
    daily_returns2 = daily_returns2[1:]
    avg_daily_ret2 = daily_returns2.mean()
    std_daily_ret2 = daily_returns2.std()

    # for benchmark

    df_trades_bnch2.ix[0, sym] = 1000

    portvals_bnch2 = msc.compute_portvals(df_trades_bnch2, startval, 9.95, 0.005)
    cum_ret_bnch2 = (portvals_bnch2[-1] / portvals_bnch2[0]) - 1

    daily_returns_bnch2 = portvals_bnch2 / portvals_bnch2.shift(1) - 1
    daily_returns_bnch2 = daily_returns_bnch2[1:]
    avg_daily_ret_bnch2 = daily_returns_bnch2.mean()
    std_daily_ret_bnch2 = daily_returns_bnch2.std()

    print "Out of Sample Date Range: {} to {}".format(sd, ed)
    print


    print "Out of Sample  Cumulative Return of Portfolio: {}".format(cum_ret2)
    print "Out of Sample Cumulative Return of Benchmark : {}".format(cum_ret_bnch2)
    print
    print "Out of Sample Standard Deviation of Portfolio: {}".format(std_daily_ret2)
    print "Out of Sample Standard Deviation of Benchmark : {}".format(std_daily_ret_bnch2)
    print
    print "Out of Sample Average Daily Return of Portfolio: {}".format(avg_daily_ret2)
    print "Out of Sample Average Daily Return of Benchmark : {}".format(avg_daily_ret_bnch2)
    print
    print "Out of Sample Final Portfolio Value of Portfolio: {}".format(portvals2[-1])
    print "Out of Sample Final Portfolio value of Benchmark :{}".format(portvals_bnch2[-1])

    portval_norm_fund2 = portvals2 / portvals2.ix[0,]
    bnch_norm_fund2 = portvals_bnch2 / portvals_bnch2.ix[0,]

    plt.figure(figsize=(16, 9))

    plt.plot(portval_norm_fund2, color='Red', label='Portfolio')
    plt.plot(bnch_norm_fund2, color='Green', label='Benchmark')

    plt.legend(fontsize = 18)
    plt.title('Manual Strategy Out of Sample Portfolio Vs Benchmark',fontsize = 20)
    plt.xlim(sd, ed)
    plt.xticks(rotation=25)
    plt.ylabel('Value' ,fontsize = 15)
    plt.xlabel('Dates' , fontsize =15)

    plt.savefig('Part4.png')


if __name__ == "__main__":
    test_code()

