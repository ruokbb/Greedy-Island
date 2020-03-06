from single_instance import conn
import json
from data_source import make_text

async def show_bag(player_id):
    data = conn.hget('player_info:bag',player_id)
    data = json.loads(data)
    data = sorted(data.items(),key=lambda x:int(x[0]))
    ctx = []
    for k,v in data:
        description = conn.hget('card_description',k)
        num = v

        if not description:
            description = '测试描述'

        message = '卡片序号:'+str(k) + '(' +str(num) + '): ' + description
        ctx.append(message)

    return await make_text(ctx)

