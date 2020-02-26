from nonebot import on_command,CommandSession,on_natural_language,IntentCommand
import redis
import nonebot
from nonebot.helpers import render_expression as expr

async def joke_get():
    conn = redis.Redis(host='139.199.0.99',port=6379,password='SHIqixin5682318!')
    str_joke = conn.rpop('joke')
    conn.close()
    return str(str_joke,encoding='utf-8')

@on_command('joke',aliases=('笑话','冷笑话'))
async def joke(session:CommandSession):
    str_joke = await joke_get()
    header = '王兄，今天也要开心哦~'
    other = '我只说笑话给王兄听，哼~'
    if session.ctx['user_id']==420484153:
        await session.send(header)
        await session.send(str_joke)
    else:
        await session.send(other)


@nonebot.scheduler.scheduled_job('cron',hour=12)
async def day_time():
    bot =nonebot.get_bot()
    message = await joke_get()
    try:
        await bot.send_private_msg(user_id=916567875, message='王妃今天也要开心哦~~')
        await bot.send_private_msg(user_id=916567875,message=message)
    except:
        pass

