import json
import time
from wxpy import *
from Accelerator.settings_config import WX_GROUP_NAME
from Accelerator.spiders import SpiderData


bot = Bot(cache_path=True)

my_grop = bot.groups().search(WX_GROUP_NAME)

if my_grop != []:
    my_grop = my_grop[0]

    spider_data = SpiderData()
    msg = spider_data.get_data()
    for item in msg:
        my_grop.send(item)
        my_grop.send("****分隔线****")
        time.sleep(30)

else:
    raise ("找不到微信群")

