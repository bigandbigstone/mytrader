from datetime import datetime, time
import numpy as np
from vnpy_ctastrategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager
)

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
  
        self.TicklastPriceArray = np.zeros(self.size)
        self.TickaskVolume1Array = np.zeros(self.size)
        self.TickbidVolume1Array = np.zeros(self.size)
        self.TickaskPrice1Array = np.zeros(self.size)
        self.TickbidPrice1Array = np.zeros(self.size)
        self.TickopenInterestArray = np.zeros(self.size)
        self.TickvolumeArray = np.zeros(self.size)
  
    # ----------------------------------------------------------------------
    def updateTick(self, tick: TickData):
        '''更新tick Array'''
        self.count += 1
        if not self.inited and self.count >= self.size:
            self.inited = True
  
        self.TicklastPriceArray[0:self.size - 1] = self.TicklastPriceArray[1:self.size]
        self.TickaskVolume1Array[0:self.size - 1] = self.TickaskVolume1Array[1:self.size]
        self.TickbidVolume1Array[0:self.size - 1] = self.TickbidVolume1Array[1:self.size]
        self.TickaskPrice1Array[0:self.size - 1] = self.TickaskPrice1Array[1:self.size]
        self.TickbidPrice1Array[0:self.size - 1] = self.TickbidPrice1Array[1:self.size]
        self.TickopenInterestArray[0:self.size - 1] = self.TickopenInterestArray[1:self.size]
        self.TickvolumeArray[0:self.size - 1] = self.TickvolumeArray[1:self.size]
  
        self.TicklastPriceArray[-1] = tick.last_price
        self.TickaskVolume1Array[-1] = tick.ask_volume_1
        self.TickbidVolume1Array[-1] = tick.bid_volume_1
        self.TickaskPrice1Array[-1] = tick.ask_price_1
        self.TickbidPrice1Array[-1] = tick.bid_price_1
        self.TickopenInterestArray[-1] = tick.open_interest
        self.TickvolumeArray[-1] = tick.volume
  
    def askBidVolumeDif(self):
        return (self.TickaskVolume1Array.sum() - self.TickbidVolume1Array.sum())

class TickOneStrategy(CtaTemplate):
    '''基于Tick的高频策略'''
    author = "SongLinshuo"
  
    # 策略参数
    fixedSize = 1
    Ticksize = 10
    initDays = 0
  
    DAY_START = time(9, 00)  # 日盘启动和停止时间
    DAY_END = time(14, 58)
    NIGHT_START = time(21, 00)  # 夜盘启动和停止时间
    NIGHT_END = time(10, 58)
  
    # 策略变量
    posPrice = 0  # 持仓价格
    pos = 0       # 持仓数量
  
  
    # 参数列表，保存了参数的名称
    parameters = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'initDays',
                 'Ticksize',
                 'fixedSize'
                 ]
  
    # 变量列表，保存了变量的名称
    variables = ['inited',
               'trading',
               'pos',
               'posPrice'
               ]
  
    # 同步列表，保存了需要保存到数据库的变量名称
    '''
    syncList = ['pos',
                'posPrice',
                'intraTradeHigh',
                'intraTradeLow']
    '''
  
    # ----------------------------------------------------------------------
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        # self.bg = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        # self.am = ArrayManager()
        #创建Array队列
        self.tickArray = TickArrayManager(self.Ticksize)

    # ----------------------------------------------------------------------
    
    def on_init(self):
        '''初始化策略'''
        self.write_log("策略初始化")
        # tick级别交易，不需要过往历史数据
        # self.load_bar(10)
        self.put_event()
  
    # ----------------------------------------------------------------------
    def on_start(self):
        '''启动策略'''
        self.write_log("策略启动")
        self.put_event()
  
    # ----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.write_log("策略停止")
        self.put_event()
  
    # ----------------------------------------------------------------------
    def on_tick(self, tick: TickData):
        '''收到行情TICK推送'''
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
                    self.short(tick.last_price, self.fixedSize, False)
                    self.cover(tick.last_price + 2,self.fixedSize, True)
                elif TA.askBidVolumeDif() < 0:
                    self.buy(tick.last_price, self.fixedSize, False)
                    self.sell(tick.last_price - 2, self.fixedSize, True)
  
            elif self.pos > 0:
                # 如果持有多单，如果已经是买入价格正向N3个点，再次判断趋势，如果已经不符合，市价卖出。如果持有，清掉之前阻止单，改挂当前价位反向2个点阻止单。
                if  tick.last_price - self.posPrice >= 3:
                    if TA.askBidVolumeDif() < 0:
                        self.cancel_all()
                        self.sell(tick.last_price - 2, self.fixedSize, True)
                    else:
                        self.cancel_all()
                        self.sell(tick.last_price, self.fixedSize, False)
  
            elif self.pos < 0:
                # 如果持有空单，如果已经是买入价格反向N3个点，再次判断趋势，如果已经不符合，市价卖出。如果持有，清掉之前阻止单，改挂当前价位反向2个点阻止单。
                if  tick.last_price - self.posPrice <= -3:
                    if TA.askBidVolumeDif() > 0:
                        self.cancel_all()
                        self.cover(tick.last_price + 2, self.fixedSize, True)
                    else:
                        self.cancel_all()
                        self.cover(tick.last_price, self.fixedSize, False)
        else:
            if self.pos > 0:
                self.sell(tick.pre_close, abs(self.pos), False)
            elif self.pos < 0:
                self.cover(tick.pre_close, abs(self.pos), False)
            elif self.pos == 0:
                return
  
    # ----------------------------------------------------------------------
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        pass
  
    # ----------------------------------------------------------------------
    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass
  
    # ----------------------------------------------------------------------
    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.posPrice = trade.price
        self.put_event()
  
    # ----------------------------------------------------------------------
    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass