import sys
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from  PyQt5.QtChart import (QChartView, QChart, QBarSeries, QBarSet,QLegend, QBarCategoryAxis, QValueAxis)
class DemoChartBarSeries(QMainWindow):
    def __init__(self, parent=None):
        super(DemoChartBarSeries, self).__init__(parent)                    # 设置窗口标题        
        self.setWindowTitle('实战 Qt for Python: QChart柱状图演示')              # 设置窗口大小        
        self.resize(480, 360)                
        self.createChart()
        
    def createChart(self):                #创建条状单元        
        barSet0 = QBarSet('Jane')        
        barSet1 = QBarSet('Jone')        
        barSet2 = QBarSet('Axel')        
        barSet3 = QBarSet('Mary')        
        barSet4 = QBarSet('Samantha')                
        barSet0.append([1, 2, 3, 4, 5, 6])        
        barSet1.append([5, 0, 0, 4, 0, 7])        
        barSet2.append([3, 5, 8, 13, 8, 5])        
        barSet3.append([5, 6, 7, 3, 4, 5])        
        barSet4.append([9, 7, 5, 3, 1, 2]) 
        #条状图        
        barSeries = QBarSeries()        
        barSeries.append(barSet0)        
        barSeries.append(barSet1)        
        barSeries.append(barSet2)        
        barSeries.append(barSet3)        
        barSeries.append(barSet4)                #创建图表        
        chart = QChart()        
        chart.addSeries(barSeries)        
        chart.setTitle('简单柱状图示例')        
        chart.setAnimationOptions(QChart.SeriesAnimations) #设置成动画显示                
        #设置横向坐标(X轴)        
        categories = ['一月', '二月', '三月', '四月', '五月', '六月']        
        axisX = QBarCategoryAxis()        
        axisX.append(categories)        
        chart.addAxis(axisX, Qt.AlignBottom)        
        barSeries.attachAxis(axisX)                
        #设置纵向坐标(Y轴)        
        axisY = QValueAxis()        
        axisY.setRange(0, 15)        
        chart.addAxis(axisY, Qt.AlignLeft)        
        barSeries.attachAxis(axisY)                
        #图例属性        
        chart.legend().setVisible(True)        
        chart.legend().setAlignment(Qt.AlignBottom)                
        #图表视图        
        chartView = QChartView(chart)        
        chartView.setRenderHint(QPainter.Antialiasing)                
        self.setCentralWidget(chartView)

if __name__ == '__main__':    
    app = QApplication(sys.argv)    
    window = DemoChartBarSeries()    
    window.show()    
    sys.exit(app.exec())  