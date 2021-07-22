'''

Student Name: Anshuta Awasthi
GT User ID: aawasthi32
GT ID: 903379179
'''

import pandas as pd
from util import get_data, plot_data
import datetime as dt
import numpy as np
import marketsimcode as msc
import ManualStrategy as ms
import StrategyLearner as sl
import random
import matplotlib.pyplot as plt


def author():
    return 'aawasthi32'


def testimpact():
    sym = 'JPM'
    start_dt = dt.datetime(2008, 1, 1)
    end_dt = dt.datetime(2009, 12, 31)
    startval = 100000

    #impactlst = np.arange(0, 0.2, 0.05)
    impactlst = [0 ,0.0005 ,0.0010, 0.0025, 0.005 ,0.010,0.025,0.05 ]
    y_ret = []
    y_sharpe = []
    y_tradeno = []
    portval =[]

    # Strategy Learner
    for  i in impactlst:
        np.random.seed(69)
        random.seed(69)
        stl = sl.StrategyLearner(verbose=False, impact=i)
        stl.addEvidence(sym, start_dt, end_dt, startval)
        trades = stl.testPolicy(sym, start_dt, end_dt, startval)

        tradeno = trades[sym].astype(bool).sum(axis=0)
        y_tradeno.append(tradeno)

        st_portvals = msc.compute_portvals(trades, startval, 0.0, 0.0)
        st_cum_ret = (st_portvals[-1] / st_portvals[0]) - 1

        st_daily_returns = st_portvals / st_portvals.shift(1) - 1
        st_daily_returns = st_daily_returns[1:]
        st_avg_daily_ret = st_daily_returns.mean()
        st_std_daily_ret = st_daily_returns.std()
        K = np.sqrt(252.0)
        st_sharpe_ratio = K * (st_avg_daily_ret / st_std_daily_ret)
        y_ret.append(st_cum_ret)
        y_sharpe.append(st_sharpe_ratio)




    plt.figure(figsize=(15, 8))

    plt.plot(impactlst,y_tradeno, label = 'No. of Trades')

    plt.legend(fontsize=18)
    plt.grid()

    plt.title('No. of trades with varying impact', fontsize=20)
    plt.xticks(fontsize =14,rotation=25)
    plt.yticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel('Value', fontsize=20)
    plt.xlabel('Impact', fontsize=20)

    plt.savefig('Exp2_b.png')
    



    plt.figure(figsize=(15, 8))

    plt.plot(impactlst, y_ret, label='Cumulative Return')
    # plt.plot(impactlst,y_tradeno, label = 'No. of Trades')

    plt.legend(fontsize=18)
    plt.grid()

    plt.title('Cumulative Return Value with varying impact', fontsize=20)
    plt.xticks(fontsize=14, rotation=25)
    plt.yticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel('Value', fontsize=20)
    plt.xlabel('Impact', fontsize=20)

    plt.savefig('Exp2_a.png')


if __name__ == "__main__":
    testimpact()



