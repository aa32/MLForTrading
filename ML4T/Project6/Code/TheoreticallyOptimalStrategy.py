import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt
import datetime as dt
import marketsimcode as ms
import numpy as np




class TheoreticallyOptimalStrategy(object) :

    def testPolicy(self,symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
        sym = [symbol]
        dates = pd.date_range(sd, ed)

        df = get_data(sym, dates)
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        #df = df / df.ix[0,:]
        price_sym = df.ix[:,1:]
        price_SPY = df.ix[:,0]

        df_trades = price_sym.copy()
        df_trades_bnch = price_sym.copy()
        df_trades[:] = 0.0
        df_trades_bnch[:] = 0.0
        d = price_sym.shape[0]-1

        holdings = 0.0
        i =0
        diff =[]

        for i  in range (0,d):
            today_price = price_sym.ix[i][0]
            after_price = price_sym.ix[i+1][0]
            diff.append(after_price - today_price)

        diff.append(0)

        price_sym['diff'] = diff

        for i in range(0, d):
            if (price_sym.ix[i,1]>0 and holdings == 0 ):
                df_trades.ix[i, symbol] = 1000
                holdings = holdings +1000

            elif (price_sym.ix[i,1]>0 and holdings == -1000):
                df_trades.ix[i, symbol] = 2000
                holdings = holdings + 2000

            elif (price_sym.ix[i,1] < 0 and holdings == 1000):
                df_trades.ix[i, symbol] = -2000
                holdings = holdings - 2000

            elif (price_sym.ix[i,1] < 0 and holdings == 0):
                df_trades.ix[i, symbol] = -1000
                holdings = holdings - 1000



        portvals = ms.compute_portvals(df_trades,sv,0.00,0.0)
        start_date = portvals.index[0]
        end_date = portvals.index[-1]
        cum_ret = (portvals[-1] / portvals[0]) - 1

        daily_returns = portvals / portvals.shift(1) - 1
        daily_returns = daily_returns[1:]
        avg_daily_ret = daily_returns.mean()
        std_daily_ret = daily_returns.std()


        #for benchmark


        df_trades_bnch.ix[0, symbol] =1000

        portvals_bnch = ms.compute_portvals(df_trades_bnch, sv, 0.00, 0.0)
        cum_ret_bnch = (portvals_bnch[-1] / portvals_bnch[0]) - 1

        daily_returns_bnch = portvals_bnch / portvals_bnch.shift(1) - 1
        daily_returns_bnch = daily_returns_bnch[1:]
        avg_daily_ret_bnch = daily_returns_bnch.mean()
        std_daily_ret_bnch = daily_returns_bnch.std()



        print "Date Range: {} to {}".format(sd, ed)

        print "Cumulative Return of Portfolio: {}".format(cum_ret)
        print "Cumulative Return of Benchmark : {}".format(cum_ret_bnch)
        print
        print "Standard Deviation of Portfolio: {}".format(std_daily_ret)
        print "Standard Deviation of Benchmark : {}".format(std_daily_ret_bnch)
        print
        print "Average Daily Return of Portfolio: {}".format(avg_daily_ret)
        print "Average Daily Return of Benchmark : {}".format(avg_daily_ret_bnch)
        print
        print "Final Portfolio Value of Portfolio: {}".format(portvals[-1])
        print "Final Portfolio value of Benchmark :{}".format(portvals_bnch[-1])

        portval_norm_fund = portvals / portvals.ix[0,]
        bnch_norm_fund = portvals_bnch / portvals_bnch.ix[0,]



        plt.plot (portval_norm_fund,color = 'Red' , label = 'Portfolio')
        plt.plot(bnch_norm_fund ,color = 'Green',label = 'Benchmark')
        plt.legend()
        plt.title( 'Theoretical Strategy Portfolio Vs Benchmark')
        plt.xlim(sd,ed)
        plt.xticks(rotation=25)
        plt.ylabel('Value')
        plt.xlabel('Dates')


        plt.savefig('Part2.png')
        return



def author():
    return 'aawasthi32'


def test_code():
    sym = 'JPM'

    start_dt = dt.datetime(2008,1,1)
    end_dt   =  dt.datetime(2009,12,31)
    startval = 100000

    tos = TheoreticallyOptimalStrategy()
    tos.testPolicy(sym,start_dt,end_dt,startval)





if __name__ == "__main__":
    test_code()