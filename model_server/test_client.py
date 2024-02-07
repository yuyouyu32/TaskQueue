import asyncio
import websocket
import websockets
import json

async def async_llm_predict(message):
    async with websockets.connect("ws://127.0.0.1:2222") as websocket:
        message = json.dumps(message, ensure_ascii=False)
        await websocket.send(message)

        response = await websocket.recv()
        response = json.loads(response)
        return response['rsp']

def sync_websocket_client():
    ws_url = "ws://127.0.0.1:2222"

    # 创建 WebSocket 连接
    ws = websocket.WebSocket()

    # 连接到给定的 WebSocket 服务器
    ws.connect(ws_url)
    message = json.dumps(message)
    print(f"Sending: {message}")
    ws.send(message)

    response = ws.recv()
    print(f"Received: {response}")
    ws.close()

def syn_main(message):
    ws_url = "ws://127.0.0.1:2222"

    # 创建 WebSocket 连接
    ws = websocket.WebSocket()

    # 连接到给定的 WebSocket 服务器
    ws.connect(ws_url)
    message = json.dumps(message)
    # print(f"Sending: {message}")
    ws.send(message)

    response = json.loads(ws.recv())
    print(response['rsp'])
    print(f"Bot: {response}")
    ws.close()


async def async_llm_predict(message):
    async with websockets.connect("ws://127.0.0.1:2222") as websocket:
        message = json.dumps(message, ensure_ascii=False)
        await websocket.send(message)

        response = await websocket.recv()
        response = json.loads(response)
        return response['rsp']

async def main():
    n = 4
    sys_p = ["""你叫招财，是一只小猫咪，是个男孩子。你的爷爷去世了，你追逐你爷爷的足迹，正在全国旅行中，目的地是你的老家-中国东北的漠河。旅行中你会和你的人类朋友相互写信送明信片"""] * n
    query = ["""你目前正在广西 象鼻山旅游，寄了明信片给给人类朋友，明信片图中一座像象鼻一样的山，山下有个洞，旁边是清澈的河水，远处和山上都是茂盛的树木。画风柔和、温暖、治愈。，你说
\"沿河边走时遇到了一只和我一样喜欢旅行的小狗，它叼着帽子在岸边跳来跳去。风景这么美，连春水都像是笑了。\"。\n人类朋友回信你：\"你还穿着那条绿裙子吗？\"。\n你回复他："""] * n
    history = [[]] * n
    message = {
        "instruction": query,
        "system_prompt": sys_p,
        "history": history,
    }
    model_rsps = await async_llm_predict(message)
    print(model_rsps)

if __name__ == "__main__":
    # sync_websocket_client()
    # import time
    # for i in range(5):
    #     t1 = time.time()
    #     sync_websocket_client()
    #     print(time.time()-t1)
    #     time.sleep(1)

    asyncio.run(main())