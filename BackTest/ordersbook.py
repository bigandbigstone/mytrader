from collections import deque
import TickDataManager.tickdatamanager as tdm
class OrdersBook(object):
    def __init__(self, tick: list):
        self.buydq, self.selldq = deque(), deque()
        self.buydic, self.selldic = dict(), dict()
        for i in range(5):
            self.buydq.append(tick[i])
            self.buydic[tick[i]] = tick[i + 10]
        for i in range(5, 10):
            self.selldq.append(tick[i])
            self.selldic[tick[i]] = tick[i + 10]
    def update(self, tick: list):
        self.buydq, self.selldq = deque(), deque()
        self.buydic, self.selldic = dict(), dict()
        for i in range(5):
            self.buydq.append(tick[i])
            self.buydic[tick[i]] = tick[i + 10]
        for i in range(5, 10):
            self.selldq.append(tick[i])
            self.selldic[tick[i]] = tick[i + 10]