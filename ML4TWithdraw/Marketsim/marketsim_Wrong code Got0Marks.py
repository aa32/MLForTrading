"""MC2-P1: Market simulator.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Anshuta Awasthi
GT User ID: aawasthi32
GT ID: 903379179
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import os  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			    		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			    		  		  		    	 		 		   		 		  
    # TODO: Your code here
    df_date = pd.read_csv("../data/$SPX.csv",index_col='Date',usecols = ['Date'] ,parse_dates=True, na_values=['nan'])
    df_orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

    df_orders.index = pd.to_datetime(df_orders.index)
    df_date.index = pd.to_datetime(df_date.index)

    df_date = df_date.sort_index()

    df_orders = df_orders.sort_index()


    df2 = df_orders.join(df_date,how  = 'inner')
    start_dt = df2.index[0]
    end_dt = df2.index[-1]

    symbols =  df2.Symbol.unique()


    df_temp = pd.read_csv("../data/{}.csv".format(symbols[0]),index_col = 'Date', parse_dates =True, usecols = ['Date', 'Adj Close' ], na_values =['nan'])
    df_temp = df_temp.rename(columns = {'Adj Close': symbols[0]})
    df_temp.index = pd.to_datetime(df_temp.index)
    df_temp = df_temp.sort_index()
    df3 = df_date.join(df_temp)


    for sym in symbols[1:]:
        df_temp = pd.read_csv("../data/{}.csv".format(sym), index_col='Date', parse_dates=True,usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': sym})
        df_temp.index = pd.to_datetime(df_temp.index)
        df_temp = df_temp.sort_index()

        df3 = df3.join(df_temp)


    df3 = df3.loc[start_dt:end_dt]

    df3['Cash'] = 1.00

    df3.fillna(method = 'ffill' , inplace = True)
    df3.fillna(method='bfill', inplace=True)


    df_trades = df3.copy()
    df_trades[:]= 0



    for index, row in df2.iterrows():
        if row["Order"] == "BUY":
            df_trades.loc[index,row["Symbol"]] = df_trades.loc[index,row["Symbol"]] + row ["Shares"]
            df_trades.loc[index, "Cash"] = df_trades.loc[index, "Cash"] - df3.loc[index,row["Symbol"]]*row["Shares"] -commission - abs(df3.loc[index,row["Symbol"]]*row["Shares"])*impact
        elif row["Order"] == "SELL":
            df_trades.loc[index, row["Symbol"]] = df_trades.loc[index, row["Symbol"]] - row["Shares"]
            df_trades.loc[index, "Cash"] = df_trades.loc[index, "Cash"] + df3.loc[index, row["Symbol"]] * row["Shares"]-commission - abs(df3.loc[index,row["Symbol"]]*row["Shares"])*impact


    previous = '1976-01-01 00:00:00'
    df_holdings = df_trades.copy()
    for index, row in df_trades.iterrows():
        if index == start_dt:
            df_holdings.loc[index,'Cash'] = df_trades.loc[index,'Cash'] + start_val

        else :

            df_holdings.loc[index] = df_holdings.loc[index] + df_holdings.loc[previous]

        previous = index

    df_values = df_holdings.copy()
    df_values = df3*df_holdings



    port_val = df_values.sum(axis = 1)
    return port_val

























    # In the template, instead of computing the value of the portfolio, we just  		   	  			    		  		  		    	 		 		   		 		  
    '''read in the value of IBM over 6 months  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,1,1)  		   	  			    		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2008,6,1)  
    '''

def author():
    return 'aawasthi32'  # replace tb34 with your Georgia Tech username.
  		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    of = "./orders/orders2.csv"
    sv = 1000000  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Process orders  		   	  			    		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file = of, start_val = sv)  		   	  			    		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		   	  			    		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			    		  		  		    	 		 		   		 		  
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
    sharpe_ratio = K * (avg_daily_ret  / std_daily_ret)


    #cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]

    #$SPX calculation----------------
    syms = ['$SPX']
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices = prices.replace('NaN', 0)
    normed = prices / prices.ix[0, :]
    #alloced = normed * allocs
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
    sharpe_ratio_SPY = K * (avg_daily_ret_SPY/ std_daily_ret_SPY)












    #cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]
  		   	  			    		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		   	  			    		  		  		    	 		 		   		 		  
    print "Date Range: {} to {}".format(start_date, end_date)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of $SPX : {}".format(sharpe_ratio_SPY)
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of Fund: {}".format(cum_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of $SPX : {}".format(cum_ret_SPY)
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of Fund: {}".format(std_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of $SPX : {}".format(std_daily_ret_SPY)
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of $SPX : {}".format(avg_daily_ret_SPY)
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Final Portfolio Value: {}".format(portvals[-1])  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
