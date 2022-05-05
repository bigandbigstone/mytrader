# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\mytrader\BackTestGUI\Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


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

        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "START"))
        self.pushButton_2.setText(_translate("MainWindow", "NEXTTICK"))
        self.pushButton_3.setText(_translate("MainWindow", "STOP"))
    
class MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
  def __init__(self):
    super(MyWindow,self).__init__()
    self.setupUi(self)