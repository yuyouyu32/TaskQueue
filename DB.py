import json
import pandas as pd

# A
with open('/home/deepspeed/HomeCatServer/data/A', 'r') as file:
    data_json = file.read()
    data_list = json.loads(data_json)
    As = {}
    for item in data_list:
        As[item['sid']] = item['message']

# Des
df = pd.read_excel('/home/deepspeed/HomeCatServer/data/DES.xlsx')
Local = df.set_index('sid')[['province_name', 'name_cn']].agg(' '.join, axis=1).to_dict()
Des = df.set_index('sid')[['des']].agg(' '.join, axis=1).to_dict()
# Special initial postcard
Local[0] = '三沙'
CatSex = {'male': '男孩子', "female": "女孩子"}
CatName = {'male': "招财", 'female': '进宝'}
CatDes = {'male': '可爱的小猫，绿色的大眼睛，穿着绿色背带裤，双手插兜，表情俏皮。', 'female': '可爱的淑女小猫，绿色的大眼睛，穿着白色上衣和绿色裙子，尾巴俏皮的弯着。'}