from datetime import datetime
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import requests
import json
from nonebot import on_command

#发送天气预报 南宁青秀区，重庆南岸
@nonebot.scheduler.scheduled_job('cron',hour=8)
async def _():
    bot = nonebot.get_bot()
    data = await get_wheater('nanning')
    a = '王兄王兄，天气预报来啦，要注意提醒王妃哦~\n'
    data_str1 = '白天天气：'+data['text_day']+'\n'+'晚间天气：'+data['text_night']+'\n'
    data_str2 = '温度变化：'+data['low']+'~~'+data['high']
    temp =  a+data_str1+data_str2

    try:
        await bot.send_private_msg(user_id=420484153,message=temp)
    except CQHttpError:
        pass


async def get_wheater(location):
    API ='https://api.seniverse.com/v3/weather/daily.json'
    KEY = 'SnJ-tUrRw_brPJICS'
    UNIT = 'c'
    LANGUAGE = 'zh-Hans'
    days = 2
    data = {'key':KEY,'location':location,'language':LANGUAGE,'unit':UNIT,'days':days}
    result = requests.get(API,params=data,timeout=1)

    # 解析json
    data = json.loads(result.text)
    now_date_data = data['results'][0]['daily'][0] #今日天气数据，字典

    return now_date_data