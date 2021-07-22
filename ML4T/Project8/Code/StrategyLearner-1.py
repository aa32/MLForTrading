""" 			  		 			     			  	   		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
import datetime as dt 			  		 			     			  	   		   	  			  	
import pandas as pd
import numpy as np
import util as ut 			  		 			     			  	   		   	  			  	
import random
import BagLearner as bal
import RTLearner as rtl
from indicators import bollingerbands,PriceSMA,MACD
from datetime import datetime, timedelta


 			  		 			     			  	   		   	  			  	
class StrategyLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    # constructor 			  		 			     			  	   		   	  			  	
    def __init__(self, verbose = False, impact=0.0): 			  		 			     			  	   		   	  			  	
        self.verbose = verbose 			  		 			     			  	   		   	  			  	
        self.impact = impact
        self.N = 10
        self.learner1  = bal.BagLearner(learner=rtl.RTLearner, verbose=False, kwargs={"leaf_size": 5}, bags=40, boost=False)

    def author(self):
        return 'aawasthi32'

    # this method should create a QLearner, and train it for trading 			  		 			     			  	   		   	  			  	
    def addEvidence(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        lookback = 20
        sym = [symbol]

        new_sd = sd - timedelta(days=lookback + 15)

        dates = pd.date_range(new_sd, ed)

        df = ut.get_data(sym, dates)
        price, sma, top_band, bottom_band, bbp = bollingerbands(df, lookback, sd,ed ,sym)
        bbp1 = bbp.loc[sd:ed]

        #print bbp1

        date2 = pd.date_range(sd, ed)
        df2 = ut.get_data(sym, date2)
        price, ema26, ema12, signal, macd, MACD_ratio = MACD(df2, sd, ed, sym)

        #print MACD_ratio

        price, sma, crossover = PriceSMA(df, lookback, sd, ed, sym)

        priceoversma = crossover.loc[sd:ed]

        #print priceoversma

        price = price.loc[sd:ed]

        #print price
        periods = self.N

        yval = (price.shift(-periods) -price)/price


        mean = yval.mean()
        std = yval.std()

        YBUY = mean + std*0.5
        YSELL = mean - std*0.5



        train = pd.concat([price,bbp1,MACD_ratio,priceoversma ,yval],axis =1)

        train.columns = [symbol , 'bbp', 'MACD_Ratio' , 'PriceOverSMA','Yval']




        conditions = [(train['Yval'] - self.impact > YBUY) ,(train['Yval'] + self.impact< YSELL)]
            
        choices = [1, -1 ]
        
        train['Y'] = np.select(conditions, choices , default = 0)

        train.dropna(axis = 0 , how = 'any', inplace = True)



        trainX = train.iloc[:,0:-2].values

        trainY = train.iloc[:,-1].values

        self.learner1.addEvidence(trainX,trainY)


 			  		 			     			  	   		   	  			  	
    # this method should use the existing policy and test it against new data 			  		 			     			  	   		   	  			  	
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        lookback = 20
        sym = [symbol]

        new_sd = sd - timedelta(days=lookback + 15)

        dates = pd.date_range(new_sd, ed)

        df = ut.get_data(sym, dates)
        price, sma, top_band, bottom_band, bbp = bollingerbands(df, lookback, sd, ed, sym)
        bbp1 = bbp.loc[sd:ed]



        date2 = pd.date_range(sd, ed)
        df2 = ut.get_data(sym, date2)
        price, ema26, ema12, signal, macd, MACD_ratio = MACD(df2, sd, ed, sym)


        price, sma, crossover = PriceSMA(df, lookback, sd, ed, sym)
        priceoversma = crossover.loc[sd:ed]



        price = price.loc[sd:ed]
        testX = pd.concat([price, bbp1, MACD_ratio, priceoversma], axis=1)
        testX.columns = [symbol, 'bbp', 'MACD_Ratio', 'PriceOverSMA']

        testX = testX.values


        queryY = self.learner1.query(testX)

        df_dates = df2[sym].loc[sd:ed]
        d = df_dates.shape[0] - 1

        trades = df_dates.copy()

        trades.ix[:] = 0.0
        holding = 0

        for i in range (0, d):
            if queryY[0][i] == 1.0 :
                if holding == 0:
                    trades.ix[i, symbol] = 1000
                    holding = holding + 1000

                elif holding == 1000:
                    trades.ix[i, symbol] = 0

                elif holding == -1000:
                    trades.ix[i, symbol] = 2000
                    holding = holding + 2000

            elif queryY[0][i] ==  -1.0:
                if holding == 0:
                    trades.ix[i, symbol] = -1000
                    holding = holding - 1000

                elif holding == -1000:
                    trades.ix[i, symbol] = 0

                elif holding == 1000:
                    trades.ix[i, symbol] = -2000
                    holding = holding - 2000

            elif queryY[0][i]  ==  0.0:
                if holding == 1000:
                    trades.ix[i, symbol] = -1000
                    holding = holding - 1000

                elif holding == 0:
                    trades.ix[i, symbol] = 0

                elif holding == -1000:
                    trades.ix[i, symbol] = 1000
                    holding = holding + 1000



        return  trades
        

        



if __name__=="__main__":
    print "One does not simply think up a strategy"

                       




                       
                       




