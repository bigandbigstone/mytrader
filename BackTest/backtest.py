#回测备份版本0，最新版本见copy4
import TickDataManager.tickdatamanager as tdm
class BackTestManager(object):
    def __init__(self):
        pass
    def outputordersbyticks(self):
        dbmanager = tdm.TickDataManager()
        ticks = dbmanager.getdatabyorder()
        n = len(ticks)
        n = 2
        pretick = ticks[0]
        buydic = self.tobuydic(pretick)
        selldic = self.toselldic(pretick)
        for i in range(1, n):
            nowtick = ticks[i]
            if nowtick[0] < pretick[0] or nowtick[10] < pretick[10]:
                # 买一价减小或买一量减少
                price, vol = 0.0, 0
                if nowtick[0] == pretick[0]:
                    # 如果是买一价没有变
                    price = nowtick[0]
                    vol = pretick[10] - nowtick[10]
                else:
                    for j in range(5):
                        if pretick[j] >= nowtick[0]:
                            # 疑点1：是买一价还是卖一价
                            price = pretick[j]
                    for j in range(10,15):
                        if pretick[j - 10] > price:
                            vol += pretick[j]
                        if pretick[j - 10] == price:
                            vol += (pretick[j] - nowtick[j])

                self.orderoutput("卖出", price, vol)
                # 疑点2: vol为负数时如何处理？
            
            if nowtick[5] > pretick[5] or nowtick[15] < pretick[15]:
                # 卖一价增大或卖一量减少
                price, vol = 0.0, 0
                if nowtick[5] == pretick[5]:
                    # 如果是买一价没有变
                    price = nowtick[5]
                    vol = pretick[15] - nowtick[15]
                else:
                    for j in range(5, 10):
                        if pretick[j] <= nowtick[5]:
                            price = pretick[j]
                    for j in range(15,20):
                        if pretick[j - 10] < price:
                            vol += pretick[j]
                        if pretick[j - 10] == price:
                            vol += (pretick[j] - nowtick[j])
                            
                self.orderoutput("买入", price, vol)
                # 疑点2: vol为负数时如何处理？
            
            # 更新非最优价买卖量
            for j in range(1,5):
                # nowtick里其他买入价格
                price, vol = nowtick[j], nowtick[j + 10]
                prevol = 0
                if price in buydic:
                    prevol = buydic[price]
                if vol > prevol:
                    self.orderoutput("买入", price, vol - prevol)
                elif prevol > vol:
                    self.orderoutput("取消", price, prevol - vol)
            
            for j in range(6,10):
                # nowtick里其他卖出价格
                price, vol = nowtick[j], nowtick[j + 10]
                prevol = 0
                if price in selldic:
                    prevol = selldic[price]
                if vol > prevol:
                    self.orderoutput("卖出", price, vol - prevol)
                elif prevol > vol:
                    self.orderoutput("取消", price, prevol - vol)

            pretick = nowtick
            buydic = self.tobuydic(pretick)
            selldic = self.toselldic(pretick)
    
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

    def orderoutput(self, type: str, price: float, vol: int):
        print(type + str(price) + ' ' + str(vol))

backtest = BackTestManager()
backtest.outputordersbyticks()