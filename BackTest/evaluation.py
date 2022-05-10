# 回测策略指标评估器
class Evaluater(object):
    # 计算年化收益率
    # 最大回撤
    # 夏普比率
    def __init__(self):
        # 合约乘数
        self.cm = 100
        # 当前资产偏移
        self.capital = 0
        # 当前回撤
        self.drawdown = 0
        # 最大回撤
        self.MAXDrawDown = 0
        # 历史资产最高值
        self.MAXcapital = 0
        # 历史资产最低值
        self.MINcapital = 0
        # 前一tick资产值
        self.pre_capital = 0
    def update_evaluation(self, capital):
        self.pre_capital = self.capital
        self.capital = capital * self.cm
        if self.pre_capital > self.capital:
            self.drawdown += self.pre_capital - self.capital
        else:
            self.drawdown = 0
        self.MAXcapital = max(self.MAXcapital, self.capital)
        self.MINcapital = min(self.MINcapital, self.capital)
        self.MAXDrawDown = max(self.MAXDrawDown, self.drawdown)

        
