'''

Student Name: Anshuta Awasthi
GT User ID: aawasthi32
GT ID: 903379179
'''


import pandas as pd
from util import get_data, plot_data
#import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import matplotlib.gridspec as gridspec

#Bollinger band calculation code is referenced from given in vectorize me ppt
def bollingerbands(df,lookback ,startdate , enddate,sym):

    price = df[sym[0]]
    rolling_std = price.rolling(window = lookback , min_periods = lookback).std()
    sma = price.rolling(window = lookback,min_periods= lookback).mean()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bbp =  (price - sma)/(2 * rolling_std)

    return price,sma,top_band,bottom_band,bbp


def PriceSMA(df,lookback ,startdate , enddate ,sym):
    price = df[sym[0]]
    rolling_std = price.rolling(window=lookback, min_periods=lookback).std()
    sma = price.rolling(window=lookback, min_periods=lookback).mean()

    crossover = price/sma


    return price ,sma,crossover



#MACD calculation code is referenced from
def MACD(df, startdate, enddate ,sym):
    price = df[sym[0]]
    ema26 = pd.Series.ewm(price, span=26).mean()
    ema12 = pd.Series.ewm(price, span=12).mean()
    macd =  ema12 - ema26
    signal = pd.Series.ewm(macd, span=9).mean()
    crossover = macd - signal
    return price , ema26 ,ema12,signal,macd,crossover

def author():
    return 'aawasthi32'



def test_code():
    sym = ['JPM']

    start_dt = pd.to_datetime('01-01-2008')
    end_dt   =  pd.to_datetime('31-12-2009')
    lookback = 20

    new_sd = start_dt - timedelta(days = lookback+15)


    dates = pd.date_range(new_sd, end_dt)

    df = get_data(sym,dates)
    price,sma,top_band,bottom_band ,bbp = bollingerbands(df,lookback ,start_dt,end_dt,sym)

    # create bbp the plot

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False,
                           gridspec_kw={'height_ratios': [2, 1]},
                           figsize=(15, 8))

    ax = ax.flatten()
    fig.suptitle('Bollinger Band - JPM', size= 25)

    ax[0].plot(price, label='Price')
    ax[0].plot(sma, label='SMA')
    ax[0].plot(top_band, label='Upper Band')
    ax[0].plot(bottom_band, label='Lower Band')
    ax[0].grid(True)
    ax[0].set_ylabel('Price' , fontsize = 15)
    ax[0].label_outer()
    ax[0].legend(loc='lower left' , fontsize = 15)

    ax[1].set_xlim(start_dt, end_dt)
    ax[1].set_ylim(-1.5, 1.5)
    ax[1].plot(bbp, label='Bollinger Band Percentage')
    ax[1].set_ylabel('BBP',fontsize = 15)
    d = price.index
    y = 1

    ax[1].fill_between(d, bbp, y, where=bbp >= y, facecolor='red')

    y2 = -1.0
    ax[1].fill_between(d, bbp, y2, where=bbp <= y2, facecolor='red')

    ax[1].grid(True)

    ax[1].set_xlabel('Date' , fontsize = 15)
    fig.savefig('Bollinger Bands.png')

    #*****************************************************************************************************
    date2 = pd.date_range(start_dt, end_dt)
    df2 = get_data(sym,date2)
    price , ema26 ,ema12,signal,macd,crossover = MACD(df2,start_dt,end_dt ,sym)

    # create the MACD plot

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False,
                           gridspec_kw={'height_ratios': [2, 1]},
                           figsize=(15, 8))

    ax = ax.flatten()


    # fig.tight_layout()
    fig.suptitle('Moving Average Convergence Divergence - JPM', size=20)

    ax[0].plot(price, label='Price')
    ax[0].plot(ema26, label='26 Period EMA')
    ax[0].plot(ema12, label='12 Period EMA')
    ax[0].grid(True)
    ax[0].set_ylabel('Price',fontsize = 15)
    ax[0].label_outer()
    ax[0].legend(loc='lower left')

    ax[1].set_xlim(start_dt, end_dt)
    # ax[1].set_ylim(-1.5, 1.5)
    ax[1].plot(signal, label='Signal')
    ax[1].plot(macd, label='MACD')
    d = price.index
    ax[1].bar(d, crossover, label='Crossover', facecolor='red')
    ax[1].set_ylim(-3.0, 3.0)
    ax[1].set_ylabel('MACD' ,fontsize =15)
    ax[1].legend(loc='lower left')
    # d = price.index

    ax[1].grid(True)

    ax[1].set_xlabel('Date',fontsize =15)
    # fig.subplots_adjust(hspace=1)
    # plt.legend((top_band,bbp,bottom_band),('Top band', 'BBP','Lower Band'))
    fig.savefig('MACD.png')
    #*****************************************************************************************************************
    # create the Price/SMA plot
    price,sma,crossover = PriceSMA(df, lookback, start_dt, end_dt ,sym)

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False,
                           gridspec_kw={'height_ratios': [2, 1]},
                           figsize=(15, 8))

    ax = ax.flatten()
    fig.suptitle('Price/SMA - JPM', size=20)

    ax[0].plot(price, label='Price')
    ax[0].plot(sma, label='SMA')
    ax[0].grid(True)
    ax[0].set_ylabel('Price',fontsize =15)
    ax[0].label_outer()
    ax[0].legend(loc='lower left')

    ax[1].set_xlim(start_dt, end_dt)
    ax[1].set_ylim(0.6, 1.30)
    ax[1].plot(crossover, label='Price/SMA')
    ax[1].set_ylabel('Price over SMA' , fontsize = 15 )
    d = price.index
    y = 1.05

    ax[1].fill_between(d, crossover, y, where=crossover >= y, facecolor='red')

    y2 = 0.95
    ax[1].fill_between(d, crossover, y2, where=crossover <= y2, facecolor='red')

    ax[1].grid(True)

    ax[1].set_xlabel('Date' , fontsize =15)
    # fig.subplots_adjust(hspace=1)
    # plt.legend((top_band,bbp,bottom_band),('Top band', 'BBP','Lower Band'))
    fig.savefig('PriceBySma.png')






if __name__ == "__main__":
    test_code()