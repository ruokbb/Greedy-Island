from nonebot import CommandSession,on_command
from .const import REQUESTS
import random
from data_source import make_text
from .data_source import yes_or_no,is_join_game,have_chosen

@on_command('minority',aliases=('少数决'))
async def minority(session:CommandSession):
    game_name = '少数决'
    id = session.ctx['user_id']
    #判断是否参加游戏
    is_join = await is_join_game(game_name,id)
    if not is_join:
        await session.send(await make_text(['未参加游戏']))
        session.switch('游戏')
        return

    #判断该次是否已经选择，等待结果
    is_chosen,result = await have_chosen(game_name,id)
    if is_chosen:
        return await session.send(await make_text(['已进行选择','当前选择为:'+result]))

    request = random.choice(REQUESTS)
    prompt = await make_text([request,'回答是/否（默认否）'])
    choise = session.get('choise',prompt=prompt)

    id = session.ctx['user_id']
    if choise =='是':
        await yes_or_no(True,game_name,id)
    else:
        await yes_or_no(False,game_name,id)


@minority.args_parser
async def _(session:CommandSession):
    message = session.current_arg_text.strip()
    if session.is_first_run:
        return
    if message == '是':
        pass
    else:
        message ='否'
    session.state[session.current_key] = message