import pymysql
import pandas as pd

class TickDataManager(object):
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                     user='root',
                     password='songlinshuo',
                     database='traderdb')
        pass
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
        row = data.loc[0]
        # csv时间格式待解决
        sql = """
        INSERT INTO tickdata1(Time, Price, Volume, Amount, OpenInt)
        VALUES (%s, %s, %s, %s, %s)
        """
        para = [row[0], row[1], row[2], row[3], row[4]]
        cursor.execute(sql,para)

    def closedb(self):
        self.db.close()

dbmanager = TickDataManager()
dbmanager.csvinput()
dbmanager.closedb()