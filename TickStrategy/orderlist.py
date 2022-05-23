# orderlist用于维护策略订单队列
# 作者 SongLinshuo
from pygments import highlight
import pymysql
# 完全实现，OK！
class OrderList(object):
    '''pos = 0
    capital = 0
    posprice = 474.0
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='songlinshuo',
                     database='traderdb')'''

    def __init__(self):
        # 用于存储每轮tick的订单新增调整值，买单为正，卖单为负
        self.orderdic = dict()
        # 系统启动修正订单
        self.add_proportion = 0.5
        # 交易手续费0.006%
        self.Service_Charge = 1 + 0.00006
        self.pos = 0
        self.capital = 0
        self.posprice = 474.0
        self.sqls = list()
        self.db = pymysql.connect(host='localhost',
                        user='root',
                        password='songlinshuo',
                        database='traderdb')
        self.delall()
        
    # 每轮tick需要调用一次清空
    def orderaddclear(self):
        self.orderdic.clear()

    '''def connectdb(self):
        self.db = pymysql.connect(host='localhost',
                     user='root',
                     password='songlinshuo',
                     database='traderdb')'''

    '''def closedb(self):
        self.db.close()'''

    def createtable(self):
        # self.connectdb()
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE IF EXISTS limitlist")
        # Offset 0为开仓，1位平仓
        # Type 0为限价买单，1为卖单
        # Height为成绩高度，订单创建时赋值为历史订单高度加新增订单大小
        # 成交订单回取消订单，降低高度，降低高度到0全部成交
        sql = """
        CREATE TABLE limitlist (
            LID INT PRIMARY KEY AUTO_INCREMENT,
            Offset INT,
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
            Offset INT,
            Type INT,
            Price FLOAT,
            Volume INT)
        """
        cursor.execute(sql)

        cursor.close()
        # self.closedb()
        
    def addorder(self, offset: int, type: int, price: float, volume: int, stop: bool, preheight: float):
        # 向策略订单队列中增加订单，包括限价订单和停止单，preheight为当前tick（或pretick）的历史积累订单高度
        # type 0为买单，1为卖单
        if type == 0:
            height = self.orderdic.get(price, 0) * self.add_proportion + volume + preheight
        else:
            height = self.orderdic.get(-1 * price, 0) * self.add_proportion + volume + preheight
        # 未实现: 应还有当前tick到下一tick的新增订单指令，当限价订单价格在其中时要增加高度修正
        # self.connectdb()
        cursor = self.db.cursor()
        if stop:
            # 若是阻止单
            sql = """
            INSERT INTO stoplist(
                Offset,
                Type,
                Price,
                Volume)
            VALUES (
                %s, %s, %s, %s
            )
            """
            try:
                # 执行sql语句
                cursor.execute(sql, [offset ,type, price, volume])
            except:
                # 发生错误时回滚
                self.db.rollback()
        else:
            # 若是限价单
            sql = """
            INSERT INTO limitlist(
                Offset,
                Type,
                Price,
                Volume,
                Height)
            VALUES (
                %s, %s, %s, %s, %s
            )
            """
            try:
                # 执行sql语句
                cursor.execute(sql, [offset ,type, price, volume, height])
            except:
                # 发生错误时回滚
                self.db.rollback()

        self.db.commit()
        cursor.close()
        # self.closedb()

    def orderinput(self, orderflow):
        # 要接入模拟交易指令，主要是针对的限价订单
        # 新增订单用于订单创建时的高度修正
        # 订单取消，高度降低
        # 订单撮合，高度降低
        # 高度降低到0，即为成交
        for order in orderflow:
            action, type, price, vol = order[0], order[1], order[2], order[3]
            if action == "新增":
                if type == "买单":
                    self.orderdic[price] = vol
                else:
                    self.orderdic[-1 * price] = vol
            elif action == "撮合" or action == "取消":
                # self.connectdb()
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
                                self.capital -= OrderVol * price * self.Service_Charge
                                print("买入" + str(price) + " " + str(OrderVol))
                            else:
                                self.pos -= OrderVol
                                self.capital += OrderVol * price * self.Service_Charge
                                print("卖出" + str(price) + " " + str(OrderVol))

                            # 更新成交价格
                            self.posprice = price
                        except:
                            self.db.rollback()

                self.db.commit()
                cursor.close()
                # self.closedb()

    # 阻止单处理, 需要传入市价和市价对应高度nowheight, 针对的是sell和cover订单
    # 故pos >= 0时，买入停止单cover视为无效；当pos <= 0时，卖出停止单sell视为无效订单
    def stoporders(self, price: float):
        # self.connectdb()
        cursor = self.db.cursor()

        # 买单停止单处理，市价高于等于停止单定价时买入 ×
        # 不应该进行买入，而应该转为限价单买入 ×
        # 原来的应该还是对的，就应该市价买入，但应该考虑pos，pos >= 0 视为无效订单
        sql = '''
        SELECT SID, Volume FROM stoplist
        WHERE Type = %s AND %s >= Price
        '''
        cursor.execute(sql, [0, price])
        orders = cursor.fetchall()
        for order in orders:
            SID, OrderVol = order[0], order[1]
            sql = '''
            DELETE FROM stoplist
            WHERE SID = %s
            '''
            if self.pos >= 0:
                pass
            else:
                try:
                    cursor.execute(sql, SID)
                    self.pos += OrderVol
                    self.capital -= OrderVol * price * self.Service_Charge
                    # 更新成交价格
                    self.posprice = price
                    print("买入" + str(price) + " " + str(OrderVol))
                    # 失效
                    # self.orderlist.addorder("待定", 0, price, OrderVol, False, nowheight)
                except:
                    self.db.rollback()
        
        # 卖单停止单处理，市价低于等于停止单定价时卖出 ×
        # 不应该直接进行卖出，而应该转为限价单卖出 √
        # 原来的应该还是对的，就应该市价卖出，但应该考虑pos，pos <= 0 视为无效订单
        sql = '''
        SELECT SID, Volume FROM stoplist
        WHERE Type = %s AND %s <= Price
        '''
        cursor.execute(sql, [1, price])
        orders = cursor.fetchall()
        for order in orders:
            SID, OrderVol = order[0], order[1]
            sql = '''
            DELETE FROM stoplist
            WHERE SID = %s
            '''
            if self.pos <= 0:
                pass
            else:
                try:
                    cursor.execute(sql, SID)
                    self.pos -= OrderVol
                    self.capital += OrderVol * price * self.Service_Charge
                    # 更新成交价格
                    self.posprice = price
                    print("卖出" + str(price) + " " + str(OrderVol))
                    # 失效
                    # self.orderlist.addorder("待定", 1, price, OrderVol, False, nowheight)
                except:
                    self.db.rollback()

        self.db.commit()
        cursor.close()
        # self.closedb()

    def delall(self):
        # 清空未成交订单包括限价和停止单
        # self.connectdb()
        cursor = self.db.cursor()
        
        # 清空表项
        cursor.execute("DELETE FROM limitlist")
        cursor.execute("DELETE FROM stoplist")

        cursor.close()
        # self.closedb()

    def getorderlist(self) -> list:
        orderl = list()
        cursor = self.db.cursor()

        sql = '''
        SELECT LID, Offset, Type, Price, Volume, Height FROM limitlist
        '''
        cursor.execute(sql)
        orders = cursor.fetchall()
        orderl.extend(orders)

        """
        # " "表空
        sql = '''
        SELECT SID, Offset, Type, Price, Volume, ' ' FROM stoplist
        '''
        cursor.execute(sql)
        orders = cursor.fetchall()
        orderl.extend(orders)
        """
        cursor.close()
        return orderl