import pandas as pd
import numpy as np
from collections import defaultdict
import math

class Averages:
    def __init__(self):
        pass

    def ema(self,values, period):
        df = pd.DataFrame(values)
        df['ema'] = df[0].ewm(span=period).mean()
        return list(df['ema'])

    def hma(self,values, period):
        df = pd.DataFrame(values)
        df['ema'] = df[0].ewm(span=period).mean()
        s = df[0]
        HMA = s.rolling(period // 2).apply(
            lambda x: ((np.arange(period // 2) + 1) * x).sum() / (np.arange(period // 2) + 1).sum(), raw=True).multiply(
            2).sub(
            s.rolling(period).apply(lambda x: ((np.arange(period) + 1) * x).sum() / (np.arange(period) + 1).sum(),
                                    raw=True)
        ).rolling(int(np.sqrt(period))).apply(
            lambda x: ((np.arange(int(np.sqrt(period))) + 1) * x).sum() / (np.arange(int(np.sqrt(period))) + 1).sum(),
            raw=True)
        return list(df['ema'])[:period] + list(HMA)[period:]

    def cci_30(self,tokens, date, sign,ema_30,ret):
        sm = 0
        #print(sign)
        for token in tokens:
            sm += ema_30[(token, date)]
        re = 0
        for token in tokens:
            w = math.sqrt(ema_30[(token, date)]) / math.sqrt(sm)
            re += w * sign[token] * ret[(token, date)]
        return re
