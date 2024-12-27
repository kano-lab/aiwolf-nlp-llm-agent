from __future__ import annotations

import configparser
import os
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING

import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

from .message_role import MessageRole
from .optional_params import OptionalParams

if TYPE_CHECKING:
    from openai.types.chat import (
        ChatCompletion,
        ChatCompletionAssistantMessageParam,
        ChatCompletionDeveloperMessageParam,
        ChatCompletionFunctionMessageParam,
        ChatCompletionSystemMessageParam,
        ChatCompletionToolMessageParam,
        ChatCompletionUserMessageParam,
    )


class ChatGPT:
    # init file key
    __config_key = "params"

    def __init__(self, config: configparser.ConfigParser) -> None:
        self.load_api_key(config=config)
        chatgpt_config = self.read_config(config=config)

        self.model: str = chatgpt_config.get(self.__config_key, "model")

        self.optional_params: OptionalParams = OptionalParams(
            frequency_penalty=chatgpt_config.getfloat(
                self.__config_key,
                "frequency_penalty",
                fallback=None,
            ),
            max_completion_tokens=chatgpt_config.getint(
                self.__config_key,
                "max_completion_tokens",
                fallback=None,
            ),
            n=chatgpt_config.getint(self.__config_key, "n", fallback=None),
            presence_penalty=chatgpt_config.getfloat(
                self.__config_key,
                "presence_penalty",
                fallback=None,
            ),
            seed=chatgpt_config.getint(self.__config_key, "seed", fallback=None),
            temperature=chatgpt_config.getfloat(self.__config_key, "temperature", fallback=None),
            top_p=chatgpt_config.getfloat(self.__config_key, "top_p", fallback=None),
        )

        self.messages: list[
            ChatCompletionDeveloperMessageParam
            | ChatCompletionSystemMessageParam
            | ChatCompletionUserMessageParam
            | ChatCompletionToolMessageParam
            | ChatCompletionFunctionMessageParam
            | ChatCompletionAssistantMessageParam
        ] = []
        self.token_model = tiktoken.encoding_for_model(model_name=self.model)

        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    @classmethod
    def read_config(cls, config: configparser.ConfigParser) -> configparser.ConfigParser:
        chatgpt_config_path: str = config.get("path", "chatgpt_config")

        if not Path(chatgpt_config_path).is_file():
            raise FileNotFoundError(chatgpt_config_path, "ChatGPTの設定ファイルが見つかりません")

        chatgpt_config = configparser.ConfigParser()
        chatgpt_config.read(chatgpt_config_path, encoding="utf-8")

        return chatgpt_config

    @classmethod
    def load_api_key(cls, config: configparser.ConfigParser) -> None:
        api_key_path: str = config.get("path", "api_key_path")

        if not Path(api_key_path).is_file():
            raise FileNotFoundError(api_key_path, "APIの設定ファイルが見つかりません")

        load_dotenv(api_key_path)

    def get_tokens(self, text: str) -> int:
        tokens: list[int] = self.token_model.encode(text)
        return len(tokens)

    @classmethod
    def make_developer_message_param(cls, content: str) -> ChatCompletionDeveloperMessageParam:
        new_message: ChatCompletionDeveloperMessageParam = {
            "content": content,
            "role": MessageRole.DEVELOPER.value,
        }
        return new_message

    @classmethod
    def make_system_message_param(cls, content: str) -> ChatCompletionSystemMessageParam:
        new_message: ChatCompletionSystemMessageParam = {
            "content": content,
            "role": MessageRole.SYSTEM.value,
        }
        return new_message

    @classmethod
    def make_user_message_param(cls, content: str) -> ChatCompletionUserMessageParam:
        new_message: ChatCompletionUserMessageParam = {
            "content": content,
            "role": MessageRole.USER.value,
        }
        return new_message

    @classmethod
    def make_assistant_message_param(cls, content: str) -> ChatCompletionAssistantMessageParam:
        new_message: ChatCompletionAssistantMessageParam = {
            "content": content,
            "role": MessageRole.ASSISTANT.value,
        }
        return new_message

    @classmethod
    def make_tool_message_param(cls, content: str) -> ChatCompletionToolMessageParam:
        new_message: ChatCompletionToolMessageParam = {
            "content": content,
            "role": MessageRole.TOOL.value,
        }
        return new_message

    @classmethod
    def make_function_message_param(cls, content: str) -> ChatCompletionFunctionMessageParam:
        new_message: ChatCompletionFunctionMessageParam = {
            "content": content,
            "role": MessageRole.FUNCTION.value,
        }
        return new_message

    def add_message(
        self,
        message: ChatCompletionDeveloperMessageParam
        | ChatCompletionSystemMessageParam
        | ChatCompletionUserMessageParam
        | ChatCompletionToolMessageParam
        | ChatCompletionFunctionMessageParam
        | ChatCompletionAssistantMessageParam,
    ) -> None:
        self.messages.append(message)

    def add_developer_message(self, content: str) -> None:
        self.add_message(message=self.make_developer_message_param(content=content))

    def add_system_message(self, content: str) -> None:
        self.add_message(message=self.make_system_message_param(content=content))

    def add_user_message(self, content: str) -> None:
        self.add_message(message=self.make_user_message_param(content=content))

    def add_assistant_message(self, content: str) -> None:
        self.add_message(message=self.make_assistant_message_param(content=content))

    def add_tool_message(self, content: str) -> None:
        self.add_message(message=self.make_tool_message_param(content=content))

    def add_function_message(self, content: str) -> None:
        self.add_message(message=self.make_function_message_param(content=content))

    def create_comment(self) -> ChatCompletion:
        chatgpt_args = {
            "model": self.model,
            "messages": self.messages,
        }

        chatgpt_args.update(
            {
                key: value
                for key, value in asdict(self.optional_params).items()
                if value is not None
            },
        )

        return self.client.chat.completions.create(**chatgpt_args)

    def close(self) -> None:
        if hasattr(self, "client"):
            self.client.close()
