from orderlist import OrderList
from vnpy.trader.constant import Direction, Offset


class BackTestTemplate(object):
    
    pos = 0
    # 持仓和持仓价格
    posPrice = 0
    # 上一成交价格，这个咋整？
    # 这个都只能在成交后在说

    def __init__(self):
        self.orderlist = OrderList()
        pass

    def buy(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send buy order to open a long position.
        """
        self.orderlist("开仓", "LONG", price, volume, stop)

    def sell(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send sell order to close a long position.
        """
        self.orderlist("平仓", "SHORT", price, volume, stop)

    def short(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send short order to open as short position.
        """
        self.orderlist("开仓", "SHORT", price, volume, stop)

    def cover(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send cover order to close a short position.
        """
        self.orderlist("开仓", "SHORT", price, volume, stop)

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