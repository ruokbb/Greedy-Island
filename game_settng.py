import redis
import const
import random

def reput_cardpool():
    conn = redis.Redis(host=const.HOST, port=const.PORT, password=const.PASSWORD, db=13)
    card_id = [i for i in range(const.CARD_POOL_NUMBERS)]

    for i in card_id:
        conn.hset('card_pool', i, i + 1)
    conn.close()
    print('完成')

def set_LK():
    a = [1,2,3,4]
    LK = random.choice(a)
    conn = redis.Redis(host=const.HOST, port=const.PORT, password=const.PASSWORD, db=13)
    conn.set('const:LN',LK)
    conn.close()

#可改进，判断是否存在即可
def set_draw_card_tag():
    conn = redis.Redis(host=const.HOST, port=const.PORT, password=const.PASSWORD, db=13)
    all_player_id = conn.hkeys('draw_card_tag')
    for i in all_player_id:
        conn.hset('draw_card_tag',i,0)
    conn.close()

if __name__ == '__main__':
    reput_cardpool()