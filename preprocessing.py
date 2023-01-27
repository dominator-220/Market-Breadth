

from plots import Plots
from moving_averages import Averages
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import plotly.offline as py
#import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.feature_selection import chi2
import pyfolio as pf
import plotly.express as px
from termcolor import colored as cl
import math
from plotly.offline import plot, iplot, init_notebook_mode
from collections import defaultdict
from datetime import datetime



avg_price = defaultdict(lambda: 0)
price_sum = defaultdict(lambda: 0)
total_cnt = defaultdict(lambda: 0)
ma_30 = defaultdict(lambda: 0)
ema_30 = defaultdict(lambda: 0)
hma_30 = defaultdict(lambda: 0)
filled_price = defaultdict(lambda: 0)
ret = defaultdict(lambda: 0)
m_cap=defaultdict(lambda:0)

li_date=[]
li_tokens=[]
val_tokens=[]
req_tokens=[]

def init_values(df):
    global val_tokens,req_tokens,avg_price,ema_30,ma_30,hma_30,filled_price,ret,li_date,li_tokens,price_sum,total_cnt
    c=['tether', 'usd-coin', 'binancecoin', 'matic-network', 'okb', 'theta-token', 'wrapped-bitcoin',
              'quant-network', 'crypto-com-chain', 'huobi-token', 'true-usd', 'kucoin-shares', 'chiliz',
              'gemini-dollar', 'compound-usd-coin', 'maker', 'rocket-pool', 'nexo', 'zilliqa', 'enjincoin', 'loopring',
              'gnosis', 'celsius-degree-token', 'swissborg', 'band-protocol', 'golem', 'iotex', 'telcoin',
              'coinex-token', 'livepeer', 'one']
    for token in c:
        val_tokens.append(token)
    d = ['tether', 'usd-coin', 'binancecoin', 'binance-usd', 'matic-network', 'staked-ether', 'okb', 'theta-token',
              'dai', 'shiba-inu-wormhole', 'hex-ethw', 'uniswap-wormhole', 'wrapped-bitcoin', 'chainlink-wormhole',
              'quant-network', 'vendetta-finance', 'near', 'frax', 'huobi-token', 'usdp', 'lido-dao-wormhole',
              'true-usd', 'usdd', 'kucoin-shares', 'chiliz', 'bittorrent', 'gemini-dollar', 'maker',
              'paxos-gold-wormhole', 'tether-gold']
    for token in d:
        req_tokens.append(token)

    df1 = df.groupby('coin')
    df2 = df.groupby('date')


    # Total Dates
    temp=sorted(list(set(df['date'])))
    for dates in temp:
        li_date.append(dates)

    df3 = df.groupby(['coin', 'date']).agg('mean')

    # replacing multiple prices of a token on a given date by their mean.

    for index, row in df.iterrows():
        price_sum[(row['coin'], row['date'])] += row['price']
        total_cnt[(row['coin'], row['date'])] += 1


    for j in price_sum:
        avg_price[j] = price_sum[j] / total_cnt[j]

    # for index, row in df.iterrows():
    #     df.loc[index, 'price'] = df3['price'][row['coin']][row['date']]

    # Since we need only one price for a given day of a token we drop the remaining ones
    df.drop_duplicates(inplace=True)
    for index, row in df.iterrows():
        m_cap[(row['coin'], row['date'])] = row['market_caps']

    temp1 = list(df.groupby(['coin'])['date'].count().reset_index(
        name='Count').sort_values(['Count'], ascending=False)['coin'].head(100))
    for tokens in temp1:
        li_tokens.append(tokens)



    for token in li_tokens:
        sum = 0
        tot = 0
        taken = [1]
        for date in li_date:
            try:
                taken.append(avg_price[(token, date)] + 1)
                indx = len(taken) - 2
                while (indx >= 0 and taken[indx] == 0):
                    taken[index] = taken[-1]
                    indx += -1
            except:
                taken.append(taken[-1])
        taken.pop(0)
        # print(taken.count(0))
        indx = 0
        for date in li_date:
            filled_price[(token, date)] = taken[indx]
            indx += 1
        avg=Averages()
        em = avg.ema(taken, 23)
        hm = avg.hma(taken, 25)
        indx = 0
        for date in li_date:
            sum += taken[indx]
            ema_30[(token, date)] = em[indx]
            hma_30[(token, date)] = hm[indx]
            if (indx < 30):
                ma_30[(token, date)] = sum / (indx + 1)
            else:
                sum -= taken[indx - 30]
                ma_30[(token, date)] = sum / 30

            if (indx > 0):
                ret[(token, date)] = np.log(taken[indx] / taken[indx - 1])
            else:
                ret[(token, date)] = 0

            indx += 1




