# coding=utf-8
import re
import requests
from .settings_config import REQUEST_URL, USER_AGENT
from .deal_mysql_data import MysqlClient
from .settings_config import HOST, USER, PASSWORD, DB, PORT


global sn_flag


class SpiderData(object):
    def __init__(self, url=REQUEST_URL, user_agent=USER_AGENT):
        self.url = url
        self.user_agent = user_agent
        self.finally_data_list = []

    def get_data(self):
        """获取数据"""
        headers = {"user-agent": self.user_agent}
        response = requests.get(url=self.url, headers=headers).json()
        re_data = response.get("nlist")
        if re_data:
            re_data = self.deal_data(re_data)
            return self.save_data(re_data)
        else:
            return None

    def deal_data(self, data_list):
        """处理爬取的数据，并重新筛选需要的数据"""
        for item in data_list:
            re_dict = {}
            re_dict["price"] = item.get("priceinfo")
            re_dict["title"] = item.get("title")
            re_dict["srcurl"] = item.get("srcurl")
            re_dict["sn"] = item.get("newsid")
            re_dict["content"] = self.deal_content_htlm(item.get("content")) if item.get("content") else None
            self.finally_data_list.append(re_dict)
        return self.finally_data_list

    def deal_content_htlm(self, content):
        """将爬取的html文本做正则去除标签"""
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', content)
        return dd

    def save_data(self, data_list):
        """保存数据"""
        mysql_client = MysqlClient(HOST, USER, PASSWORD, DB, PORT)
        cursor = mysql_client.cursor()
        db = mysql_client.db_ins()
        re_data_list = []
        for data in data_list:
            sn = int(data.get("sn"))
            sql = "select * from goods where sn={0}".format(sn)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result == ():
                re_data_list.append(data)
                sql = "insert into `goods` (title, price, srcurl, sn, content) values('{0}','{1}','{2}','{3}','{4}')".format(
                    data.get("title"), data.get("price"), data.get("srcurl"), int(data.get("sn")), data.get("content")
                )
                try:
                    cursor.execute(sql)
                    # 提交
                    db.commit()
                except Exception as e:
                    # 错误回滚
                    db.rollback()
            else:
                break
        cursor.close()
        return re_data_list


if __name__ == '__main__':
    getData = SpiderData(REQUEST_URL, USER_AGENT)
    re_data = getData.get_data()
    if re_data:
        print(getData.deal_data(re_data))