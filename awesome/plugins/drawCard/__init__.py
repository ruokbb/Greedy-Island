from nonebot import on_command,CommandSession
from .data_source import draw_card
from data_source import make_text
from data_source import is_regist
from const import CARD_POOL_NUMBERS

@on_command('ck',aliases=('抽卡','我的回合'))
async def drawCard(session:CommandSession):

    #判断是否已注册
    player_id = session.ctx['user_id']
    name = session.state.get('name')
    await is_regist(player_id, session,name)

    number = session.get('number')
    my_card_id = await draw_card(player_id=player_id)
    if len(my_card_id)==0:
        return await session.send('抽卡失败，您已抽过卡')
    a = ['抽卡结果如下：']
    id_text = ''
    for i in my_card_id:
        if i>CARD_POOL_NUMBERS:
            i = str(i)+ '（抽卡失败，已达上限）'
        id_text+= str(i) +'  '
    a.append(id_text)
    message = await make_text(a)
    await session.send(message)

@drawCard.args_parser
async def _(session:CommandSession):
    message = session.current_arg_text.strip()
    session.current_key = 'name'
    if session.is_first_run:
        session.current_key='number'

    if session.current_key=='number':
        pass
    else:
        session.state['name'] = message











