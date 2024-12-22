# aiwolf-nlp-llm-agent

人狼知能コンテスト(自然言語部門)の生成AIを使用したサンプルエージェントです。\
このプログラムは[aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)をベースにしているため、実行方法などの詳細はこちらをご覧ください。

## 構成
[aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)との差分の構成を記述します。
```.
└── src
    ├── res
    │   ├── __init__.py
    │   ├── env.example
    │   └── prompt.py
    └── utils
        └── llm
            └── ChatGPT
                ├── __init__.py
                ├── aiwolf_nlp_gpt.py
                ├── chatgpt.py
                └── message_role.py
```

## プロンプトの変更方法
`src/res/prompt.py`の内容を変更することで与えるプロンプトを変更することができます。詳細は以下に記述します。

### [src/res/prompt.py]
`get_common_prompt`: 全命令に共通する内容を記述しているプロンプトです。(`src/player/agent.py`の`initialize`で設定しています。
)

`get_talk_prompt`: `talk`の際に命令する内容を記述しているプロンプトです。(`src/player/agent.py`の`talk`で設定しています。
)


## 環境構築
[aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)の環境構築に加え、以下の内容を実行してください。

1. 以下のコマンドの実行
    ```
    cp src/res/env.example src/res/.env
    ```
1. OpenAIのAPIキーを`src/res/.env`ファイルに記述する(ChatGPTを使用する場合)

## ChatGPTの設定について
APIで使用可能な設定の内、一部のみ`src/utils/llm/ChatGPT/chatgpt.py`に記述してあります。詳細は以下のリファレンスをご参照ください。

[API reference](https://platform.openai.com/docs/api-reference/chat)