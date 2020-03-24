
from single_instance import conn

async def get_game(next=False):
    """
    获取当前游戏名字，或者下次游戏信息
    :param next: 下次游戏信息
    :return:
    """
    if next:
        info = '下轮游戏：抢椅子，时间：2020.4.17'
        return info
    else:
        name = conn.get('game:name')
        return str(name)

async def join_game(game_name,id):
    """
    参加游戏，将用户id保存到game_name:users
    param name:
    :param id:
    """
    conn.lpush(game_name+':users',id)