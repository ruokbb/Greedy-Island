import redis
import const
from nonebot import CommandSession
async def make_text(text):
    """

    :param text: 可迭代的协议，每一个相当于一行
    :return: str
    """
    new_text = '——————————\n'

    for i in text:
        new_text = new_text+i+'\n'
    new_text += '——————————'
    return new_text


async def is_regist(player_id,session:CommandSession,name=None):
    """
    判断是否已经注册,没有注册就在下次调用时注册。使用三大功能时调用一次该函数，返回False
    则是未注册，第二次调用进行name字段设置实现注册
    :param name: 玩家名称
    :param player_id: qq号
    :param session:
    :return:
    """
    conn = redis.Redis(host=const.HOST, port=const.PORT, password=const.PASSWORD, db=13)

    if name is not None:
        #为玩家进行注册
        conn.sadd('player_info:regist',player_id)
        conn.hset('player_info:name',player_id,name)
        await session.send('注册成功')

    if conn.sismember('player_info:regist',player_id):
        return
    else:
        message = ['输入用户名完成注册']
        message = await make_text(message)
        session.pause(message)
