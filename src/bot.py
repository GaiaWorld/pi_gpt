# -*- coding:utf-8 -*-

import json
import openai

CONFIG_PATH = "config/config.json"

# OpenAI 的 参数见:
# https://platform.openai.com/docs/api-reference/chat/create


def parse_config():
    with open(CONFIG_PATH, 'r', encoding="utf8") as f:
        config = json.load(f)
        prompts = {}
        for k, v in config["prompts"].items():
            arr = []
            for i in v:
                arr.append({
                    "role": i["role"],
                    "content": i["content"].replace("{error_str}", config["error_str"])
                })
            prompts[k] = arr
        config["prompts"] = prompts

        return config


class ChatBot(object):

    def __init__(self):
        self.model = "gpt-3.5-turbo"

        # 对话历史，不包括提示
        self.history = []

        self.stop = ""
        self.stream = False
        # 可以生成几个回答作为候选，一般是1条
        self.n = 1

        config = parse_config()

        self.debug = config["debug"]

        # 用户的 API_KEY
        self.api_key = config["api_key"]

        self.error_str = config["error_str"]

        self.use_prompt = config["use_prompt"]

        # 上下文提示：作为system存在
        # 总是插到最新一条问题的前面去
        self.prompts = config["prompts"]

        # [-2, 2] 正数阻挠token出现，以便于模型讨论新主题
        self.presence_penalty = config["presence_penalty"]

        # [-2, 2] 正数 会基于他们出现的频率去阻挠token，降低重复同样的话
        self.frequency_penalty = config["frequency_penalty"]

        # 温度 [0, 2]，值越大 越 放开自我
        # > 0.8 更随机
        # < 0.2 更 确定
        # 和 top_p 参数 同义，这里不考虑 top_p
        self.temperature = config["temperature"]

        # 限制 问题+答复 的 总共token，如果超过就不会再回答
        self.max_tokens = config["max_tokens"]

        # 最大的用户对话数，1条对话 = 2个记录
        self.max_chat_count = config["max_chat_count"]

    def ask(self, question):
        r = {
            "content": "",
            "errcode": 0,
            "total_tokens": 0,
        }
        try:
            messages = self.history[-2*self.max_chat_count:]

            # 每次问问题之前，加上系统提示，以免之前的回答被冲掉
            prommpts = self.prompts[self.use_prompt]
            messages.extend(prommpts)
            # print(messages)

            record = {
                "role": "user",
                "content": question
            }
            messages.append(record)
            self.history.append(record)

            if self.debug:
                data = json.dumps(messages, sort_keys=True, indent=4)
                data = data.encode('utf-8').decode('unicode_escape')

                print(f"仅用于调试：这一次 的 messages 参数 如下：\n {data} \n")

            # answer = {
            #   "usage": {
            #       "completion_tokens": 24,
            #       "prompt_tokens": 41,
            #       "total_tokens": 65
            #   },
            #   "choices": [{
            #       "index": 0,
            #       "finish_reason": "stop",
            #       "message": {
            #           "role": "assistant"
            #           "content": "...",
            #       }
            #   }]
            # }
            openai.api_key = self.api_key
            answer = openai.ChatCompletion.create(
                # 必须
                model=self.model,
                messages=messages,

                # Optional
                n=self.n,
                max_tokens=self.max_tokens,
                temperature=self.temperature,

                presence_penalty=self.presence_penalty,
                frequency_penalty=self.frequency_penalty,

                stop=self.stop,
                stream=self.stream,
            )

            reply = answer.choices[0]["message"]["content"]
            if reply.startswith(self.error_str):
                reply = "请询问相关的问题"
                del (self.history[-1])
            else:
                self.history.append({
                    "role": "assistant",
                    "content": reply
                })

            if self.debug:
                rmb = 7 * 100 * 0.002 / 1000 * answer.usage.total_tokens
                print(f"仅用于调试：")
                print("    1美元 = 7元，价格：$0.002 / 1000 tokens")
                print(f"   这一次 的 费用 如下：{round(rmb, 2)} 分钱")
                
                data = json.dumps(answer.usage, sort_keys=True, indent=4)
                data = data.encode('utf-8').decode('unicode_escape')
                print(f"{data}")

            r = {
                "errcode": 0,
                "total_tokens": answer.usage.total_tokens,
                "content": reply
            }
        except openai.error.AuthenticationError as err:
            print(f"==== 请输入 OpenAI Key: {err}")
            r = {
                "errcode": -1,
                "total_tokens": 0,
                "content": "请输入 OpenAI Key"
            }
        except openai.error.APIConnectionError as err:
            msg = "连接错误，请检查代理 或者 网络: 代理需要打开TUN模式，同时关闭系统代理"
            print(msg)
            r = {
                "errcode": -2,
                "total_tokens": 0,
                "content": msg
            }
        except openai.error.APIError as err:
            msg = f"遇到 API 错误，查看错误原因：{err}"
            print(msg)
            r = {
                "errcode": -3,
                "total_tokens": 0,
                "content": msg
            }
        return r


if __name__ == "__main__":
    box = ChatBot()

    is_continue = True
    while is_continue:
        question = input("（回车退出）有什么可以帮助你：")

        is_continue = len(question.strip()) > 0

        if is_continue:
            answer = box.ask(question)
            print(answer["content"])
