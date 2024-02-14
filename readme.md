# 须知
- 请确保已安装[mirai-api-http](https://github.com/project-mirai/mirai-api-http) 并[正确配置](https://github.com/avilliai/wReply/blob/master/setting.yml) <br>
- 需要[获取apikey](https://open.bigmodel.cn/)
- 本项目分离自[Manyana](https://github.com/avilliai/Manyana) 
# 🚀部署
从[release下载](https://github.com/avilliai/Bergml/releases/tag/chaglm) 最新的压缩包<br>
解压<br>
填写settings.yaml<br>
双击berglm.exe
# ☁如何填写settings.yaml
>settings.yaml配置文件的每一个可配置项基本都有注释

这里是十分重要的一部分<br>
项目的**chatglm使用的是[外部服务](https://open.bigmodel.cn/) 你需要去注册并获取一个apikey**，填写进chatGLMKey，付费api但价格还算合适
```
bot:
  http-api-key: '1234567890'   #mirai-api-http的vertify key
  http-api-port: 23456         #mirai-api-http的port
  botqq: 919467430             #机器人的qq
  master: 1840094972           #你的qq
  botname: yucca               #机器人的名字
chatGLMKey: fsldkjfsldfsahfol #chatGLM的apiKey，从https://open.bigmodel.cn/获取
```
# 😎部署语音合成服务(可选)
部署后配置settings.yaml中对应的项，如果你部署了，那么请把下面的选项设置为0-100的数字，否则不会调用，其余配置项都有相应的注释，请自行查看<br>
speaker必须是你在语音合成服务中已经部署了的模型
```
chatGLM:
  voiceRate: 0 #语音回复几率,为0则不开启
  speaker: 东雪莲    #bert_vits语音合成默认设置角色
```
## colab部署(推荐)
[点击并依次运行即可](https://colab.research.google.com/drive/1n8lI6pOiDtli2zC5fL9PZ9TZqbOafqma?usp=sharing)<br>
把输出的url粘贴进settings.yaml
## 本地部署
[bert_vits_sever](https://github.com/avilliai/Bert_Vits2_Sever/tree/master)
# 🎲可用指令
```
授权#qq号     #给特定用户授权
授权群#群号    #给群授权
取消授权#qq号   #你知道的
取消授权群#群号 
xx说xxxx     #语音合成服务，需要完成语音合成sever部署
#下面是一些其他的api，不稳定，只是附加功能，不需要配置，不支持多轮对话，项目的重点是chatglm+bert_vits2，这些以后或许会专门做
/xh你好     #讯飞星火
/wx你好     #文心一言
/chat你好   #gpt3.5

```

<div align="center">
   <img width="70%" height="70%" src="https://moe-counter.glitch.me/get/@:berglm" alt="logo"></br>
</div>
