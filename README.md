# aiwolf-nlp-llm-agent
人狼知能コンテスト(自然言語部門)の生成AI(ChatGPT, Gemini)を使用したサンプルエージェントです。\
このプログラムは[aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)をベースにしているため、実行方法などの詳細はこちらをご覧ください。

## 対象者
* 人狼知能コンテスト(自然言語部門)に興味はあるが、何から手をつければ良いかわからない方
* 人狼知能コンテスト(自然言語部門)に参加する予定で、ChatGPT,Geminiを使用する予定の方

## 構成
[aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)との差分の構成を記述します。
```.
.
└── src
    ├── res
    │   ├── __init__.py
    │   ├── config.ini.example
    │   ├── env.example
    │   ├── llm
    │   │   ├── chatgpt.ini.example
    │   │   └── gemini.ini.example
    │   └── prompt.py
    └── utils
        ├── agent_util.py
        └── llm
            ├── ChatGPT
            │   ├── __init__.py
            │   ├── aiwolf_nlp_gpt.py
            │   ├── chatgpt.py
            │   ├── message_role.py
            │   └── optional_params.py
            └── Gemini
                ├── __init__.py
                ├── gemini.py
                └── message_role.py
```


## 環境構築
[aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)の環境構築に加え、以下の内容を実行してください。

1. 以下のコマンドの実行
    ```
    cp src/res/env.example src/res/.env
    cp src/res/llm/chatgpt.ini.example src/res/llm/chatgpt.ini
    cp src/res/llm/gemini.ini.example src/res/llm/gemini.ini
    ```
1. OpenAIのAPIキーを`src/res/.env`ファイル内の`OPENAI_API_KEY`に記述する(ChatGPTを使用する場合)
    
    APIキーは[OpenAI Platform](https://platform.openai.com/docs/overview)から作成することができます。
1. GeminiのAPIキーを`src/res/.env`ファイル内の`GEMINI_API_KEY`に記述する(Geminiを使用する場合)
    
    APIキーは[Google AI for Developers](https://ai.google.dev/gemini-api/docs?hl=ja)の、`Gemini APIキーを取得する`から作成することができます。

## プロンプトの変更方法
`src/res/prompt.py`の内容を変更することで与えるプロンプトを変更することができます。詳細は以下に記述します。

### [src/res/prompt.py]
`get_common_prompt`: 全命令に共通する内容を記述しているプロンプトです。(`src/player/agent.py`の`initialize`で設定しています。
)

`get_talk_prompt`: `talk`の際に命令する内容を記述しているプロンプトです。(`src/player/agent.py`の`talk`で設定しています。
)

## 生成AIのパラメータの変更方法

### ChatGPT
`src/res/llm/chatgpt.ini`に以下のような内容でパラメータを設定するファイルが存在します。\
`model`は必須項目であり、他の項目は任意です。\
使用する項目はコメントアウトを外し、値を設定してご使用ください。\
それぞれのパラメータの値や意味については[API reference](https://platform.openai.com/docs/api-reference/chat)をご確認ください。

```sh
[params]
model = gpt-3.5-turbo
# frequency_penalty =
# max_completion_tokens = 
# n = 
# presence_penalty = 
# seed = 
# temperature = 
# top_p = 
```

### Gemini
`src/res/llm/gemini.ini`に以下のような内容でパラメータを設定するファイルが存在します。\
`model`は必須項目であり、他の項目は任意です。\
使用する項目はコメントアウトを外し、値を設定してご使用ください。\
それぞれのパラメータの値や意味については[API reference](https://ai.google.dev/api/generate-content?hl=ja#generationconfig)をご確認ください。

```sh
[params]
model = gemini-1.5-flash
# candidate_count = 
# max_output_tokens = 
# temperature = 
# top_p = 
# top_k = 
# seed = 
# presence_penalty = 
# requency_penalty = 
```

## ChatGPTの設定について
APIで使用可能な設定の内、一部のみ`src/utils/llm/ChatGPT/chatgpt.py`に記述してあります。詳細は以下のリファレンスをご参照ください。

[API reference](https://platform.openai.com/docs/api-reference/chat)


## Geminiの設定について
[API reference](https://ai.google.dev/api/generate-content?hl=ja#generationconfig)