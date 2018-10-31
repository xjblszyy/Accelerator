# coding=utf-8
import pymysql
from .settings_config import HOST, USER, PASSWORD, DB, PORT


class MysqlClient(object):
    def __init__(self, host, user, password, db, port):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db
        self.port = port
        self.db = pymysql.connect(host=self.host, user=self.user,
                             password=self.password, db=self.db_name, port=self.port)

    def db_ins(self):
        return self.db

    def cursor(self):
        cur = self.db.cursor()
        return cur

    def close(self):
        self.db.close()


if __name__ == '__main__':
    mysql_client = MysqlClient(HOST, USER, PASSWORD, DB, PORT)
    db = mysql_client.db_ins()
    cur = mysql_client.cursor()
    # sql = "select * from goods where sn=1234"
    sql = "insert into goods (title, price, srcurl, sn, content) values('title02', '250元', 'www.duote.com','1', 'very good')"
    try:
        cur.execute(sql)
        # 提交
        db.commit()
    except Exception as e:
        # 错误回滚
        db.rollback()
    finally:
        mysql_client.close()

