import requests
from nonebot import on_command,on_natural_language,CommandSession,NLPSession,IntentCommand
from aiocqhttp.message import escape
from nonebot.helpers import render_expression,context_id
import json

EXPR_DONT_UNDERSTAND=(
    '王兄，人家不懂啦~',
    '不听不听我不听，王兄饶了我把~~',
    '王兄不要~，我还小，什么都不懂~~',
    '王兄王兄，我想喝冰阔落~'
)

@on_command('tuling')
async def tuling(session:CommandSession):
    message = session.state.get('message')

    reply = await get_tuling_answer(session,message)

    if reply:
        await session.send(escape(reply))
    else:
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))



@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0,'tuling',args={'message':session.msg_text})

async def get_tuling_answer(session:CommandSession,message:str):
    if not message:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'


    data ={
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": message
            }
        },
        "userInfo": {
            "apiKey": "610a38d3c0ad4ad9ba0ad8386f8caa2e",
            "userId": context_id(session.ctx,use_hash=True)
        }
    }

    try:
        response = requests.post(url,data=json.dumps(data)).text
        response = json.loads(response)
        if response['results']:
            for i in response['results']:
                if i['resultType']=='text':
                    return i['values']['text']
    except BaseException :
        return None