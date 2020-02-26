from nonebot import on_command,CommandSession
from .data_source import draw_card
from data_source import make_text
from data_source import is_regist

@on_command('ck',aliases=('抽卡','我的回合'))
async def drawCard(session:CommandSession):

    #判断是否已注册
    player_id = session.ctx['user_id']
    name = session.state.get('name')
    await is_regist(player_id, session,name)

    number = session.get('number')
    my_card_id = await draw_card(k=number,player_id=player_id)
    if len(my_card_id)==0:
        return await session.send('抽卡失败，您已抽过卡')
    a = ['抽卡结果如下：']
    id_text = ''
    for i in my_card_id:
        if i>500:
            i = str(i)+ '（已达上限）'
        id_text+= str(i) +'  '
    a.append(id_text)
    message = await make_text(a)
    await session.send(message)

@drawCard.args_parser
async def _(session:CommandSession):
    message = session.current_arg_text.strip()
    number=5
    session.current_key = 'name'
    if session.is_first_run:
        if not message:
            number=5
        else:
            try:
                number = int(message)
                if number<=0 or number>5:
                    number = 5
            except ValueError:
                await session.send('参数错误，按照最大值5进行抽卡')
                number=5
        session.current_key='number'
    if session.current_key=='number':
        session.state['number'] = number
    else:
        session.state['name'] = message











