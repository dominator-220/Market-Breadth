# MARKET BREADTH

## A stratgey implementing the concept of market breadth.



For Running the Code, just run the command (python script.py path) in terminal where path is the file location of your price data.

* Main.py specifies the type of strategy which we are using and the start and end date on ehich we run the strategy.
* perprocessing.py perprocesses the data and find all important stuff like required tokens,moving_averages,price value and market cap.
* moving_averages.py contains all the moving averages function like ema,ma,hma and cci_returns
* plots.py contains all the plots which we are using for the backtesting purposes
* strategy.py contains the 3 type of strategies Price_Strategy,Market_Cap_Strategy and Fixed_Percentage_Strategy. You can specify which type of strategy you want to run in main.py
* backtesting.py is responsible for all the backtesting stuffs including plots.