from single_instance import conn

async def yes_or_no(join:bool,game_name,id):
    """
    保存两个选择的玩家ID,并记录该玩家已选择
    :param join: 选择YES为True
    :param game_name: 游戏名称，在这里是少数决
    :param id:
    """
    if join:
        conn.lpush(game_name+':Yes',id)
        conn.hset(game_name + ':have_chosen', id,'Yes')
    else:
        conn.lpush(game_name+':No',id)
        conn.hset(game_name + ':have_chosen', id, 'No')

async def is_join_game(game_name,id):
    """
    判断当前用户ID是否参加了游戏
    :param id:
    """
    users_list = conn.lrange(game_name+':users',0,-1)
    if not users_list:
        # 不为空
        if id in users_list:
            return True
    return False

async def have_chosen(game_name,id):
    users = conn.hkeys(game_name+':have_chosen')
    if id in users:
        result = conn.hget(game_name+':have_chosen',id)
        return True, result
    else:
        return False, ''