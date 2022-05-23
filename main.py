# 无图形界面高频回测系统主程序
# 作者 SongLinshuo
from BackTest.backtest_copy_4 import BackTestManager

if __name__=='__main__':
    bt = BackTestManager()
    bt.btmain()