from __future__ import annotations

from typing import TYPE_CHECKING

from .chatgpt import ChatGPT

if TYPE_CHECKING:
    import configparser

    from openai.types.chat import ChatCompletion


class AIWolfNLPChatGPT(ChatGPT):
    def __init__(self, config: configparser.ConfigParser, system_instruction:str) -> None:
        super().__init__(config=config)

        self.add_system_message(content=system_instruction)

    def set_action_time_out(self, action_timeout: int) -> None:
        self.client.timeout = action_timeout

    def create_comment(self, content: str) -> str:
        self.add_user_message(content=content)

        response: ChatCompletion = super().create_comment()

        self.add_assistant_message(content=response.choices[0].message.content)

        return response.choices[0].message.content
