- [Python Bot use ChatGPT](#python-bot-use-chatgpt)
  - [1. 运行](#1-运行)
  - [2. 配置 config/config.json](#2-配置-configconfigjson)
  - [3. TODO](#3-todo)
    - [3.1. 工程](#31-工程)
    - [3.2. 技术](#32-技术)
  - [4. 范例：我是数学老师，只能问我数学题](#4-范例我是数学老师只能问我数学题)
  - [5. 参考](#5-参考)


# Python Bot use ChatGPT

基于 ChatGPT 的 python 聊天机器人

## 1. 运行

代理: 需要关闭`系统代理`，只打开`TUN模式`

+ 环境: Python 3.10, pip3
+ 安装: **pip3 install openai**
+ 配置: config/config.json, 具体见下面 “配置” 的 章节
+ 运行: run.bat

## 2. 配置 config/config.json

||||
|--|--|--|
|api_key|你在 OpenAI 分配的 Key，如果没有，请找运维配置||
|debug|如果为 true，则 运行时候，控制台会输出每次的问题的完整信息||
|max_tokens|问题 + 回答 的 总token|注意：这涉及到您的 `项目经费`||
|temperature|温度，值在[0, 2]|小于0.2，回答很确定；大于0.8，回答的很随机||
|max_chat_count|每次询问最多带多少以前用户的问题|一条对话2个记录，不含promps的数量；注意：这涉及到您的 `项目经费`|
|presence_penalty|[-2,2]，意义暂时未明，保留||
|frequency_penalty|[-2,2]，意义暂时未明，保留||
|use_prompt|默认用 prompts 中 的 哪个||
|error_str|prompts 的 {error_str}的替换，用于让程序知道 用户问了一个和设定场景无关的话题，下次就不将该问题加到 gpt 中了|
|prompts|调教，是一个 obejct，每个值都是一个场景，里面可以放这个场景的系统提示和用例|见范例：一个高中物理老师|

## 3. TODO

### 3.1. 工程

+ 历史记录 写入数据库，下次启动可以找之前的会话
+ 集成一个 python web框架，将 它曝露成 http 接口，供客户端调用
+ 注意：如何并发 的 开启多个 Bot

### 3.2. 技术

+ [加上 Embedding](https://github.com/gannonh/gpt3.5-turbo-pgvector)，可以在庞大的历史记录中，找和问题最相关的 上传
+ 改进 调教提示，让其更明确范围
    - 目前：只要问一个和数学沾边的问题，就可以绕过限制
    - 例子：李白是数学家吗？或者 李白懂数学吗？
    - 然后就可以问李白的其他事情了。。。
+ 和 [LangChain]() 连起来，打通 底层数据库和chatgpt

## 4. 范例：我是数学老师，只能问我数学题

见 **config/config.json**

``` json
{
    "api_key": "",
 
    "debug": true,

    "temperature": 0.5,
    "max_tokens": 2048,
    "max_chat_count": 3,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "use_prompt": "default",
    "error_str": "YN",
    "prompts": {
        "default": [
            {
                "role": "system",
                "content": "你从现在开始，只是一名数学老师，遇到非数学问题，或者遇到你不确定是数学方面的问题，一律在回答的最前面加上{error_str}"
            },
            {
                "role": "user",
                "content": "李白活了多少岁？"
            },
            {
                "role": "assistant",
                "content": "{error_str}"
            },
            {
                "role": "user",
                "content": "太阳距离冥王星有多少公里？"
            },
            {
                "role": "assistant",
                "content": "{error_str}"
            }
        ]
    }
}
```

## 5. 参考

+ [如何做定制化](https://github.com/JimmyLv/jimmylv.github.io/issues/398)
+ [OpenAI API 参数](https://platform.openai.com/docs/api-reference/chat/create)