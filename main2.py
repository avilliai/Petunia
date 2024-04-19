import asyncio
import logging
import os
import random
import re
import threading

import colorlog
import httpx
import requests
import yaml
import google.generativeai as genai
import zhipuai
from mirai import Mirai, WebSocketAdapter, Voice, GroupMessage, At, Plain, Image
from mirai.bot import Startup
from openai import OpenAI
class CListen(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.mLoop = loop

    def run(self):
        asyncio.set_event_loop(self.mLoop)  # 在新线程中开启一个事件循环

        self.mLoop.run_forever()
async def translate(text,mode="ZH_CN2JA"):
    URL=f"https://api.pearktrue.cn/api/translate/?text={text}&type={mode}"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(URL)
        #print(r.json()["data"]["translate"])
        return r.json()["data"]["translate"]

def cozeBotRep(url,text,proxy,channelid=None):
    os.environ["http_proxy"] = proxy
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "messages": text,
        "stream": False
    }

    r = requests.post(url, headers=headers, json=data)
    print(r)
    print(r.text)
    print(r)
    if r.status_code == 200:
        result = r.json()
        return result.get('choices')[0].get('message')

    else:
        print(f'Error: {r.status_code}')
def newLogger():
    # 创建一个logger对象
    logger = logging.getLogger("villia")
    # 设置日志级别为DEBUG，这样可以输出所有级别的日志
    logger.setLevel(logging.DEBUG)
    # 创建一个StreamHandler对象，用于输出日志到控制台
    console_handler = logging.StreamHandler()
    # 设置控制台输出的日志格式和颜色
    logger.propagate = False
    console_format = '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    console_colors = {
        'DEBUG': 'white',
        'INFO': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    console_formatter = colorlog.ColoredFormatter(console_format, log_colors=console_colors)
    console_handler.setFormatter(console_formatter)
    # 将控制台处理器添加到logger对象中
    logger.addHandler(console_handler)
    # 使用不同级别的方法来记录不同重要性的事件
    return logger
def random_str(random_length=6,chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789@$#_%'):
    """
    生成随机字符串作为验证码
    :param random_length: 字符串长度,默认为6
    :return: 随机字符串
    """
    string = ''

    length = len(chars) - 1
    # random = Random()
    # 设置循环每次取一个字符用来生成随机数
    for i in range(7):
        string +=  ((chars[random.randint(0, length)]))
    return string
async def lolimigpt2(prompt,meta):
    url="https://api.lolimi.cn/API/AI/c.php?"
    prompt.insert(0,{"role":"user","content":meta})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色"})
    async with httpx.AsyncClient(timeout=200) as client:
        r = await client.post(url=url,json=prompt)
        return {"role":"assistant","content":r.text}


async def geminirep(ak, messages):
    # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
    GOOGLE_API_KEY = ak

    genai.configure(api_key=GOOGLE_API_KEY)

    # model = genai.GenerativeModel('gemini-pro')
    generation_config = {
        "candidate_count": 1,
        "max_output_tokens": 256,
        "temperature": 1.0,
        "top_p": 0.7,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    # print(type(messages))

    response = model.generate_content(messages)

    # print(response.text)
    return response.text
async def glm4(prompt,meta):
    prompt.insert(0,{"role":"user","content":meta})
    prompt.insert(1, {"role": "assistant", "content": "好的~"})
    url = f"https://api.lolimi.cn/API/AI/zp.php?msg={str(prompt)}"
    async with httpx.AsyncClient(timeout=100) as client:  # 100s超时
        r = await client.get(url)  # 发起请求
        #print(r.json())
        return {"role": "assistant", "content": r.json().get("data").get("output")}
def gptOfficial(prompt,apikeys,proxy,bot_info):
    os.environ["OPENAI_API_KEY"] = random.choice(apikeys)
    os.environ["http_proxy"] = proxy  # 指定代理，解决连接问题
    os.environ["https_proxy"] = proxy  # 指定代理，解决连接问题
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    prompt.insert(0,{"role":"user","content":bot_info})
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model="gpt-3.5-turbo",
        stream=False,
    )
    #print(chat_completion.choices[0].message.content)
    return {"role":"assistant","content":chat_completion.choices[0].message.content}
def gptUnofficial(prompt,apikeys,proxy,bot_info):
    os.environ["OPENAI_API_KEY"] = random.choice(apikeys)
    client = OpenAI(
        # This is the default and can be omitted
        base_url="https://api.chatanywhere.com.cn",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的主人喵"})
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model="gpt-3.5-turbo",
        stream=False,
    )
    # print(chat_completion.choices[0].message.content)
    return {"role": "assistant", "content": chat_completion.choices[0].message.content}

async def drawe(prompt,path= "./test.png"):
    url=f"https://api.lolimi.cn/API/AI/sd.php?msg={prompt}&mode=动漫"

    async with httpx.AsyncClient(timeout=40) as client:
        r = await client.get(url)
        with open(path,"wb") as f:
            f.write(r.content)
        # print(path)
        return path
async def draw1(prompt,path="./test.png"):
    url=f"https://api-collect.idcdun.com/v1/images/generations?prompt={prompt}&n=1&model=dall-e-3&size=1024x1024"
    async with httpx.AsyncClient(timeout=40) as client:
        r = await client.get(url)
        url2=r.json().get("data")[0].get("url")
        async with httpx.AsyncClient(timeout=40) as client:
            r1 = await client.get(url2)
        with open(path, "wb") as f:
            f.write(r1.content)
        # print(path)
        return path
def main(bot,logger):
    with open('data/noRes.yaml', 'r', encoding='utf-8') as f:
        noRes1 = yaml.load(f.read(), Loader=yaml.FullLoader)
    noRes=noRes1.get("noRes")
    with open('settings.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    voicegg=result.get("chatGLM").get("voiceGenerateSource")
    glmReply = result.get("chatGLM").get("glmReply")
    replyModel = result.get("chatGLM").get("model")
    trustglmReply = result.get("chatGLM").get("trustglmReply")
    context= result.get("chatGLM").get("context")
    maxPrompt = result.get("chatGLM").get("maxPrompt")
    voiceLangType = str(result.get("chatGLM").get("langType"))
    allcharacters=result.get("chatGLM").get("bot_info")
    maxTextLen = result.get("chatGLM").get("maxLen")
    voiceRate = result.get("chatGLM").get("voiceRate")
    speaker = result.get("chatGLM").get("speaker")
    withText=result.get("chatGLM").get("withText")
    chatGLM_api_key=result.get("apiKeys").get("chatGLMKey")
    geminiapikey=result.get("apiKeys").get('geminiapiKey')
    gptkeys=result.get("apiKeys").get("openaikeys")
    proxy=result.get("proxy")
    CoziUrl=result.get("apiKeys").get("CoziUrl")
    botName=result.get("bot").get('botName')
    master=result.get("bot").get("master")
    gptdev=result.get("gpt3.5-dev")
    if proxy!="":
        os.environ["http_proxy"] = proxy
    newLoop = asyncio.new_event_loop()
    listen = CListen(newLoop)
    listen.setDaemon(True)
    listen.start()
    with open('data/chatGLMCharacters.yaml', 'r', encoding='utf-8') as f:
        result2223 = yaml.load(f.read(), Loader=yaml.FullLoader)
    global chatGLMCharacters
    chatGLMCharacters = result2223
    with open('data/GeminiData.yaml', 'r', encoding='utf-8') as f:
        cha0 = yaml.load(f.read(), Loader=yaml.FullLoader)
    global GeminiData
    GeminiData=cha0
    with open('data/chatGLMData.yaml', 'r', encoding='utf-8') as f:
        cha = yaml.load(f.read(), Loader=yaml.FullLoader)
    global chatGLMData
    chatGLMData=cha
    with open('data/permit.yaml', 'r', encoding='utf-8') as f:
        trusts = yaml.load(f.read(), Loader=yaml.FullLoader)
    global trustUser,trustGroups
    trustUser=trusts.get("users")
    trustGroups=trusts.get("groups")
    @bot.on(GroupMessage)
    async def aidrawf(event: GroupMessage):
        if str(event.message_chain).startswith("画 "):
            tag=str(event.message_chain).replace("画 ","")
            if os.path.exists("./data/pictures"):
                pass
            else:
                os.mkdir("./data/pictures")
            path = "data/pictures/" + random_str() + ".png"
            logger.info("发起ai绘画请求，path:"+path+"|prompt:"+tag)
            try:
                logger.info("接口1绘画中......")
                p=await drawe(tag,path)
                await bot.send(event,Image(path=p),True)
            except Exception as e:
                logger.error(e)
                await bot.send(event,"接口绘画失败.......")
            try:
                logger.info("接口2绘画中......")
                p=await draw1(tag,path)
                await bot.send(event,Image(path=p),True)
            except Exception as e:
                logger.error(e)
                await bot.send(event,"接口2绘画失败.......")
    # 用于chatGLM清除本地缓存
    @bot.on(GroupMessage)
    async def clearPrompt(event: GroupMessage):
        global chatGLMData, GeminiData
        if str(event.message_chain) == "/clear":
            try:
                chatGLMData.pop(event.sender.id)
                # 写入文件
                with open('data/chatGLMData.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(chatGLMData, file, allow_unicode=True)
                await bot.send(event, "已清除近期记忆")
            except:
                logger.error("清理缓存出错，无本地对话记录")
            try:
                GeminiData.pop(event.sender.id)
                # 写入文件
                with open('data/GeminiData.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(GeminiData, file, allow_unicode=True)
                await bot.send(event, "已清除近期记忆")
            except:
                logger.error("清理缓存出错，无本地对话记录")
        elif str(event.message_chain) == "/allclear" and event.sender.id == master:
            try:
                chatGLMData = {"f": "hhh"}
                # chatGLMData.pop(event.sender.id)
                # 写入文件
                with open('data/chatGLMData.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(chatGLMData, file, allow_unicode=True)

                with open('data/GeminiData.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(chatGLMData, file, allow_unicode=True)
                await bot.send(event, "已清除所有用户的prompt")
            except:
                await bot.send(event, "清理缓存出错，无本地对话记录")

    # 群内chatGLM回复
    @bot.on(GroupMessage)
    async def atReply(event: GroupMessage):
        global chatGLMData, chatGLMCharacters,GeminiData,trustUser,trustGroups
        if At(bot.qq) in event.message_chain and (glmReply == True or (trustglmReply == True and str(event.sender.id) in trustUser) or event.group.id in trustGroups):
            if event.sender.id in chatGLMCharacters:
                if chatGLMCharacters.get(event.sender.id) == "gpt3.5":

                    rth = "gpt3.5"
                    await modelReply(event, rth)
                elif (chatGLMCharacters.get(event.sender.id) == "Cozi"):
                    await modelReply(event, chatGLMCharacters.get(event.sender.id))
                elif chatGLMCharacters.get(event.sender.id) == "lolimigpt":
                    await modelReply(event, chatGLMCharacters.get(event.sender.id))
                elif chatGLMCharacters.get(event.sender.id) == "glm-4":
                    await modelReply(event, chatGLMCharacters.get(event.sender.id))
                elif chatGLMCharacters.get(event.sender.id) == "Gemini":
                    text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "").replace("/g", "")
                    for saa in noRes:
                        if text == saa:
                            logger.warning("与屏蔽词匹配，Gemini不回复")
                            return
                    logger.info("gemini开始运行")
                    if text == "" or text == " ":
                        text = "在吗"
                    geminichar = allcharacters.get("Gemini").replace("【bot】", botName).replace("【用户】",
                                                                                               event.sender.member_name)
                    # 构建新的prompt
                    tep = {"role": "user", "parts": [text]}
                    # print(type(tep))
                    # 获取以往的prompt
                    if event.sender.id in GeminiData and context == True:
                        prompt = GeminiData.get(event.sender.id)
                        prompt.append({"role": "user", 'parts': [text]})
                        # 没有该用户，以本次对话作为prompt
                    else:
                        await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                        prompt = [{"role": "user", "parts": [geminichar]},
                                  {"role": 'model', "parts": ["好的，已了解您的需求，我会扮演好你设定的角色"]}]
                        prompt.append(tep)
                    logger.info("gemini接收提问:" + text)
                    try:
                        # logger.info(geminiapikey)
                        r = await geminirep(ak=random.choice(geminiapikey), messages=prompt)
                        # 更新该用户prompt
                        prompt.append({"role": 'model', "parts": [r]})
                        await tstt(r, event)

                        GeminiData[event.sender.id] = prompt
                        # 写入文件
                        with open('data/GeminiData.yaml', 'w', encoding="utf-8") as file:
                            yaml.dump(GeminiData, file, allow_unicode=True)

                        # asyncio.run_coroutine_threadsafe(asyncgemini(geminiapikey,prompt, event,text), newLoop)
                        # st1 = await chatGLM(selfApiKey, meta1, prompt)
                    except Exception as e:
                        logger.error(e)
                        await bot.send(event, "gemini启动出错\n请重试")
                elif type(chatGLMCharacters.get(event.sender.id)) == dict:
                    text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "")
                    logger.info("分支1")
                    for saa in noRes:
                        if text == saa:
                            logger.warning("与屏蔽词匹配，chatGLM不回复")
                            return
                    if text == "" or text == " ":
                        text = "在吗"
                    # 构建新的prompt
                    tep = {"role": "user", "content": text}
                    # print(type(tep))
                    # 获取以往的prompt
                    if event.sender.id in chatGLMData and context == True:
                        prompt = chatGLMData.get(event.sender.id)
                        prompt.append({"role": "user", "content": text})

                    # 没有该用户，以本次对话作为prompt
                    else:
                        await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                        prompt = [tep]
                        chatGLMData[event.sender.id] = prompt
                    # 或者开启了信任用户回复且为信任用户
                    if str(event.sender.id) in trustUser and trustglmReply == True:
                        logger.info("信任用户进行chatGLM提问")
                        selfApiKey = chatGLM_api_key
                    elif glmReply == True:
                        logger.info("开放群聊glm提问")
                        selfApiKey = chatGLM_api_key
                    else:
                        await bot.send(event, "Error,该模型不可用")
                        return

                    # 获取角色设定
                    if event.sender.id in chatGLMCharacters:
                        meta1 = chatGLMCharacters.get(event.sender.id)
                    else:
                        logger.warning("读取meta模板")
                        with open('settings.yaml', 'r', encoding='utf-8') as f:
                            resy = yaml.load(f.read(), Loader=yaml.FullLoader)
                        meta1 = resy.get("chatGLM").get("bot_info").get("default")


                    setName = event.sender.member_name
                    meta1["user_name"] = meta1.get("user_name").replace("指挥", setName)
                    meta1["user_info"] = meta1.get("user_info").replace("指挥", setName).replace("yucca", botName)
                    meta1["bot_info"] = meta1.get("bot_info").replace("指挥", setName).replace("yucca", botName)
                    meta1["bot_name"] = botName

                    logger.info("chatGLM接收提问:" + text)
                    try:
                        logger.info("当前meta:" + str(meta1))
                        asyncio.run_coroutine_threadsafe(asyncchatGLM(selfApiKey, meta1, prompt, event, setName, text),
                                                         newLoop)
                        # st1 = await chatGLM(selfApiKey, meta1, prompt)


                    except:
                        await bot.send(event, "chatGLM启动出错，请联系master\n或重试")
            # 判断模型
            elif replyModel == "gpt3.5":

                rth = "gpt3.5"
                await modelReply(event, rth)
            elif replyModel == "Cozi":
                await modelReply(event, replyModel)
            elif replyModel == "glm-4":
                await modelReply(event, replyModel)
            elif replyModel == "lolimigpt" :
                await modelReply(event, replyModel)
            elif replyModel == "Gemini" :
                text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "").replace("/g", "")
                for saa in noRes:
                    if text == saa:
                        logger.warning("与屏蔽词匹配，Gemini不回复")
                        return
                logger.info("gemini开始运行")
                if text == "" or text == " ":
                    text = "在吗"
                # 构建新的prompt
                tep = {"role": "user", "parts": [text]}
                geminichar = allcharacters.get("Gemini").replace("【bot】", botName).replace("【用户】",
                                                                                           event.sender.member_name)
                # print(type(tep))
                # 获取以往的prompt
                if event.sender.id in GeminiData and context == True:
                    prompt = GeminiData.get(event.sender.id)
                    prompt.append({"role": "user", 'parts': [text]})
                    # 没有该用户，以本次对话作为prompt
                else:
                    await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                    prompt = [{"role": "user", "parts": [geminichar]},
                              {"role": 'model', "parts": ["好的，已了解您的需求，我会扮演好你设定的角色"]}]
                    prompt.append(tep)
                logger.info("gemini接收提问:" + text)
                try:
                    # logger.info(geminiapikey)
                    r = await geminirep(ak=random.choice(geminiapikey), messages=prompt)
                    # 更新该用户prompt
                    prompt.append({"role": 'model', "parts": [r]})
                    await tstt(r, event)

                    GeminiData[event.sender.id] = prompt
                    # 写入文件
                    with open('data/GeminiData.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(GeminiData, file, allow_unicode=True)

                    # asyncio.run_coroutine_threadsafe(asyncgemini(geminiapikey,prompt, event,text), newLoop)
                    # st1 = await chatGLM(selfApiKey, meta1, prompt)
                except Exception as e:
                    logger.error(e)
                    GeminiData.pop(event.sender.id)
                    # 写入文件
                    with open('data/GeminiData.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(GeminiData, file, allow_unicode=True)
                    await bot.send(event, "gemini启动出错\n请重试")
            elif replyModel == "characterglm":
                text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "")
                logger.info("分支1")
                for saa in noRes:
                    if text == saa:
                        logger.warning("与屏蔽词匹配，chatGLM不回复")
                        return
                if text == "" or text == " ":
                    text = "在吗"
                # 构建新的prompt
                tep = {"role": "user", "content": text}
                # print(type(tep))
                # 获取以往的prompt
                if event.sender.id in chatGLMData and context == True:
                    prompt = chatGLMData.get(event.sender.id)
                    prompt.append({"role": "user", "content": text})

                # 没有该用户，以本次对话作为prompt
                else:
                    await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                    prompt = [tep]
                    chatGLMData[event.sender.id] = prompt
                # logger.info("当前prompt"+str(prompt))
                selfApiKey = chatGLM_api_key
                # 获取角色设定
                if event.sender.id in chatGLMCharacters:
                    meta1 = chatGLMCharacters.get(event.sender.id)
                else:
                    logger.warning("读取meta模板")
                    with open('settings.yaml', 'r', encoding='utf-8') as f:
                        resy = yaml.load(f.read(), Loader=yaml.FullLoader)
                    meta1 = resy.get("chatGLM").get("bot_info").get("default")

                setName = event.sender.member_name
                meta1["user_name"] = meta1.get("user_name").replace("指挥", setName)
                meta1["user_info"] = meta1.get("user_info").replace("指挥", setName).replace("yucca", botName)
                meta1["bot_info"] = meta1.get("bot_info").replace("指挥", setName).replace("yucca", botName)
                meta1["bot_name"] = botName

                logger.info("chatGLM接收提问:" + text)
                try:
                    logger.info("当前meta:" + str(meta1))
                    asyncio.run_coroutine_threadsafe(asyncchatGLM(selfApiKey, meta1, prompt, event, setName, text), newLoop)
                    # st1 = await chatGLM(selfApiKey, meta1, prompt)


                except:
                    await bot.send(event, "chatGLM启动出错，请联系master\n或重试")

    @bot.on(GroupMessage)
    async def permitUserandGroup(event:GroupMessage):
        global trustUser, trustGroups
        if event.sender.id==master:
            if str(event.message_chain).startswith("授权#"):
                try:
                    trustUser.append(int(str(event.message_chain).replace("授权#","")))
                    ppp={"groups":trustGroups,"users":trustUser}
                    with open('data/permit.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(ppp, file, allow_unicode=True)
                    await bot.send(event,"授权成功")
                except:
                    await bot.send(event,"授权失败")
            elif str(event.message_chain).startswith("授权群#"):
                try:
                    trustGroups.append(int(str(event.message_chain).replace("授权群#","")))
                    ppp={"groups":trustGroups,"users":trustUser}
                    with open('data/permit.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(ppp, file, allow_unicode=True)
                    await bot.send(event,"授权群成功")
                except:
                    await bot.send(event,"授权失败")
    @bot.on(Startup)
    async def sgggggg(event: Startup):
        await bot.send_friend_message(master,"master指令：\n授权群#群号\n授权#QQ号\n\n用户指令：\n@bot 角色")
    @bot.on(GroupMessage)
    async def ttsssss(event: GroupMessage):
        modelScope = ["BT", "塔菲", "阿梓", "otto", "丁真", "星瞳", "东雪莲", "嘉然", "孙笑川", "亚托克斯", "文静", "鹿鸣", "奶绿", "七海", "恬豆",
                      "科比"]
        outVitsSpeakers = "空, 荧, 派蒙, 纳西妲, 阿贝多, 温迪, 枫原万叶, 钟离, 荒泷一斗, 八重神子, 艾尔海森, 提纳里, 迪希雅, 卡维, 宵宫, 莱依拉, 赛诺, 诺艾尔, 托马, 凝光, 莫娜, 北斗, 神里绫华, 雷电将军, 芭芭拉, 鹿野院平藏, 五郎, 迪奥娜, 凯亚, 安柏, 班尼特, 琴, 柯莱, 夜兰, 妮露, 辛焱, 珐露珊, 魈, 香菱, 达达利亚, 砂糖, 早柚, 云堇, 刻晴, 丽莎, 迪卢克, 烟绯, 重云, 珊瑚宫心海, 胡桃, 可莉, 流浪者, 久岐忍, 神里绫人, 甘雨, 戴因斯雷布, 优菈, 菲谢尔, 行秋, 白术, 九条裟罗, 雷泽, 申鹤, 迪娜泽黛, 凯瑟琳, 多莉, 坎蒂丝, 萍姥姥, 罗莎莉亚, 留云借风真君, 绮良良, 瑶瑶, 七七, 奥兹, 米卡, 夏洛蒂, 埃洛伊, 博士, 女士, 大慈树王, 三月七, 娜塔莎, 希露瓦, 虎克, 克拉拉, 丹恒, 希儿, 布洛妮娅, 瓦尔特, 杰帕德, 佩拉, 姬子, 艾丝妲, 白露, 星, 穹, 桑博, 伦纳德, 停云, 罗刹, 卡芙卡, 彦卿, 史瓦罗, 螺丝咕姆, 阿兰, 银狼, 素裳, 丹枢, 黑塔, 景元, 帕姆, 可可利亚, 半夏, 符玄, 公输师傅, 奥列格, 青雀, 大毫, 青镞, 费斯曼, 绿芙蓉, 镜流, 信使, 丽塔, 失落迷迭, 缭乱星棘, 伊甸, 伏特加女孩, 狂热蓝调, 莉莉娅, 萝莎莉娅, 八重樱, 八重霞, 卡莲, 第六夜想曲, 卡萝尔, 姬子, 极地战刃, 布洛妮娅, 次生银翼, 理之律者, 真理之律者, 迷城骇兔, 希儿, 魇夜星渊, 黑希儿, 帕朵菲莉丝, 天元骑英, 幽兰黛尔, 德丽莎, 月下初拥, 朔夜观星, 暮光骑士, 明日香, 李素裳, 格蕾修, 梅比乌斯, 渡鸦, 人之律者, 爱莉希雅, 爱衣, 天穹游侠, 琪亚娜, 空之律者, 终焉之律者, 薪炎之律者, 云墨丹心, 符华, 识之律者, 维尔薇, 始源之律者, 芽衣, 雷之律者, 苏莎娜, 阿波尼亚, 陆景和, 莫弈, 夏彦, 左然".replace(
            " ", "").split(",")
        msg = "".join(map(str, event.message_chain[Plain]))
        # 匹配指令
        if "说" in str(event.message_chain):
            if str(event.message_chain).split("说")[0] in modelScope:
                spk=str(event.message_chain).split("说")[0]
                txt=str(event.message_chain).replace(spk+"说","")
                logger.info(f"语音合成任务 text: {txt}, speaker: {spk}")
                p=await superVG({"text": txt, "speaker": spk},"modelscopeTTS")
                await bot.send(event,Voice(path=p))
            if str(event.message_chain).split("说")[0] in outVitsSpeakers:
                spk = str(event.message_chain).split("说")[0]
                txt = str(event.message_chain).replace(spk + "说", "")
                logger.info(f"语音合成任务 text: {txt}, speaker: {spk}")
                p=await superVG({"text": txt, "speaker": spk}, "outVits")
                await bot.send(event, Voice(path=p))
        if "角色" in str(event.message_chain) and At(bot.qq) in event.message_chain:
            str1=""
            str1 += "outVits语音合成可用角色如下：\n" + str(outVitsSpeakers) + "\n\nbert_vits2可用角色如下：\n" + str(
                ["BT", "塔菲", "阿梓", "otto", "丁真", "星瞳", "东雪莲", "嘉然", "孙笑川", "亚托克斯", "文静", "鹿鸣", "奶绿", "七海", "恬豆", "科比"])
            await bot.send(event, str1)
            await bot.send(event, "可发送 xx说.......  以进行语音合成")
    async def tstt(r, event):
        if len(r) < maxTextLen and random.randint(0, 100) < voiceRate and event.type != 'FriendMessage':
            data1 = {}
            data1['speaker'] = speaker

            # print(path)
            st8 = re.sub(r"（[^）]*）", "", r)  # 使用r前缀表示原始字符串，避免转义字符的问题
            data1["text"] = st8
            st1 = r
            try:

                logger.info(f"调用{voicegg}语音合成")
                path = await superVG(data1, voicegg, voiceLangType)
                await bot.send(event, Voice(path=path))
                if withText == True:
                    await bot.send(event, st1, True)
            except Exception as e:
                logger.error(e)
                await bot.send(event, st1, True)

        else:
            await bot.send(event, r, True)
    async def modelReply(event,modelHere):
        global chatGLMData, chatGLMCharacters,GeminiData

        if event.type != 'FriendMessage':
            bot_in = str(f"你是{botName},我是" + event.sender.member_name + "," + allcharacters.get(
            "gpt3.5")).replace("【bot】",botName).replace("【用户】", event.sender.member_name)
            lolimi_bot_in = str("你是" + botName + ",我是" + event.sender.member_name + "," + allcharacters.get(
                "lolimigpt")).replace("【bot】",botName).replace("【用户】", event.sender.member_name)
            glm4_bot_in = str("你是" + botName + ",我是" + event.sender.member_name + "," + allcharacters.get(
                "glm-4")).replace("【bot】",botName).replace("【用户】", event.sender.member_name)
        else:
            bot_in = str("你是" + botName + ",我是" + event.sender.nickname + "," + allcharacters.get(
                "gpt3.5")).replace("【bot】",
                                   botName).replace("【用户】", event.sender.nickname)
            lolimi_bot_in = str("你是" + botName + ",我是" + event.sender.nickname + "," + allcharacters.get(
                "lolimigpt")).replace("【bot】",
                                      botName).replace("【用户】", event.sender.nickname)
            glm4_bot_in = str("你是" + botName + ",我是" + event.sender.nickname + "," + allcharacters.get(
                "glm-4")).replace("【bot】",
                                      botName).replace("【用户】", event.sender.nickname)
        try:
            text = str(event.message_chain).replace("@" + str(bot.qq) + " ", '').replace("/gpt", "")
            if text == "" or text == " ":
                text = "在吗"
            for saa in noRes:
                #print(text, saa)
                if text == saa:

                    logger.warning("与屏蔽词匹配，不回复")
                    return
            if event.sender.id in chatGLMData:
                prompt1 = chatGLMData.get(event.sender.id)
                prompt1.append({"content": text, "role": "user"})
            else:
                prompt1 = [{"content": text, "role": "user"}]
                await bot.send(event, "即将开始对话，如果遇到异常请发送 /clear 清理对话")
            logger.info(f"{modelHere}  bot 接受提问：" + text)
            loop = asyncio.get_event_loop()
            if modelHere=="gpt3.5":
                if gptdev==False:
                    rep = await loop.run_in_executor(None, gptOfficial, prompt1, gptkeys, proxy, bot_in)
                else:
                    rep = await loop.run_in_executor(None, gptUnofficial, prompt1, gptkeys, proxy, bot_in)
            elif modelHere=="Cozi":
                rep = await loop.run_in_executor(None, cozeBotRep, CoziUrl, prompt1, proxy)
            elif modelHere=="lolimigpt":
                rep = await lolimigpt2(prompt1,lolimi_bot_in)
                if "令牌额度" in rep.get("content"):
                    logger.error("没金币了喵")
                    await bot.send(event, "api没金币了喵\n请发送 @bot 可用角色模板 以更换其他模型", True)
                    return
                if "敏感词汇" in rep.get("content"):
                    logger.error("敏感词了搁这")
                    await bot.send(event, "触发了敏感词审核，已自动清理聊天记录", True)
                    try:
                        chatGLMData.pop(event.sender.id)
                    except Exception as e:
                        logger.error(e)
                    return

            elif modelHere=="glm-4":
                rep=await glm4(prompt1,glm4_bot_in)
                if "禁止违规问答" == rep.get("content"):
                    logger.error("敏感喽，不能用了")
                    await bot.send(event,rep.get("content"))
                    await bot.send(event,"触发了敏感内容审核，已自动清理聊天记录")
                    try:
                        chatGLMData.pop(event.sender.id)
                    except Exception as e:
                        logger.error(e)
                    return
            prompt1.append(rep)
            # 超过10，移除第一个元素

            if len(prompt1) > maxPrompt:
                logger.error(f"{modelHere} prompt超限，移除元素")
                del prompt1[0]
                del prompt1[0]
            chatGLMData[event.sender.id] = prompt1
            # 写入文件
            with open('data/chatGLMData.yaml', 'w', encoding="utf-8") as file:
                yaml.dump(chatGLMData, file, allow_unicode=True)
            logger.info(f"{modelHere} bot 回复：" + rep.get('content'))
            await tstt(rep.get('content'), event)
        except Exception as e:
            logger.error(e)
            try:
                chatGLMData.pop(event.sender.id)
                logger.info("清理用户prompt")
            except Exception as e:
                logger.error("清理用户prompt出错")

            await bot.send(event, "出错，自动清理异常prompt.....请重试，如果无效请 联系master反馈问题", True)

    async def superVG(data, mode, langmode="<zh>"):
        if langmode == "<jp>":
            try:
                # r=await translate(data.get("text"))
                # print(r)
                data["text"] = await translate(data.get("text"))
            except:
                print("语音合成翻译出错")
        elif langmode == "<en>":
            try:
                # r=await translate(data.get("text"))
                # print(r)
                data["text"] = await translate(data.get("text"), "ZH_CN2EN")
            except:
                print("语音合成翻译出错")
        if mode == "outVits":
            speaker = data.get("speaker")
            text = data.get("text")
            # os.system("where python")
            # p = random_str() + ".mp3"
            # p = "data/voices/" + p
            p = "data/voices/" + random_str() + '.wav'
            url = f"https://api.lolimi.cn/API/yyhc/y.php?msg={text}&speaker={speaker}"
            async with httpx.AsyncClient(timeout=200) as client:
                r = await client.post(url)
                newUrl = r.json().get("music")
                print("outvits语音合成路径：" + p)
                r1 = requests.get(newUrl)
                with open(p, "wb") as f:
                    f.write(r1.content)
                # await change_sample_rate(p)
                return p
        elif mode == "modelscopeTTS":
            speaker = data.get("speaker")
            text = data.get("text")
            if text == "" or text == " ":
                text = "哼哼"
            if speaker == "阿梓":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azusa-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azusa-Bert-VITS2-2.3/gradio/file="
            elif speaker == "otto":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/otto-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/otto-Bert-VITS2-2.3/gradio/file="
            elif speaker == "塔菲":
                speaker = "taffy"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Taffy-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Taffy-Bert-VITS2/gradio/file="
            elif speaker == "星瞳":
                speaker = "XingTong"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/XingTong-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/XingTong-Bert-VITS2/gradio/file="
            elif speaker == "丁真":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/DZ-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/DZ-Bert-VITS2-2.3/gradio/file="
            elif speaker == "东雪莲":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azuma-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azuma-Bert-VITS2-2.3/gradio/file="
            elif speaker == "嘉然":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Diana-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Diana-Bert-VITS2-2.3/gradio/file="
            elif speaker == "孙笑川":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/SXC-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/SXC-Bert-VITS2/gradio/file="
            elif speaker == "鹿鸣":
                speaker = "Lumi"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Lumi-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Lumi-Bert-VITS2/gradio/file="
            elif speaker == "文静":
                speaker = "Wenjing"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Wenjing-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Wenjing-Bert-VITS2/gradio/file="
            elif speaker == "亚托克斯":
                speaker = "Aatrox"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Aatrox-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Aatrox-Bert-VITS2/gradio/file="
            elif speaker == "奶绿":
                speaker = "明前奶绿"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/LAPLACE-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/LAPLACE-Bert-VITS2-2.3/gradio/file="
            elif speaker == "七海":
                speaker = "Nana7mi"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Nana7mi-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Nana7mi-Bert-VITS2/gradio/file="
            elif speaker == "恬豆":
                speaker = "Bekki"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Bekki-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Bekki-Bert-VITS2/gradio/file="
            elif speaker == "科比":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Kobe-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Kobe-Bert-VITS2-2.3/gradio/file="
            data = {
                "data": [text, speaker, 0.5, 0.5, 0.9, 1, "auto", None, "Happy", "Text prompt", "", 0.7],
                "event_data": None,
                "fn_index": 0,
                "dataType": ["textbox", "dropdown", "slider", "slider", "slider", "slider", "dropdown", "audio",
                             "textbox",
                             "radio", "textbox", "slider"],
                "session_hash": "xjwen214wqf"
            }
            p = "data/voices/" + random_str() + '.wav'
            async with httpx.AsyncClient(timeout=200) as client:
                r = await client.post(url, json=data)
                newurl = newurp + \
                         r.json().get("data")[1].get("name")
                async with httpx.AsyncClient(timeout=200) as client:
                    r = await client.get(newurl)
                    with open(p, "wb") as f:
                        f.write(r.content)
                    return p

    # CharacterchatGLM部分
    def chatGLM(api_key, bot_info, prompt, model1):
        model1 = "characterglm"
        logger.info("当前模式:" + model1)
        zhipuai.api_key = api_key
        if model1 == "chatglm_pro":
            response = zhipuai.model_api.sse_invoke(
                model="chatglm_pro",
                prompt=prompt,
                temperature=0.95,
                top_p=0.7,
                incremental=True
            )
        elif model1 == "chatglm_std":
            response = zhipuai.model_api.sse_invoke(
                model="chatglm_std",
                prompt=prompt,
                temperature=0.95,
                top_p=0.7,
                incremental=True
            )
        elif model1 == "chatglm_lite":
            response = zhipuai.model_api.sse_invoke(
                model="chatglm_lite",
                prompt=prompt,
                temperature=0.95,
                top_p=0.7,
            )
        else:
            response = zhipuai.model_api.sse_invoke(
                model="characterglm",
                meta=bot_info,
                prompt=prompt,
                incremental=True
            )
        str1 = ""
        for event in response.events():
            if event.event == "add":
                str1 += event.data
                # print(event.data)
            elif event.event == "error" or event.event == "interrupted":
                str1 += event.data
                # print(event.data)
            elif event.event == "finish":
                str1 += event.data
                # print(event.data)
                print(event.meta)
            else:
                str1 += event.data
                # print(event.data)
        # print(str1)
        return str1

    # 创建一个异步函数
    async def asyncchatGLM(apiKey, bot_info, prompt, event, setName, text):
        global chatGLMData

        loop = asyncio.get_event_loop()
        # 使用 loop.run_in_executor() 方法来将同步函数转换为异步非阻塞的方式进行处理
        # 第一个参数是执行器，可以是 None、ThreadPoolExecutor 或 ProcessPoolExecutor
        # 第二个参数是同步函数名，后面跟着任何你需要传递的参数
        # result=chatGLM(apiKey,bot_info,prompt)
        with open('settings.yaml', 'r', encoding='utf-8') as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        model1 = result.get("chatGLM").get("model")
        st1 = await loop.run_in_executor(None, chatGLM, apiKey, bot_info, prompt, model1)
        # 打印结果
        # print(result)
        st11 = st1.replace(setName, "指挥")
        logger.info("chatGLM:" + st1)
        if len(st1) < maxTextLen and random.randint(0, 100) < voiceRate and event.type != 'FriendMessage':
            data1 = {}
            data1['speaker'] = speaker

            # print(path)
            st8 = re.sub(r"（[^）]*）", "", st1)  # 使用r前缀表示原始字符串，避免转义字符的问题
            data1["text"] = st8

            try:

                logger.info(f"调用{voicegg}语音合成")
                path = await superVG(data1, voicegg, voiceLangType)
                await bot.send(event, Voice(path=path))
                if withText == True:
                    await bot.send(event, st1, True)
            except Exception as e:
                logger.error(e)

                await bot.send(event, st1, True)
        else:
            if len(st1) > 400:
                await bot.send(event, st1[:100], True)
                await bot.send(event, "🐱‍💻回复可能存在异常，\n请发送 /clear 以清理当前聊天(无需艾特)", True)
                try:
                    prompt.remove(prompt[-1])
                    chatGLMData[event.sender.id] = prompt
                except:
                    logger.error("chatGLM删除上一次对话失败")
                return
            await bot.send(event, st1, True)
        if context == True:
            # 更新该用户prompt
            prompt.append({"role": "assistant", "content": st1})
            # 超过10，移除第一个元素

            if len(prompt) > maxPrompt:
                logger.error("glm prompt超限，移除元素")
                del prompt[0]
                del prompt[0]
            chatGLMData[event.sender.id] = prompt
            # 写入文件
            with open('data/chatGLMData.yaml', 'w', encoding="utf-8") as file:
                yaml.dump(chatGLMData, file, allow_unicode=True)
if __name__ == '__main__':
    with open('settings.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    config=result.get("bot")
    qq=int(config.get('botqq'))
    key=config.get("http-api-key")
    port= int(config.get("http-api-port"))
    bot = Mirai(qq, adapter=WebSocketAdapter(
        verify_key=key, host='localhost', port=port
    ))
    botName = config.get('botName')
    master=int(config.get('master'))



    #芝士logger
    logger=newLogger()
    logger.info("欢迎使用")
    logger.info("项目源地址：https://github.com/avilliai/Bergml")
    logger.info("此项目拆分自Manyana：https://github.com/avilliai/Manyana")
    main(bot,logger)
    try:
        bot.run()
    except Exception as e:
        logger.error(e)
        input("出错，按任意键退出")