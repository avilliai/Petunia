[为看不懂文档的用户准备的视频教程](https://github.com/avilliai/Bergml/releases/tag/idn)
# 须知
- 请确保已安装[mirai-api-http](https://github.com/project-mirai/mirai-api-http) 并[正确配置](https://github.com/avilliai/wReply/blob/master/setting.yml) <br>
  - [下载mirai-api-http](https://github.com/project-mirai/mirai-api-http) 放进mirai/plugins文件夹
  - 启动一次Mirai，关闭
  - 用[配置](https://github.com/avilliai/wReply/blob/master/setting.yml) 替换config/net.mamoe.mirai-api-http/setting.yml
  - 启动mirai，至此，完成Mirai部分配置
# 🚀部署
从[release下载](https://github.com/avilliai/Bergml/releases) 最新的压缩包<br>
解压<br>
填写Petunia/settings.yaml<br>
双击berglm.exe
# ☁如何填写Petunia/settings.yaml
>settings.yaml配置文件的每一个可配置项基本都有注释

这里是十分重要的一部分<br>
## 与Mirai连接(overflow用户一样，本身就一家的。)
确保已安装[mirai-api-http](https://github.com/project-mirai/mirai-api-http) 并[正确配置](https://github.com/avilliai/wReply/blob/master/setting.yml) <br>
如果你用的是[配置](https://github.com/avilliai/wReply/blob/master/setting.yml) ，编辑后三项即可<br>
```
bot:
  http-api-key: '1234567890'   #mirai-api-http的vertify key
  http-api-port: 23456         #mirai-api-http的port
  botqq: 919467430             #机器人的qq
  master: 1840094972           #你的qq
  botname: yucca               #机器人的名字
```
## 选择模型
模型可选lolimigpt(免费无需key，不稳定)/glm-4(免费无需key，不稳定)/Gemini(免费需代理，配置geminiapiKey)/Cozi(免费需代理，配置CoziUrl)/characterglm(付费，配置chatGLMKey)/gpt3.5(付费，配置openaikeys)<br>


| 模型(settings.yaml中的model设置) | 介绍                                                                                                                                   | 配置项(apikeys对应)             | 评价                                               |
|----------------|--------------------------------------------------------------------------------------------------------------------------------------|---------------------------|--------------------------------------------------|
| characterglm   | 智谱的超拟人大模型，在这里[申请](https://open.bigmodel.cn/)                                                                                         | chatGLMKey                   | 付费api，贵，敏感词多，但效果不错                               |
| lolimigpt      | 免费gpt3.5                                                                                                                             | 【无需配置】                    | 免费，不稳定                                           |
| glm-4          | 免费glm-4                                                                                                                              | 【无需配置】                    | 免费，不稳定                                           |
| gpt3.5         | 官方gpt3.5，需要填写代理proxy项                                                                                                                | openai-keys<br>proxy      | 不建议使用，官方贵，并且需要配置代理                               |
| gpt3.5         | 同样是gpt3.5，无需代理，[免费申请apikey](https://github.com/chatanywhere/GPT_API_free?tab=readme-ov-file) 使用此apikey需要把gpt3.5-dev的值修改为true         | openai-keys<br>gpt3.5-dev | 免费，稳定，无代理时首选                                     |
| Cozi           | GPT4，基于[coze-discord](https://github.com/deanxv/coze-discord-proxy)，教程请查看[Here](https://github.com/avilliai/Manyana/issues/4)，最好配置代理 | cozi<br>proxy(建议)         | 免费。需要discord小号，每个账号每天都有次数限制(gpt4 100次/天)，可配置多个小号 |
| gemini         | 谷歌Gemini，在这里[申请apikey](https://ai.google.dev/tutorials/setup?hl=zh-cn)，需配置proxy                                                      | gemini<br>proxy           | 免费，稳定，有代理时首选                                     |

```
chatGLM:
  .......
  model: Gemini    #在这里选择你的模型
  .......
```
## 配置模型对应的apikey

```
apiKeys:
  #支持填写多个key
  chatGLMKey: xxxxxx  #chatGLM的apiKey，从https://open.bigmodel.cn/获取
  geminiapiKey:       #gemini，从https://ai.google.dev/tutorials/setup?hl=zh-cn获取
    - xxxxxx
  openaikeys:         #openai官方apikey，需要代理
    - xxxxxxx
    - xxxxxxx
  CoziUrl: "xxxxx"    #coze+discord白嫖gpt4，需要部署，参考https://github.com/avilliai/Manyana/issues/4
#在这里设置代理
proxy: "http://127.0.0.1:10809"             #代理，如果是clash，一般填"http://127.0.0.1:7890" 如果ssr，一般"http://127.0.0.1:1080" 如果v2ray，一般"http://127.0.0.1:10809"
```
## 设置语音合成
```
chatGLM:
  ......(前略)
  #语音合成配置部分
  voiceGenerateSource: modelscopeTTS  #可选modelscopeTTS和outVits
  maxLen: 70    #语音合成最大长度限制，超出则返回文本。
  voiceRate: 100 #语音回复几率,为0则不开启
  langType: "<zh>"  #语音合成语言类型，仅对modelscopeTTS部分角色生效
  #modelscopeTTS模式可用角色["BT","塔菲","阿梓","otto","丁真","星瞳","东雪莲","嘉然","孙笑川","亚托克斯","文静","鹿鸣","奶绿","七海","恬豆","科比"]，该模式下任选其一填入即可
  speaker: 东雪莲          #语音合成默认音源，根据你的合成模式设定。outVits模式的角色(个人推荐填 瑶瑶)看https://api.lolimi.cn/?action=doc&id=181
  ......(后略)
```
# 🎲可用指令
```
授权#qq号     #给特定用户授权
授权群#群号    #给群授权
xx说xxxx     #语音合成服务，需要完成语音合成sever部署
画 xxxx     #dall-e-3绘画，免费api不太稳定，指令如 画 an anime girlish，only 1 character in picture，white sleeveless dress，chocker，Amyamya，White light blue long hair，the main color of hair is white，cute face，light blue eyes，black ribbon，off-shoulder dress，smiling face，suit for using as   avatar，could see full head with margin，Slightly sideways body
```
>Petunia相当于[Manyana](https://github.com/avilliai/Manyana) 的简化版，更多bot功能实现都在Manyana中，其部署要比Petunia复杂，但教程目前相对完善，如感兴趣可自行查看

# 🎄最后
如果觉得项目还不错的话给个star喵，给个star谢谢喵

<div align="center">
   <img width="70%" height="70%" src="https://moe-counter.glitch.me/get/@:berglm" alt="logo"></br>
</div>

