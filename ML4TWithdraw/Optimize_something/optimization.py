"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import scipy.optimize as spo
  		   	  			    		  		  		    	 		 		   		 		  
# This is the function that will be tested by the autograder  		   	  			    		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		   	  			    		  		  		    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		   	  			    		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY'] # only SPY, for comparison later
    prices = prices.replace('NaN', 0)
    prices_SPY = prices_SPY.replace('NaN',0)

  		   	  			    		  		  		    	 		 		   		 		  
    # find the allocations for the optimal portfolio  		   	  			    		  		  		    	 		 		   		 		  
    # note that the values here ARE NOT meant to be correct for a test case

    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    allocs = optimizemaxsr (syms,prices)
    #print allocs
    # Get daily portfolio value
    cr, adr, sddr,sr = assess_portfolio(sd,ed,syms,allocs)

  		   	  			    		  		  		    	 		 		   		 		  
    # Compare daily portfolio value with SPY using a normalized plot  		   	  			    		  		  		    	 		 		   		 		  
    if gen_plot:
        normed = prices / prices.ix[0, :]
        pos_val = normed * allocs
        port_val = pos_val.sum(axis=1)
        # add code to plot here  		   	  			    		  		  		    	 		 		   		 		  
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = df_temp/df_temp.ix[0,:]
        #plt.plot(df_temp,label = df_temp.keys.values)
        df_temp.plot(title='Daily Portfolio Value and SPY')
        plt.legend(loc = 'upper left')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(linewidth=1)
        plt.savefig('plot.png')
        pass  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    return allocs, cr, adr, sddr, sr




def assess_portfolio(sd,ed,syms,allocs,rfr=0.0, sf=252.0):


    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices = prices.replace('NaN', 0)
    normed = prices/prices.ix[0,:]
    alloced = normed*allocs
    pos_val = alloced
    # Get daily portfolio value
    #port_val = prices_SPY  add code here to compute daily portfolio values
    port_val = pos_val.sum(axis=1)
    cr =(port_val[-1]/port_val[0])-1

    daily_returns = port_val/port_val.shift(1)-1
    daily_returns = daily_returns[1:]
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    K = np.sqrt(sf)
    sr = K* (adr/sddr)
    return cr, adr, sddr,sr


def max_sharpe_ratio(allocs,prices):
    prices = prices.replace('NaN', 0)
    normed = prices / prices.ix[0, :]
    alloced = normed * allocs
    pos_val = alloced
    port_val = pos_val.sum(axis=1)
    cr = (port_val[-1] / port_val[0]) - 1

    daily_returns = port_val / port_val.shift(1) - 1
    daily_returns = daily_returns[1:]
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    K = np.sqrt(252)
    maxsharpe =( K * (adr / sddr))*-1

    return maxsharpe


def optimizemaxsr(syms,prices):
    num = len(syms)
    guess = np.empty(num)
    guess.fill(1.0/num)
    #print guess
    args = prices
    constraints = ({'type': 'eq', 'fun': lambda inputs: 1-np.sum(inputs)})
    bounds = tuple((0, 1) for i in range(num))
    result = spo.minimize(max_sharpe_ratio,guess,args = (prices,),method='SLSQP', bounds=bounds, constraints=constraints)
    allocs = result.x
    return allocs


def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # This function WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			    		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			    		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,06,01)
    end_date = dt.datetime(2009,06,01)
    symbols = ['IBM', 'X', 'GLD', 'JPM']
  		   	  			    		  		  		    	 		 		   		 		  
    # Assess the portfolio  		   	  			    		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)
  		   	  			    		  		  		    	 		 		   		 		  
    # Print statistics  		   	  			    		  		  		    	 		 		   		 		  
    print "Start Date:", start_date  		   	  			    		  		  		    	 		 		   		 		  
    print "End Date:", end_date  		   	  			    		  		  		    	 		 		   		 		  
    print "Symbols:", symbols  		   	  			    		  		  		    	 		 		   		 		  
    print "Allocations:", allocations  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio:", sr  		   	  			    		  		  		    	 		 		   		 		  
    print "Volatility (stdev of daily returns):", sddr  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return:", adr  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return:", cr  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
