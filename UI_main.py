# 图形界面高频回测系统主程序
# 作者 SongLinshuo
import sys
from PyQt5 import QtWidgets
from BackTestGUI.Ui_Mainwindow import MyWindow
import qdarkstyle
from qdarkstyle.light.palette import LightPalette

if __name__=='__main__':
  app = QtWidgets.QApplication(sys.argv)
  app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=LightPalette()))
  window = MyWindow()
  window.show()
  sys.exit(app.exec_())