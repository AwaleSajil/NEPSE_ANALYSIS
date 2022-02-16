from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Import the backtrader platform
import backtrader as bt
from backtrader.indicators.basicops import PeriodN
# from backtrader import strategy


class BaseStrategy(bt.Strategy):
    params = dict(
        fast_ma=5,
        slow_ma=15,
    )

    def __init__(self):
        # omitting a data implies self.datas[0] (aka self.data and self.data0)
        # fast_ma = bt.ind.EMA(period=self.p.fast_ma)
        # slow_ma = bt.ind.EMA(period=self.p.slow_ma)
        # our entry point
        # self.crossup = bt.ind.CrossUp(fast_ma, slow_ma)
        # self.crossdown = bt.ind.CrossDown(fast_ma, slow_ma)
        self.atr = bt.ind.ATR(period=14)
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)
        self.bband = bt.indicators.BBands(self.datas[0], period=20)


class TestStrategy(BaseStrategy):
    params = dict(
        stop_loss=0.02,
        trail=False
    )

    def notify_order(self, order):
        if not order.status == order.Completed:
            return  # discard any other notification

        if not self.position:  # we left the market
            print('SELL@price: {:.2f}'.format(order.executed.price))
            return

        # We have entered the market
        print('BUY @price: {:.2f}'.format(order.executed.price))

        if not self.p.trail:
            stop_price = order.executed.price * (1.0 - self.p.stop_loss)
            stop_price = order.executed.price  - 15* self.atr
            self.close(exectype=bt.Order.Stop, price=stop_price)
        else:
            self.close(exectype=bt.Order.StopTrail, trailamount=self.p.trail)

    def next(self):
        # print(self.bband.lines.top.get(), self.bband.lines.mid.get(),self.bband.lines.bot.get())
        # if not self.position and self.crossup > 0:
        #     # not in the market and signal triggered
        #     self.buy()
        # elif self.crossdown > 0:
        #     self.close()

        print(self.datas[0].datetime.date(0))
        print(self.bband.lines.mid.get(), self.datas[0].close.get(),self.rsi.get())
        print(not self.position,self.bband.lines.mid > self.datas[0].close,self.rsi < 30)
        # print(self.bband.lines.mid < self.datas[0].close and self.rsi > 70 and self.position.size > 0)

        if not self.position and self.bband.lines.mid > self.datas[0].close and self.rsi < 40:
            print("HI")
            # print(self.rsi.get())
            self.buy() 
        elif self.bband.lines.mid < self.datas[0].close and self.rsi > 80 and self.position.size > 0:
            print("Bye")
            print(self.position.size)
            # print(self.rsi.get())
            # print(self.bband.lines.mid.get() , self.datas[0].close.get())
            self.close()

# # Create a Stratey
# class TestStrategy(bt.Strategy):

#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries
#         self.dataclose = self.datas[0].close

#         # To keep track of pending orders
#         self.order = None

#         self.params = dict(
#         stop_loss=0.1,  # price is 2% less than the entry point
#         trail=False,
#         )

#     def log(self, txt, dt=None):
#         ''' Logging function for this strategy'''
#         dt = dt or self.datas[0].datetime.date(0)
#         print('%s, %s' % (dt.isoformat(), txt))

#     def notify_order(self, order):
#         if order.status in [order.Submitted, order.Accepted]:
#             # Buy/Sell order submitted/accepted to/by broker - Nothing to do
#             return
#         # Check if an order has been completed
#         # Attention: broker could reject order if not enough cash
#         if order.status in [order.Completed]:
#             if order.exectype in [bt.Order.Stop]:
#                 self.log('STOP-LOSS EXECUTED, %.2f' % order.executed.price)
#             if order.isbuy():
#                 self.log('BUY EXECUTED, %.2f' % order.executed.price)
#                 pass
#             elif order.issell():
#                 self.log('SELL EXECUTED, %.2f' % order.executed.price)
#                 pass

#             self.bar_executed = len(self)

#         elif order.status in [order.Canceled, order.Margin, order.Rejected]:
#             self.log('Order Canceled/Margin/Rejected')

#         # Write down: no pending order
#         self.order = None




#     def notify_trade(self, trade):
#         if not trade.isclosed:
#             return
#         self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
#                  (trade.pnl, trade.pnlcomm))



#     def next(self):
#         # print(self.position)
#         # print()
#         # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])

#         # Check if an order is pending ... if yes, we cannot send a 2nd one
#         if self.order:
#             return

#          # Check if we are in the market
#         if not self.position:

#             # Not yet ... we MIGHT BUY if ...
#             if self.dataclose[0] < self.dataclose[-1]:
#                     # current close less than previous close

#                     if self.dataclose[-1] < self.dataclose[-2]:
#                         # previous close less than the previous close

#                         # BUY, BUY, BUY!!! (with default parameters)
#                         self.log('BUY CREATE, %.2f' % self.dataclose[0])

#                         # Keep track of the created order to avoid a 2nd order
#                         self.order = self.buy()

#                         if not self.params['trail']:
#                             # stop_price = self.data.close[0] * (1.0 - self.params['stop_loss'])
#                             stop_price = self.data.close[0] - 2
#                             self.close(exectype=bt.Order.Stop, price=stop_price)
#                         else:
#                             self.close(exectype=bt.Order.StopTrail,trailamount=self.p.trail)

#         else:

#             # Already in the market ... we might sell
#             if len(self) >= (self.bar_executed + 5):
#                 # SELL, SELL, SELL!!! (with all possible default parameters)
#                 # self.log('SELL CREATE, %.2f' % self.dataclose[0])

#                 # Keep track of the created order to avoid a 2nd order
#                 # self.order = self.close()
#                 pass


        