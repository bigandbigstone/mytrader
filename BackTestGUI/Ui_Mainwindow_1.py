# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\mytrader\BackTestGUI\Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from BackTest.backtest_copy_5 import BackTestManager

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1080, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.orderflow = QtWidgets.QTableView(self.centralwidget)
        self.orderflow.setGeometry(QtCore.QRect(20, 20, 256, 311))
        self.orderflow.setObjectName("orderflow")

        self.orderlist = QtWidgets.QTableView(self.centralwidget)
        self.orderlist.setGeometry(QtCore.QRect(20, 360, 256, 331))
        self.orderlist.setObjectName("orderlist")
        
        self.histogram = QtWidgets.QGraphicsView(self.centralwidget)
        self.histogram.setGeometry(QtCore.QRect(310, 190, 731, 501))
        self.histogram.setObjectName("histogram")
        
        self.strategy = QtWidgets.QTableView(self.centralwidget)
        self.strategy.setGeometry(QtCore.QRect(310, 20, 401, 141))
        self.strategy.setObjectName("strategy")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(830, 30, 181, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.StartButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.StartButton.setObjectName("StartButton")
        self.verticalLayout.addWidget(self.StartButton)
        self.StartButton.clicked.connect(self.StartAction)

        self.NextButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.NextButton.setObjectName("NextButton")
        self.verticalLayout.addWidget(self.NextButton)
        self.NextButton.setEnabled(True)
        self.NextButton.clicked.connect(self.NextAction)

        self.StopButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.StopButton.setObjectName("StopButton")
        self.verticalLayout.addWidget(self.StopButton)
        self.StopButton.clicked.connect(self.StopAction)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.p = BackTestManager(main_win=self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.StartButton.setText(_translate("MainWindow", "START"))
        self.NextButton.setText(_translate("MainWindow", "NEXTTICK"))
        self.StopButton.setText(_translate("MainWindow", "STOP"))

    def update_orderflow(self, orderf):
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['操作', '方向', '价位', '容量'])
        self.orderflow.setModel(self.model)
        for order in orderf:
            item1 = QtGui.QStandardItem(order[0])
            item2 = QtGui.QStandardItem(order[1])
            item3 = QtGui.QStandardItem(str(order[2]))
            item4 = QtGui.QStandardItem(str(order[3]))
            self.model.appendRow([item1,item2,item3,item4])
        self.orderflow.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # time.sleep(0.5)
        # pass

    def update_orderlist(self):
        pass

    def update_strategy(self):
        pass

    def update_histogram(self):
        pass

    def StartAction(self):
        self.p.start()
    
    def NextAction(self):
        pass

    def StopAction(self):
        pass

class MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
  def __init__(self):
    super(MyWindow,self).__init__()
    self.setupUi(self)