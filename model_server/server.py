import websockets
import asyncio
from .model import Model
from .config import *
import json
import time


ALL_TIME = 0
Process_Count = 0
Word_Count = 0

async def process_requests(request_queue):
    model = Model() 
    while True:
        if not request_queue.empty():
            try:
                websocket, message = await request_queue.get()
                message = json.loads(message)
                start = time.time()
            #   generation_config={
            #     "chat_format": "chatml",
            #     "eos_token_id": 151643,
            #     "pad_token_id": 151643,
            #     "max_window_size": 6144,
            #     "max_new_tokens": 512,
            #     "do_sample": True,
            #     "top_k": 0,
            #     "top_p": 0.8,
            #     "repetition_penalty": 1.1,
            #     "transformers_version": "4.31.0"
            # }
                # response = model.predict(prompt=message['instruction'], system_prompt="{AFK游戏}{最新}#请模拟AFK游戏玩家间的对话", histories=history)
                responses = model.predict_batch(prompts=message['instruction'], system_prompts=message['system_prompt'], histories=message['history'])
                end = time.time()
                global ALL_TIME, Process_Count, Word_Count
                ALL_TIME += end - start
                Process_Count += 1
                Word_Count += len(message['system_prompt'])
                Word_Count += sum(len(s) for s in message['instruction'])
                Word_Count += sum(len(s) for s in responses)
                print("INST:\n{}\nRSP:\n{}\n".format(message['instruction'], responses))
                print("Average Process time/iter：{}".format(ALL_TIME/Process_Count))
                print("Average Process time/word：{}".format(ALL_TIME/Word_Count))
                rsp = {'rsp': responses}
                rsp = json.dumps(rsp)
                await websocket.send(rsp)
                await websocket.close()

            except Exception as e:
                print(e)
        else:
            await asyncio.sleep(0.3)

async def handle_websocket_request(websocket, path, request_queue):
    async for message in websocket:
        # print(f"Received: {message}")
        await request_queue.put((websocket, message))
        # print("qsize {}".format(request_queue.qsize()))

async def main():
    request_queue = asyncio.Queue()

    # Create a background task to process requests
    background_task = asyncio.create_task(process_requests(request_queue))

    # Start the server
    server = await websockets.serve(
        lambda websocket, path: handle_websocket_request(websocket, path, request_queue),
        MODEL_SERVER_IP,
        MODEL_SERVER_PORT
    )

    print("WebSocket server started")
    await server.wait_closed()

    # Cancel the background task
    background_task.cancel()
    await background_task

if __name__ == "__main__":
    asyncio.run(main())
