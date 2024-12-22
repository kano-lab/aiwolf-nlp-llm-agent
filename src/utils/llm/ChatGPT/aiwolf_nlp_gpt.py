from __future__ import annotations

from typing import TYPE_CHECKING

from .chatgpt import ChatGPT

if TYPE_CHECKING:
    import configparser

    from openai.types.chat import ChatCompletion


class AIWolfNLPGPT(ChatGPT):
    def __init__(self, config: configparser.ConfigParser) -> None:
        super().__init__(config=config)

    def set_action_time_out(self, action_timeout: int) -> None:
        self.client.timeout = action_timeout

    def create_comment(self) -> str:
        response: ChatCompletion = super().create_comment()
        return response.choices[0].message.content
