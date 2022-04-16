import asyncio
import aiomysql
# import pymysql
import pandas as pd

class TickDataManager(object):
    def __init__(self):
        pass

    async def connectdb(self):
        self.db = await aiomysql.connect(host='localhost',
                     user='root',
                     password='songlinshuo',
                     database='traderdb')

    async def createtable(self):
        await self.connectdb()
        cursor = await self.db.cursor()
        await cursor.execute("DROP TABLE IF EXISTS tickdata2")
        sql = """
        CREATE TABLE tickdata1 (
            Time DATETIME,
            Price FLOAT,
            Volume INT,
            Amount INT,
            OpenInt INT,
            TotalVol BIGINT,
            TotalAmount BIGINT,
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
        await cursor.execute(sql)
        cursor.close()
        self.closedb()

    async def csvinput(self, start: int):
        data = pd.read_csv("E:\办公\毕设\DCi1809 - 副本.csv", sep = ",", parse_dates = ["Time"])
        n = len(data)
        await self.connectdb()
        cursor = await self.db.cursor()
        for i in range(start, n):
            print(i)
            row = data.loc[i]
            sql = """
            INSERT INTO tickdata2(
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
                await cursor.execute(sql, para)
                await self.db.commit()
            except:
                # 发生错误时回滚
                await self.db.rollback()
        await cursor.close()
        await self.closedb()

    async def closedb(self):
        await self.db.close()

dbmanager = TickDataManager()
asyncio.run(dbmanager.createtable())
asyncio.run(dbmanager.csvinput(0))