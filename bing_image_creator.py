# -*- coding:utf-8 -*-
import logging
import os
import random
import sys

import colorlog
import httpx
import yaml
from bingart import BingArt
from mirai import Mirai, WebSocketAdapter, GroupMessage, Image, At, Startup, FriendMessage, Shutdown


def newLogger():
    # 创建一个logger对象
    logger = logging.getLogger("bing art")
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
async def bingCreate(sockProxy,prompt,_U,kiev):
    os.environ["http_proxy"]=sockProxy
    os.environ["https_proxy"]=sockProxy
    bing_art = BingArt(auth_cookie_U=_U,auth_cookie_KievRPSSecAuth=kiev,auto=True)
    results = bing_art.generate_images(prompt)
    #print(results)
    paths=[]
    for i in results.get("images"):
        url2 = i.get("url")
        async with httpx.AsyncClient(timeout=40) as client:
            r1 = await client.get(url2)
        path = "data/pictures/" + random_str() + ".png"
        paths.append(path)
        with open(path, "wb") as f:
            f.write(r1.content)
        # print(path)
    return paths
def main(bot,logger):
    with open('bing_dalle3_config.yaml', 'r', encoding='utf-8') as f:
        resulttr = yaml.load(f.read(), Loader=yaml.FullLoader)
    sock5proxy=resulttr.get("sock5-proxy")
    bing_image_creator_key=resulttr.get("bing-image-creator")
    @bot.on(GroupMessage)
    async def selfBingDraw(event: GroupMessage):
        if str(event.message_chain).startswith("画"):
            tag = str(event.message_chain).replace("画 ", "")
            if bing_image_creator_key.get("_U") != "" and bing_image_creator_key.get("KievRPSSecAuth") != "":
                try:
                    logger.info(f"bing接口发起请求:{tag}")
                    p = await bingCreate(sock5proxy, tag, bing_image_creator_key.get("_U"),
                                         bing_image_creator_key.get("KievRPSSecAuth"))
                    plist = []
                    for i in p:
                        plist.append(Image(path=i))
                    await bot.send(event, plist, True)
                    logger.info("完成，发送")
                except Exception as e:
                    logger.error(e)
                    await bot.send(event, "bing cookie过期或网络连接错误，请检查")
if __name__ == '__main__':
    with open('bing_dalle3_config.yaml', 'r', encoding='utf-8') as f:
        resulttr = yaml.load(f.read(), Loader=yaml.FullLoader)
    sock5proxy=resulttr.get("sock5-proxy")
    bing_image_creator_key=resulttr.get("bing-image-creator")
    if bing_image_creator_key.get("_U") != "" and bing_image_creator_key.get("KievRPSSecAuth") != "":
        with open('settings.yaml', 'r', encoding='utf-8') as f:
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
        config = result.get("bot")
        qq = int(config.get('botqq'))
        key = config.get("http-api-key")
        port = int(config.get("http-api-port"))
        bot = Mirai(qq, adapter=WebSocketAdapter(
            verify_key=key, host='localhost', port=port
        ))
        logger = newLogger()
        logger.info("bing-image-creator")
        logger.info("https://github.com/avilliai/Petunia")
        main(bot,logger)
        bot.run()