import websockets
import re
import aiohttp
from aiohttp.formdata import FormData
import asyncio
import json
import time


from merge import *
from QueueManager import TaskQueueManager, MsgQueueManager
from config import *

async def async_llm_predict(message):
    timeout = 60
    async with websockets.connect("ws://127.0.0.1:2222", ping_timeout=timeout, close_timeout=timeout) as websocket:
        message = json.dumps(message, ensure_ascii=False)
        await websocket.send(message)

        response = await websocket.recv()
        response = json.loads(response)
        return response['rsp']

async def process_messages():
    access_token = ''
    task_queue = TaskQueueManager(PROJECT, TOKEN, TTR)
    msg_queue = MsgQueueManager(APPID, SECRET, ENV_ID)  
    while True:
        try:
            size = await task_queue.get_queue_size("user_msg")
            if size > 0:
                message, count, rsps, task_ids, next_infos, querys, errs = await task_queue.pull_task_from_queue(MaxBatchSize)
                if count == 0: continue
                print("predict begin...")
                model_rsps = await async_llm_predict(message)
                print("predict end...")
                for index in range(count):
                    print("process {} ...".format(index))
                    query = querys[index]
                    model_rsp = re.sub(Pattern, '', model_rsps[index])
                    merged_rsp = merge(querys[index], model_rsp, next_infos[index][0], next_infos[index][1])
                    rsps[index]['msg'] = merged_rsp
                    rsp = json.dumps(rsps[index], ensure_ascii=False)
                    print("await upload_file")
                    async with aiohttp.ClientSession() as session:
                        await msg_queue.upload_file(session, access_token=access_token, msg_folder='msg_v2', open_id=rsps[index]['openid'], file_name=f"{rsps[index]['resp_sid']}.txt",rsp=rsp)
                    print("await delete_task_from_queue")
                    await task_queue.delete_task_from_queue("user_msg", task_ids[index])
                    print('response:', rsps[index]['msg'])
                    print(f"task_id: {task_ids[index]}, openid: {rsps[index]['openid']} Done.")
                    print('ERROR INFO', errs)
                    with open('logs/conversation.txt', 'a') as f:
                        f.write('========\n')
                        f.write(f'task_id:{task_ids[index]}\n')
                        f.write(f'query:{query}\n')
                        f.write(f'rsp:{model_rsp}\n')
                        f.write(f'merged:{merged_rsp}\n')
            await asyncio.sleep(1)  # Sleep for 1 second before next iteration
        except Exception as e:
            print(f"Time {time.time()}, {time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}, An error occurred: {e}")
            await asyncio.sleep(3)
    
if __name__ == '__main__':
    asyncio.run(process_messages())
