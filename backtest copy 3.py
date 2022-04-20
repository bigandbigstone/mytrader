import tickdatamanager as tdm
class BackTestManager(object):
    # 回测思路，由生成的交易指令确定下单策略订单到成交面的高度
    # 即历史订单尾+新增或取消的订单修正（乘0.5加在历史订单尾）（与策略订单同周期的）
    # 下一tick级进行撮合判断，在撮合范围则订单成交，非撮合范围则降低策略订单到成交面的高度，降低的距离为撮合量（成交）
    def __init__(self):
        pass
    def outputordersbyticks(self):
        dbmanager = tdm.TickDataManager()
        ticks = dbmanager.getdatabyorder()
        n = len(ticks)
        n = 30
        pretick = ticks[0]
        buydic = self.tobuydic(pretick)
        selldic = self.toselldic(pretick)
        for i in range(1, n):
            nowtick = ticks[i]
            
            # 对买一价的处理
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
                    elif nowtick[j] == pretick[0]:
                        price = nowtick[j]
                        vol = nowtick[j + 10]
                        if pretick[10] > vol:
                            self.orderoutput("取消", "买单", price, pretick[10] - vol)
                        elif pretick[10] < vol:
                            self.orderoutput("新增", "买单", price, vol - pretick[10])
                    else:
                        break
            
            # 对卖一价的处理
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
                    elif nowtick[j] == pretick[5]:
                        price = nowtick[j]
                        vol = nowtick[j + 10]
                        if pretick[10] > vol:
                            self.orderoutput("取消", "卖单", price, pretick[10] - vol)
                        elif pretick[10] < vol:
                            self.orderoutput("新增", "卖单", price, vol - pretick[10])
                    else:
                        break

            # 更新非最优价买卖量
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
        print(action + ' ' + type + ' ' + str(price) + ' ' + str(vol))


backtest = BackTestManager()
backtest.outputordersbyticks()