import aiohttp
import json
import base64
from aiohttp import FormData
from DB import *
from Prompts import *

class TaskQueueManager:
    def __init__(self, project, token, ttr=60):
        self.project = project
        self.token = token
        self.ttr = ttr
        self.base_url = f"https://lilith-cat-release.lilithgame.com/queue-api/{self.project}/"

    @staticmethod
    def process_rsp(rsp):
        if rsp == '':
            return None
        rsp = json.loads(rsp)
        rsp['data'] = json.loads(base64.b64decode(rsp['data']).decode('utf-8'))
        return rsp

    async def push_task_into_queue(self, queue, data, delay=0, ttl=60, tries=3):
        url = self.base_url + f"{queue}?delay={delay}&ttl={ttl}&tries={tries}"
        async with aiohttp.ClientSession() as session:
            headers = {"X-token": self.token}
            async with session.put(url, headers=headers, data=data) as response:
                result = await response.text()
                return self.process_rsp(result)

    async def get_queue_size(self, queue: str):
        url = self.base_url + f"{queue}/size"
        async with aiohttp.ClientSession() as session:
            headers = {"X-token": self.token}
            async with session.get(url, headers=headers) as response:
                result = await response.text()
                return int(result)

    async def get_task_from_queue(self, queue: str):
        url = self.base_url + f"{queue}?ttr={self.ttr}"
        async with aiohttp.ClientSession() as session:
            headers = {"X-token": self.token}
            async with session.get(url, headers=headers) as response:
                result = await response.text()
                return self.process_rsp(result)

    async def delete_task_from_queue(self, queue: str, task_id):
        url = self.base_url + f"{queue}/delete/{task_id}"
        async with aiohttp.ClientSession() as session:
            headers = {"X-token": self.token}
            async with session.delete(url, headers=headers) as response:
                code = response.status
                return code

    async def pull_task_from_queue(self, batch_size=4):
        system_prompts, task_prompts, histories, rsps, task_ids, next_infos, querys, errs = [], [], [], [], [], [], [], []
        count = 0
        for _ in range(batch_size):
            try:
                result = await self.get_task_from_queue("user_msg")
                if not result:
                    continue
                print("Task info:", result)
                task_id, task_data = result['task_id'], result['data']
                openid, cat_gender = task_data['openid'], task_data['cat_gender']
                s_sid, r_sid = task_data['send_sid'], task_data['resp_sid']
                A, des = As.get(s_sid, ''), Des.get(s_sid, CatDes[cat_gender])
                next_A = As.get(r_sid, '')
                next_loc = Local[r_sid]
                system_prompt = system_template.format(name=CatName[cat_gender], sex=CatSex[cat_gender])
                task_prompt = task_template.format(local=Local[s_sid], des=des, A=A, B=task_data['msg'])
                rsp_data = {
                        "sender": "llm",
                        "openid": openid,
                        "msg": "",
                        "send_sid": s_sid,
                        "resp_sid": r_sid,
                    }
                print("task_prompt", task_prompt)
                system_prompts.append(system_prompt)
                task_prompts.append(task_prompt)
                querys.append(task_data['msg'])
                histories.append([])
                rsps.append(rsp_data)
                task_ids.append(task_id)
                next_infos.append((next_loc, next_A))
                errs.append(None)
                count += 1
            except Exception as e:
                print(e)
                system_prompts.append('')
                task_prompts.append('')
                histories.append([])
                errs.append(e)
        message = {
            "instruction": task_prompts[:count],
            "system_prompt": system_prompts[:count],
            "history": histories[:count]
        }
        print('message', message)
        return message, count, rsps, task_ids, next_infos, querys, errs

class MsgQueueManager:
    def __init__(self, appid, secret, env_id):
        self.appid = appid
        self.secret = secret
        self.env_id = env_id
        self.token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.secret}"
    
    async def get_access_token(self, session):
        async with session.get(self.token_url) as response:
            response = await response.json()
        return response.get("access_token")

    async def upload_file(self, session, access_token, msg_folder, open_id, file_name, rsp):
        upload_url = "https://api.weixin.qq.com/tcb/uploadfile"
        file_path = f"{msg_folder}/{open_id}/cat/{file_name}"
        data = json.dumps({
            "env": self.env_id,
            "path": file_path
        }, ensure_ascii=False)

        async with session.post(f"{upload_url}?access_token={access_token}", data=data) as response:
            response = await response.json()
            # Handle access token expiration
            if response.get("errcode") in {40001, 41001}:
                print('=====access_token expired=====')
                access_token = await self.get_access_token(session)
                async with session.post(f"{upload_url}?access_token={access_token}", data=data) as new_response:
                    response = await new_response.json()
            
            # Proceed with the file upload
            file_upload_url = response.get("url")
            upload_data = FormData()
            upload_data.add_field('key', file_path)
            upload_data.add_field('Signature', response.get("authorization"))
            upload_data.add_field('x-cos-security-token', response.get("token"))
            upload_data.add_field('x-cos-meta-fileid', response.get("cos_file_id"))
            upload_data.add_field('file', rsp, filename=file_name, content_type='text/plain')
            
            async with session.post(file_upload_url, data=upload_data) as upload_response:
                return upload_response
