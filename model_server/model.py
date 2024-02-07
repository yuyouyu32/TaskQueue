import importlib
from .config import *
from .language_models import *
from typing import Union, List, Tuple

class Model:
    def __init__(self):
        if MODEL_NAME not in MODEL_CLASS:
            raise ValueError("MODEL_NAME should be one of {}".format(MODEL_CLASS.keys()))
        module_name, class_name, path, ckpt_path  = MODEL_CLASS[MODEL_NAME]
        module = importlib.import_module(module_name)
        model_class = getattr(module, class_name)
        self.model: Union[BaichuanLLM, QwenLLM] = model_class(path, ckpt_path)
        print("Model {} loaded".format(MODEL_NAME))

    def predict(self, prompt: str, system_prompt: str= "", histories: List[Tuple[str, str]] = None, generation_config: dict = None) -> str:
        rsp =  self.model.predict(prompt=prompt, system_prompt=system_prompt, history=histories, generation_config=generation_config)
        return rsp

    def predict_batch(self, prompts: List[str], system_prompts: List[str], histories: List[List[Tuple[str, str]]], generation_config: dict = None) -> str:
        rsp =  self.model.predict_batch(prompts=prompts, system_prompts=system_prompts, histories=histories, generation_config=generation_config)
        return rsp



def unit_test():
    n = 4
    sys_p = ["""你叫招财，是一只小猫咪，是个男孩子。你的爷爷去世了，你追逐你爷爷的足迹，正在全国旅行中，目的地是你的老家-中国东北的漠河。旅行中你会和你的人类朋友相互写信送明信片"""] * n
    query = ["""你目前正在广西 象鼻山旅游，寄了明信片给给人类朋友，明信片图中一座像象鼻一样的山，山下有个洞，旁边是清澈的河水，远处和山上都是茂盛的树木。画风柔和、温暖、治愈。，你说
\"沿河边走时遇到了一只和我一样喜欢旅行的小狗，它叼着帽子在岸边跳来跳去。风景这么美，连春水都像是笑了。\"。\n人类朋友回信你：\"你还穿着那条绿裙子吗？\"。\n你回复他："""] * n
    history = [[]] * n

    model = Model()
    response = model.predict_batch(prompts=query, system_prompts=sys_p, histories=history)
    print(response)

if __name__ == "__main__":
    unit_test()

