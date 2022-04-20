from datetime import datetime, time
import numpy as np

class TickArrayManager(object):
    '''
    Tick序列管理工具, 负责:
    1. Tick时间序列的维护
    2. 常用技术指标的计算
    '''
    # ----------------------------------------------------------------------
    def __init__(self, size=10):
        '''TickArrayManager初始化'''
        self.count = 0  # 缓存计数
        self.size = size  # 缓存大小
        self.inited = False  # True if count>=size
  
        self.TickaskVolume1Array = np.zeros(self.size)
        self.TickbidVolume1Array = np.zeros(self.size)
  
    # ----------------------------------------------------------------------
    def updateTick(self, tick: list):
        '''更新tick Array'''
        self.count += 1
        if not self.inited and self.count >= self.size:
            self.inited = True
  
        self.TickaskVolume1Array[0:self.size - 1] = self.TickaskVolume1Array[1:self.size]
        self.TickbidVolume1Array[0:self.size - 1] = self.TickbidVolume1Array[1:self.size]
  
        self.TickaskVolume1Array[-1] = tick[0]
        self.TickbidVolume1Array[-1] = tick[5]
  
    def askBidVolumeDif(self):
        return (self.TickaskVolume1Array.sum() - self.TickbidVolume1Array.sum())

class TickOneStrategy(object):
    '''基于Tick的高频策略'''
    name = "TickOneStrategy"
    class_name = "TickOneStrategy"
    author = "SongLinshuo"
  
    # 策略参数
    fixedSize = 1
    Ticksize = 10
    initDays = 0
  
    DAY_START = time(9, 00)  # 日盘启动和停止时间
    DAY_END = time(14, 58)
    NIGHT_START = time(21, 00)  # 夜盘启动和停止时间
    NIGHT_END = time(10, 58)
  
    # ----------------------------------------------------------------------
    def __init__(self):
        #创建Array队列
        self.tickArray = TickArrayManager(self.Ticksize)

    # ----------------------------------------------------------------------
    def on_tick(self, tick: list):
        '''收到行情TICK推送'''
        # tick.last_price 修改为 tick[20]
        # tick.pre_close 修改为 tick[21]
        currentTime = datetime.now().time()
        # 平当日仓位, 如果当前时间是结束前日盘15点28分钟,或者夜盘10点58分钟，如果有持仓，平仓。
        if ((currentTime >= self.DAY_START and currentTime <= self.DAY_END) or
            (currentTime >= self.NIGHT_START and currentTime <= self.NIGHT_END)):
            TA = self.tickArray
            TA.updateTick(tick)
            if not TA.inited:
                return
            if self.pos == 0:
                # 如果空仓，分析过去10个对比，ask卖方多下空单，bid买方多下多单，并防止两个差价阻止单
                if TA.askBidVolumeDif() > 0:
                    self.short(tick[20], self.fixedSize, False)
                    self.cover(tick[20] + 2,self.fixedSize, True)
                elif TA.askBidVolumeDif() < 0:
                    self.buy(tick[20], self.fixedSize, False)
                    self.sell(tick[20] - 2, self.fixedSize, True)
  
            elif self.pos > 0:
                # 如果持有多单，如果已经是买入价格正向N3个点，再次判断趋势，如果已经不符合，市价卖出。如果持有，清掉之前阻止单，改挂当前价位反向2个点阻止单。
                if  tick[20] - self.posPrice >= 3:
                    if TA.askBidVolumeDif() < 0:
                        self.cancel_all()
                        self.sell(tick[20] - 2, self.fixedSize, True)
                    else:
                        self.cancel_all()
                        self.sell(tick[20], self.fixedSize, False)
  
            elif self.pos < 0:
                # 如果持有空单，如果已经是买入价格反向N3个点，再次判断趋势，如果已经不符合，市价卖出。如果持有，清掉之前阻止单，改挂当前价位反向2个点阻止单。
                if  tick[20] - self.posPrice <= -3:
                    if TA.askBidVolumeDif() > 0:
                        self.cancel_all()
                        self.cover(tick[20] + 2, self.fixedSize, True)
                    else:
                        self.cancel_all()
                        self.cover(tick[20], self.fixedSize, False)
        else:
            if self.pos > 0:
                self.sell(tick[21], abs(self.pos), False)
            elif self.pos < 0:
                self.cover(tick[21], abs(self.pos), False)
            elif self.pos == 0:
                return

    def sell():
        pass

    def buy():
        pass

    def short():
        pass

    def cover():
        pass
    
    def cancel_all():
        pass