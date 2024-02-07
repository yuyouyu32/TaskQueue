MODEL_CLASS = {
        # 'baichuan-13b-2':('model_server.language_models.baichuan', 'BaichuanLLM', '/mnt_data/llm_weight/Baichuan2-13B-Chat'),
        # 'Qwen-14B-Chat': ('model_server.language_models.qwen', 'QwenLLM', '/mnt_data/llm_weight/Qwen-14B-Chat'),
        #'HomeCat': ('model_server.language_models.qwen', 'QwenLLM', '/mnt_data/llm_weight/Qwen-14B-Chat', '/mnt_data/jeriffli/maomao_lora2'),
        'HomeCat': ('model_server.language_models.qwen', 'QwenLLM', '/mnt_data/llm_weight/Qwen-14B-Chat', '/mnt_data/maomao/chat_wcom_model2/checkpoint-14000'),
    }

MODEL_NAME = "HomeCat"
MODEL_SERVER_IP = "127.0.0.1" 
MODEL_SERVER_PORT = 2222
