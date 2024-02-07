import random

merge_templates = []
merge_templates.append("""{rsp}。我现在已经到{loc}了哦!{A}""")
merge_templates.append("""{rsp}。话说我现在已经到{loc}了!看我给你的照片，{A}""")
merge_templates.append("""{rsp}。我现在在{loc}呢!{A}""")
merge_templates.append("""{rsp}。我到{loc}啦!{A}""")
merge_templates.append("""{rsp}。我在{loc}呢!{A}""")
merge_templates.append("""{rsp}。我现在在{loc}!{A}""")
merge_templates.append("""{rsp}。我来到{loc}了。{A}""")

merge_templates.append("""我刚刚到{loc}就给你写信啦。{rsp}。快看这次我给你的照片吧，{A}""")
merge_templates.append("""我现在是在{loc}给你写信哦~{rsp}。快看这次我给你的照片吧，{A}""")
merge_templates.append("""我现在在{loc}给你发明信片哦。{rsp}。快看这次我给你的照片吧，{A}""")

merge_templates.append("""{rsp}。我现在在{loc},感觉挺不错！{A}""")
merge_templates.append("""{rsp}。我来{loc}啦，感觉很棒哦！{A}""")
merge_templates.append("""{rsp}。我现在在{loc}，这里很不错呢~{A}""")
merge_templates.append("""{rsp}。到{loc}啦，真是个不错的地方！{A}""")
merge_templates.append("""{rsp}。到{loc}啦，这很好玩喵~{A}""")

merge_templates.append("""{rsp},我现在去了一个新的地方了哦。{A}""")
merge_templates.append("""{rsp},我到其他地方啦。{A}""")
merge_templates.append("""{rsp},我又到了新地方啦。{A}""")
merge_templates.append("""{rsp},我来到另一个地方啦。{A}""")

special_loc_merge_templates = {'三沙': [], '漠河': []}
special_loc_merge_templates['三沙'].append("""{rsp}。{A}""")
special_loc_merge_templates['三沙'].append("""{rsp}。我还在三沙呢。{A}""")
special_loc_merge_templates['三沙'].append("""{rsp}。{A}""")
special_loc_merge_templates['漠河'].append("""{rsp}。我回到家啦！{A}""")
special_loc_merge_templates['漠河'].append("""{rsp}。我已经到家啦。{A}""")
special_loc_merge_templates['漠河'].append("""{rsp}。终于到家了喵呜。{A}""")

special_words = []
special_words.append(('大模型', '你在说啥，听不太懂呢喵~'))
special_words.append(('llm', '你在说啥，听不太懂呢喵~'))
special_words.append(('chat', '你在说啥，听不太懂呢喵~'))
special_words.append(('chatgpt', '你在说啥，听不太懂呢喵~'))
special_words.append(('小冰', '你在说啥，听不太懂呢喵~'))
special_words.append(('语言模型', '你在说啥，听不太懂呢喵~'))
special_words.append(('ai', '你在说啥，听不太懂呢喵~'))
special_words.append(('人工智能', '你在说啥，听不太懂呢喵~'))
special_words.append(('助手', '你在说啥，听不太懂呢喵~'))
special_words.append(('智能体', '你在说啥，听不太懂呢喵~'))
special_words.append(('openai', '你在说啥，听不太懂呢喵~'))
special_words.append(('微软', '你在说啥，听不太懂呢喵~'))
special_words.append(('机器学习', '你在说啥，听不太懂呢喵~'))
special_words.append(('深度学习', '你在说啥，听不太懂呢喵~'))

def filter_process(query, response):
    for trigger_w, sp_rsp in special_words:
        if trigger_w in response.lower() or  trigger_w in query.lower():
            return sp_rsp
    return response

def random_process_location(pos, scene):
    if len(scene) > 0:
        t = random.random()
        if t > 0.66:
            return pos + "的" + scene
        elif t > 0.33:
            return scene
        else:
            return pos + "" + scene

def merge(query, response, next_location, next_A):
    print("=======")
    print(response)
    print(next_location)
    print(next_A)

    response = filter_process(query, response)

    if " " in next_location:
        pos, scene = next_location.split(" ")
    else:
        pos, scene = next_location, ''

    if pos in special_loc_merge_templates:
        merge_template = random.choice(special_loc_merge_templates[pos]) 
        res = merge_template.replace("{rsp}", response)
        res = res.replace("{A}", next_A)
    else:
        merge_template = random.choice(merge_templates) 
        next_location = random_process_location(pos, scene)
        res = merge_template.replace("{rsp}", response)
        res = res.replace("{loc}", next_location)
        res = res.replace("{A}", next_A)
    return res

