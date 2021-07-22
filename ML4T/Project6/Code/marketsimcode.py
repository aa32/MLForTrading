import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def compute_portvals(df_trades, start_val=100000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    df_trades = df_trades.sort_index()

    start_dt = df_trades.index[0]
    end_dt = df_trades.index[-1]

    symbols = list(df_trades)

    dates = pd.date_range(start_dt, end_dt)

    df3 = get_data(symbols, dates)

    valid_days = df_trades.index.isin(df3.index.values)
    df_trades = df_trades[valid_days]

    df_trades['Cash'] = 0.0
    df3['Cash'] =1.0

    df3.fillna(method='ffill', inplace=True)
    df3.fillna(method='bfill', inplace=True)

    sym = symbols[0]
    #df3 = df3['JPM']


    '''

    valid_days = df3.index.isin(df_trades.index.values)
    df3 = df3[valid_days]
    
    '''





    for index, row in df_trades.iterrows():
        #print row
        #print df_trades.loc[index, sym]

        if  (df_trades.loc[index, sym] >0):
            df_trades.loc[index, "Cash"] = df_trades.loc[index, "Cash"] - df3.loc[index,sym] * row[sym] - commission - abs(df3.loc[index, sym] * row[sym]) * impact
        elif (df_trades.loc[index, sym] <0):
            df_trades.loc[index, "Cash"] = df_trades.loc[index, "Cash"] - df3.loc[index, sym] * row[sym] - commission - abs(df3.loc[index, sym] * row[sym]) * impact




    df_holdings = df_trades.copy()
    df_holdings.ix[0, 'Cash'] = start_val + df_trades['Cash'][0]
    n = df_holdings.shape[0]
    for i in range(1, n):
        df_holdings.ix[i, :] += df_holdings.ix[i - 1, :]


    df_values = df_holdings.copy()
    df_values = df3 * df_holdings




    port_val = df_values.sum(axis=1)



    return port_val


def author():
    return 'aawasthi32'  # replace tb34 with your Georgia Tech username.

'''
def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[
            0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

        # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    cum_ret = (portvals[-1] / portvals[0]) - 1

    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    K = np.sqrt(252.0)
    sharpe_ratio = K * (avg_daily_ret / std_daily_ret)

    # cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]

    # $SPX calculation----------------
    syms = ['$SPX']
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices = prices.replace('NaN', 0)
    normed = prices / prices.ix[0, :]
    # alloced = normed * allocs
    pos_val = normed
    # Get daily portfolio value
    # port_val = prices_SPY  add code here to compute daily portfolio values
    port_val = pos_val.sum(axis=1)
    cum_ret_SPY = (port_val[-1] / port_val[0]) - 1

    daily_returns = port_val / port_val.shift(1) - 1
    daily_returns = daily_returns[1:]
    avg_daily_ret_SPY = daily_returns.mean()
    std_daily_ret_SPY = daily_returns.std()
    K = np.sqrt(252.0)
    sharpe_ratio_SPY = K * (avg_daily_ret_SPY / std_daily_ret_SPY)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}"
    print "Standard Devi
    
    
'''






