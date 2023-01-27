from plots import Plots
import pyfolio as pf
import matplotlib.pyplot as plt


def backtest(st,tc):

    print("Buy and hold returns:", st.df_returns['bnh_returns'].cumsum()[-1])
    print("Strategy returns:", st.df_returns['strategy_returns'].cumsum()[-1])
    Plot=Plots()
    Plot.plot1(st.df_returns, st.buy_price, st.sell_price,st.c_price)


    Plot.plot2(st.df_returns)
    Plot.plot_returns(st.df_returns)
    Plot.plot3(st.df_returns, st.buy_price1, st.sell_price1)
    Plot.plot4(st.df_returns, tc, st.buy_price, st.sell_price, st.c_price)
    #     fig=go.Figure([go.Scatter(x=df_returns.index, y=df_returns['tot'])])
    #     fig.show()
    # plotting strategy historical performance over time
    df_returns=st.df_returns

    df_returns[['bnh_returns', 'strategy_returns']] = df_returns[['bnh_returns', 'strategy_returns']].cumsum()
    df_returns[['bnh_returns', 'strategy_returns']].plot(grid=True, figsize=(12, 8))
    Plot.c_plot(df_returns)

    pf.create_simple_tear_sheet(df_returns['strategy_returns'].diff())
    plt.show()
