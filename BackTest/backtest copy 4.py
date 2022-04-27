import TickDataManager.tickdatamanager as tdm
import TickStrategy.backtest_tick_one_strategy as ts
class BackTestManager(object):
    # 回测思路，由生成的交易指令确定下单策略订单到成交面的高度
    # 即历史订单尾+新增或取消的订单修正（乘0.5加在历史订单尾）（与策略订单同周期的）
    # 下一tick级进行撮合判断，在撮合范围则订单成交，非撮合范围则降低策略订单到成交面的高度，降低的距离为撮合量（成交）
    def __init__(self):
        self.dbmanager = tdm.TickDataManager()
        self.ticks = self.dbmanager.getdatabyorder()
        self.strategy = ts.TickOneStrategy()
        
    def outputordersbyticks(self):
        n = len(self.ticks)
        n = 30
        pretick = self.ticks[0]
        buydic = self.tobuydic(pretick)
        selldic = self.toselldic(pretick)
        for i in range(1, n):
            # 步骤1 预处理1 删除订单队列增值
            self.strategy.orderlist.orderaddclear()

            # 步骤2 预处理2 用于新建订单时的历史订单高度积累
            self.strategy.updatetickdic(buydic, selldic)

            # 步骤3 预处理3 生成模拟交易指令，并有上一轮的策略限价订单成交判定
            nowtick = self.ticks[i]
            # 步骤3.1 对买一价的处理
            if nowtick[0] == pretick[0]:
                # 买一价未发送变化
                price, vol = 0.0, 0
                if nowtick[10] < pretick[10]:
                    # 买一量减小
                    price = nowtick[0]
                    vol = pretick[10] - nowtick[10]
                    self.orderoutput("撮合", "买单", price, vol)
                elif nowtick[10] > pretick[10]:
                    # 买一量增大
                    price = nowtick[0]
                    vol = nowtick[10] - pretick[10]
                    self.orderoutput("新增", "买单", price, vol)
            elif nowtick[0] < pretick[0]:
                # 买一价减小
                price, vol = 0.0, 0
                for j in range(5):
                    if pretick[j] > nowtick[0]:
                        # 疑点1：是买一价还是卖一价
                        price = pretick[j]
                        vol = pretick[j + 10]
                        self.orderoutput("撮合", "买单", price, vol)
                    else:
                        break
                # 对当前买一价的处理
                price = nowtick[0]
                vol = nowtick[10]
                if price in buydic:
                    prevol = buydic[price]
                    if prevol > vol:
                        self.orderoutput("撮合", "买单", price, prevol - vol)
                    elif prevol < vol:
                        self.orderoutput("新增", "买单", price, vol - prevol)
                else:
                    self.orderoutput("新增", "买单", price, vol)
            else:
                # 买一价增大
                price, vol = 0.0, 0
                for j in range(5):
                    if nowtick[j] > pretick[0]:
                        price = nowtick[j]
                        vol = nowtick[j + 10]
                        self.orderoutput("新增", "买单", price, vol)
                    else:
                        break
            
            # 步骤3.2 更新非最优价买量
            for j in range(1,5):
                # nowtick里其他买入价格
                price, vol = nowtick[j], nowtick[j + 10]
                prevol = 0
                if price in buydic:
                    prevol = buydic[price]
                if vol > prevol:
                    self.orderoutput("新增", "买单", price, vol - prevol)
                elif prevol > vol:
                    self.orderoutput("取消", "买单", price, prevol - vol)

            # 步骤3.3 对卖一价的处理
            if nowtick[5] == pretick[5]:
                # 卖一价未发送变化
                price, vol = 0.0, 0
                if nowtick[15] < pretick[15]:
                    # 卖一量减小
                    price = nowtick[5]
                    vol = pretick[15] - nowtick[15]
                    self.orderoutput("撮合", "卖单", price, vol)
                elif nowtick[15] > pretick[15]:
                    # 卖一量增大
                    price = nowtick[5]
                    vol = nowtick[15] - pretick[15]
                    self.orderoutput("新增", "卖单", price, vol)
            elif nowtick[5] > pretick[5]:
                # 卖一价增大
                price, vol = 0.0, 0
                for j in range(5, 10):
                    if pretick[j] < nowtick[5]:
                        price = pretick[j]
                        vol = pretick[j + 10]
                        self.orderoutput("撮合", "卖单", price, vol)
                    else:
                        break
                # 对当前卖一价的处理
                price = nowtick[5]
                vol = nowtick[15]
                if price in selldic:
                    prevol = selldic[price]
                    if prevol > vol:
                        self.orderoutput("撮合", "卖单", price, prevol - vol)
                    elif prevol < vol:
                        self.orderoutput("新增", "卖单", price, vol - prevol)
                else:
                    self.orderoutput("新增", "卖单", price, vol)
            else:
                # 卖一价减小
                price, vol = 0.0, 0
                for j in range(5,10):
                    if nowtick[j] < pretick[5]:
                        price = nowtick[j]
                        vol = nowtick[j + 10]
                        self.orderoutput("新增", "卖单", price, vol)
                    else:
                        break
            
            # 步骤3.4 更新非最优价卖量
            for j in range(6,10):
                # nowtick里其他卖出价格
                price, vol = nowtick[j], nowtick[j + 10]
                prevol = 0
                if price in selldic:
                    prevol = selldic[price]
                if vol > prevol:
                    self.orderoutput("新增", "卖单", price, vol - prevol)
                elif prevol > vol:
                    self.orderoutput("取消", "卖单", price, prevol - vol)
            
            # 步骤4 处理上一轮的策略停止单，输入最近成交价格last_price
            self.strategy.orderlist.stoporders(pretick[20])

            # 步骤5 本轮策略进行，因为有用于订单成交判定的成交高度修正，所以要放在最后
            self.strategy.on_tick(pretick)

            # 步骤6 tick数据更新
            pretick = nowtick
            buydic = self.tobuydic(pretick)
            selldic = self.toselldic(pretick)
            print()
    
    def tobuydic(self, tick: list) -> dict:
        dic = dict()
        for i in range(5):
            dic[tick[i]] = tick[i + 10]
        return dic
    
    def toselldic(self, tick: list) -> dict:
        dic = dict()
        for i in range(5, 10):
            dic[tick[i]] = tick[i + 10]
        return dic

    def orderoutput(self, action: str, type: str, price: float, vol: int):
        # print(action + ' ' + type + ' ' + str(price) + ' ' + str(vol))
        # 包括了新增订单高度修正，上一轮限价订单成交判定
        self.strategy.orderlist.orderinput(action, type, price, vol)