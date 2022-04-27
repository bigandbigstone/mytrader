# 未实现
from pygments import highlight
import pymysql

class OrderList(object):
    pos = 0
    capital = 0

    def __init__(self):
        # 用于存储每轮tick的订单新增调整值，买单为正，卖单为负
        self.orderdic = dict()
        pass
    
    # 每轮tick需要调用一次清空
    def orderaddclear(self):
        self.orderdic.clear()

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
            LID INT PRIMARY KEY AUTO_INCREMENT,
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
            SID INT PRIMARY KEY AUTO_INCREMENT,
            Type INT,
            Price FLOAT,
            Volume INT)
        """
        cursor.execute(sql)

        cursor.close()
        self.closedb()
        
    def addorder(self, offset: str, type: int, price: float, volume: int, stop: bool):
        # 向策略订单队列中增加订单，包括限价订单和停止单
        # type 0为买单，1为卖单
        if type == 0:
            height = self.orderdic.get(price, 10)
        else:
            height = self.orderdic.get(-1 * price, 10)
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

    def orderinput(self,action: str, type: str, price: float, vol: int):
        # 要接入模拟交易指令，主要是针对的限价订单
        # 新增订单用于订单创建时的高度修正
        # 订单取消，高度降低
        # 订单撮合，高度降低
        # 高度降低到0，即为成交
        if action == "新增":
            if type == "买单":
                self.orderdic[price] = vol
            else:
                self.orderdic[-1 * price] = vol
        elif action == "撮合" or action == "取消":
            self.connectdb()
            cursor = self.db.cursor()

            sql = '''
            SELECT LID, Height, Volume FROM limitlist
                WHERE Type = %s AND Price = %s
            '''
            if type == "买单":
                cursor.execute(sql, [0, price])
            else:
                cursor.execute(sql, [1, price])

            orders = cursor.fetchall()
            for order in orders:
                LID, Height, OrderVol = order[0], order[1], order[2]
                Height -= vol
                if Height > 0:
                    # 更新高度
                    sql = '''
                    UPDATE limitlist SET Height = %s WHERE LID = %s
                    '''
                    try:
                        cursor.execute(sql,[Height, LID])
                    except:
                        self.db.rollback()
                else:
                    sql = '''
                    DELETE FROM limitlist
                    WHERE LID = %s
                    '''
                    try:
                        cursor.execute(sql, LID)
                        # 成交部分已经实现
                        if type == "买单":
                            self.pos += OrderVol
                            self.capital -= OrderVol * price
                        else:
                            self.pos -= OrderVol
                            self.capital += OrderVol * price
                    except:
                        self.db.rollback()

            self.db.commit()
            cursor.close()
            self.closedb()

    # 阻止单处理
    def stoporders(self):
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

olist = OrderList()