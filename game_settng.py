import redis
import const
import random
from single_instance import conn

def reput_cardpool():
    card_id = [i for i in range(const.CARD_POOL_NUMBERS)]
    for i in card_id:
        conn.hset('card_pool', i, i + 1)
    print('完成')

def set_LK():
    a = [1,2,3,4]
    LK = random.choice(a)
    conn.set('const:LN',LK)

#可改进，判断是否存在即可
def set_draw_card_tag():
    all_player_id = conn.hkeys('draw_card_tag')
    for i in all_player_id:
        conn.hset('draw_card_tag',i,0)

if __name__ == '__main__':
    reput_cardpool()