from HomeCatServer import *
from Prompts import *
from DB import *

r1 = [0,1,123,124,125,126,129,130,131,133,134,139,140,141,142,144,146,147,153,155,157,159,160,163,164,172,173,178,179,180,183,118,120]
r2 = [0,1,170,171,175,176,177,180,184,186,196,197,198,200,201,204,206,211,212,219,220,224,225,231,235,237,239,240,245, 118,120]
r3 = [0,1,2,9,11,13,14,15,23,26,31,34,36,40,47,48,49,53,57,61,68,70,72,73,79,84,85,86,94,95,96,99,105,108,109,110,118,120]
rs = [r1, r2, r3]
async def test():
    while 1:
        print('\n\n')
        print('==='*5)

        cat_gender = "female"

        r = random.choice(rs)
        s_sid_index = random.randint(0, len(r)) 
        r_sid_index = random.randint(s_sid_index+1, len(r)) 
        s_sid = r[s_sid_index]
        r_sid = r[r_sid_index]

        A, des = As.get(s_sid, ''), Des.get(s_sid, CatDes[cat_gender])
        loc = Local[s_sid]

        next_A = As.get(r_sid, '')
        next_loc = Local[r_sid]

        print(A)
        print(loc, '->', next_loc)

        query = input('query:')
        system_prompt = system_template.format(name=CatName[cat_gender], sex=CatSex[cat_gender])
        task_prompt = task_template.format(local=loc, des=des, A=A, B=query)
        

        message = {
            "instruction": [task_prompt],
            "system_prompt": [system_prompt],
            "history": [[]]
        }
        print('message:')
        print(message)
        model_rsps = await async_llm_predict(message)
        rsp = re.sub(Pattern, '', model_rsps[0])
        print('rsp')
        print(rsp)
        merge_rsp = merge(query, rsp, next_loc, next_A)
        print('merge_rsp')
        print(merge_rsp)


if __name__ == '__main__':
    asyncio.run(test())
