import pandas as pd
import numpy as np
from collections import defaultdict
from preprocessing import li_date,li_tokens,filled_price,ema_30,ret,val_tokens,m_cap
import pyfolio as pf
from moving_averages import Averages
from datetime import datetime

class Trades:
    def __init__(self):
        self.df_returns=pd.DataFrame([])
        self.buy_price = []
        self.sell_price = []
        self.c_price = []
        self.buy_price1 = []
        self.sell_price1 = []
        self.c_price1 = []



    def Price_Strategy(self,data, tc,start_date,last_date):
        c1=47
        c2=7
        c3=33
        #     df=data.copy()
        #     df['bnh_returns']=[ret[(row['coin'],row['date'])] for index,row in df.iterrows()]

        #     df['ma30'] = [ma_30[(row['coin'],row['date'])] for index,row in df.iterrows()]
        #     #df['std'] = df['Adj Close'].rolling(window=20).std()
        #     df['price']=  [filled_price[(row['coin'],row['date'])] for index,row in df.iterrows()]
        # c1 is number of days you go for short signal once the call is generated.
        # c2 is the number of days you wait for shorting once the call is generated.
        # c3 is the number of days you go for long signal once the call is generated.

        str_returns = defaultdict(lambda: 0)
        cci_returns = defaultdict(lambda: 0)
        sign = defaultdict(lambda: 0)
        sm = defaultdict(lambda: 0)
        last = 0
        # signal=defaultdict(lambda:0)
        indx = 1
        format = '%Y-%m-%d'
        li = []

        last1 = 0
        last2 = 0
        # c1=[750:930]
        # c2=[1200:1530]
        dates = li_date[start_date:last_date]
        last_tot = 0
        for date in dates:
            self.buy_price.append(np.nan)
            self.sell_price.append(np.nan)
            self.c_price.append(np.nan)
            self.buy_price1.append(np.nan)
            self.sell_price1.append(np.nan)
            self.c_price1.append(np.nan)
            z = []
            for token in li_tokens:
                z.append([filled_price[(token, date)], token])
            z.sort(reverse=True)
            res = [i[1] for i in z[:31]]

            tot = 0
            for token in res:
                if (filled_price[(token, date)] > ema_30[(token, date)]):
                    tot += 1
            li.append(tot)
            # print(date,tot-last_tot)
            k = tot - last_tot
            for token in li_tokens:
                if (token != tc):
                    continue
                #             print(date,sign[token],ret[(token,li_date[indx])])
                str_returns[datetime.strptime(date, format)] += sign[token] * ret[(token, date)]
                sm[datetime.strptime(date, format)] += ret[(token, date)]
            avg=Averages()

            cci_returns[datetime.strptime(date, format)] = avg.cci_30(val_tokens, date, sign,ema_30,ret)

            # cooldown period of short call is over
            if (last == 1):
                last = 0
                if (sign[tc] == 0):
                    pass
                else:
                    self.c_price[-1] = filled_price[(tc, date)]
                    self.c_price1[-1] = tot

                    for token in li_tokens:
                        sign[token] = 0
                last = 0
            # cooldown period of long call is over.
            if (last2 > c3):
                # print(date,last2)
                last2 = 0
                if (sign[tc] == 0):
                    pass
                else:
                    self.c_price[-1] = filled_price[(tc, date)]
                    self.c_price1[-1] = tot

                    for token in li_tokens:
                        sign[token] = 0

            # waiting period before actually shorting is over and you can short now.
            if (last1 == 1):
                # print(date,last1,last2)
                if (last2 >= 1 and last2 <= c3):

                    last1 += c3 - last2 + 1
                    last += c3 - last2 + 1
                else:

                    self.sell_price[-1] = filled_price[(tc, date)]

                    for token in li_tokens:
                        if (sign[token] == 0):
                            sign[token] = -1

            # condition triggering call for long
            if (tot < 4 and last == 0 and last2 == 0):
                self.buy_price[-1] = filled_price[(tc, date)]
                self.buy_price1[-1] = tot
                for token in li_tokens:
                    sign[token] = 1
                last2 = 1

            # condition triggering call for short
            if (tot > 24 and last == 0):
                if (tot > 31):
                    pass
                else:
                    self.sell_price1[-1] = tot
                    last = c1
                    last1 = c2
            if (last > 0):
                last -= 1
            if (last2 > 0):
                last2 += 1
            if (last1 > 0):
                last1 -= 1
            last_tot = tot

            #         if(tot<3):
            #             for token in li_tokens:
            #                 if(sign[token]==-1):
            #                     sign[token]=0
            indx += 1
        df_returns = pd.DataFrame(str_returns, index=[0]).T
        df_returns.rename(columns={0: 'strategy_returns'}, inplace=True)
        df_returns['bnh_returns'] = [sm[date] for date in df_returns.index]
        df_returns['cci_returns'] = [cci_returns[date] for date in df_returns.index]

        df_returns[['cci_returns']] = df_returns[['cci_returns']].cumsum()
        df_returns['price'] = [filled_price[(tc, dates[i])] for i in range(len(df_returns))]
        df_returns['tot'] = [li[i] for i in range(len(df_returns))]
        self.df_returns=df_returns



    def Market_Cap_Strategy(self,data, tc,start_date,last_date):
        #     df=data.copy()
        #     df['bnh_returns']=[ret[(row['coin'],row['date'])] for index,row in df.iterrows()]

        #     df['ma30'] = [ma_30[(row['coin'],row['date'])] for index,row in df.iterrows()]
        #     #df['std'] = df['Adj Close'].rolling(window=20).std()
        #     df['price']=  [filled_price[(row['coin'],row['date'])] for index,row in df.iterrows()]
        c1=49
        c2=10
        c3=35

        str_returns = defaultdict(lambda: 0)
        cci_returns = defaultdict(lambda: 0)
        sign = defaultdict(lambda: 0)
        sm = defaultdict(lambda: 0)
        last = 0
        # signal=defaultdict(lambda:0)
        indx = 1
        format = '%Y-%m-%d'
        li = []
        last1 = 0
        last2 = 0
        # c1=[750:930]
        # c2=[1200:1530]
        dates = li_date[start_date:last_date]
        last_tot = 0
        for date in dates:
            self.buy_price.append(np.nan)
            self.sell_price.append(np.nan)
            self.c_price.append(np.nan)
            self.buy_price1.append(np.nan)
            self.sell_price1.append(np.nan)
            self.c_price1.append(np.nan)

            z = []
            for token in li_tokens:
                z.append([m_cap[(token, date)], token])
            z.sort(reverse=True)
            res = [i[1] for i in z[:15]]

            tot = 0
            for token in res:
                if (filled_price[(token, date)] > ema_30[(token, date)]):
                    tot += 1
            li.append(tot)
            # print(date,tot-last_tot)
            k = tot - last_tot
            for token in li_tokens:
                if (token != tc):
                    continue
                #             print(date,sign[token],ret[(token,li_date[indx])])
                str_returns[datetime.strptime(date, format)] += sign[token] * ret[(token, date)]
                sm[datetime.strptime(date, format)] += ret[(token, date)]
            avg = Averages()
            cci_returns[datetime.strptime(date, format)] = avg.cci_30(val_tokens, date, sign,ema_30,ret)

            if (last == 1):
                last = 0
                if (sign[tc] == 0):
                    pass
                else:
                    self.c_price[-1] = filled_price[(tc, date)]
                    self.c_price1[-1] = tot

                    for token in li_tokens:
                        sign[token] = 0
                last = 0
            if (last2 > c3):
                # print(date,last2)
                last2 = 0
                if (sign[tc] == 0):
                    pass
                else:
                    self.c_price[-1] = filled_price[(tc, date)]
                    self.c_price1[-1] = tot

                    for token in li_tokens:
                        sign[token] = 0

            if (last1 == 1):
                # print(date,last1,last2)
                if (last2 >= 1 and last2 <= c3):

                    last1 += c3 - last2 + 1
                    last += c3 - last2 + 1
                else:

                    self.sell_price[-1] = filled_price[(tc, date)]

                    for token in li_tokens:
                        if (sign[token] == 0):
                            sign[token] = -1

            if (tot < 3 and last == 0 and last2 == 0):
                self.buy_price[-1] = filled_price[(tc, date)]
                self.buy_price1[-1] = tot
                for token in li_tokens:
                    sign[token] = 1
                last2 = 1

            if (tot > 11 and last == 0):
                if (tot > 70):
                    pass
                else:
                    self.sell_price1[-1] = tot
                    last = c1
                    last1 = c2
            if (last > 0):
                last -= 1
            if (last2 > 0):
                last2 += 1
            if (last1 > 0):
                last1 -= 1
            last_tot = tot

            #         if(tot<3):
            #             for token in li_tokens:
            #                 if(sign[token]==-1):
            #                     sign[token]=0
            indx += 1

        df_returns = pd.DataFrame(str_returns, index=[0]).T
        df_returns.rename(columns={0: 'strategy_returns'}, inplace=True)
        df_returns['bnh_returns'] = [sm[date] for date in df_returns.index]
        df_returns['cci_returns'] = [cci_returns[date] for date in df_returns.index]

        df_returns[['cci_returns']] = df_returns[['cci_returns']].cumsum()
        df_returns['price'] = [filled_price[(tc, dates[i])] for i in range(len(df_returns))]
        df_returns['tot'] = [li[i] for i in range(len(df_returns))]
        self.df_returns=df_returns



    def Fixed_Percentage_Strategy(self,data, tc,start_date,end_date):
        c1=49
        c2=10
        c3=35
        #     df=data.copy()
        #     df['bnh_returns']=[ret[(row['coin'],row['date'])] for index,row in df.iterrows()]

        #     df['ma30'] = [ma_30[(row['coin'],row['date'])] for index,row in df.iterrows()]
        #     #df['std'] = df['Adj Close'].rolling(window=20).std()
        #     df['price']=  [filled_price[(row['coin'],row['date'])] for index,row in df.iterrows()]

        str_returns = defaultdict(lambda: 0)
        cci_returns = defaultdict(lambda: 0)
        sign = defaultdict(lambda: 0)
        sm = defaultdict(lambda: 0)
        last = 0
        # signal=defaultdict(lambda:0)
        indx = 1
        format = '%Y-%m-%d'
        li = []

        last1 = 0
        last2 = 0
        # c1=[750:930]
        # c2=[1200:1530]
        dates = li_date[start_date:end_date]
        last_tot = 0
        for date in dates:
            self.buy_price.append(np.nan)
            self.sell_price.append(np.nan)
            self.c_price.append(np.nan)
            self.buy_price1.append(np.nan)
            self.sell_price1.append(np.nan)
            self.c_price1.append(np.nan)

            z = []
            al = 0

            for token in li_tokens:
                if (m_cap[(token, date)] != 0):
                    al += 1
                z.append([m_cap[(token, date)], token])
            al = min(al, 100)
            hi = ((8 * al) / 10) + 1
            lo = al / 12
            z.sort(reverse=True)
            res = [i[1] for i in z[:al]]

            tot = 0
            for token in z[:al]:
                if (filled_price[(token[1], date)] > ema_30[(token[1], date)]):
                    tot += 1
            li.append(tot)
            # print(date,tot-last_tot)
            k = tot - last_tot
            for token in li_tokens:
                if (token != tc):
                    continue
                #             print(date,sign[token],ret[(token,li_date[indx])])
                str_returns[datetime.strptime(date, format)] += sign[token] * ret[(token, date)]
                sm[datetime.strptime(date, format)] += ret[(token, date)]
            avg=Averages()
            cci_returns[datetime.strptime(date, format)] = avg.cci_30(val_tokens, date, sign, ema_30, ret)

            if (last == 1):
                last = 0
                if (sign[tc] == 0):
                    pass
                else:
                    self.c_price[-1] = filled_price[(tc, date)]
                    self.c_price1[-1] = tot

                    for token in li_tokens:
                        sign[token] = 0
                last = 0
            if (last2 > c3):
                # print(date,last2)
                last2 = 0
                if (sign[tc] == 0):
                    pass
                else:
                    self.c_price[-1] = filled_price[(tc, date)]
                    self.c_price1[-1] = tot

                    for token in li_tokens:
                        sign[token] = 0

            if (last1 == 1):
                # print(date,last1,last2)
                if (last2 >= 1 and last2 <= c3):

                    last1 += c3 - last2 + 1
                    last += c3 - last2 + 1
                else:

                    self.sell_price[-1] = filled_price[(tc, date)]

                    for token in li_tokens:
                        if (sign[token] == 0):
                            sign[token] = -1

            if (tot < lo and last == 0 and last2 == 0):
                self.buy_price[-1] = filled_price[(tc, date)]
                self.buy_price1[-1] = tot
                for token in li_tokens:
                    sign[token] = 1
                last2 = 1

            if (tot > hi and last == 0):
                self.sell_price1[-1] = tot
                last = c1
                last1 = c2
            if (last > 0):
                last -= 1
            if (last2 > 0):
                last2 += 1
            if (last1 > 0):
                last1 -= 1
            last_tot = tot

            #         if(tot<3):
            #             for token in li_tokens:
            #                 if(sign[token]==-1):
            #                     sign[token]=0
            indx += 1
        df_returns = pd.DataFrame(str_returns, index=[0]).T
        df_returns.rename(columns={0: 'strategy_returns'}, inplace=True)
        df_returns['bnh_returns'] = [sm[date] for date in df_returns.index]
        df_returns['cci_returns'] = [cci_returns[date] for date in df_returns.index]

        df_returns[['cci_returns']] = df_returns[['cci_returns']].cumsum()
        df_returns['price'] = [filled_price[(tc, dates[i])] for i in range(len(df_returns))]
        df_returns['tot'] = [li[i] for i in range(len(df_returns))]
        self.df_returns=df_returns











