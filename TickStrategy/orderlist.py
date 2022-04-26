# 未实现
from pygments import highlight
import pymysql

class OrderList(object):
    def __init__(self):
        pass

    def connectdb(self):
        self.db = pymysql.connect(host='localhost',
                     user='root',
                     password='songlinshuo',
                     database='traderdb')

    def closedb(self):
        self.db.close()

    def createtable(self):
        self.connectdb()
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE IF EXISTS limitlist")
        # Type 0为限价买单，1为卖单
        # Height为成绩高度，订单创建时赋值为历史订单高度加新增订单大小
        # 成交订单回取消订单，降低高度，降低高度到0全部成交
        sql = """
        CREATE TABLE limitlist (
            Type INT,
            Price FLOAT,
            Volume INT,
            Height FLOAT)
        """
        cursor.execute(sql)

        cursor.execute("DROP TABLE IF EXISTS stoplist")
        # 停止单中没有高低，按市价单成交方式成交
        sql = """
        CREATE TABLE stoplist (
            Type INT,
            Price FLOAT,
            Volume INT)
        """
        cursor.execute(sql)

        cursor.close()
        self.closedb()
        
    def addorder(self, offset: str, type: str, price: float, volume: int, stop: bool):
        # 向策略订单队列中增加订单，包括限价订单和停止单
        # type 0为买单，1为卖单
        height = 0.0
        # 未实现: 应还有当前tick到下一tick的新增订单指令，当限价订单价格在其中时要增加高度修正
        self.connectdb()
        cursor = self.db.cursor()
        if stop:
            # 若是阻止单
            sql = """
            INSERT INTO stoplist(
                Type,
                Price,
                Volume)
            VALUES (
                %s, %s, %s
            )
            """
            try:
                # 执行sql语句
                cursor.execute(sql, [type, price, volume])
            except:
                # 发生错误时回滚
                self.db.rollback()
        else:
            # 若是限价单
            sql = """
            INSERT INTO limitlist(
                Type,
                Price,
                Volume,
                Height)
            VALUES (
                %s, %s, %s, %s
            )
            """
            try:
                # 执行sql语句
                cursor.execute(sql, [type, price, volume, height])
            except:
                # 发生错误时回滚
                self.db.rollback()

        self.db.commit()
        cursor.close()
        self.closedb()

    def orderfinishedornot(self):
        # 要接入模拟交易指令
        # 新增订单用于订单创建时的高度修正
        # 订单取消，高度降低
        # 订单撮合，高度降低
        # 高度降低到0，即为成交
        pass

    def delall(self):
        # 清空未成交订单包括限价和停止单
        self.connectdb()
        cursor = self.db.cursor()
        
        # 截断清空，truncate table tbl_name
        cursor.execute("TRUNCATE TABLE limitlist")
        cursor.execute("TRUNCATE TABLE stoplist")

        cursor.close()
        self.closedb()