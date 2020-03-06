from nonebot import on_command,CommandSession
from data_source import is_regist
from .data_source import show_bag

@on_command('卡包',aliases=('背包','bb'))
async def bag_show(session:CommandSession):
    #判断是否已注册
    player_id = session.ctx['user_id']
    name = session.state.get('name')
    await is_regist(player_id, session,name)

    message = await show_bag(player_id)
    await session.send(message)

@bag_show.args_parser
async def _(session:CommandSession):
    message = session.current_arg_text.strip()
    session.current_key = 'name'
    if session.is_first_run:
        session.current_key = 'show'

    if session.current_key == 'name':
        session.state['name'] = message