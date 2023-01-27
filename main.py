
import subprocess


def install(name):
    subprocess.call(['pip3', 'install', name])


# install('yfinance')
# install('pyfolio')
# install('numpy')
# install('pandas')
# install('plotly')
# install('seaborn')
# install('sklearn')
# install('termcolor')

from backtesting import backtest
from preprocessing import init_values
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
from strategy import Trades




def main(path):
    # path=''
    df = pd.read_csv(path)
    init_values(df)

    tc = 'wrapped-bitcoin'
    s1=Trades()
    start_date=1200
    end_date=1430
    s1.Price_Strategy(df, tc,start_date,end_date)
    backtest(s1,tc)

