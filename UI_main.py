import sys
from PyQt5 import QtWidgets
from BackTestGUI.Ui_Mainwindow_1 import MyWindow
  
if __name__=='__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MyWindow()
  window.show()
  sys.exit(app.exec_())