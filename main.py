# -*- coding:utf-8 -*-
import logging
import colorlog
from mirai import Mirai, WebSocketAdapter
import yaml
def newLogger():
    # 创建一个logger对象
    logger = logging.getLogger("bert_chatter")
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
# -*- coding: utf-8 -*-
import asyncio
import json
import random
import re
import uuid
from asyncio import sleep

import httpx
#import poe
import yaml
from mirai import Image, Voice, Startup
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain
import threading
from asyncio import sleep

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

import zhipuai
def chatGLM1(api_key,bot_info,prompt):
    zhipuai.api_key = api_key
    response = zhipuai.model_api.sse_invoke(
        model="characterglm",
        meta= bot_info,
        prompt= prompt,
        incremental=True
    )
    str1=""
    for event in response.events():
      if event.event == "add":
          str1+=event.data
          #print(event.data)
      elif event.event == "error" or event.event == "interrupted":
          str1 += event.data
          #print(event.data)
      elif event.event == "finish":
          str1 += event.data
          #print(event.data)
          print(event.meta)
      else:
          str1 += event.data
          #print(event.data)
    #print(str1)
    return str1

async def taffySayTest(data,url,proxy=None):
    if url=='':
        url = "http://localhost:9080/synthesize"  # 后端服务的地址
        async with httpx.AsyncClient(timeout=200) as client:
            r = await client.post(url, json=json.dumps(data))
            p = "data/voices/" + random_str() + '.wav'
            with open(p, "wb") as f:
                f.write(r.content)
            return p
    else:
        if str(url).endswith("/synthesize"):
            pass
        else:
            url+="/synthesize"
        proxies = {
            "http://": proxy,
            "https://": proxy
        }
        # 请求参数

        async with httpx.AsyncClient(timeout=200,proxies=proxies) as client:
            r=await client.post(url, json=json.dumps(data))
            p="data/voices/"+random_str()+'.wav'
            #print(p)
            with open(p, "wb") as f:
                f.write(r.content)
            return p
class CListen(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.mLoop = loop

    def run(self):
        asyncio.set_event_loop(self.mLoop)  # 在新线程中开启一个事件循环

        self.mLoop.run_forever()
def main(bot,logger):
    file_object = open("data/mylog.log")
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()
    print(all_the_text)
    #读取个性化角色设定
    with open('data/chatGLMCharacters.yaml', 'r', encoding='utf-8') as f:
        result2223 = yaml.load(f.read(), Loader=yaml.FullLoader)
    global chatGLMCharacters
    chatGLMCharacters = result2223

    with open('data/chatGLMData.yaml', 'r', encoding='utf-8') as f:
        cha = yaml.load(f.read(), Loader=yaml.FullLoader)
    global chatGLMData
    chatGLMData=cha

    with open('settings.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    berturl=result.get("bert_colab")
    chatGLM_api_key=result.get("chatGLMKey")
    proxy=result.get("proxy")
    glmReply = result.get("chatGLM").get("glmReply")
    privateGlmReply = result.get("chatGLM").get("privateGlmReply")
    meta = result.get("chatGLM").get("bot_info").get("default")
    context= result.get("chatGLM").get("context")
    maxPrompt = result.get("chatGLM").get("maxPrompt")
    allcharacters=result.get("chatGLM").get("bot_info")

    maxTextLen = result.get("chatGLM").get("maxLen")
    voiceRate = result.get("chatGLM").get("voiceRate")
    speaker = result.get("chatGLM").get("speaker")
    withText=result.get("chatGLM").get("withText")

    config = result.get("bot")
    botName = config.get("botname")
    master=config.get("master")

    with open('data/permit.yaml', 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    global permitgroups
    permitgroups = data.get("groups")
    global permituser
    permituser = data.get("users")

    #线程预备
    newLoop = asyncio.new_event_loop()
    listen = CListen(newLoop)
    listen.setDaemon(True)
    listen.start()
    #私聊使用chatGLM,对信任用户或配置了apiKey的用户开启
    @bot.on(FriendMessage)
    async def GLMFriendChat(event:FriendMessage):
        global chatGLMData,chatGLMCharacters
        if str(event.sender.id) in permituser:
            logger.info("信任用户进行chatGLM提问")
            selfApiKey=chatGLM_api_key
        elif privateGlmReply==True:
            selfApiKey = chatGLM_api_key
        else:
            return
        if str(event.message_chain) == "/clearGLM":
            return
        text = str(event.message_chain)
        logger.info("私聊glm接收消息："+text)
        # 构建新的prompt
        tep = {"role": "user", "content": text}
        # print(type(tep))
        # 获取以往的prompt
        if event.sender.id in chatGLMData:
            prompt = chatGLMData.get(event.sender.id)
            prompt.append({"role": "user", "content": text})
        # 没有该用户，以本次对话作为prompt
        else:
            prompt = [tep]
            chatGLMData[event.sender.id] = prompt
        if event.sender.id in chatGLMCharacters:
            meta1 = chatGLMCharacters.get(event.sender.id)
        else:
            logger.warning("读取meta模板")
            with open('settings.yaml', 'r', encoding='utf-8') as f:
                resy = yaml.load(f.read(), Loader=yaml.FullLoader)
            meta1 = resy.get("chatGLM").get("bot_info").get("default")


        setName = event.sender.nickname

        meta1["user_name"] = meta1.get("user_name").replace("指挥", setName)
        meta1["user_info"] = meta1.get("user_info").replace("指挥", setName).replace("yucca",botName)
        meta1["bot_info"] = meta1.get("bot_info").replace("指挥", setName).replace("yucca",botName)
        meta1["bot_name"] = botName

        try:
            logger.info("当前meta:" + str(meta1))
            #st1 = await chatGLM(selfApiKey, meta1, prompt)
            asyncio.run_coroutine_threadsafe(asyncchatGLM(selfApiKey, meta1, prompt, event, setName, text), newLoop)

        except:
            await bot.send(event, "chatGLM启动出错，请联系master检查apiKey或重试")

    # 私聊中chatGLM清除本地缓存
    @bot.on(FriendMessage)
    async def clearPrompt(event: FriendMessage):
        global chatGLMData
        if str(event.message_chain) == "/clearGLM":
            try:
                chatGLMData.pop(event.sender.id)
                # 写入文件
                with open('data/chatGLMData.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(chatGLMData, file, allow_unicode=True)
                await bot.send(event,"已清除近期记忆")
            except:
                await bot.send(event, "清理缓存出错，无本地对话记录")

    @bot.on(FriendMessage)
    async def showCharacter(event:FriendMessage):
        if str(event.message_chain)=="可用角色模板" or "角色模板" in str(event.message_chain):
            st1=""
            for isa in allcharacters:
                st1+=isa+"\n"
            await bot.send(event,"对话可用角色模板：\n"+st1+"\n发送：设定#角色名 以设定角色")
    @bot.on(FriendMessage)
    async def setCharacter(event:FriendMessage):
        global chatGLMCharacters
        if str(event.message_chain).startswith("设定#"):
            if str(event.message_chain).split("#")[1] in allcharacters:

                meta1 = allcharacters.get(str(event.message_chain).split("#")[1])

                setName = event.sender.nickname
                meta1["user_info"] = meta1.get("user_info").replace("指挥", setName).replace("yucca", botName)
                meta1["bot_info"] = meta1.get("bot_info").replace("指挥", setName).replace("yucca", botName)
                meta1["bot_name"] = botName
                meta1["user_name"] = setName
                chatGLMCharacters[event.sender.id] = meta1

                logger.info("当前：",chatGLMCharacters)
                with open('data/chatGLMCharacters.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(chatGLMCharacters, file, allow_unicode=True)
                await bot.send(event,"设定成功")
            else:
                await bot.send(event,"不存在的角色")

    @bot.on(GroupMessage)
    async def showCharacter(event:GroupMessage):
        if str(event.message_chain)=="可用角色模板" or (At(bot.qq) in event.message_chain and "角色模板" in str(event.message_chain)):
            st1=""
            for isa in allcharacters:
                st1+=isa+"\n"
            await bot.send(event,"对话可用角色模板：\n"+st1+"\n发送：设定#角色名 以设定角色")
    @bot.on(GroupMessage)
    async def setCharacter(event:GroupMessage):
        global chatGLMCharacters
        if str(event.message_chain).startswith("设定#"):
            if str(event.message_chain).split("#")[1] in allcharacters:
                meta1=allcharacters.get(str(event.message_chain).split("#")[1])
                setName = event.sender.member_name
                meta1["user_name"] = meta1.get("user_name").replace("指挥", setName)
                meta1["user_info"] = meta1.get("user_info").replace("指挥", setName).replace("yucca", botName)
                meta1["bot_info"] = meta1.get("bot_info").replace("指挥", setName).replace("yucca", botName)
                meta1["bot_name"] = botName

                chatGLMCharacters[event.sender.id] =meta1
                logger.info("当前：",chatGLMCharacters)
                with open('data/chatGLMCharacters.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(chatGLMCharacters, file, allow_unicode=True)
                await bot.send(event,"设定成功")
            else:
                await bot.send(event,"不存在的角色")



    #群内chatGLM回复
    @bot.on(GroupMessage)
    async def atReply(event: GroupMessage):
        global chatGLMData,chatGLMCharacters,permituser,permitgroups

        if (glmReply == True or event.sender.id in permituser or event.group.id in permitgroups) and At(bot.qq) in event.message_chain:
            text = str(event.message_chain).replace("@" + str(bot.qq) + "", '').replace(" ","")
            logger.info("分支1")

            if text=="" or text==" ":
                text="在吗"
            #构建新的prompt
            tep={"role": "user","content": text}
            #print(type(tep))
            #获取以往的prompt
            if event.sender.id in chatGLMData and context==True:
                prompt=chatGLMData.get(event.sender.id)
                prompt.append({"role": "user","content": text})

            #没有该用户，以本次对话作为prompt
            else:
                prompt=[tep]
                chatGLMData[event.sender.id] =prompt
            #logger.info("当前prompt"+str(prompt))

            if str(event.sender.id) in permituser:
                logger.info("信任用户进行chatGLM提问")
                selfApiKey = chatGLM_api_key
            else:
                selfApiKey = chatGLM_api_key

            #获取角色设定
            if event.sender.id in chatGLMCharacters:
                meta1=chatGLMCharacters.get(event.sender.id)
            else:
                logger.warning("读取meta模板")
                with open('settings.yaml', 'r', encoding='utf-8') as f:
                    resy = yaml.load(f.read(), Loader=yaml.FullLoader)
                meta1 = resy.get("chatGLM").get("bot_info").get("default")

            setName = event.sender.member_name
            meta1["user_name"] = meta1.get("user_name").replace("指挥", setName)
            meta1["user_info"] = meta1.get("user_info").replace("指挥", setName).replace("yucca",botName)
            meta1["bot_info"]=meta1.get("bot_info").replace("指挥",setName).replace("yucca",botName)
            meta1["bot_name"]=botName

            logger.info("chatGLM接收提问:" + text)
            try:
                logger.info("当前meta:"+str(meta1))
                asyncio.run_coroutine_threadsafe(asyncchatGLM(selfApiKey, meta1, prompt, event, setName, text), newLoop)
                #st1 = await chatGLM(selfApiKey, meta1, prompt)

            except:
                await bot.send(event, "chatGLM启动出错，请联系master检查apiKey或重试")

    #用于chatGLM清除本地缓存
    @bot.on(GroupMessage)
    async def clearPrompt(event:GroupMessage):
        global chatGLMData
        if str(event.message_chain)=="/clearGLM":
            try:
                chatGLMData.pop(event.sender.id)
                # 写入文件
                with open('data/chatGLMData.yaml', 'w', encoding="utf-8") as file:
                    yaml.dump(chatGLMData, file, allow_unicode=True)
                await bot.send(event,"已清除近期记忆")
            except:
                await bot.send(event,"清理缓存出错，无本地对话记录")



    @bot.on(GroupMessage)
    async def gpt3(event: GroupMessage):
        if str(event.message_chain).startswith("/chat"):
            s = str(event.message_chain).replace("/chat", "")
            try:
                logger.info("gpt3.5接收信息：" + s)
                url = "https://api.lolimi.cn/API/AI/mfcat3.5.php?sx=你是一个可爱萝莉&msg="+s+"&type=json"
                async with httpx.AsyncClient(timeout=40) as client:
                    # 用get方法发送请求
                    response = await client.get(url=url)
                s=response.json().get("data")
                s = s.replace(r"\n", "\n")

                logger.info("gpt3.5:" + s)
                await bot.send(event, s, True)
            except:
                logger.error("调用gpt3.5失败，请检查网络或重试")
                await bot.send(event, "无法连接到gpt3.5，请检查网络或重试")
    #科大讯飞星火ai
    @bot.on(GroupMessage)
    async def gpt3(event: GroupMessage):
        if str(event.message_chain).startswith("/xh"):
            s = str(event.message_chain).replace("/xh", "")
            try:
                logger.info("讯飞星火接收信息：" + s)
                url = "https://api.lolimi.cn/API/AI/xh.php?msg=" + s
                async with httpx.AsyncClient(timeout=40) as client:
                    # 用get方法发送请求
                    response = await client.get(url=url)
                s = response.json().get("data").get("output")
                s = s.replace(r"\n", "\n")
                logger.info("讯飞星火:" + s)
                await bot.send(event, s, True)
            except:
                logger.error("调用讯飞星火失败，请检查网络或重试")
                await bot.send(event, "无法连接到讯飞星火，请检查网络或重试")

    # 文心一言
    @bot.on(GroupMessage)
    async def gpt3(event: GroupMessage):
        if str(event.message_chain).startswith("/wx"):
            s = str(event.message_chain).replace("/wx", "")
            try:
                logger.info("文心一言接收信息：" + s)
                url = "https://api.lolimi.cn/API/AI/wx.php?msg=" + s
                async with httpx.AsyncClient(timeout=40) as client:
                    # 用get方法发送请求
                    response = await client.get(url=url)
                s = response.json().get("data").get("output")
                s=s.replace(r"\n","\n")

                logger.info("文心一言:" + s)
                await bot.send(event, s, True)
            except:
                logger.error("调用文心一言失败，请检查网络或重试")
                await bot.send(event, "无法连接到文心一言，请检查网络或重试")


    @bot.on(GroupMessage)
    async def permmitgroupandusers(event: GroupMessage):
        global permituser,permitgroups
        if event.sender.id==master:
            try:
                if str(event.message_chain).startswith("授权群#"):
                    logger.info("增加授权群")
                    groupid=int(str(event.message_chain).replace("授权群#",""))
                    permitgroups.append(groupid)
                    with open('data/permit.yaml', 'r', encoding='utf-8') as file:
                        data9 = yaml.load(file, Loader=yaml.FullLoader)
                    data9["groups"]=permitgroups
                    with open('data/permit.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(data9, file, allow_unicode=True)
                    await bot.send(event, "操作成功")
                if str(event.message_chain).startswith("授权#"):
                    logger.info("增加授权用户")
                    userid=int(str(event.message_chain).replace("授权#",""))
                    permituser.append(userid)
                    with open('data/permit.yaml', 'r', encoding='utf-8') as file:
                        data9 = yaml.load(file, Loader=yaml.FullLoader)
                    data9["users"]=permituser
                    with open('data/permit.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(data9, file, allow_unicode=True)
                    await bot.send(event, "操作成功")
                if str(event.message_chain).startswith("取消授权群#"):
                    logger.info("取消群授权")
                    groupid=int(str(event.message_chain).replace("取消授权群#",""))
                    permitgroups.remove(groupid)
                    with open('data/permit.yaml', 'r', encoding='utf-8') as file:
                        data9 = yaml.load(file, Loader=yaml.FullLoader)
                    data9["groups"]=permitgroups
                    with open('data/permit.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(data9, file, allow_unicode=True)
                    await bot.send(event, "操作成功")
                if str(event.message_chain).startswith("取消授权#"):
                    logger.info("取消用户授权")
                    userid=int(str(event.message_chain).replace("取消授权#",""))
                    permituser.remove(userid)
                    with open('data/permit.yaml', 'r', encoding='utf-8') as file:
                        data9 = yaml.load(file, Loader=yaml.FullLoader)
                    data9["users"]=permituser
                    with open('data/permit.yaml', 'w', encoding="utf-8") as file:
                        yaml.dump(data9, file, allow_unicode=True)
                    await bot.send(event,"操作成功")
            except:
                await bot.send(event,"操作失败，不存在的目标")





    #CharacterchatGLM部分
    def chatGLM(api_key,bot_info,prompt,model1):
        logger.info("当前模式:"+model1)
        zhipuai.api_key = api_key
        if model1=="chatglm_pro":
            response = zhipuai.model_api.sse_invoke(
                model="chatglm_pro",
                prompt=prompt,
                temperature=0.95,
                top_p=0.7,
                incremental=True
            )
        elif model1=="chatglm_std":
            response = zhipuai.model_api.sse_invoke(
                model="chatglm_std",
                prompt=prompt,
                temperature=0.95,
                top_p=0.7,
                incremental=True
            )
        elif model1=="chatglm_lite":
            response = zhipuai.model_api.sse_invoke(
                model="chatglm_lite",
                prompt=prompt,
                temperature=0.95,
                top_p=0.7,
            )
        else:
            response = zhipuai.model_api.sse_invoke(
                model="characterglm",
                meta= bot_info,
                prompt= prompt,
                incremental=True
            )
        str1=""
        for event in response.events():
          if event.event == "add":
              str1+=event.data
              #print(event.data)
          elif event.event == "error" or event.event == "interrupted":
              str1 += event.data
              #print(event.data)
          elif event.event == "finish":
              str1 += event.data
              #print(event.data)
              print(event.meta)
          else:
              str1 += event.data
              #print(event.data)
        #print(str1)
        return str1
    # 创建一个异步函数
    async def asyncchatGLM(apiKey,bot_info,prompt,event,setName,text):
        global chatGLMData

        loop = asyncio.get_event_loop()
        # 使用 loop.run_in_executor() 方法来将同步函数转换为异步非阻塞的方式进行处理
        # 第一个参数是执行器，可以是 None、ThreadPoolExecutor 或 ProcessPoolExecutor
        # 第二个参数是同步函数名，后面跟着任何你需要传递的参数
        #result=chatGLM(apiKey,bot_info,prompt)
        with open('settings.yaml', 'r', encoding='utf-8') as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        model1 = result.get("chatGLM").get("model")
        st1 = await loop.run_in_executor(None, chatGLM,apiKey,bot_info,prompt,model1)
        # 打印结果
        #print(result)
        st11 = st1.replace(setName, "指挥")
        if len(st1)<maxTextLen and random.randint(0,100)<voiceRate:
            data1={}
            data1['speaker']=speaker
            logger.info("调用bert_vits语音回复")
            #print(path)
            st8 = re.sub(r"（[^）]*）", "", st1)  # 使用r前缀表示原始字符串，避免转义字符的问题
            data1["text"] = st8
            path=await taffySayTest(data1,berturl,proxy)
            await bot.send(event, Voice(path=path))
            if withText==True:
                await bot.send(event,st1)
        else:
            await bot.send(event, st1, True)
        if len(st1) > 400:
            await bot.send(event, "🐱‍💻回复可能存在异常\n请发送 /clearGLM 以清理当前聊天(无需艾特)",True)
            try:
                prompt.remove(prompt[-1])
                chatGLMData[event.sender.id]=prompt
            except:
                logger.error("chatGLM删除上一次对话失败")
            return

        logger.info("chatGLM:" + st1)

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
    logger.info("语音合成sever部署：https://colab.research.google.com/drive/1n8lI6pOiDtli2zC5fL9PZ9TZqbOafqma?usp=sharing")
    main(bot,logger)
    bot.run()