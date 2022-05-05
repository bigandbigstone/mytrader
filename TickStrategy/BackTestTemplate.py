# BackTest策略基类
from TickStrategy.orderlist import OrderList

class BackTestTemplate(object):
    
    '''pos = 0
    posPrice = 0
    # 持仓和持仓价格在orderlist中实现'''
    
    # 上一成交价格，这个咋整？
    # 这个都只能在成交后在说
    # Offset 0为开仓，1位平仓
    # Type 0为买单，1位卖单
    
    orderlist = OrderList()

    def __init__(self):
        pass
    
    def updatetickdic(self, prebuydic: dict, preselldic: dict):
        self.buydic = prebuydic
        self.selldic = preselldic

    def getheight(self, price: float) -> float:
        if price in self.buydic:
            return self.buydic[price]
        elif price in self.selldic:
            return self.selldic[price]
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
        self.orderlist.addorder(0, 0, price, volume, stop, self.getheight(price))
        print(1)

    def sell(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send sell order to close a long position.
        """
        self.orderlist.addorder(1, 1, price, volume, stop, self.getheight(price))
        print(2)

    def short(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send short order to open as short position.
        """
        self.orderlist.addorder(0, 1, price, volume, stop, self.getheight(price))
        print(3)

    def cover(
        self,
        price: float,
        volume: int,
        stop: bool = False
    ):
        """
        Send cover order to close a short position.
        """
        self.orderlist.addorder(1, 0, price, volume, stop, self.getheight(price))
        if stop:
            print(4)
        else:
            print(5)
        

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