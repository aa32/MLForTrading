'''

Student Name: Anshuta Awasthi
GT User ID: aawasthi32
GT ID: 903379179
'''



import matplotlib.pyplot as plt
import pandas as pd
import warnings
import datetime as dt
import numpy as np
import marketsimcode as msc
import ManualStrategy as ms
import StrategyLearner as sl
import random






def author():
    return 'aawasthi32'


def testStrategy():

    sym = 'JPM'
    start_dt = dt.datetime(2008, 1, 1)
    end_dt = dt.datetime(2009, 12, 31)
    startval = 100000


    # Manual Strategy

    mss = ms.ManualStrategy()
    long,short,df_trades = mss.testPolicy(sym, start_dt, end_dt, startval)

    df_trades_bnch = df_trades.copy()
    df_trades_bnch.ix[:] = 0.0



    portvals = msc.compute_portvals(df_trades, startval, 0.0, 0.0)
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    cum_ret = (portvals[-1] / portvals[0]) - 1

    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    K = np.sqrt(252.0)
    sharpe_ratio = K * (avg_daily_ret / std_daily_ret)
    warnings.filterwarnings("ignore")

    # Strategy Learner
    np.random.seed(69)
    random.seed(69)
    stl = sl.StrategyLearner(verbose = False, impact=0.0)
    stl.addEvidence(sym,start_dt, end_dt, startval)
    trades = stl.testPolicy(sym, start_dt, end_dt, startval)


    st_portvals = msc.compute_portvals(trades, startval,0.0, 0.0)
    st_cum_ret = (st_portvals[-1] / st_portvals[0]) - 1
    st_daily_returns = st_portvals / st_portvals.shift(1) - 1
    st_daily_returns = st_daily_returns[1:]
    st_avg_daily_ret = st_daily_returns.mean()
    st_std_daily_ret = st_daily_returns.std()
    K = np.sqrt(252.0)
    st_sharpe_ratio = K * (st_avg_daily_ret / st_std_daily_ret)


    # for benchmark

    df_trades_bnch.ix[0, sym] = 1000
    df_trades_bnch.ix[-1,sym] = -1000

    portvals_bnch = msc.compute_portvals(df_trades_bnch, startval, 0.0, 0.0)
    cum_ret_bnch = (portvals_bnch[-1] / portvals_bnch[0]) - 1

    daily_returns_bnch = portvals_bnch / portvals_bnch.shift(1) - 1
    daily_returns_bnch = daily_returns_bnch[1:]
    avg_daily_ret_bnch = daily_returns_bnch.mean()
    std_daily_ret_bnch = daily_returns_bnch.std()
    K = np.sqrt(252.0)
    sharpe_ratio_bnch = K * (avg_daily_ret_bnch / std_daily_ret_bnch)
    


    print
    print "In sample Date Range: {} to {}".format(start_dt, end_dt)
    print


    print "In-Sample Cumulative Return in Manual Strategy: {}".format(cum_ret)
    print "in-sample cumulative return in Strategy Learner : {}".format(st_cum_ret)
    print "in-sample cumulative return in benchmark : {}".format(cum_ret_bnch)
    print
    print "in-sample standard deviation in Manual Strategy: {}".format(std_daily_ret)
    print "In-Sample Standard Deviation in Strategy Learner : {}".format(st_std_daily_ret)
    print "In-Sample Standard Deviation in benchmark : {}".format(std_daily_ret_bnch)
    print
    print "In-Sample Average Daily Return in Manual Strategy: {}".format(avg_daily_ret)
    print "In-Sample Average Daily Return in Strategy Learner: {}".format(st_avg_daily_ret)
    print "In-Sample Average Daily Return in benchmark : {}".format(avg_daily_ret_bnch)
    print
    print "In-Sample Sharpe Ratio in Manual Strategy: {}".format(sharpe_ratio)
    print "In-Sample Sharpe Ratio in Strategy Learner: {}".format(st_sharpe_ratio)
    print "In-Sample Sharpe Ratio in benchmark : {}".format(sharpe_ratio_bnch)
    print

    print "In-Sample Final Portfolio Value in Manual Strategy: {}".format(portvals[-1])
    print "In-Sample Final Portfolio value in Strategy Learner :{}".format(st_portvals[-1])
    print "In-Sample Final Portfolio value in benchmark :{}".format(portvals_bnch[-1])

    print

    print '**************************************************************************'
    print



    portval_norm_fund = portvals / portvals.ix[0,]
    bnch_norm_fund = portvals_bnch / portvals_bnch.ix[0,]
    strategy_norm_fund = st_portvals / st_portvals.ix[0,]


    plt.plot(portval_norm_fund, color='Blue'    , label='Manual Strategy')
    plt.plot(bnch_norm_fund, color='Red', label='Benchmark')
    plt.plot(strategy_norm_fund, color='Green', label='ML Strategy')


    plt.legend(fontsize =10)
    plt.title('Manual Strategy Vs ML Strategy Vs Benchmark' ,fontsize = 15)
    plt.xlim(start_dt, end_dt)
    plt.xticks(rotation=25)
    plt.ylabel('Value' , fontsize =15)
    plt.xlabel('Dates', fontsize =15)

    plt.savefig('Exp1.png')
    



if __name__ == "__main__":
    testStrategy()

