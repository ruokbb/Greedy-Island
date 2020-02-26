from nonebot import permission,on_command,CommandSession
import redis
import const
import json
from nonebot.helpers import render_expression

@on_command('connect',aliases=('连接','连接基金会'))
async def connect(session:CommandSession):
    #判断是否已经连接
    conn = redis.Redis(host=const.HOST,port=const.PORT,password=const.PASSWORD,db=13)
    number = session.ctx['user_id']
    info = conn.hget('num_to_info',number)
    hint = await const.make_text(['基金会将于整点清空连接数据，及时退出，重新连接'
                                     ])
    if not conn.sadd('connect_list',number) and info:
        message = await const.make_text(['已经处于连接状态'])
        await session.send(message)
        await session.send(hint)
        return

    #连接成功,已注册
    if info:
        error_str = session.state.get('error')
        if error_str:
            message = await const.make_text(['连接失败'
                                             ,'原因：携带多余参数如下'
                                             ,error_str
                                             ,'行为混乱，理智损失'
                                             ])
            await session.send(message)
            return
        message = '--成功接入基金会内部网络--\n'
        await session.send(message)
        await session.send(hint)
    else:
        #没有注册
        tick = await const.make_text(['————警告————'
                                      ,'发送昵称将会进行注册'
                                      ,'恐惧将会不止于克苏鲁'])

        # 设置数据库账号名字属性的对应
        new_name = session.get('name',prompt=tick)
        info = {
            'name':new_name,
            'nous':100,
            'knowledge':30,
            'sp':50
        }
        info = json.dumps(info)
        conn.hset('num_to_info',number,info)
        message = await const.make_text(['———注册成功———',
                                         '——基金会欢迎您——'])
        await session.send(message)
        await session.send(hint)
        conn.close()



@connect.args_parser
async def _(session:CommandSession):
    message = session.current_arg_text.strip()

    #第一次运行，携带多余参数，行为混乱
    if session.is_first_run:
        if message:
            session.state['error'] = message
        return

    #注册账号，没有输入有效姓名字符
    if not message:
        session.pause('—请输入正确名称—')

    session.state[session.current_key] = message

@on_command('info',aliases=('个人资料','个人'))
async def info(session:CommandSession):
    conn = redis.Redis(host=const.HOST, port=const.PORT, password=const.PASSWORD, db=13)

    #查看是否连接，如果不是
    number = session.ctx['user_id']
    is_connect = await const.is_connect(number,conn)
    if not is_connect:
        await session.send(render_expression(const.EXPR_DONT_UNDERSTAND))
        return

    info = conn.hget('num_to_info', number)
    info_dic = json.loads(info)

    message = await const.make_text(['代号：'+str(info_dic['name'])
                                     ,'理智：'+str(info_dic['nous'])
                                     ,'学识：'+str(info_dic['knowledge'])
                                     ,'超然值：'+str(info_dic['sp'])
                                     ])
    await session.send(message)