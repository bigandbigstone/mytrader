class OrderList(object):
    def __init__(self):
        # 创建订单队列
        self.olist = list()
        
    def addorder(self):
        pass

    def orderfinishedornot(self):
        # 要接入模拟交易指令
        # 新增订单用于订单创建时的高度修正
        # 订单取消，高度降低
        # 订单撮合，高度降低
        # 高度降低到0，即为成交
        pass