import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.offline as py
import plotly.express as px
import numpy as np


class Plots:
    def __init__(self):
        pass

    def plot1(self, df,buy_price, sell_price, c_price):
        plt.figure(figsize=(25, 10  ))
        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)

        ax1.plot(df['price'], color='skyblue', linewidth=2, label='CLOSE')
        ax1.plot(df.index, buy_price, marker='^', color='green', markersize=7, label='HOLD SIGNAL', linewidth=0)
        ax1.plot(df.index, sell_price, marker='v', color='red', markersize=7, label='SELL SIGNAL', linewidth=0)
        ax1.plot(df.index, c_price, marker='<', color='blue', markersize=7, label='LEAVE SIGNAL', linewidth=0)
        #     plt.savefig('price.png')
        ax1.legend()

    def plot2(self,df):
        fig = make_subplots(rows=2, cols=1)

        fig.append_trace(go.Scatter(
            x=df.index,
            y=df['price'],
            name="price"), row=1, col=1)

        fig.append_trace(go.Scatter(
            x=df.index,
            y=df['tot'], name='total tokens'
        ), row=2, col=1)

        fig.update_layout(height=500, width=1000, title_text="Subplots")
        fig.show()

    def plot3(self,df, buy_price, sell_price):

        fig = px.line(df, x=df.index, y=df['tot'])

        # Add Scatter plot
        indx = 0
        for date in df.index:
            if (sell_price[indx] != np.nan):
                fig.add_trace(go.Scatter(x=[date], y=[sell_price[indx]], showlegend=False, mode='markers',
                                         marker=dict(
                                             symbol='arrow-down',
                                             color="red",
                                             size=16
                                         )))
            if (buy_price[indx] != np.nan):
                fig.add_trace(go.Scatter(x=[date], y=[buy_price[indx]], showlegend=False, mode='markers',
                                         marker=dict(
                                             symbol='arrow-up',
                                             color="green",
                                             size=16
                                         )))
            indx += 1

        # Display the plot
        fig.show()

    def plot4(self,df, tc, buy_price, sell_price, c_price):
        fig = make_subplots(rows=2, cols=1)

        fig.append_trace(go.Scatter(
            x=df.index,
            y=df['price'],
            name="price"), row=1, col=1)
        indx = 0
        for date in df.index:
            if (sell_price[indx] != np.nan):
                fig.append_trace(go.Scatter(x=[date], y=[sell_price[indx]], showlegend=False, mode='markers',
                                            marker=dict(
                                                symbol='arrow-down',
                                                color="red",
                                                size=10
                                            )), row=1, col=1)
            if (buy_price[indx] != np.nan):
                fig.append_trace(go.Scatter(x=[date], y=[buy_price[indx]], showlegend=False, mode='markers',
                                            marker=dict(
                                                symbol='arrow-up',
                                                color="green",
                                                size=10
                                            )), row=1, col=1)
            if (c_price[indx] != np.nan):
                fig.append_trace(go.Scatter(x=[date], y=[c_price[indx]], showlegend=False, mode='markers',
                                            marker=dict(
                                                symbol='arrow-right',
                                                color="black",
                                                size=10
                                            )), row=1, col=1)

            indx += 1

        fig.append_trace(go.Scatter(
            x=df.index,
            y=df['tot'], name='total tokens', line_color='orange'
        ), row=2, col=1)

        fig.update_layout(height=500, width=1000, title_text=tc)
        fig.show()

    def c_plot(self,df):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['bnh_returns'],
            name="Buy and Hold returns"))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['strategy_returns'],
            name="Strategy returns"))

        fig.update_layout(height=500, width=1000, title_text='Strategy vs buy and Hold returns for wrapped-bitcoin')
        fig.show()



    def plot_returns(self,df):
        fig = px.line(df, x=df.index, y=df['cci_returns'])
        fig.show()
