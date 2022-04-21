# 未实现
from pygments import highlight

class OrderList(object):
    def __init__(self):
        # 创建订单队列，包括限价订单和阻止单
        self.limitlist = list()
        self.stoplist = list()
        
    def addorder(self, offset: str, direction: str, price: float, volume: int, stop: bool):
        # 向订单队列中增加订单，包括限价订单和停止单
        # 未实现: 应还有当前tick到下一tick的新增订单指令，当限价订单价格在其中时要增加高度修正
        height = 0
        if stop:
            # 若是阻止单
            self.stoplist.append([direction, price, volume, height])
        else:
            # 若是限价单
            self.limitlist.append([direction, price, volume, height])


    def orderfinishedornot(self):
        # 要接入模拟交易指令
        # 新增订单用于订单创建时的高度修正
        # 订单取消，高度降低
        # 订单撮合，高度降低
        # 高度降低到0，即为成交
        pass

    def delall(self):
        # 清空未成交订单包括限价和停止单
        self.limitlist.clear()
        self.stoplist.clear()