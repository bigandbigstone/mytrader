from orderlist import OrderList
from vnpy.trader.constant import Direction, Offset

class BackTestTemplate(object):
    
    '''pos = 0
    posPrice = 0
    # 持仓和持仓价格在orderlist中实现'''
    
    # 上一成交价格，这个咋整？
    # 这个都只能在成交后在说

    def __init__(self):
        self.orderlist = OrderList()
    
    def updatetickdic(self, pretickdic: dict):
        self.tickdic = pretickdic

    def getheight(self, price: float) -> float:
        if price in self.tickdic:
            return self.tickdic[price]
        else:
            return 0.0

    def buy(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send buy order to open a long position.
        """
        self.orderlist.addorder("开仓", 0, price, volume, stop, self.getheight(price))

    def sell(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send sell order to close a long position.
        """
        self.orderlist.addorder("平仓", 1, price, volume, stop, self.getheight(price))

    def short(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send short order to open as short position.
        """
        self.orderlist.addorder("开仓", 1, price, volume, stop, self.getheight(price))

    def cover(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send cover order to close a short position.
        """
        self.orderlist.addorder("平仓", 0, price, volume, stop, self.getheight(price))

    def cancel_all(self):
        """
        Cancel all orders sent by strategy.
        """
        self.orderlist.delall()

    def write_log(self, msg: str):
        """
        Write a log message.
        """
        pass