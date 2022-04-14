import pymysql
import pandas as pd

class TickDataManager(object):
    def __init__(self):
        pass
    def connectdb(self):
        self.db = pymysql.connect(host='localhost',
                     user='root',
                     password='songlinshuo',
                     database='traderdb')
    def createtable(self):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE IF EXISTS tickdata1")
        sql = """
        CREATE TABLE tickdata1 (
            Time DATETIME,
            Price FLOAT,
            Volume INT,
            Amount INT,
            OpenInt INT,
            TotalVol INT,
            TotalAmount INT,
            Price2 FLOAT,
            Price3 FLOAT,
            LastClose FLOAT,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            SP1 FLOAT,
            SP2 FLOAT,
            SP3 FLOAT,
            SP4 FLOAT,
            SP5 FLOAT,
            SV1 INT,
            SV2 INT,
            SV3 INT,
            SV4 INT,
            SV5 INT,
            BP1 FLOAT,
            BP2 FLOAT,
            BP3 FLOAT,
            BP4 FLOAT,
            BP5 FLOAT,
            BV1 INT,
            BV2 INT,
            BV3 INT,
            BV4 INT,
            BV5 INT,
            isBuy INT)
        """
        cursor.execute(sql)
    def csvinput(self):
        data = pd.read_csv("E:\办公\毕设\DCi1809 - 副本.csv", sep = ",", parse_dates = ["Time"])
        cursor = self.db.cursor()
        for i in range(1000):
            row = data.loc[i]
            sql = """
            INSERT INTO tickdata1(
                Time,
                Price,
                Volume,
                Amount,
                OpenInt,
                TotalVol,
                TotalAmount,
                Price2,
                Price3,
                LastClose,
                Open,
                High,
                Low,
                SP1,
                SP2,
                SP3,
                SP4,
                SP5,
                SV1,
                SV2,
                SV3,
                SV4,
                SV5,
                BP1,
                BP2,
                BP3,
                BP4,
                BP5,
                BV1,
                BV2,
                BV3,
                BV4,
                BV5,
                isBuy)
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """
            para = list(row)
            try:
                # 执行sql语句
                cursor.execute(sql, para)
                # 执行sql语句
                self.db.commit()
            except:
                # 发生错误时回滚
                self.db.rollback()

    def closedb(self):
        self.db.close()

dbmanager = TickDataManager()
dbmanager.connectdb()
dbmanager.createtable()
dbmanager.closedb()

dbmanager.connectdb()
dbmanager.csvinput()
dbmanager.closedb()

dbmanager.connectdb()
dbmanager.csvinput()
dbmanager.closedb()