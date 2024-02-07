from HomeCatServer import *
import random

def unit_test():
    size = asyncio.run(get_queue_size("user_msg"))
    print('size', size)
    result = asyncio.run(get_task_from_queue("user_msg"))
    task_id = result['task_id']
    openid = result['data']['openid']
    random_rsp = ['是吧', '还得是志凯!', '志凯还是🐂啊~', '要允许自己开心更久一点-kuma']
    rsp_data = \
    {
        "sender": "llm",
        "openid": openid,
        "msg": random_rsp[random.randint(0, len(random_rsp)-1)],
        "send_sid": 0,
        "resp_sid": 1,
    }
    rsp_data = json.dumps(rsp_data)
    rsp_res = asyncio.run(put_rsp_into_queue(openid, rsp_data))
    print(rsp_res)
    asyncio.run(delete_task_from_queue("user_msg", task_id))

unit_test()
