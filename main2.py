import asyncio
import json
import logging
import os
import random
import re
import threading

import colorlog
import httpx
import requests
import websockets
import yaml
import google.generativeai as genai
import zhipuai
from mirai import Mirai, WebSocketAdapter, Voice, GroupMessage, At, Plain, Image, FriendMessage
from mirai.bot import Startup
from openai import OpenAI
class CListen(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.mLoop = loop

    def run(self):
        asyncio.set_event_loop(self.mLoop)  # 在新线程中开启一个事件循环

        self.mLoop.run_forever()
def anotherGPT35(prompt,id):
    prompt=prompt[-1]["content"]
    url=f"https://api.shenke.love/api/ChatGPT.php?msg={prompt}&id={id}"
    r = requests.get(url).json()["data"]["message"]
    return {"role": "assistant", "content": r}
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
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    async with httpx.AsyncClient(timeout=200) as client:
        r = await client.post(url=url,json=prompt)
        return {"role":"assistant","content":r.text}

def relolimigpt2(fuckprompt,meta):
    url = "https://api.lolimi.cn/API/AI/c.php?"
    fuckprompt.insert(0, {"role": "user", "content": meta})
    fuckprompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    r = requests.post(url=url, json=fuckprompt)
    return {"role": "assistant", "content": r.text}
def gpt4hahaha(prompt,meta):
    prompt.insert(0, {"role": "user", "content": meta})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt = str(prompt).replace("\"", "%22").replace("\'", "%22")
    url=f"https://api.alcex.cn/API/gpt-4/v2.php?messages={prompt}"
    r = requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
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
def grop(prompt,bot_info):
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt = str(prompt).replace("\"", "%22").replace("\'", "%22")
    url=f"https://api.alcex.cn/API/ai/grop.php?messages={prompt}"
    r=requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
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
def kimi(prompt,bot_info):
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt=str(prompt).replace("\"","%22").replace("\'","%22")

    url = f"https://api.alcex.cn/API/ai/kimi.php?messages={prompt}"
    #print(url)
    r=requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
def qingyan(prompt,bot_info):
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt=str(prompt).replace("\"","%22").replace("\'","%22")

    url = f"https://api.alcex.cn/API/chatglm/?messages={prompt}"
    #print(url)
    r=requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}

def lingyi(prompt,bot_info):
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt=str(prompt).replace("\"","%22").replace("\'","%22")

    url = f"https://api.alcex.cn/API/ai/zeroyi.php?messages={prompt}"
    #print(url)
    r=requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
def stepAI(prompt,bot_info):
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt=str(prompt).replace("\"","%22").replace("\'","%22")

    url = f"https://api.alcex.cn/API/ai/step.php?messages={prompt}"
    #print(url)
    r=requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
def qwen(prompt,bot_info):
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt=str(prompt).replace("\"","%22").replace("\'","%22")

    url = f"https://api.alcex.cn/API/ai/qwen.php?messages={prompt}"
    #print(url)
    r=requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
def gptvvvv(prompt,bot_info):
    prompt.insert(0, {"role": "user", "content": bot_info})
    prompt.insert(1, {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"})
    prompt=str(prompt).replace("\"","%22").replace("\'","%22")

    url = f"https://api.alcex.cn/API/gpt-4/v2.php?messages={prompt}&model=gpt-3.5-turbo"
    #print(url)
    r=requests.get(url).json()
    return {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
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
        print(url2)
        async with httpx.AsyncClient(timeout=40) as client:
            r1 = await client.get(url2)
        with open(path, "wb") as f:
            f.write(r1.content)
        # print(path)
        return path
async def draw3(prompt,path="./test.png"):
    url=f"https://api.alcex.cn/API/ai/novelai.php?tag={prompt}"
    async with httpx.AsyncClient(timeout=40) as client:
        r1 = await client.get(url)
    with open(path, "wb") as f:
        f.write(r1.content)
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
    friendRep=result.get("chatGLM").get("friendRep")
    randomModelPriority = result.get("chatGLM").get("random&PriorityModel")
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
            i = 1
            while i < 10:
                logger.info(f"第{i}次请求")
                try:
                    logger.info("接口1绘画中......")
                    p = await draw1(tag, path)
                    await bot.send(event, Image(path=p), True)
                    logger.info("完成任务，发送图片")
                    return
                except Exception as e:
                    logger.error(e)
                    logger.error("接口1绘画失败.......")
                    # await bot.send(event,"接口1绘画失败.......")
                i += 1
            await bot.send(event, "接口1绘画失败.......")

    @bot.on(GroupMessage)
    async def aidrawf1(event: GroupMessage):
        if str(event.message_chain).startswith("画 "):
            tag = str(event.message_chain).replace("画 ", "")
            if os.path.exists("./data/pictures"):
                pass
            else:
                os.mkdir("./data/pictures")
            path = "data/pictures/" + random_str() + ".png"
            logger.info("发起ai绘画请求，path:" + path + "|prompt:" + tag)
            i = 1
            while i < 10:
                logger.info(f"第{i}次请求")
                try:
                    logger.info("接口2绘画中......")
                    p = await drawe(tag, path)
                    await bot.send(event, Image(path=p), True)
                    return
                except Exception as e:
                    logger.error(e)
                    logger.error("接口2绘画失败.......")
                    # await bot.send(event,"接口2绘画失败.......")
                i += 1
            await bot.send(event, "接口2绘画失败.......")

    @bot.on(GroupMessage)
    async def aidrawf13(event: GroupMessage):
        if str(event.message_chain).startswith("画 "):
            tag = str(event.message_chain).replace("画 ", "")
            if os.path.exists("./data/pictures"):
                pass
            else:
                os.mkdir("./data/pictures")
            path = "data/pictures/" + random_str() + ".png"
            logger.info("发起ai绘画请求，path:" + path + "|prompt:" + tag)
            i = 1
            while i < 10:
                logger.info(f"第{i}次请求")
                try:
                    logger.info("接口3绘画中......")
                    p = await draw3(tag, path)
                    await bot.send(event, Image(path=p), True)
                    return
                except Exception as e:
                    logger.error(e)
                    logger.error("接口3绘画失败.......")
                    # await bot.send(event,"接口2绘画失败.......")
                i += 1
            await bot.send(event, "接口3绘画失败.......")
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
    # 用于chatGLM清除本地缓存
    @bot.on(FriendMessage)
    async def clearPrompt(event: FriendMessage):
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
                if chatGLMCharacters.get(event.sender.id) == "Gemini":
                    text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "").replace("/g", "")
                    for saa in noRes:
                        if text == saa or text=="角色":
                            logger.warning("与屏蔽词匹配，Gemini不回复")
                            return
                    logger.info("gemini开始运行")
                    if text == "" or text == " ":
                        text = "在吗"
                    geminichar = allcharacters.get("Gemini").replace("【bot】", botName).replace("【用户】",
                                                                                               event.sender.member_name)
                    # 构建新的prompt
                    tep = {"role": "user", "parts": [text]}
                    # 获取以往的prompt
                    if event.sender.id in GeminiData and context == True:
                        prompt = GeminiData.get(event.sender.id)
                        prompt.append({"role": "user", 'parts': [text]})
                        # 没有该用户，以本次对话作为prompt
                    else:
                        await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                        prompt = [{"role": "user", "parts": [geminichar]},
                                  {"role": 'model', "parts": ["好的，已了解您的需求~我会扮演好您设定的角色。"]}]
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
                        if text == saa or text=="角色":
                            logger.warning("与屏蔽词匹配，chatGLM不回复")
                            return
                    if text == "" or text == " ":
                        text = "在吗"
                    # 构建新的prompt
                    tep = {"role": "user", "content": text}
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
                else:
                    await modelReply(event, replyModel)
            # 判断模型
            if replyModel == "Gemini" :
                text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "").replace("/g", "")
                for saa in noRes:
                    if text == saa or text=="角色":
                        logger.warning("与屏蔽词匹配，Gemini不回复")
                        return
                logger.info("gemini开始运行")
                if text == "" or text == " ":
                    text = "在吗"
                # 构建新的prompt
                tep = {"role": "user", "parts": [text]}
                geminichar = allcharacters.get("Gemini").replace("【bot】", botName).replace("【用户】",
                                                                                           event.sender.member_name)
                # 获取以往的prompt
                if event.sender.id in GeminiData and context == True:
                    prompt = GeminiData.get(event.sender.id)
                    prompt.append({"role": "user", 'parts': [text]})
                    # 没有该用户，以本次对话作为prompt
                else:
                    await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                    prompt = [{"role": "user", "parts": [geminichar]},
                              {"role": 'model', "parts": ["好的，已了解您的需求~我会扮演好您设定的角色。"]}]
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
                    if text == saa or text=="角色":
                        logger.warning("与屏蔽词匹配，chatGLM不回复")
                        return
                if text == "" or text == " ":
                    text = "在吗"
                # 构建新的prompt
                tep = {"role": "user", "content": text}
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
            else:
                await modelReply(event, replyModel)
    @bot.on(FriendMessage)
    async def friendReply(event: FriendMessage):
        global chatGLMData, chatGLMCharacters, GeminiData, trustUser, trustGroups
        if (glmReply == True or (trustglmReply == True and str(event.sender.id) in trustUser) or friendRep==True):
            if event.sender.id in chatGLMCharacters:
                if chatGLMCharacters.get(event.sender.id) == "Gemini":
                    text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "").replace("/g",
                                                                                                                 "")
                    for saa in noRes:
                        if text == saa or text == "角色":
                            logger.warning("与屏蔽词匹配，Gemini不回复")
                            return
                    logger.info("gemini开始运行")
                    if text == "" or text == " ":
                        text = "在吗"
                    geminichar = allcharacters.get("Gemini").replace("【bot】", botName).replace("【用户】",
                                                                                               event.sender.nickname)
                    # 构建新的prompt
                    tep = {"role": "user", "parts": [text]}
                    # 获取以往的prompt
                    if event.sender.id in GeminiData and context == True:
                        prompt = GeminiData.get(event.sender.id)
                        prompt.append({"role": "user", 'parts': [text]})
                        # 没有该用户，以本次对话作为prompt
                    else:
                        await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                        prompt = [{"role": "user", "parts": [geminichar]},
                                  {"role": 'model', "parts": ["好的，已了解您的需求~我会扮演好您设定的角色。"]}]
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
                        if text == saa or text == "角色":
                            logger.warning("与屏蔽词匹配，chatGLM不回复")
                            return
                    if text == "" or text == " ":
                        text = "在吗"
                    # 构建新的prompt
                    tep = {"role": "user", "content": text}
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

                    setName = event.sender.nickname
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
                else:
                    await modelReply(event, chatGLMCharacters.get(event.sender.id))
            # 判断模型
            if replyModel == "Gemini":
                text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ", "").replace("/g", "")
                for saa in noRes:
                    if text == saa or text == "角色":
                        logger.warning("与屏蔽词匹配，Gemini不回复")
                        return
                logger.info("gemini开始运行")
                if text == "" or text == " ":
                    text = "在吗"
                # 构建新的prompt
                tep = {"role": "user", "parts": [text]}
                geminichar = allcharacters.get("Gemini").replace("【bot】", botName).replace("【用户】",
                                                                                           event.sender.nickname)
                # 获取以往的prompt
                if event.sender.id in GeminiData and context == True:
                    prompt = GeminiData.get(event.sender.id)
                    prompt.append({"role": "user", 'parts': [text]})
                    # 没有该用户，以本次对话作为prompt
                else:
                    await bot.send(event, "即将开始对话，请注意，如果遇到对话异常，请发送 /clear 以清理对话记录(不用艾特)", True)
                    prompt = [{"role": "user", "parts": [geminichar]},
                              {"role": 'model', "parts": ["好的，已了解您的需求~我会扮演好您设定的角色。"]}]
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
                    if text == saa or text == "角色":
                        logger.warning("与屏蔽词匹配，chatGLM不回复")
                        return
                if text == "" or text == " ":
                    text = "在吗"
                # 构建新的prompt
                tep = {"role": "user", "content": text}
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

                setName = event.sender.nickname
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
            else:
                await modelReply(event, replyModel)
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
        await bot.send_friend_message(master,"master指令：\n授权群#群号\n授权#QQ号\n\n用户指令：\n@bot 角色\n画 xxxx")
    @bot.on(GroupMessage)
    async def ttsssss(event: GroupMessage):
        modelScope = ["BT", "塔菲", "阿梓", "otto", "丁真", "星瞳", "东雪莲", "嘉然", "孙笑川", "亚托克斯", "文静", "鹿鸣", "奶绿", "七海", "恬豆",
                      "科比"]
        outVitsSpeakers = "空, 荧, 派蒙, 纳西妲, 阿贝多, 温迪, 枫原万叶, 钟离, 荒泷一斗, 八重神子, 艾尔海森, 提纳里, 迪希雅, 卡维, 宵宫, 莱依拉, 赛诺, 诺艾尔, 托马, 凝光, 莫娜, 北斗, 神里绫华, 雷电将军, 芭芭拉, 鹿野院平藏, 五郎, 迪奥娜, 凯亚, 安柏, 班尼特, 琴, 柯莱, 夜兰, 妮露, 辛焱, 珐露珊, 魈, 香菱, 达达利亚, 砂糖, 早柚, 云堇, 刻晴, 丽莎, 迪卢克, 烟绯, 重云, 珊瑚宫心海, 胡桃, 可莉, 流浪者, 久岐忍, 神里绫人, 甘雨, 戴因斯雷布, 优菈, 菲谢尔, 行秋, 白术, 九条裟罗, 雷泽, 申鹤, 迪娜泽黛, 凯瑟琳, 多莉, 坎蒂丝, 萍姥姥, 罗莎莉亚, 留云借风真君, 绮良良, 瑶瑶, 七七, 奥兹, 米卡, 夏洛蒂, 埃洛伊, 博士, 女士, 大慈树王, 三月七, 娜塔莎, 希露瓦, 虎克, 克拉拉, 丹恒, 希儿, 布洛妮娅, 瓦尔特, 杰帕德, 佩拉, 姬子, 艾丝妲, 白露, 星, 穹, 桑博, 伦纳德, 停云, 罗刹, 卡芙卡, 彦卿, 史瓦罗, 螺丝咕姆, 阿兰, 银狼, 素裳, 丹枢, 黑塔, 景元, 帕姆, 可可利亚, 半夏, 符玄, 公输师傅, 奥列格, 青雀, 大毫, 青镞, 费斯曼, 绿芙蓉, 镜流, 信使, 丽塔, 失落迷迭, 缭乱星棘, 伊甸, 伏特加女孩, 狂热蓝调, 莉莉娅, 萝莎莉娅, 八重樱, 八重霞, 卡莲, 第六夜想曲, 卡萝尔, 姬子, 极地战刃, 布洛妮娅, 次生银翼, 理之律者, 真理之律者, 迷城骇兔, 希儿, 魇夜星渊, 黑希儿, 帕朵菲莉丝, 天元骑英, 幽兰黛尔, 德丽莎, 月下初拥, 朔夜观星, 暮光骑士, 明日香, 李素裳, 格蕾修, 梅比乌斯, 渡鸦, 人之律者, 爱莉希雅, 爱衣, 天穹游侠, 琪亚娜, 空之律者, 终焉之律者, 薪炎之律者, 云墨丹心, 符华, 识之律者, 维尔薇, 始源之律者, 芽衣, 雷之律者, 苏莎娜, 阿波尼亚, 陆景和, 莫弈, 夏彦, 左然".replace(
            " ", "").split(",")
        fireflySpeaker = ['消沉的患者_ZH', '九条孝行_JP', '岩夫_EN', '芷巧_EN', '阿扎尔_EN', '芙萝拉_JP', '花火_ZH', '萨姆_EN', '邓恩_JP',
                          '轰大叔_ZH', '重佐_JP', '希儿_ZH', '希露瓦_ZH', '捕头_EN', '一之濑明日奈', '珐露珊母亲_JP', '长生_ZH', '铁尔南_JP',
                          '理村爱理', '柴田_JP', '可可利亚_EN', '艾伯特_JP', '阿圆_JP', '流萤_EN', '舍利夫_EN', '耕一_ZH', '米卡_EN', '埃洛伊_EN',
                          '科尔特_ZH', '裁判_EN', '戴因斯雷布_EN', '高善_JP', '狮子堂泉', '托帕&账账_ZH', '埃舍尔_ZH', '空井咲', '接笏_ZH', '佐天泪子',
                          '百闻_JP', '杰帕德_JP', '柊千里_JP', '博来_EN', '消沉的患者_JP', '田铁嘴_JP', '梦主_EN', '娜塔莎_JP', '阿守_ZH',
                          '娜比雅_ZH', '镜流_ZH', '珊瑚_EN', '昆钧_JP', '朔次郎_EN', '琳妮特_JP', '木木_JP', '查尔斯_ZH', '紫月季_EN',
                          '留云借风真君_ZH', '莫娜_ZH', '克雷薇_ZH', '霍夫曼_ZH', '净砚_EN', '桑博_EN', '弗洛朗_JP', '埃斯蒙德_JP',
                          'shajinma_ZH', '艾伦_EN', '甘雨_EN', '停云_JP', '拉赫曼_JP', '海妮耶_JP', '羽生田千鹤_JP', '莲见（体操服）', '卡莉娜_JP',
                          '罗莎莉亚_ZH', '隐书_ZH', '金人会长_EN', '观众_JP', '大隆_EN', '凯西娅_JP', '木木_EN', '深渊使徒_EN', '秋泉红叶',
                          '丹吉尔_ZH', '卢卡奇_JP', '温迪_ZH', '室笠朱音(茜)', '慧心_JP', '老章_JP', 'shajinma_EN', '拉赫曼_ZH', '大慈树王_ZH',
                          '夏洛蒂_ZH', '小野寺_JP', '皮特_JP', '今谷三郎_JP', '广大_JP', '星_ZH', '林尼_ZH', '坎蒂丝_ZH', '吴船长_ZH', '胡尚_EN',
                          '浅黄睦月', '公司的业务员代表_JP', '若叶日向', '乌宰尔_JP', '萨赫哈蒂_EN', '斯科特_ZH', '法拉娜_ZH', '朝颜花江', '宏达_EN',
                          '芙宁娜_ZH', '霄老大_EN', '甘雨_JP', '娜德瓦_ZH', '宁禄_JP', '贝雅特丽奇_JP', '螺丝咕姆_JP', '雷泽_EN', '恕筠_EN',
                          '金忽律_ZH', '帕维耶_EN', '间宵时雨', '巨大谜钟_EN', '黑泽京之介_ZH', '菲谢尔_ZH', '阿山婆_JP', '萨姆_ZH', '砂金_JP',
                          '舍利夫_ZH', '绮良良_ZH', '赛索斯_JP', '上杉_JP', '炒冷饭机器人_ZH', '巴达维_ZH', '宫子（泳装）', '杜吉耶_EN', '秤亚津子',
                          '古关忧', '将司_EN', '黛比_JP', '玛吉_JP', '丽莎_ZH', '维利特_EN', '知贵_JP', '记忆中的声音_ZH', '夜兰_ZH', '木南杏奈_EN',
                          '凯亚_ZH', '韵宁_EN', '巴尔塔萨_JP', '波提欧_JP', '忧（泳装）', '丹羽_EN', '老高_EN', '戴因斯雷布_ZH', '乔瓦尼_ZH',
                          '日奈（泳装）', '角楯花凛', '阿汉格尔_ZH', '钱德拉_JP', '才羽桃井', '莫塞伊思_JP', '光之_JP', '幻胧_ZH', '立本_EN', '河和静子',
                          '娜塔莎_EN', '波提欧_EN', '讨嫌的小孩_ZH', '科林斯_ZH', '北斗_JP', '烟绯_EN', '班尼特_ZH', '安静的宾客_JP', '劳维克_JP',
                          '琴_JP', '黑天鹅_JP', '丹恒•饮月_EN', '药王秘传魁首_ZH', '黛比_ZH', '辛焱_EN', '丹枢_EN', '重云_ZH', '木南杏奈_ZH',
                          '毗伽尔_JP', '卡卡瓦夏的姐姐_EN', '莱欧斯利_ZH', '黑田_ZH', '柯莱_EN', '造物翻译官_JP', '艾伯特_EN', '小野寺_ZH', '徐六石_ZH',
                          '葵_ZH', '罗刹_EN', '鹤城（泳装）', '雅各_JP', '响（应援团）', '凯西娅_EN', '札齐_ZH', '副警长_ZH', '荒谷_EN', '九条裟罗_ZH',
                          '瑞安维尔_JP', '接笏_EN', '罗莎莉亚_JP', '维格尔_EN', '裁判_JP', '新之丞_EN', '若心_JP', '温和的声音_ZH', '布洛克_JP',
                          '菲谢尔_JP', '神里绫人_JP', '立本_ZH', '沙扎曼_ZH', '卡波特_ZH', '深渊法师_JP', '重佐_ZH', '琳琅_JP', '维多利亚_EN',
                          '尚博迪克_EN', '宛烟_ZH', '鹿野院平藏_ZH', '博士_JP', '费迪南德_JP', '伊莎朵_ZH', '莎拉_EN', '老戴_JP', '拉齐_JP',
                          '削月筑阳真君_JP', '绮良良_JP', '小乐_ZH', '芙卡洛斯_EN', '玻瑞亚斯_ZH', '安柏_JP', '博来_ZH', '伯恩哈德_ZH', '锭前纱织',
                          '斯薇塔_ZH', '夏彦', '加拉赫_JP', '砂糖_ZH', '法赫尔_JP', '法哈德_EN', '白露_EN', '阿扎木_EN', '提纳里_EN', '商人_EN',
                          '瓦尔特_JP', '瓦乐瑞娜_ZH', '加福尔_JP', '莺儿_EN', '毗伽尔_EN', '海芭夏_ZH', '胡尚_ZH', '劳伦斯_ZH', '毗伽尔_ZH',
                          '白术_EN', '杰娜姬_JP', '芹香（正月）', '胡尚_JP', '小乐_JP', '派蒙_EN', '真_JP', '元太_EN', '瑶瑶_JP', '狐妖_JP',
                          '捕快_ZH', '阿尔卡米_EN', '老孟_JP', '安西_EN', '赤司纯子', '皮特_ZH', '桐生桔梗', '阿祇_ZH', '薇若妮卡_EN', '菲米尼_EN',
                          '西衍先生_EN', '刻薄的小孩_JP', '半夏_EN', '警长_JP', '札齐_EN', '石头老板_JP', '老孟_ZH', '大肉丸_ZH', '符玄_EN',
                          '古谷升_JP', '贝雅特丽奇_EN', '卡萝蕾_EN', '佩拉_JP', '花角玉将_EN', '桂乃芬_ZH', '贝雅特丽奇_ZH', '凯西娅_ZH', '埃斯蒙德_EN',
                          '杜吉耶_JP', '胡桃_ZH', '蒂埃里_JP', '纳菲斯_JP', '琳琅_EN', '嘉义_ZH', '温世玲_JP', '今谷佳祐_JP', '肢体评委_EN',
                          '伊利亚斯_JP', '扇喜葵', '劳维克_ZH', '那维莱特_ZH', '卡莉娜_ZH', '香菱_ZH', '齐米亚_JP', '迪娜泽黛_EN', '岩明_ZH',
                          '阿鸠_JP', '马姆杜_JP', '面具_EN', '北斗_ZH', '纳比尔_EN', '歌蒂_JP', '伯恩哈德_JP', '塞萨尔的日记_JP', '稻生_EN',
                          '卡芙卡_ZH', '罗刹_JP', '年长的患者_JP', '玲可_ZH', '往昔的回声_JP', '筑梦师_EN', '卡莉娜_EN', '安西_JP', '年长的患者_ZH',
                          '萨赫哈蒂_ZH', '阿仁_JP', '常九爷_JP', '塞萨尔的日记_ZH', '发抖的流浪者_EN', '阿雩_EN', '奥泰巴_ZH', '久利须_EN', '朔次郎_JP',
                          '莎拉_ZH', '小仓澪_ZH', '菲米尼_ZH', '丹花伊吹', '巴达维_EN', '迈蒙_EN', '阿伟_EN', '音濑小玉', '托帕&账账_JP', '萍姥姥_ZH',
                          '巴穆恩_EN', '白石歌原', '厨子_EN', '悠策_EN', '萨齐因_EN', '妮露_JP', '狐妖_EN', '阿蕾奇诺_EN', '水羽三森',
                          '浮游风蕈兽·元素生命_ZH', '阿守_JP', '元太_ZH', '福尔茨_ZH', '狐妖_ZH', '星期日_JP', '安武_EN', '阿来_ZH', '北村_JP',
                          '唐娜_ZH', '纳菲斯_EN', '白洲梓', '妮露_ZH', '楠楠_JP', '拍卖会工作人员_JP', '布洛妮娅_EN', '陆行岩本真蕈·元素生命_EN',
                          '刻晴_EN', '笼钓瓶一心_EN', '枫原万叶_JP', '深渊法师_ZH', '刃_ZH', '卡维_EN', '欧菲妮_ZH', '长生_JP', '鹿野院平藏_JP',
                          '天叔_EN', '浮烟_ZH', '马姆杜_ZH', '漱玉_JP', '伊萨克_EN', '楚仪_JP', '考特里亚_JP', '古田_EN', '宇泽玲纱', '新之丞_ZH',
                          '华劳斯_JP', '星稀_EN', '宁禄_ZH', '梅里埃_JP', '迪肯_JP', '长生_EN', '丹羽_JP', '闲云_ZH', '希格雯_ZH', '洛恩_EN',
                          '厨子_JP', '奇妙的船_EN', '消沉的患者_EN', '莫里斯_JP', '帕姆_EN', '老高_JP', '时（兔女郎）', '明曦_JP', '阿斯法德_JP',
                          '维卡斯_JP', '三田_EN', '式大将_ZH', '拉伊德_EN', '辛焱_JP', '迪希雅_ZH', '筑梦师_ZH', '卡布斯_ZH', '托马_ZH',
                          '芭芭拉_ZH', '星稀_ZH', '塔杰·拉德卡尼_JP', '丹恒_ZH', '绿芙蓉_EN', '谢赫祖拜尔_ZH', '西衍先生_JP', '梦主_JP', '歌蒂_ZH',
                          '库塞拉_JP', '大辅_EN', '波洛_ZH', '巴哈利_EN', '卡卡瓦夏_EN', '贝努瓦_EN', '老芬奇_ZH', '辛克尔_JP', '霍夫曼_EN',
                          '布尔米耶_JP', '公输师傅_ZH', '玛文_EN', '被俘的信徒_JP', '慈祥的女声_ZH', '恶龙_ZH', '回声海螺_ZH', '埃勒曼_EN',
                          '真理医生_ZH', '爱德华医生_ZH', '奇妙的船_ZH', '药子纱绫', '法赫尔_EN', '神里绫华_EN', '埃泽_ZH', '昆恩_JP', '夏妮_ZH',
                          '陆景和', '信博_JP', '科玫_JP', '言笑_JP', '罗莎莉亚_EN', '旁白_ZH', '嘉明_EN', '伊丝黛莱_ZH', '伊原木好美', '玛达赫_ZH',
                          '卡布斯_JP', '凯瑟琳_JP', '康纳_EN', '青镞_ZH', '罗巧_EN', '鬼方佳代子', '久岐忍_ZH', '稻生_JP', '厨子_ZH',
                          '猎犬家系成员_EN', '卯师傅_EN', '行秋_ZH', '浮游水蕈兽·元素生命_JP', '塞琉斯_EN', '久岐忍_EN', '埃泽_EN', '乌维_EN',
                          '柊千里_ZH', '行秋_EN', '马姆杜_EN', '花火_EN', '今谷香里_JP', '阿基维利_JP', '垃垃撕圾_ZH', '保姆_JP',
                          '拉格沃克•夏尔•米哈伊尔_EN', '瓦乐瑞娜_EN', '舒翁_JP', '天雨亚子', '莺儿_ZH', '有乐斋_EN', '捕快_EN', '剑阵中的声音_EN',
                          '玥辉_EN', '斑目百兵卫_JP', '阿蕾奇诺_ZH', '赛索斯_EN', '诗筠_EN', '商人_ZH', '大和田_JP', '塔里克_EN', '艾文_ZH',
                          '吉莲_EN', '砂金_ZH', '阿慈谷日富美', '希格雯_JP', '月雪宫子', '优菈_ZH', '公主_EN', '维多克_EN', '拉齐_ZH', '理查_JP',
                          '希儿_EN', '行秋_JP', '钟表小子_JP', '重云_JP', '阿幸_EN', '界种科科员_JP', '藿藿_EN', '钟表匠_JP', 'asideb_EN',
                          '里卡尔_EN', '塔杰·拉德卡尼_ZH', '埃勒曼_JP', '小钩晴', '卡玛尔_JP', '商华_ZH', '帕斯卡_EN', '银枝_ZH', '米凯_ZH',
                          '嚣张的小孩_ZH', '达达利亚_JP', '塔杰·拉德卡尼_EN', '加藤洋平_ZH', '蒂玛乌斯_ZH', '阿维丝_JP', '大慈树王_JP', '荒泷一斗_ZH',
                          '鹿野奈奈_EN', '史瓦罗_EN', '常九爷_EN', '阿往_ZH', '克拉拉_ZH', '绘星_EN', '杜拉夫_ZH', '引导员_JP', '塞塔蕾_JP',
                          '露子_JP', '夜兰_JP', '银狼_JP', '伊洁贝儿_JP', '竺子_ZH', '阿夫辛_EN', '伊落玛丽', '荒泷一斗_JP', '荒泷一斗_EN',
                          '阿雩_JP', '石头老板_ZH', '白露_JP', '旅行者_ZH', '亚卡巴_ZH', '九条镰治_ZH', '萨福万_JP', '苍老的声音_JP', '百识_JP',
                          '陸八魔阿露', '霄翰_EN', '小川_JP', '西瓦尼_ZH', '花冈柚子', '冰室濑名', '吴船长_EN', '勘解由小路紫', '克洛琳德_ZH', '素裳_JP',
                          '青镞_JP', '拉赫曼_EN', '爱贝尔_EN', '艾米绮_ZH', '伊萨克_ZH', '伊利亚斯_EN', '安托万_JP', '维多利亚_ZH', '阿泰菲_EN',
                          '达达利亚_EN', '安静的宾客_ZH', '陆行岩本真蕈·元素生命_JP', '青雀_ZH', '侯章_ZH', '诺艾尔_JP', '星期日_EN', '帕维耶_ZH',
                          '界种科科员_EN', '伽吠毗陀_EN', '智树_ZH', '暮夜剧团团长_JP', '魔女N_JP', '斯万_JP', '银杏_ZH', '戴派_EN', '维尔芒_EN',
                          '慧心_ZH', '沃特林_JP', '阿佩普_EN', '艾尔海森_JP', '女士_ZH', '拉格沃克•夏尔•米哈伊尔_ZH', '枫_JP', '博士_ZH', '温迪_JP',
                          '梅里埃_ZH', '绮珊_EN', '琳妮特_EN', '辛克尔_EN', '柴田_EN', '天见和香', '阿扎尔_JP', '芭芭拉_JP', '莱依拉_JP', '莱昂_JP',
                          '艾丝妲_ZH', '葛瑞丝_JP', '松烟_JP', '珊瑚宫心海_ZH', '钱德拉_EN', '乐平波琳_EN', '埃舍尔_JP', '玥辉_JP', '阿守_EN',
                          '贾拉康_JP', '阿巴图伊_ZH', '拉伊德_ZH', '艾薇拉_EN', '宵宫_ZH', '女声_EN', '布洛妮娅_ZH', '黄泉_ZH', '安托万_EN',
                          '玛塞勒_JP', '慈祥的女声_JP', '卢卡_JP', '恕筠_JP', '薇娜_EN', '阿尼斯_JP', '夏洛蒂_EN', '阿贝多_EN', '丝柯克_EN',
                          '迪娜泽黛_JP', '砂糖_EN', '卡维_JP', '御坂美琴', '羽沼真琴', '阿祇_EN', '年长的患者_EN', '神里绫华_ZH', '维多利亚_JP',
                          '维尔芒_ZH', '柊千里_EN', '玛乔丽_JP', '那维莱特_EN', '坎蒂丝_EN', '重佐_EN', '雷泽_JP', '库斯图_JP', '寒鸦_ZH',
                          '天目十五_JP', '焦躁的丹鼎司医士_EN', '副警长_JP', '燕翠_EN', '初音未来', '空_ZH', '莫塞伊思_EN', '艾米绮_JP', '猎犬家系成员_ZH',
                          '莱提西娅_JP', '巴穆恩_ZH', '纳比尔_ZH', '法伊兹_EN', '刻薄的小孩_ZH', '诗筠_JP', '钟表匠_ZH', '千织_EN',
                          '祖莉亚·德斯特雷_JP', '华劳斯_ZH', '慈祥的女声_EN', '塞塔蕾_ZH', '造物翻译官_EN', '艾丝妲_JP', '费迪南德_ZH', '徐六石_EN',
                          '朱里厄_JP', '真白（泳装）', '阿旭_JP', '萨齐因_ZH', '维格尔_ZH', '新之丞_JP', '维卡斯_ZH', '七七_JP', '侯章_JP',
                          '茂才公_EN', '顺吉_EN', '田铁嘴_ZH', '宏达_JP', '法拉娜_EN', '巴穆恩_JP', '茂才公_ZH', '奥兹_EN', '一平_ZH', '戒野美咲',
                          '韦尔纳_ZH', '天叔_JP', '阿汉格尔_EN', '小贩_JP', '隐书_EN', '珐露珊_ZH', '白老先生_EN', '萍姥姥_EN', '菜菜子_EN',
                          '派蒙_ZH', '伊迪娅_JP', '迪尔菲_EN', '叶德_JP', '伽吠毗陀_JP', '银狼_EN', '掘掘博士_EN', '嘉义_JP', '珐露珊_EN',
                          '基娅拉_JP', '托帕&账账_EN', '兴修_JP', '焦躁的丹鼎司医士_ZH', '唐娜_JP', '公输师傅_JP', '贡达法_JP', '艾丝妲_EN',
                          '神智昏乱的云骑_EN', '祖莉亚·德斯特雷_ZH', '三月七_EN', '天目十五_EN', '伦纳德_JP', '长门幸子_EN', '小组长_JP', '才羽绿',
                          '嘉义_EN', '咲（泳装）', '露尔薇_EN', '旅行者_JP', '捕快_JP', '笼钓瓶一心_ZH', '黑馆晴奈', '蒂埃里_ZH', '青雀_EN',
                          '妮欧莎_JP', '加拉赫_ZH', '薇尔_ZH', '守护者的意志_JP', '莎塔娜_EN', '阿尼斯_ZH', '波洛_EN', '迪娜泽黛_ZH', '芭芭拉_EN',
                          '大毫_EN', '阿露（正月）', '卯师傅_ZH', '讨嫌的小孩_EN', '朱达尔_JP', '雷电将军_ZH', '银杏_JP', '下仓惠', '藿藿_JP',
                          '加萨尼_EN', '夏妮_EN', '停云_EN', '埃德_EN', '罗伊斯_EN', '维卡斯_EN', '特纳_JP', '卡布斯_EN', '玛乔丽_ZH',
                          '若藻（泳装）', '慧心_EN', '法哈德_JP', '有原则的猎犬家系成员_EN', '朋义_EN', '悠策_JP', '丹吉尔_EN', '翡翠_JP',
                          '拉格沃克•夏尔•米哈伊尔_JP', '西尔弗_JP', '大隆_JP', '暮夜剧团团长_EN', '江蓠_EN', '杰洛尼_JP', '面具_JP', '奥泰巴_EN',
                          '菲谢尔_EN', '艾丽_ZH', '爱贝尔_ZH', '大和田_ZH', '哲平_JP', '可莉_ZH', '绮良良_EN', '阮•梅_ZH', '宵宫_JP', '烟绯_JP',
                          '埃泽_JP', '乌宰尔_EN', '三月七_JP', '卡维_ZH', '阿佩普_ZH', '凝光_JP', '镜流_EN', '有原则的猎犬家系成员_ZH', '奥兹_JP',
                          '费索勒_ZH', '艾迪恩_JP', '鬼婆婆_EN', '诺艾尔_EN', '七七_EN', '艾莉丝_ZH', '圆堂志美子', '各务千寻', '卡波特_EN',
                          '薇若妮卡_ZH', '埃勒曼_ZH', '杜吉耶_ZH', '斯坦利_JP', '希格雯_EN', '被俘的信徒_ZH', '镜流_JP', '冒失的帕拉德_JP', '古山_JP',
                          '银镜伊织', '斯坦利_EN', '淮安_JP', '露子_ZH', '西拉杰_ZH', '伊庭_JP', '阿洛瓦_ZH', '景元_ZH', '阿往_JP', '严苛评委_ZH',
                          '丝柯克_JP', '七叶寂照秘密主_EN', '泽维尔_EN', '发抖的流浪者_JP', '金忽律_EN', '紫月季_ZH', '歌住樱子', '徐六石_JP',
                          '莫塞伊思_ZH', '岩夫_ZH', '阿尼斯_EN', '卯师傅_JP', '重云_EN', '木木_ZH', '阿基维利_EN', '菲约尔_ZH', '被俘的信徒_EN',
                          '羽川莲见', '特纳_EN', '石头_EN', '里卡尔_ZH', '巴哈利_ZH', '守月铃美', '岩夫_JP', '五郎_ZH', '信使_JP', '安守实里',
                          '艾尔海森_EN', '艾莉丝_EN', '遥香（正月）', '云叔_ZH', '村田_JP', '阿兰_ZH', '埃洛伊_ZH', '掇星攫辰天君_JP', '沃特林_ZH',
                          '齐米亚_ZH', '埃德蒙多_EN', '亚卡巴_JP', '枫原景春_JP', '温迪_EN', '瑞安维尔_EN', '斯薇塔_EN', '七叶寂照秘密主_JP', '凝光_ZH',
                          '明曦_ZH', '昆钧_ZH', '梁沐_JP', '科玫_EN', '阮•梅_EN', '迪希雅_EN', '长野原龙之介_EN', '鳄渊明里', '捕头_ZH',
                          '迪卢克_JP', '茂才公_JP', '日富美（泳装）', '德沃沙克_JP', '海芭夏_EN', '迪奥娜_EN', '可可利亚_ZH', '荒谷_ZH', '迪肯_EN',
                          '埃德_ZH', '莺儿_JP', '寒腿叔叔_ZH', '德田_ZH', '讨嫌的小孩_JP', '九条镰治_EN', '凯瑟琳_EN', '枫原万叶_ZH', '迪希雅_JP',
                          '知更鸟_JP', '九条裟罗_JP', '伊草遥香', '安东尼娜_ZH', '今谷香里_EN', '康纳_ZH', '巴达维_JP', '阿伟_JP', '雅各_ZH',
                          '艾伦_ZH', '佩拉_EN', '星际和平播报_EN', '刀疤刘_EN', '稻城萤美_ZH', '畅畅_EN', '木南杏奈_JP', '星际和平播报_ZH', '波提欧_ZH',
                          '悠策_ZH', '里卡尔_JP', '凯瑟琳_ZH', '霄翰_JP', '会场广播_EN', '贝努瓦_ZH', '瑶瑶_ZH', '玛格丽特_ZH', '男声_ZH',
                          '洛伦佐_EN', '库塞拉的信件_JP', '嘉玛_EN', '安西_ZH', '艾迪恩_ZH', '托克_EN', '阿贝多_JP', '青镞_EN', '葵_JP',
                          '莱昂_ZH', '爱德琳_EN', '男声_EN', '克拉拉_EN', '姬子_EN', '夏沃蕾_JP', '五郎_JP', '查尔斯_EN', '德拉萝诗_JP',
                          '炒冷饭机器人_JP', '雕像_EN', '漱玉_EN', '净砚_JP', '寒鸦_JP', '玻瑞亚斯_EN', '黑田_JP', '阿伟_ZH', '加福尔_ZH',
                          '林尼_JP', '警长_EN', '奥列格_ZH', '古山_EN', '有乐斋_JP', '刻晴_ZH', '居勒什_EN', '波洛_JP', '戈尔代_JP', '伊织（泳装）',
                          '荧_EN', '阿斯法德_ZH', '阿扎木_JP', '信使_EN', '绍祖_JP', '恕筠_ZH', '彦卿_ZH', '幻胧_JP', '阿夫辛_JP', '黄泉_EN',
                          '炒冷饭机器人_EN', '罗伊斯_JP', '云堇_ZH', '冷漠的男性_JP', '铁尔南_ZH', '西拉杰_EN', '若心_ZH', '巫女_JP', '阿娜耶_ZH',
                          '阿金_EN', '卡莉露_JP', '蒂埃里_EN', '乾玮_JP', '女士_EN', '剑先鹤城', '莱欧斯利_EN', '五郎_EN', '史瓦罗_JP',
                          '肢体评委_JP', '巴列维_JP', '杜拉夫_JP', '嚣张的小孩_JP', '维利特_JP', '驭空_EN', '恶龙_EN', '丹枢_ZH', '纯也_EN',
                          '麦希尔_ZH', '菲约尔_EN', '雪衣_EN', '迪尔菲_ZH', '奥列格_EN', '阿巴图伊_JP', '侯章_EN', '云堇_JP', '一平_JP',
                          '阿拉夫_ZH', '伊庭_ZH', '塞萨尔的日记_EN', '久岐忍_JP', '浮游风蕈兽·元素生命_JP', '瓦乐瑞娜_JP', '古田_JP', '神智昏乱的云骑_JP',
                          '龙二_EN', '迪肯_ZH', '巨大谜钟_JP', '旅行者_EN', '拍卖师_ZH', '近卫南', '德沃沙克_ZH', '村田_EN', '艾伯特_ZH', '言笑_ZH',
                          '伯恩哈德_EN', '佩拉_ZH', '查宝_JP', '云叔_JP', '丹恒_EN', '寒腿叔叔_JP', '砂狼白子', '镜中人_JP', '流萤_JP', '迈勒斯_JP',
                          '长野原龙之介_JP', '砂糖_JP', '阿兰_JP', '北村_EN', '亚卡巴_EN', '赛诺_EN', '素裳_EN', '垃垃撕圾_EN', '槌永日和',
                          '三田_JP', '史瓦罗_ZH', '埃德_JP', '吴船长_JP', '翡翠_EN', '鬼婆婆_JP', '罗刹_ZH', '莱依拉_ZH', '蒂玛乌斯_JP',
                          '手岛_JP', '枫原景春_EN', '不破莲华', '捕头_JP', '娜维娅_ZH', '狼哥_JP', '玲可_EN', '派蒙_JP', '雪衣_ZH', '李丁_ZH',
                          '奥空绫音', '迈蒙_JP', '梓（泳装）', '夏沃蕾_ZH', '八重神子_EN', '梅里埃_EN', '乾玮_EN', '舒伯特_JP', '连烟_EN', '塞德娜_EN',
                          '嘉玛_ZH', '绘星_JP', '寒腿叔叔_EN', '界种科科员_ZH', '火宫千夏', '珠函_ZH', '望雅_ZH', '安静的宾客_EN', '信使_ZH',
                          '记忆中的声音_EN', '黑天鹅_EN', '美游（泳装）', '香菱_EN', '连烟_JP', '奥兹_ZH', '魈_EN', '宵宫_EN', '宁禄_EN',
                          '法伊兹_ZH', '稻城萤美_EN', '蒂玛乌斯_EN', '刻晴_JP', '忠诚的侍从_JP', '琴_EN', '姬木梅露', '龙二_JP', '一平_EN',
                          '海妮耶_EN', '艾尔海森_ZH', '连烟_ZH', '药王秘传魁首_JP', '白术_ZH', '小川_EN', '凯亚_JP', '驭空_JP', '玛达赫_JP',
                          '甘雨_ZH', '阿来_JP', '怀疑的患者_ZH', '库塞拉的信件_EN', '阿圆_ZH', '黑崎小雪', '塞塔蕾_EN', '旁白_JP', '驭空_ZH',
                          '大慈树王_EN', '闲云_JP', '泽田_ZH', '纳西妲_ZH', '邓恩_ZH', '白子（骑行）', '银狼_ZH', '海妮耶_ZH', '玛格丽特_JP',
                          '法伊兹_JP', '掇星攫辰天君_ZH', '巴尔塔萨_EN', '悦_JP', '法拉娜_JP', '帕姆_JP', '丰见小鸟', '望雅_EN', '艾洛迪_EN',
                          '老戴_ZH', '朱城瑠美', '空_EN', '浣溪_ZH', '杰洛尼_EN', '维尔德_JP', '笼钓瓶一心_JP', '虎克_ZH', '哲平_EN', '烟绯_ZH',
                          '伦纳德_ZH', '可莉_EN', '艾洛迪_ZH', '九条孝行_EN', '佳代子（正月）', '景元_JP', '天叔_ZH', '池仓玛丽娜', '宏达_ZH',
                          '向导_JP', '迪卢克_EN', '正人_JP', '洛恩_JP', '阿尔卡米_ZH', '悦_ZH', '伦纳德_EN', '科尔特_JP', '贝努瓦_JP', '老戴_EN',
                          '玛达赫_EN', '千织_JP', '沙坎_EN', '卡莉露_ZH', '浮游水蕈兽·元素生命_ZH', '瓦尔特_EN', '阿往_EN', '明星日鞠', '托马_JP',
                          '莎拉_JP', '独孤朔_EN', '芙卡洛斯_ZH', '尤利安_JP', '艾琳_ZH', '苍森美弥', '卡卡瓦夏_ZH', '若心_EN', '安东尼娜_JP', '柚岛夏',
                          '卡西迪_ZH', '闲云_EN', '叶德_ZH', '符玄_ZH', '拍卖师_JP', '迪奥娜_JP', '绿芙蓉_JP', '泽田_JP', '西拉杰_JP',
                          '尤利安_ZH', '卡西迪_JP', '纯也_JP', '艾琳_EN', '白老先生_ZH', '星稀_JP', '回声海螺_EN', '夏洛蒂_JP', '多莉_JP',
                          '老芬奇_JP', '阿兰_EN', '阿圆_EN', '丹恒•饮月_JP', '托帕_EN', '飞鸟马时', '赛诺_JP', '雅各_EN', '拍卖会工作人员_ZH',
                          '库斯图_ZH', '大肉丸_JP', '松浦_JP', '伊德里西_EN', '科尔特_EN', '帕斯卡_JP', '理水叠山真君_ZH', '斯科特_EN',
                          '留云借风真君_EN', '阿娜耶_EN', '深渊使徒_ZH', '斯嘉莉_ZH', '冥火大公_ZH', '西衍先生_ZH', '卓也_EN', '爱德华医生_EN',
                          '李丁_JP', '钟表小子_ZH', '卓也_ZH', '阿扎尔_ZH', '流浪者_EN', '传次郎_EN', '尤苏波夫_ZH', '春原心奈', '威严的男子_EN',
                          '孟迪尔_JP', '帕维耶_JP', '鲁哈维_EN', '艾薇拉_ZH', '狼哥_EN', '阿佩普_JP', '托帕_JP', '石头_ZH', '赛诺_ZH',
                          '马洛尼_EN', '埃洛伊_JP', '卡卡瓦夏的姐姐_JP', '龙二_ZH', '星际和平播报_JP', '星_EN', '萨赫哈蒂_JP', '米卡_JP',
                          '苍老的声音_EN', '埃尔欣根_EN', '阿蕾奇诺_JP', '商人_JP', '米沙_ZH', '塞琉斯_ZH', '魔女N_EN', '将司_JP', '贾拉康_ZH',
                          '鹫见芹奈', '杜拉夫_EN', '尚博迪克_JP', '巴蒂斯特_ZH', '星期日_ZH', '丹羽_ZH', '芹奈（圣诞）', '神里绫华_JP', '今谷香里_ZH',
                          '公主_JP', '黄泉_JP', '优香（体操服）', '戴因斯雷布_JP', '埃尔欣根_JP', '光之_ZH', '春原瞬', '丽莎_EN', '阿贝多_ZH',
                          '淮安_EN', '玻瑞亚斯_JP', '副警长_EN', '守护者的意志_ZH', '莱斯格_JP', '砂金_EN', '木村_ZH', '独眼小僧_EN', '三月七_ZH',
                          '稻城萤美_JP', '银枝_EN', '伊利亚斯_ZH', '伊迪娅_ZH', 'asideb_ZH', '欧菲妮_JP', '尾巴_EN', '艾文_JP', '乌维_ZH',
                          '真理医生_JP', '卡萝蕾_ZH', '昆钧_EN', '阿山婆_EN', '丹枢_JP', '会场广播_ZH', '乔瓦尼_EN', '坎蒂丝_JP', '八重神子_JP',
                          '维多克_JP', '福尔茨_JP', '春日椿', '巴沙尔_JP', '艾莉丝_JP', '佐西摩斯_EN', '银杏_EN', '莱提西娅_EN', '老克_JP', '杏山和纱',
                          '卡莉露_EN', '某人的声音_JP', '舒伯特_EN', '阿洛瓦_EN', '静子（泳装）', '伊丝黛莱_EN', '德拉萝诗_ZH', '黑天鹅_ZH', '吉莲_ZH',
                          '严苛评委_EN', '丹吉尔_JP', '科林斯_JP', '姬子_JP', '筑梦师_JP', '老章_EN', '智树_JP', '理查_ZH', '大毫_ZH',
                          '真理医生_EN', '吉莲_JP', '素裳_ZH', '白露_ZH', '昆恩_EN', '梦主_ZH', '凝光_EN', '霞泽美游', '阿巴图伊_EN', '塞琉斯_JP',
                          '往昔的回声_EN', '帕帕克_JP', '查尔斯_JP', '萍姥姥_JP', '知更鸟_EN', '佩尔西科夫_JP', '贡达法_EN', '杰娜姬_EN', '荧_ZH',
                          '维利特_ZH', '浮游水蕈兽·元素生命_EN', '李丁_EN', '枣伊吕波', '劳伦斯_EN', '伊庭_EN', '迈勒斯_EN', '八重神子_ZH', '幻胧_EN',
                          '冷漠的男性_EN', '纪香_JP', '巫女_ZH', '留云借风真君_JP', '岩明_JP', '年幼的孩子_ZH', '枫原万叶_EN', '仲正一花', '流浪者_ZH',
                          '多莉_ZH', '珠函_JP', '光之_EN', '百闻_EN', '黑塔_EN', '景元_EN', '知易_EN', '佐西摩斯_ZH', '梦茗_JP', '枫香（正月）',
                          '拍卖师_EN', '谢赫祖拜尔_EN', '黑塔_JP', '紫月季_JP', '耕一_JP', '海芭夏_JP', '露子_EN', '怀疑的患者_JP', '虎克_JP',
                          '阿来_EN', '纳比尔_JP', '伊丝黛莱_JP', '帕斯卡_ZH', '公输师傅_EN', '青雀_JP', '手岛_ZH', '德田_JP', '申鹤_JP',
                          '黑塔_ZH', '真_EN', '阿汉格尔_JP', '有原则的猎犬家系成员_JP', '卡萝蕾_JP', '费索勒_JP', '阿娜耶_JP', '田铁嘴_EN',
                          '年幼的孩子_EN', '黑见芹香', '岚姐_ZH', '阿祇_JP', '小鸟游星野', '埃尔欣根_ZH', '塔里克_ZH', '克列门特_ZH', '魔女N_ZH',
                          '弗洛朗_EN', '阿金_JP', '克洛琳德_JP', '伊莎朵_EN', '宛烟_JP', '胡桃_EN', '唐娜_EN', '静山真白', '艾琳_JP', '乌维_JP',
                          '纳西妲_JP', '珊瑚宫心海_EN', '平山_ZH', '温和的声音_EN', '松浦_EN', '米凯_EN', '菲尔汀_JP', '娜比雅_EN', '金人会长_JP',
                          '查宝_EN', '螺丝咕姆_ZH', '斯坦利_ZH', '博士_EN', '琴_ZH', '黑泽京之介_EN', '沃特林_EN', '西瓦尼_EN', '艾文_EN',
                          '岚姐_EN', '半夏_JP', '加藤洋平_JP', '克洛琳德_EN', '小川_ZH', '和香（温泉）', '托帕_ZH', '博来_JP', '库塞拉_EN',
                          '沙扎曼_EN', '维多克_ZH', '巫女_EN', '台词评委_EN', '娜比雅_JP', '舒蕾_JP', '早柚_ZH', '爱德琳_ZH', '娜维娅_EN',
                          '露尔薇_ZH', '多莉_EN', '芙卡洛斯_JP', '查宝_ZH', '勇美枫', '阿幸_ZH', '冒失的帕拉德_ZH', '鹿野院平藏_EN', '深渊法师_EN',
                          '长门幸子_ZH', '费斯曼_ZH', '斯万_EN', '狐坂若藻', '卡芙卡_EN', '天真的少年_JP', '雪衣_JP', '天童爱丽丝', '克拉拉_JP',
                          '知易_ZH', '空_JP', '雷泽_ZH', '金忽律_JP', '巴蒂斯特_JP', '舍利夫_JP', '九条镰治_JP', '诺艾尔_ZH', '寒鸦_EN',
                          '嘉明_ZH', '石头_JP', '今谷三郎_EN', '霄老大_JP', '叶德_EN', '莉莉安_JP', '娜塔莎_ZH', '克雷薇_JP', '螺丝咕姆_EN',
                          '菲尔戈黛特_ZH', '怀疑的患者_EN', '桂乃芬_EN', '莱依拉_EN', '韵宁_JP', '卡卡瓦夏的姐姐_ZH', '尾巴_JP', '乙花堇', '艾丽_JP',
                          '塞德娜_JP', '燕翠_ZH', '西尔弗_ZH', '阿扎木_ZH', '埃斯蒙德_ZH', '鲁哈维_JP', '德拉萝诗_EN', '自称渊上之物_JP', '霍夫曼_JP',
                          '木村_JP', '德沃沙克_EN', '洛伦佐_ZH', '知更鸟_ZH', '彦卿_EN', '铁尔南_EN', '妮露_EN', '迪奥娜_ZH', '阿晃_EN',
                          '今谷佳祐_EN', '大肉丸_EN', '珊瑚宫心海_JP', '昌虎_EN', '立本_JP', '一心传名刀_EN', '剑阵中的声音_ZH', '钟表匠_EN',
                          '天目十五_ZH', '巨大谜钟_ZH', '左然', '温和的声音_JP', '阿晃_ZH', '焦躁的丹鼎司医士_JP', '久利须_ZH', '玛乔丽_EN', '沙寅_ZH',
                          '泽田_EN', '尾巴_ZH', '丹恒_JP', '回声海螺_JP', '晴霓_JP', '公主_ZH', '早濑优香', '穹_EN', '冷漠的男性_ZH', '神里绫人_ZH',
                          '雷电将军_JP', '米卡_ZH', '食蜂操祈', '小涂真纪', '阿夫辛_ZH', '小仓澪_JP', '高善_EN', '埃舍尔_EN', '塞德娜_ZH', '阿鸠_EN',
                          '朋义_ZH', '白术_JP', '夜兰_EN', '银枝_JP', '叶卡捷琳娜_JP', '艾丽_EN', '科拉莉_ZH', '考特里亚_EN', '警觉的流浪者_JP',
                          '费迪南德_EN', '斯嘉莉_JP', '桐藤渚', '帮派老大_ZH', '云堇_EN', '村田_ZH', '杰克_ZH', '阿利娅_JP', '希露瓦_EN', '古山_ZH',
                          '桑博_ZH', '七七_ZH', '夏沃蕾_EN', '弗洛朗_ZH', '克列门特_JP', '科拉莉_JP', '夏妮_JP', '江蓠_JP', '那维莱特_JP',
                          '安武_JP', '加萨尼_ZH', '绍祖_EN', '维尔德_ZH', '居勒什_ZH', '韵宁_ZH', '阿幸_JP', '葵_EN', '商华_JP', '金人会长_ZH',
                          '琳妮特_ZH', '阿丰_JP', '美甘尼禄', '莱昂_EN', '魈_ZH', '莱斯格_EN', '翡翠_ZH', '佐西摩斯_JP', '贾拉康_EN', '科林斯_EN',
                          '七叶寂照秘密主_ZH', '独孤朔_JP', '邓恩_EN', '浮烟_EN', '尤苏波夫_EN', '侍从丙_ZH', '古田_ZH', '绿芙蓉_ZH', '佐城巴',
                          '提纳里_ZH', '舒伯特_ZH', '芙萝拉_ZH', '有乐斋_ZH', '芷巧_JP', '莫弈', '知易_JP', '阿鸠_ZH', '长野原龙之介_ZH',
                          '居勒什_JP', '理水叠山真君_JP', '流萤_ZH', '早柚_EN', '乔瓦尼_JP', '久田泉奈', '琳琅_ZH', '铜花瞬', '广大_ZH',
                          '菲尔戈黛特_JP', '浮烟_JP', '晴霓_EN', '半夏_ZH', '圣园未花', '河童_JP', '林尼_EN', '式大将_EN', '维尔芒_JP', '睦月（正月）',
                          '博易_JP', '七尾_EN', '卢卡_EN', '卓也_JP', '小乐_EN', '今谷佳祐_ZH', '晴霓_ZH', '札齐_JP', '杰帕德_EN',
                          'asideb_JP', '博易_EN', '柚子（女仆）', '纪芳_JP', '九条裟罗_EN', '停云_ZH', '漱玉_ZH', '信博_EN', '叶卡捷琳娜_EN',
                          '莱斯格_ZH', '祖莉亚·德斯特雷_EN', '平山_EN', '竺子_JP', '康纳_JP', '塔里克_JP', '伊德里西_ZH', '一心传名刀_JP', '朔次郎_ZH',
                          '哈伦_JP', '小野寺_EN', '传次郎_JP', '江蓠_ZH', '中务桐乃', '薇尔_JP', '一心传名刀_ZH', '尤苏波夫_JP', '冥火大公_JP',
                          '独眼小僧_ZH', '基娅拉_ZH', '朝比奈菲娜', '歌蒂_EN', '朱里厄_EN', '迈勒斯_ZH', '阿旭_ZH', '嘉玛_JP', '长门幸子_JP',
                          '纯水精灵_EN', '望雅_JP', '北斗_EN', '纳菲斯_ZH', '严苛评委_JP', '沙寅_JP', '阿洛瓦_JP', '诺尔伯特_JP', '辛焱_ZH',
                          '乐平波琳_ZH', '芙宁娜_EN', '尾刃康娜', '米沙_JP', '娜维娅_JP', '守护者的意志_EN', '克雷薇_EN', '贡达法_ZH', '可可利亚_JP',
                          '维格尔_JP', '钟离_JP', '杰洛尼_ZH', '芙萝拉_EN', '克列门特_EN', '柊慎介_JP', '加藤洋平_EN', '自称渊上之物_ZH',
                          '削月筑阳真君_EN', '引导员_ZH', '轰大叔_JP', '远黛_ZH', '娜德瓦_JP', '西瓦尼_JP', '风仓萌绘', '连河切里诺', '宛烟_EN',
                          '广大_EN', '班尼特_JP', '花角玉将_ZH', '诗筠_ZH', '迈蒙_ZH', '剑阵中的声音_JP', '考特里亚_ZH', '艾薇拉_JP', '加萨尼_JP',
                          '白老先生_JP', '鬼怒川霞', '珐露珊_JP', '安柏_EN', '冒失的帕拉德_EN', '牛牧朱莉', '和元泉艾米', '合欢垣吹雪', '特纳_ZH',
                          '卡芙卡_JP', '帕梅拉_EN', '奇怪的云骑_EN', '远黛_JP', '镜中人_EN', '耕一_EN', '阮•梅_JP', '基娅拉_EN', '玛吉_EN',
                          '松浦_ZH', '桂乃芬_JP', '哈伦_EN', '老孟_EN', '鹿野奈奈_ZH', '费索勒_EN', '爱清枫香', '纯水精灵_ZH', '雕像_JP', '玥辉_ZH',
                          '暮夜剧团团长_ZH', '刀疤刘_JP', '上杉_EN', '奇怪的云骑_ZH', '花角玉将_JP', '羽生田千鹤_ZH', '薇尔_EN', '歌原（应援团）',
                          '优菈_JP', '凯亚_EN', '莫娜_EN', '莱欧斯利_JP', '法哈德_ZH', '德田_EN', '瓦尔特_ZH', '巴列维_EN', '巴蒂斯特_EN',
                          '旁白_EN', '杰克_EN', '桑博_JP', '艾米绮_EN', '劳维克_EN', '舒翁_EN', '奥列格_JP', '理水叠山真君_EN', '钟表小子_EN',
                          '柯莱_ZH', '千织_ZH', '薇若妮卡_JP', '博易_ZH', '娜德瓦_EN', '卡西迪_EN', '阿拉夫_JP', '星野（泳装）', '卡波特_JP',
                          '申鹤_EN', '小仓澪_EN', '爱贝尔_JP', '加拉赫_EN', '镜中人_ZH', '流浪者_JP', '托克_JP', '女声_JP', '嘉良_ZH',
                          '葛瑞丝_EN', '斯薇塔_JP', '拉齐_EN', '格莉莎_JP', '葛瑞丝_ZH', '药王秘传魁首_EN', '冥火大公_EN', '明日奈（兔女郎）', '猫塚响',
                          '穹_JP', '手岛_EN', '深渊使徒_JP', '伽吠毗陀_ZH', '巴哈利_JP', '罗巧_JP', '穹_ZH', '帮派老大_EN', '造物翻译官_ZH',
                          '珠函_EN', '独眼小僧_JP', '嘉良_EN', '忠诚的侍从_EN', '韦尔纳_EN', '沙寅_EN', '岩明_EN', 'shajinma_JP', '鲁哈维_ZH',
                          '麦希尔_EN', '莎塔娜_JP', '老芬奇_EN', '刃_JP', '醉醺醺的宾客_ZH', '久利须_JP', '克罗索_JP', '伊莎朵_JP', '女士_JP',
                          '年幼的孩子_JP', '虎克_EN', '杰帕德_ZH', '爱德琳_JP', '克罗索_ZH', '伊德里西_JP', '维尔德_EN', '早柚_JP', '艾洛迪_JP',
                          '记忆中的声音_JP', '明曦_EN', '千鸟满', '阿诺德_JP', '钟离_EN', '朱特_JP', '百识_ZH', '露尔薇_JP', '阿山婆_ZH',
                          '垃垃撕圾_JP', '霄老大_ZH', '米沙_EN', '十六夜野宫', '菲米尼_JP', '皮特_EN', '加福尔_EN', '阿尔卡米_JP', '卡卡瓦夏_JP',
                          '瑶瑶_EN', '齐米亚_EN', '欧菲妮_EN', '绘星_ZH', '珊瑚_JP', '燕翠_JP', '阿诺德_EN', '朋义_JP', '辛克尔_ZH', '马洛尼_JP',
                          '麦希尔_JP', '嚣张的小孩_EN', '布洛妮娅_JP', '哲平_ZH', '独孤朔_ZH', '阿拉夫_EN', '小贩_EN', '拍卖会工作人员_EN',
                          '阿斯法德_EN', '彦卿_JP', '理查_EN', '尼禄（兔女郎）', '空崎日奈', '霄翰_ZH', '米凯_JP', '薇娜_JP', '提纳里_JP',
                          '黑泽京之介_JP', '阿芬迪_EN', '劳伦斯_JP', '引导员_EN', '阿晃_JP', '轰大叔_EN', '商华_EN', '萨齐因_JP', '克罗索_EN',
                          '班尼特_EN', '钟离_ZH', '莱提西娅_ZH', '桑上果穗', '花凛（兔女郎）', '帕姆_ZH', '达达利亚_ZH', '阿芬迪_JP', '梁沐_ZH',
                          '藿藿_ZH', '小贩_ZH', '苍老的声音_ZH', '帕梅拉_JP', '台词评委_JP', '韦尔纳_JP', '科拉莉_EN', '嘉明_JP', '希露瓦_JP',
                          '星_JP', '百识_EN', '奇怪的云骑_JP', '浣溪_EN', '梁沐_EN', '恶龙_JP', '珊瑚_ZH', '赛索斯_ZH', '胡桃_JP', '千世（泳装）',
                          '刃_EN', '托马_EN', '白子（泳装）', '浦和花子', '下江小春', '魈_JP', '托克_ZH', '杰克_JP', '刻薄的小孩_EN', '元太_JP',
                          '泉奈（泳装）', '男声_JP', '芷巧_ZH', '阿灼_JP', '式大将_JP', '谢赫祖拜尔_JP', '管家奥斯威尔_JP', '智树_EN', '佩尔西科夫_ZH',
                          '伊萨克_JP', '卢卡_ZH', '隐书_JP', '丽莎_JP', '费斯曼_JP', '高善_ZH', '上杉_ZH', '丹恒•饮月_ZH', '淮安_ZH', '生盐诺亚',
                          '佩尔西科夫_EN', '黑田_EN', '奥泰巴_JP', '纳西妲_EN', '悦_EN', '萨姆_JP', '莫娜_JP', '阿旭_EN', '符玄_JP', '阿灼_EN',
                          '云叔_EN', '净砚_ZH', '费斯曼_EN', '泽维尔_JP', '柯莱_JP', '芙宁娜_JP', '荧_JP', '迪尔菲_JP', '福尔茨_EN', '荒谷_JP',
                          '乐平波琳_JP', '今谷三郎_ZH', '鹿野奈奈_JP', '爱德华医生_JP', '斯嘉莉_EN', '优菈_EN', '常九爷_ZH', '洛伦佐_JP', '大毫_JP',
                          '瑞安维尔_ZH', '申鹤_ZH', '神里绫人_EN', '玛格丽特_EN', '竺子_EN', '可莉_JP', '雷电将军_EN', '艾迪恩_EN', '华劳斯_EN',
                          '丝柯克_ZH', '希儿_JP', '百闻_ZH', '会场广播_JP', '舒蕾_EN', '掇星攫辰天君_EN', '香菱_JP', '尤利安_EN', '黛比_EN',
                          '平山_JP', '大和田_EN', '嘉良_JP', '发抖的流浪者_ZH', '迪卢克_ZH', '女声_ZH', '花火_JP', '阿雩_ZH', '玲可_JP',
                          '斯科特_JP', '安东尼娜_EN', '奇妙的船_JP', '罗伊斯_ZH', '纯也_ZH', '远黛_EN', '向导_EN', '木村_EN',
                          '陆行岩本真蕈·元素生命_ZH', '拉伊德_JP', '玛塞勒_ZH', '忠诚的侍从_ZH', '帮派老大_JP', '接笏_JP', '洛恩_ZH', '菜菜子_JP',
                          '向导_ZH', '楚仪_EN', '警长_ZH', '库斯图_EN', '绮珊_JP', '艾伦_JP', '削月筑阳真君_ZH', '沙坎_JP', '玛塞勒_EN',
                          '言笑_EN', '姬子_ZH', '纯水精灵_JP', '玛吉_ZH', '菲尔戈黛特_EN', '泽维尔_ZH', '浣溪_JP', '安柏_ZH', '伊迪娅_EN',
                          '自称渊上之物_EN', '岚姐_JP', '沙扎曼_JP', '猎犬家系成员_JP', '羽生田千鹤_EN', '大野月咏', '爱丽丝（女仆）']

        # 匹配指令
        if "说" in str(event.message_chain):
            spk = str(event.message_chain).split("说")[0]
            txt = str(event.message_chain).replace(spk + "说", "")
            if str(event.message_chain).split("说")[0] in modelScope:

                logger.info(f"语音合成任务 text: {txt}, speaker: {spk}")
                p=await superVG({"text": txt, "speaker": spk},"modelscopeTTS")
                await bot.send(event,Voice(path=p))
            if str(event.message_chain).split("说")[0] in outVitsSpeakers:
                spk = str(event.message_chain).split("说")[0]
                txt = str(event.message_chain).replace(spk + "说", "")
                logger.info(f"语音合成任务 text: {txt}, speaker: {spk}")
                try:
                    p=await superVG({"text": txt, "speaker": spk}, "outVits")
                    await bot.send(event, Voice(path=p))
                except:
                    pass
            if str(event.message_chain).split("说")[0]+"_ZH" in fireflySpeaker:
                p = await superVG({"text": txt, "speaker": str(event.message_chain).split("说")[0]+"_ZH"},"firefly")
                await bot.send(event, Voice(path=p))
            elif str(event.message_chain).split("说")[0]+"_JP" in fireflySpeaker:
                p = await superVG({"text": txt, "speaker": str(event.message_chain).split("说")[0]+"_JP"},"firefly")
                await bot.send(event, Voice(path=p))
            elif str(event.message_chain).split("说")[0]+"_EN" in fireflySpeaker:
                p = await superVG({"text": txt, "speaker": str(event.message_chain).split("说")[0]+"_EN"},"firefly")
                await bot.send(event, Voice(path=p))
            elif str(event.message_chain).split("说")[0] in fireflySpeaker:
                p = await superVG(data={"text": txt, "speaker": str(event.message_chain).split("说")[0]},mode="firefly",langmode="<jp>")
                await bot.send(event, Voice(path=p))

        if "角色"==str(event.message_chain).replace("@"+str(bot.qq)+" ","") and At(bot.qq) in event.message_chain:
            logger.info("查询可用角色模板")
            #await bot.send(event,Image(url="https://img2.imgtp.com/2024/04/20/MvtwZXqt.jpg"))
            await bot.send(event,[f"modelscope可用speaker:{str(modelScope)}",Image(path="data/图片-1717384652980.png")])
            await bot.send(event,"可发送 xx说xxxxxxxx")
    async def tstt(r, event):
        if len(r) < maxTextLen and random.randint(0, 100) < voiceRate:
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

    async def loop_run_in_executor(executor, func, *args):
        try:
            r = await executor.run_in_executor(None, func, *args)
            logger.info(f"并发调用 | successfully running funcname：{func.__name__} result：{r.get('content')}")
            return [str(func.__name__), r]
        except Exception as e:
            # logger.error(f"Error running {func.__name__}: {e}")
            return [str(func.__name__), None]

    async def modelReply(event,modelHere):
        global chatGLMData, chatGLMCharacters,GeminiData
        try:
            if event.type != 'FriendMessage':
                bot_in = str(f"你是{botName},我是" + event.sender.member_name + "," + allcharacters.get(
                modelHere)).replace("【bot】",botName).replace("【用户】", event.sender.member_name)
            else:
                bot_in = str("你是" + botName + ",我是" + event.sender.nickname + "," + allcharacters.get(
                    modelHere)).replace("【bot】",
                                       botName).replace("【用户】", event.sender.nickname)
        except:
            logger.error("获取用户名失败，使用nickname")
            bot_in = str("你是" + botName + ",我是" + event.sender.nickname + "," + allcharacters.get(
                modelHere)).replace("【bot】",
                                    botName).replace("【用户】", event.sender.nickname)

        try:
            loop = asyncio.get_event_loop()
            text = str(event.message_chain).replace("@" + str(bot.qq) + " ", '').replace("/gpt", "")
            if text == "" or text == " ":
                text = "在吗"
            for saa in noRes:
                #print(text, saa)
                if text == saa or text=="角色":
                    logger.warning("与屏蔽词匹配，不回复")
                    return
            if event.sender.id in chatGLMData:
                prompt1 = chatGLMData.get(event.sender.id)
                prompt1.append({"content": text, "role": "user"})
            else:
                prompt1 = [{"content": text, "role": "user"}]
                await bot.send(event, "即将开始对话，如果遇到异常请发送 /clear 清理对话")
                if modelHere=="anotherGPT3.5" or modelHere=="random":
                    rep=await loop.run_in_executor(None,anotherGPT35,[{"role": "user", "content": bot_in}],event.sender.id)
                    await bot.send(event,"初始化角色完成")
            logger.info(f"{modelHere}  bot 接受提问：" + text)

            if modelHere == "random":
                tasks = []
                logger.warning("请求所有模型接口")
                #print(f"0哈哈哈:{prompt1}")
                # 将所有模型的执行代码包装成异步任务，并添加到任务列表
                # tasks.append(loop_run_in_executor(loop, gptUnofficial if gptdev else gptOfficial, prompt1, gptkeys, proxy,bot_in))
                tasks.append(loop_run_in_executor(loop, cozeBotRep, CoziUrl, prompt1, proxy))
                tasks.append(loop_run_in_executor(loop, kimi, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, qingyan, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, grop, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, lingyi, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, relolimigpt2, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, stepAI, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, qwen, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, gptvvvv, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, gpt4hahaha, prompt1, bot_in))
                tasks.append(loop_run_in_executor(loop, anotherGPT35, prompt1, event.sender.id))
                #tasks.append(loop_run_in_executor(loop,localAurona,prompt1,bot_in))
                # ... 添加其他模型的任务 ...
                #莫名其妙真的是
                aim = {"role": "user", "content": bot_in}
                prompt1 = [i for i in prompt1 if i != aim]
                aim = {"role": "assistant", "content": "好的，已了解您的需求~我会扮演好您设定的角色。"}
                prompt1 = [i for i in prompt1 if i != aim]

                done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
                reps = {}
                # 等待所有任务完成
                rep = None
                for task in done:
                    result = task.result()[1]
                    if result is not None:
                        if "content" not in result:
                            continue
                        if "无法解析" in result.get("content") or "账户余额不足" in result.get("content") or "令牌额度" in result.get(
                                "content") or "敏感词汇" in result.get("content") or "request id" in result.get(
                            "content") or "This model's maximum" in result.get(
                            "content") or "solve CAPTCHA to" in result.get("content") or "输出错误请联系站长" in result.get(
                            "content") or "接口失败" in result.get("content") or "ip请求过多" in result.get("content"):
                            continue
                        reps[task.result()[0]] = task.result()[1]
                        # reps.append(task.result())  # 添加可用结果

                # 如果所有任务都完成但没有找到非None的结果
                if len(reps) == 0:
                    logger.warning("所有模型都未能返回有效回复")
                    raise Exception
                # print(reps)
                modeltrans = {"gptX": "gptvvvv", "清言": "qingyan", "通义千问": "qwen", "anotherGPT3.5": "anotherGPT35",
                              "lolimigpt": "relolimigpt2", "step": "stepAI"}
                for priority in randomModelPriority:
                    if priority in modeltrans:
                        priority = modeltrans.get(priority)
                    if priority in reps:
                        rep = reps.get(priority)
                        logger.info(f"random模型选择结果：{priority}: {rep}")
                        break
            elif modelHere == "gpt3.5":
                if gptdev == True:
                    rep = await loop.run_in_executor(None, gptUnofficial, prompt1, gptkeys, proxy, bot_in)
                else:
                    rep = await loop.run_in_executor(None, gptOfficial, prompt1, gptkeys, proxy, bot_in)
            elif modelHere == "Cozi":
                rep = await loop.run_in_executor(None, cozeBotRep, CoziUrl, prompt1, proxy)
            elif modelHere=="anotherGPT3.5":
                rep=await loop.run_in_executor(None,anotherGPT35,prompt1,event.sender.id)
            elif modelHere == "kimi":
                rep = await loop.run_in_executor(None, kimi, prompt1, bot_in)
            elif modelHere == "清言":
                rep = await loop.run_in_executor(None, qingyan, prompt1, bot_in)
            elif modelHere == "lingyi":
                rep = await loop.run_in_executor(None, lingyi, prompt1, bot_in)
            elif modelHere == "step":
                rep = await loop.run_in_executor(None, stepAI, prompt1, bot_in)
            elif modelHere == "通义千问":
                rep = await loop.run_in_executor(None, qwen, prompt1, bot_in)
            elif modelHere == "gptX":
                rep = await loop.run_in_executor(None, gptvvvv, prompt1, bot_in)
            elif modelHere == "grop":
                rep = await loop.run_in_executor(None, grop, prompt1, bot_in)
            elif modelHere=="lolimigpt":
                rep = await lolimigpt2(prompt1,bot_in)
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
                rep=await glm4(prompt1,bot_in)
                if "禁止违规问答" == rep.get("content"):
                    logger.error("敏感喽，不能用了")
                    await bot.send(event,rep.get("content"))
                    await bot.send(event,"触发了敏感内容审核，已自动清理聊天记录")
                    try:
                        chatGLMData.pop(event.sender.id)
                    except Exception as e:
                        logger.error(e)
                    return
            #print(f"2哈哈哈：{prompt1}")
            #logger.info(rep)
            prompt1.append(rep)
            #logger.info(prompt1)
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
        if langmode == "<zh>":
            speaker = data.get("speaker")
            if "_" in str(speaker):
                bbb = str(speaker).split("_")[1]
                if bbb == "ZH":
                    langmode = "<zh>"
                if bbb == "EN":
                    langmode = "<en>"
                if bbb == "JP":
                    langmode = "<jp>"
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

            with open('settings.yaml', 'r', encoding='utf-8') as f:
                resultb = yaml.load(f.read(), Loader=yaml.FullLoader)

            modelscopeCookie = resultb.get("apiKeys").get("modelscopeCookie")
            if modelscopeCookie == "":
                modelscopeCookie = "cna=j117HdPDmkoCAXjC3hh/4rjk; ajs_anonymous_id=5aa505b4-8510-47b5-a1e3-6ead158f3375; t=27c49d517b916cf11d961fa3769794dd; uuid_tt_dd=11_99759509594-1710000225471-034528; log_Id_click=16; log_Id_pv=12; log_Id_view=277; xlly_s=1; csrf_session=MTcxMzgzODI5OHxEdi1CQkFFQ180SUFBUkFCRUFBQU12LUNBQUVHYzNSeWFXNW5EQW9BQ0dOemNtWlRZV3gwQm5OMGNtbHVad3dTQUJCNFkwRTFkbXAwV0VVME0wOUliakZwfHNEIp5sKWkjeJWKw1IphSS3e4R_7GyEFoKKuDQuivUs; csrf_token=TkLyvVj3to4G5Mn_chtw3OI8rRA%3D; _samesite_flag_=true; cookie2=11ccab40999fa9943d4003d08b6167a0; _tb_token_=555ee71fdee17; _gid=GA1.2.1037864555.1713838369; h_uid=2215351576043; _xsrf=2|f9186bd2|74ae7c9a48110f4a37f600b090d68deb|1713840596; csg=242c1dff; m_session_id=769d7c25-d715-4e3f-80de-02b9dbfef325; _gat_gtag_UA_156449732_1=1; _ga_R1FN4KJKJH=GS1.1.1713838368.22.1.1713841094.0.0.0; _ga=GA1.1.884310199.1697973032; tfstk=fE4KxBD09OXHPxSuRWsgUB8pSH5GXivUTzyBrU0oKGwtCSJHK7N3ebe0Ce4n-4Y8X8wideDotbQ8C7kBE3queYwEQ6OotW08WzexZUVIaNlgVbmIN7MQBYNmR0rnEvD-y7yAstbcoWPEz26cnZfu0a_qzY_oPpRUGhg5ntbgh_D3W4ZudTQmX5MZwX9IN8ts1AlkAYwSdc9sMjuSF8g56fGrgX9SFbgs5bGWtBHkOYL8Srdy07KF-tW4Wf6rhWQBrfUt9DHbOyLWPBhKvxNIBtEfyXi_a0UyaUn8OoyrGJ9CeYzT1yZbhOxndoh8iuFCRFg38WZjVr6yVWunpVaQDQT762H3ezewpOHb85aq5cbfM5aaKWzTZQ_Ss-D_TygRlsuKRvgt_zXwRYE_VymEzp6-UPF_RuIrsr4vHFpmHbxC61Ky4DGguGhnEBxD7Zhtn1xM43oi_fHc61Ky4DGZ6xfGo3-rjf5..; isg=BKKjOsZlMNqsZy8UH4-lXjE_8ygE86YNIkwdKew665XKv0I51IGvHCUz7_tDrx6l"
            headersa = {
                "Content-Type": "application/json",
                "Origin": "https://www.modelscope.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                "Cookie": modelscopeCookie
            }
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
            async with httpx.AsyncClient(timeout=200,headers=headersa) as client:
                r = await client.post(url, json=data)
                newurl = newurp + \
                         r.json().get("data")[1].get("name")
                async with httpx.AsyncClient(timeout=200,headers=headersa) as client:
                    r = await client.get(newurl)
                    with open(p, "wb") as f:
                        f.write(r.content)
                    return p
        elif mode=="firefly":
            datap = data
            uri = "wss://fs.firefly.matce.cn/queue/join"
            session_hash = "1fki0r8hg8mj"

            async with websockets.connect(uri) as ws:
                # 连接后发送的第一次请求
                await ws.send(json.dumps({"fn_index": 4, "session_hash": session_hash}))
                await ws.send(json.dumps(
                    {"data": [datap.get("speaker")], "event_data": None, "fn_index": 1, session_hash: "1fki0r8hg8mj"}))
                while True:
                    message = await ws.recv()
                    print("Received '%s'" % message)
                    data = json.loads(message)
                    # 当消息中包含 'name' 并且是所需文件路径时
                    if "output" in data and "data" in data["output"]:
                        ibn = data["output"]["data"][0]
                        exampletext = data["output"]["data"][1]
                        break
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps({"fn_index": 4, "session_hash": session_hash}))
                await ws.send(
                    json.dumps({"data": [ibn], "event_data": None, "fn_index": 2, "session_hash": "1fki0r8hg8mj"}))
                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    # 当消息中包含 'name' 并且是所需文件路径时
                    if "output" in data and "data" in data["output"]:
                        for item in data["output"]["data"]:
                            if item and "name" in item and "/tmp/gradio/" in item["name"]:
                                # 提取文件的路径
                                example = item["name"]
                                # print(f"这里是请求结果：{example}")
                                break
                        break
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps({"fn_index": 4, "session_hash": session_hash}))
                # 连接后发送的第二次请求
                await ws.send(json.dumps({"data": [datap.get("text"), True, {"name": f"{example}",
                                                                             "data": f"https://fs.firefly.matce.cn/file={example}",
                                                                             "is_file": True, "orig_name": "audio.wav"},
                                                   exampletext, 0, 90, 0.7, 1.5, 0.7, datap.get("speaker")],
                                          "event_data": None, "fn_index": 4, "session_hash": "1fki0r8hg8mj"}))

                # 等待并处理服务器的消息
                while True:
                    message = await ws.recv()
                    print("Received '%s'" % message)
                    data = json.loads(message)
                    # 当消息中包含 'name' 并且是所需文件路径时
                    if "output" in data and "data" in data["output"]:
                        for item in data["output"]["data"]:
                            if item and "name" in item and "/tmp/gradio/" in item["name"]:
                                # 提取文件的路径
                                file_path = item["name"]
                                # 拼接 URL
                                full_url = f"https://fs.firefly.matce.cn/file={file_path}"
                                break
                        break
                p = "data/voices/" + random_str() + '.wav'
                async with httpx.AsyncClient(timeout=200) as client:
                    r = await client.get(full_url)
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
        if len(st1) < maxTextLen and random.randint(0, 100) < voiceRate:
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
        logger.error("出错，检查Mirai是否正常启动，以及settings.yaml中的配置是否正确")