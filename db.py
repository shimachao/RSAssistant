# -*-coding:UTF-8-*-

import sqlite3


class DB:

    def __init__(self, database):
        self.conn = sqlite3.connect(database=database)
        self.cursor = self.conn.cursor()

    def select_today_record(self):
        """ 查询今天是否有记录
        :return: 如果成功，返回元组，失败返回None
        """
        sql = "select * from sign_records where date = date()"
        self.cursor.execute(sql)
        r = self.cursor.fetchone()
        return r

    def insert(self, time, gold):

        sql = "insert into sign_records (date, time, gold) VALUES(date(), '%s', %d)" % (time, gold)
        self.cursor.execute(sql)
        self.conn.commit()

    def select_all(self):
        """
        :return: 所有记录组成的list，每个list的元素对应一条记录
        """
        sql = "select * from sign_records"
        self.cursor.execute(sql)

        r = self.cursor.fetchall()

        return r

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.conn:
            self.conn.close()
            self.conn = None


if __name__ == '__main__':
    db = DB(database='sign_records.db')

    r = db.select_today_record()
    print(r)
    print(type(r))

    db.close()
