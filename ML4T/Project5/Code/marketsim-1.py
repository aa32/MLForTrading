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
                                                                                              
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission= 9.95, impact=0.005):
    # this is the function the autograder will call to test your code                                                                                             
    # NOTE: orders_file may be a string, or it may be a file object. Your                                                                                             
    # code should work correctly with either input                                                                                                
    # TODO: Your code here

    df_orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

    df_orders.index = pd.to_datetime(df_orders.index)

    df_orders = df_orders.sort_index()


    start_dt = df_orders.index[0]
    end_dt = df_orders.index[-1]



    symbols =  list(df_orders.Symbol.unique())
    
    dates = pd.date_range(start_dt, end_dt)



    df3 = get_data(symbols, dates)

    valid_days = df_orders.index.isin(df3.index.values)
    df_orders = df_orders[valid_days]



    df3['Cash'] = 1.00

    df3.fillna(method = 'ffill' , inplace = True)
    df3.fillna(method='bfill', inplace=True)


    df_trades = df3.copy()
    df_trades[:]= 0




    for index, row in df_orders.iterrows():
        if row["Order"] == "BUY":
            df_trades.loc[index,row["Symbol"]] = df_trades.loc[index,row["Symbol"]] + row ["Shares"]
            df_trades.loc[index, "Cash"] = df_trades.loc[index, "Cash"] - df3.loc[index,row["Symbol"]]*row["Shares"] -commission - abs(df3.loc[index,row["Symbol"]]*row["Shares"])*impact
        elif row["Order"] == "SELL":
            df_trades.loc[index, row["Symbol"]] = df_trades.loc[index, row["Symbol"]] - row["Shares"]
            df_trades.loc[index, "Cash"] = df_trades.loc[index, "Cash"] + df3.loc[index, row["Symbol"]] * row["Shares"]-commission - abs(df3.loc[index,row["Symbol"]]*row["Shares"])*impact


    df_holdings = df_trades.copy()
    df_holdings.ix[0, 'Cash'] = start_val+df_trades['Cash'] [0]
    n  = df_holdings.shape[0]
    for i in range(1,n):
        df_holdings.ix[i,:] += df_holdings.ix[i-1,:]


    df_values = df_holdings.copy()
    df_values = df3*df_holdings



    port_val = df_values.sum(axis = 1)


    return port_val
	  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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

    # Compare portfolio against $SPX                                                                                
    print "Date Range: {} to {}".format(start_date, end_date)                                                                               
    print                                                                               
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)                                                                               
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)                                                                               
    print                                                                               
    print "Cumulative Return of Fund: {}".format(cum_ret)                                                                               
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)                                                                               
    print                                                                               
    print "Standard Deviation of Fund: {}".format(std_daily_ret)                                                                                
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)                                                                                
    print                                                                               
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)                                                                              
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)                                                                              
    print                                                                               
    print "Final Portfolio Value: {}".format(portvals[-1])                                                                              
                                                                                
if __name__ == "__main__":                                                                              
    test_code()                             





