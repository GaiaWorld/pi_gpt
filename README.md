- [Python Bot use ChatGPT](#python-bot-use-chatgpt)
  - [1. 运行](#1-运行)
  - [2. 配置 config/config.json](#2-配置-configconfigjson)
  - [3. 关于 prompts](#3-关于-prompts)
  - [4. TODO](#4-todo)
    - [4.1. 工程](#41-工程)
    - [4.2. 技术](#42-技术)
  - [5. 范例：我是数学机器人，只能问我数学题](#5-范例我是数学机器人只能问我数学题)
  - [6. 参考](#6-参考)


# Python Bot use ChatGPT

基于 ChatGPT 的 python 聊天机器人

## 1. 运行

代理: 需要关闭`系统代理`，只打开`TUN模式`

+ 环境: Python 3.10, pip3
+ 安装: **pip3 install openai**
+ 配置: config/config.json, 具体见下面 “配置” 的 章节
+ 运行: run.bat
    - 如果 config/config.json 不存在，会从 config_template.json 拷贝一份出来

## 2. 配置 config/config.json

|键|范本初始值|作用|说明|
|--|--|--|--|
|api_key|必填|你在 OpenAI 分配的 Key，如果没有，请找运维配置||
|debug|true|如果为 true，则 运行时候，控制台会输出每次的问题的完整信息||
|max_tokens|2048|问题 + 回答 的 总token|注意：这涉及到您的 `项目经费`||
|temperature|0.5|温度，值在[0, 2]|小于0.2，回答很确定；大于0.8，回答的很随机||
|max_chat_count|3|每次询问最多带多少以前用户的问题|一条对话2个记录，不含promps的数量；注意：这涉及到您的 `项目经费`|
|presence_penalty|0|[-2,2]，意义暂时未明，保留||
|frequency_penalty|0|[-2,2]，意义暂时未明，保留||
|use_prompt|"default"|默认用 prompts 中 的 哪个||
|error_str|"YN"|prompts 的 {error_str}的替换，用于让程序知道 用户问了一个和设定场景无关的话题，下次就不将该问题加到 gpt 中了|
|prompts|无|调教，是一个 obejct，每个值都是一个场景，里面可以放这个场景的系统提示和用例|见范例：`数学机器人`|

## 3. 关于 prompts

**初步建议**：最好用 `system` 这个角色；因为它不会干扰你的上下文。

prompts 由很多场景组成，用于做很多类任务，一类任务有一个明显的提示；

这里最简单的就只有 一个 默认场景

默认场景，由一连串的 提示构成，每个提示 有两个键：`role`, `content`

+ `role`: 只有 三个值，代表三种角色
    - `system`: 相当于 画外音，催眠作用，该角色可以放在任何地方
    - `user`: 用户角色，一般放用户的问题
    - `assistant`: 机器人角色，用于放 chatgpt的回答
+ `contenet`: 根据`role`的值，分别对应以下三个部分的内容：画外音，用户，chatgpt

用于调教的提示，可以自己编造上面的画外音，用户，和 机器人 的 内容，作为范例让chatgpt知道怎么回答问题；

每个角色都可以连续放多个，比如 你可以 连续几个 `assistant`，那么下一个问题，可能chatgpt就会回复多次；

除了 钱/token 这个因素，可以尽情放开你的想象力；

要观察具体的顺序：让 `debug` = true, 观察 控制台 即可

## 4. TODO

### 4.1. 工程

+ 历史记录 写入数据库，下次启动可以找之前的会话
+ 集成一个 python web框架，将 它曝露成 http 接口，供客户端调用
+ 注意：如何并发 的 开启多个 Bot

### 4.2. 技术

+ [加上 Embedding](https://github.com/gannonh/gpt3.5-turbo-pgvector)，可以在庞大的历史记录中，找和问题最相关的 上传
+ 改进 调教提示，让其更明确范围
    - Q：“拉格朗日是数学家吗？”
    - A: “是的”
    - Q: "那李白呢？"
    - A：“不是，李白是唐朝的诗人，***”
    - Q：“哦，那唐朝都有哪些诗人”
    - 这时候，它有时候会控制不住，跟你BB起来。。。但有时候又有身为数学机器的自觉。
+ 和 [LangChain]() 连起来，打通 底层数据库和chatgpt

## 5. 范例：我是数学机器人，只能问我数学题

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
                "content": "你从现在开始，仅仅是数学机器人，除了数学问题，其他的一无所知，如果你判断这可能不是数学问题，或者 玩家跟你聊非数学方面的话题或者人物，一律只回复{error_str}，比如：李白是数学家吗？李白活了多少岁？杜甫这辈写了几首诗歌？等这些问题，统一回复{error_str}。"
            }
        ]
    }
}
```

## 6. 参考

+ [如何做定制化](https://github.com/JimmyLv/jimmylv.github.io/issues/398)
+ [OpenAI API 参数](https://platform.openai.com/docs/api-reference/chat/create)
