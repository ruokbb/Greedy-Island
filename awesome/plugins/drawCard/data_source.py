import random
import redis
import const
import json

async def draw_card(k,player_id):
    """
    抽过卡了返回空列表
    :param k: 抽卡的数量
    :param player_id: 用户id qq号
    """
    conn = redis.Redis(host=const.HOST, port=const.PORT, password=const.PASSWORD, db=13)
    #判断是否抽过卡
    player_info = conn.hget('draw_card_tag',player_id)
    if player_info:
        conn.close()
        return []


    #提取幸运数字
    lucky_number = conn.get('const:LN')
    if lucky_number==k:
        WEIGHTS = [i + 1 for i in range(k*100)]
        card_id = [i for i in range(k*100)]
    else:
        WEIGHTS = [i + 1 for i in range(const.CARD_POOL_NUMBERS)]
        card_id = [i for i in range(const.CARD_POOL_NUMBERS)]

    #抽卡，当抽到的某张卡超出上线时提示玩家抽取失败
    my_card_id = random.choices(card_id, k=k, weights=WEIGHTS)
    my_card = []
    for i in my_card_id:
        result = await card_pool(i,conn)
        if result:
            my_card.append(i)
        else:
            my_card.append(i+const.CARD_POOL_NUMBERS*2)

    #将抽到的卡添加到用户背包
    await save_card(my_card,conn,player_id)
    conn.close()
    return my_card


async def card_pool(card_id,conn:redis.Redis):
    """
     判断卡池该卡是否抽满，抽满就抽卡失败
    :param card_id:
    :param conn:
    :return:
    """
    a = int(conn.hget('card_pool',card_id))
    if a <= 0:#抽满了
        return False
    else:
        conn.hset('card_pool',card_id,a-1)
        return True


async def save_card(card_list:list,conn:redis.Redis,player_id):
    """
    将抽到的卡添加到用户背包,redis hashmap
    :param player_id:
    :param card_list:
    :param conn:
    """
    card_dict = conn.hget('player_info:bag', player_id)
    if not card_dict:
        card_dict = {}
    else:
        card_dict = json.loads(card_dict)

    for card_id in card_list:
        if card_id>const.CARD_POOL_NUMBERS:
            continue
        else:
            num = card_dict.get(card_id,0)
            num +=1
            card_dict[card_id] = num
    card_dict_json = json.dumps(card_dict)
    conn.hset('player_info:bag',player_id,card_dict_json)
