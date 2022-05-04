import sys
from PyQt5 import QtWidgets
from BackTestGUI.Ui_Mainwindow import MyWindow
from BackTest.backtest_copy_4 import BackTestManager   
  
if __name__=='__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MyWindow()
  window.show()
  bt = BackTestManager(window)
  bt.btmain()
  sys.exit(app.exec_())