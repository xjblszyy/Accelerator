import json
import time
from wxpy import *
from Accelerator.settings_config import WX_GROUP_NAME
from Accelerator.spiders import SpiderData


bot = Bot(cache_path=True, console_qr=True)

my_grop = bot.groups().search(WX_GROUP_NAME)

if my_grop != []:
    my_grop = my_grop[0]

    spider_data = SpiderData()
    msg = spider_data.get_data()
    for item in msg:
        title = "商品:{0}({1})".format(item.get("title"), item.get("price"))
        my_grop.send(title)
        url = "购买链接:{0}".format(item.get("srcurl"))
        my_grop.send(url)
        content = "商品介绍:{0}".format(item.get("content"))
        my_grop.send(content)
        my_grop.send("****************************")
        time.sleep(15)

else:
    raise ("找不到微信群")

