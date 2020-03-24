from nonebot import on_command,CommandSession
from data_source import is_regist
from .data_source import get_game,join_game
from data_source import make_text
from const import GAME_KEY

@on_command('game',aliases=('游戏',))
async def game_list(session:CommandSession):
    # 判断是否已注册
    player_id = session.ctx['user_id']
    name = session.state.get('name')
    await is_regist(player_id, session, name)

    #获取当前游戏
    game_name = await get_game()
    message = ['当前游戏为：'+game_name,'是否参加游戏(是/否)']
    message = await make_text(message)
    await session.send(message)
    join = session.get('join')

    if join =='是':
        #参加游戏，切换会话
        await join_game(game_name,session.ctx['user_id'])
        await session.send(await make_text(['游戏参加成功']))
        session.switch(game_name)
    else:
        #提示下次游戏时间
        info = await get_game(True)
        await session.send(await make_text(['游戏参加失败',info]))


@game_list.args_parser
async def _(session:CommandSession):
    message = session.current_arg_text.strip()
    if session.current_key =='join':
        if message == '是':
            pass
        else:
            message = '否'
    session.state[session.current_key] = message


