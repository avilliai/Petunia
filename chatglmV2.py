# -*- coding:utf-8 -*-
import logging
import colorlog
from flask import Flask, request

import yaml
import asyncio
import json
import random
import re
import uuid
from asyncio import sleep
import zhipuai
import httpx
import yaml
from zhipuai import ZhipuAI
import threading
from asyncio import sleep
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

#芝士logger
logger=newLogger()
logger.info("欢迎使用")
logger.info("项目源地址：https://github.com/avilliai/Bergml")
logger.info("语音合成sever部署：https://colab.research.google.com/drive/1n8lI6pOiDtli2zC5fL9PZ9TZqbOafqma?usp=sharing")



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



class CListen(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.mLoop = loop

    def run(self):
        asyncio.set_event_loop(self.mLoop)  # 在新线程中开启一个事件循环

        self.mLoop.run_forever()
#线程预备
newLoop = asyncio.new_event_loop()
listen = CListen(newLoop)
listen.setDaemon(True)
listen.start()

app = Flask(__name__)

@app.route('/synthesize', methods=['POST'])
async def synthesize():
    # 解析请求中的参数
    data = request.get_json()
    data=json.loads(data)
    selfApiKey = data['apiKey']
    try:
        meta1=data["meta"]
        logger.info("当前meta:" + str(meta1))
    except:
        logger.warning("无meta")
    prompt = data['prompt']
    model = data['model']

    try:
        if "meta" not in data:
            b = asyncio.run_coroutine_threadsafe(asyncchatGLM(selfApiKey, prompt, model), newLoop)
            b = b.result()
            return b
        else:
            b=asyncio.run_coroutine_threadsafe(asyncchatGLM(selfApiKey,  prompt,model,meta1), newLoop)
            b=b.result()
            return b
        #st1 = await chatGLM(selfApiKey, meta1, prompt)

    except Exception as e:
        return "chatGLM出错，请联系master检查apiKey或重试"
#CharacterchatGLM部分
def chatGLM(api_key,bot_info,prompt,model1):
    logger.info("当前模式:"+model1)
    zhipuai.api_key = api_key
    client = ZhipuAI(api_key=api_key)  # 请填写您自己的APIKey
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
    elif model1=="cogview-3":

        response = client.images.generations(
            model="cogview-3",  # 填写需要调用的模型名称
            prompt=prompt,
        )
        print(response.data[0].url)
        return response.data[0].url
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
async def asyncchatGLM(apiKey,prompt,model1,bot_info=None):


    loop = asyncio.get_event_loop()

    st1 = await loop.run_in_executor(None, chatGLM,apiKey,bot_info,prompt,model1)
    # 打印结果
    return st1

app.run(debug=True, host='127.0.0.1', port=9088)